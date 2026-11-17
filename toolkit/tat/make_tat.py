import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import vlib
from vlib import font, txt, put, ease, clamp, BLK, XB, BD, WHITE
from eng3d import *

HERE = "/home/claude/work/tat"
SC = json.load(open(f"{HERE}/scenes.json")); TOTAL = sum(s["dur"] for s in SC)
W, H, FPS, S = 1080, 1920, 30, 2
ACC = (255, 196, 46); RED = (240, 70, 70); GREY = (150, 156, 162)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
import functools
@functools.lru_cache(maxsize=None)
def mono(sz): return ImageFont.truetype(MONO, sz)
vlib.CF = font(XB, 58)

def wt(k, sub, nth=0):
    c = 0
    for w, a, b in SC[k]["words"]:
        if w.lower().strip(".,:;!?") == sub.lower():
            if c == nth: return a
            c += 1
    raise KeyError(f"{k}:{sub}")
def seg_at(T):
    for k, s in enumerate(SC):
        if T < s["start"] + s["dur"]: return k
    return len(SC) - 1

# ---------- teams ----------
SPR_A = make_player((34, 150, 82), (245, 245, 245), (34, 150, 82))
SPR_AGK = make_player((30, 30, 34), (30, 30, 34), (30, 30, 34))
SPR_B = make_player((232, 232, 236), (40, 42, 48), (232, 232, 236))
SPR_BGK = make_player((245, 150, 40), (40, 42, 48), (245, 150, 40))
SPR_FALL = SPR_A.rotate(78, Image.BICUBIC, expand=True)
BASE_A = [(-45, 0), (-15, -22), (-20, -8), (-20, 8), (-15, 22), (4, -14), (0, 0), (4, 14), (24, -22), (28, 0), (24, 22)]
BASE_B = [(50.5, 0), (36, -18), (37, -6), (37, 6), (36, 18), (22, -12), (20, 0), (22, 12), (-4, -20), (-8, 2), (-4, 20)]

def lerp2(a, b, u): return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
def path_at(keys, t):
    """keys: [(t, value)] -> eased interpolation"""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys[:-1], keys[1:]):
        if t <= t1:
            u = smooth((t - t0) / (t1 - t0)) if t1 > t0 else 1
            return tuple(np.asarray(v0, float) * (1 - u) + np.asarray(v1, float) * u)
    return keys[-1][1]
def arc(p0, p1, u, h):
    x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u
    z0 = p0[2] if len(p0) > 2 else 0.11; z1 = p1[2] if len(p1) > 2 else 0.11
    return (x, y, z0 + (z1 - z0) * u + h * 4 * u * (1 - u))

class St:
    def __init__(s):
        s.A = list(BASE_A); s.B = list(BASE_B); s.ball = (0.6, 0.3, 0.11); s.rings = []; s.paths = []; s.zones = []; s.labels = []
        s.cards = []; s.bar = "bar"; s.flag = False; s.fallen = set(); s.ball_hidden = False; s.hl = set()

# ---------- steps: (state, camera keys) ----------
META = [
    ("EVOLUÇÃO", "AS REGRAS DO FUTEBOL", "DE 1863 ATÉ HOJE"),
    ("01 · 1863", "SÓ COM OS PÉS", "NASCEM AS 13 PRIMEIRAS REGRAS"),
    ("02 · 1872", "ESCANTEIO", "SAIU PELA LINHA DE FUNDO"),
    ("03 · 1875", "TRAVESSÃO", "ANTES, ERA UMA FITA"),
    ("04 · 1891", "PÊNALTI", "O \"CHUTE DA MORTE\""),
    ("05 · 1925", "IMPEDIMENTO", "DE 3 PARA 2 ADVERSÁRIOS"),
    ("06 · 1970", "CARTÕES", "COPA DO MÉXICO"),
    ("07 · 1992", "RECUO", "GOLEIRO NÃO PEGA COM A MÃO"),
    ("08 · 2018", "VAR", "O LANCE REVISTO NO VÍDEO"),
    ("09 · 2025", "8 SEGUNDOS", "GOLEIRO NÃO PODE ENROLAR"),
    ("E AGORA?", "QUAL A PRÓXIMA?", "COMENTA A REGRA QUE VOCÊ MUDARIA"),
]

def step0(t, s):
    s.ball = (0.8 + t * 0.6, 0.4, 0.11); s.A[6] = (t * 0.6, 0)
    return [(0, (-2, -20, 34), (4, 0, 0), 50), (5.3, (-6, -30, 12), (6, 0, 0.5), 48)]

def step1(t, s):
    k = 1; x = 28 + t * 1.1
    s.A[9] = (x, 0.5 * math.sin(t)); s.ball = (x + 0.75, 0.5 * math.sin(t) + 0.15 * math.sin(t * 6), 0.11)
    s.B[2] = (37 - t * 0.4, -3); s.B[3] = (36.5 - t * 0.4, 4)
    s.rings.append((s.A[9], ACC)); s.hl.add(("A", 9))
    tb = wt(k, "bola") - 0.2
    if t > tb: s.labels.append(((s.A[9][0], s.A[9][1], 2.45), "MÃO? PROIBIDO", RED, t - tb))
    if t > wt(k, "pés") - 0.3: s.labels.append(((s.ball[0], s.ball[1], 0.3), "SÓ O PÉ", ACC, t - wt(k, "pés") + 0.3))
    return [(0, (20, -11, 4.0), (31, 1, 0.9), 50), (6.5, (26, -10, 3.6), (37, 1, 0.9), 50)]

def step2(t, s):
    k = 2; tb = wt(k, "bola") - 0.2; tf = wt(k, "fundo") + 0.1; te = wt(k, "escanteio") - 0.1
    s.B[1] = (40, -12); s.A[8] = (34, -24); s.A[9] = (44, -3); s.A[10] = (42, 8); s.B[2] = (45, -5); s.B[3] = (45, 3)
    s.flag = True
    p0 = (40.6, -12.4, 0.11); p1 = (54.5, -21, 0.11)
    if t < tb: s.ball = p0
    elif t < te:
        u = clamp((t - tb) / (tf - tb)); s.ball = arc(p0, p1, u, 2.5)
        s.paths.append(([p0[:2] + (0.03,), (p1[0], p1[1], 0.03)], RED, True))
        s.zones.append(([(52.5, -34, 0.02), (56, -34, 0.02), (56, 34, 0.02), (52.5, 34, 0.02)], (240, 70, 70, 40)))
        if t > tf - 0.3: s.labels.append(((52.5, -17, 0.4), "LINHA DE FUNDO", RED, t - tf + 0.3))
    if t >= te:
        s.A[8] = (53.3, -34.6); c0 = (52.3, -33.6, 0.11); c1 = (45, -3, 1.6)
        u = clamp((t - te - 0.6) / 1.1)
        s.ball = arc(c0, c1, u, 3.5) if u > 0 else c0
        pts = [arc(c0, c1, i / 24, 3.5) for i in range(25)]
        s.paths.append(([(p[0], p[1], 0.03) for p in pts], ACC, True)); s.paths.append((pts, ACC + (150,), False))
        s.rings.append(((52.5, -34), ACC)); s.labels.append(((52.5, -34, 2.2), "ESCANTEIO", ACC, t - te))
    return [(0, (32, -50, 15), (47, -16, 0), 50), (6.8, (34, -48, 13), (48, -18, 0), 50)]

def step3(t, s):
    k = 3; tt_ = wt(k, "travessão") - 0.2; ta = wt(k, "antes") - 0.2
    s.B[0] = (52, 0.3); s.A[9] = (44, -2); s.ball = (43.3, -1.6, 0.11)
    s.bar = "tape" if t < tt_ else "bar"
    if t > tt_: s.labels.append(((52.5, 0, 3.1), "TRAVESSÃO", ACC, t - tt_))
    s.pip = ("ANTES DE 1875", ta) if t > ta else None
    return [(0, (38, -9, 2.3), (52.5, 0, 1.5), 48), (7.0, (41, -6.5, 2.0), (52.5, 0, 1.5), 46)]

def step4(t, s):
    k = 4; tp = wt(k, "pênalti") - 0.3; tk = wt(k, "chute") - 0.2
    s.B[0] = (52.2, 0); s.A[9] = (40.2, -0.9); s.ball = (41.5, 0, 0.11)
    for i, p in [(1, (35, -12)), (2, (34, -4)), (3, (34, 5)), (4, (35, 13))]: s.B[i] = p
    s.A[8] = (33, -9); s.A[10] = (33, 10)
    pul = 0.5 + 0.5 * math.sin(t * 6)
    s.rings.append(((41.5, 0), ACC))
    if t > tp:
        s.zones.append(([(52.5, -20.16, 0.02), (36, -20.16, 0.02), (36, 20.16, 0.02), (52.5, 20.16, 0.02)], ACC + (int(26 + 14 * pul),)))
        s.labels.append(((41.5, 0, 0.3), "11 METROS", ACC, t - tp))
    if t > tk:
        u = clamp((t - tk) / 0.45); s.ball = arc((41.5, 0, 0.11), (53.0, 2.7, 1.5), u, 0.4)
        if u >= 1: s.labels.append(((52.5, 2.7, 3.0), "GOL", ACC, t - tk - 0.45))
        s.B[0] = (52.2, -1.2 * clamp((t - tk) / 0.35))
    return [(0, (30.5, -4.5, 3.6), (50, 0.5, 0.8), 46), (6.0, (32.5, -3.8, 3.3), (51, 0.5, 0.8), 44)]

def step5(t, s):
    k = 5; tn = wt(k, "bastam") - 0.2; tg = wt(k, "ataque") - 0.3
    s.B[0] = (51, 0); s.B[1] = (38, -14); s.B[2] = (36.5, -4); s.B[3] = (36.5, 5); s.B[4] = (39, 14)
    s.B[5] = (28, -8); s.B[6] = (27, 3); s.B[7] = (29, 12)
    s.A[9] = (38.5, 2); s.A[6] = (20, 0); s.A[8] = (30, -20); s.A[10] = (31, 22); s.A[5] = (22, -10); s.A[7] = (23, 10)
    s.ball = (20.7, 0.3, 0.11)
    new = t > tn
    lx = 38 if not new else 38 + 1 * smooth((t - tn) / 0.6)
    col = RED if not new else ACC
    if t > 1.2:
        s.paths.append(([(lx, -HY, 0.03), (lx, HY, 0.03)], col, True))
        s.zones.append(([(lx, -HY, 0.02), (HX, -HY, 0.02), (HX, HY, 0.02), (lx, HY, 0.02)], (col + (30,))))
        for i in ([0, 4, 1] if not new else [0, 4]): s.rings.append((s.B[i], col))
        s.labels.append(((lx, -HY + 3, 0.3), "PRECISAVA DE 3" if not new else "AGORA BASTAM 2", col, t - (1.2 if not new else tn)))
        s.hl.add(("A", 9))
    if t > tg:
        u = clamp((t - tg) / 1.1); s.ball = arc((20.7, 0.3, 0.11), (45, 4, 0.11), u, 1.5)
        s.A[9] = lerp2((38.5, 2), (45.5, 3.4), smooth((t - tg) / 1.2))
        s.paths.append(([(20.7, 0.3, 0.03), (45, 4, 0.03)], ACC, True))
        s.labels.append(((44, 4, 2.2), "ESPAÇO!", ACC, t - tg - 0.6)) if t > tg + 0.6 else None
    return [(0, (16, -42, 30), (40, 0, 0), 50), (9.4, (20, -38, 26), (40, 1, 0), 48)]

YCARD = Image.new("RGBA", (100, 140), (0, 0, 0, 0)); ImageDraw.Draw(YCARD).rounded_rectangle((0, 0, 99, 139), 10, fill=(250, 205, 40))
RCARD = Image.new("RGBA", (100, 140), (0, 0, 0, 0)); ImageDraw.Draw(RCARD).rounded_rectangle((0, 0, 99, 139), 10, fill=(230, 45, 45))
def step6(t, s):
    k = 6; tf = wt(k, "estreiam") - 0.6; ty = wt(k, "amarelo") - 0.2; tr = wt(k, "vermelho") - 0.2
    ax = 6 + 2.6 * smooth(t / 2.6); s.A[6] = (ax, -1.5); s.ball = (ax + 0.8, -1.4, 0.11)
    bp = path_at([(0, (11, -6)), (tf, (9.6, -3.5)), (tf + 0.35, (8.4, -1.7))], t); s.B[6] = bp
    if t > tf + 0.3: s.fallen.add(("A", 6)); s.ball = (9.6, -0.6, 0.11)
    s.rings.append((s.B[6], RED if t > tf + 0.3 else (200, 200, 200)))
    if t > ty: s.cards.append(((s.B[6][0], s.B[6][1], 2.5 + 0.08 * math.sin(t * 4)), YCARD if t < tr else RCARD, t - (ty if t < tr else tr)))
    if t > tf + 0.3: s.labels.append(((8.6, -1.5, 0.3), "FALTA", RED, t - tf - 0.3))
    return [(0, (1, -13, 4.5), (9, 0, 1.0), 48), (7.2, (3, -11.5, 4), (9.5, -1, 1.0), 46)]

def step7(t, s):
    k = 7; tr = wt(k, "recuo") - 0.3; tp = wt(k, "pegar") - 0.3
    s.A[0] = (-50, 0); s.A[2] = (-36, 6); s.A[1] = (-33, -14); s.B[9] = (-38, -3); s.B[8] = (-34, 12)
    p0 = (-35.3, 6.2, 0.11); p1 = (-49.2, 0.4, 0.11)
    if t < tr: s.ball = p0
    else:
        u = clamp((t - tr) / 1.3); s.ball = arc(p0, p1, u, 0.0)
        s.paths.append(([p0[:2] + (0.03,), (p1[0], p1[1], 0.03)], (230, 230, 230), True))
    s.rings.append((s.A[0], RED if t > tp else ACC))
    if t > tp: s.labels.append(((-50, 0, 2.5), "MÃO: NÃO", RED, t - tp))
    if t > tp + 1.0:
        u = clamp((t - tp - 1.0) / 1.2); s.ball = arc(p1, (-15, -4, 0.11), u, 12)
        s.labels.append(((-50.5, -1, 0.3), "SÓ COM O PÉ", ACC, t - tp - 1.0))
    return [(0, (-36, -13, 6.5), (-46, 1, 0.6), 48), (6.8, (-38, -11.5, 6), (-47, 1, 0.6), 46)]

def step8(t, s):
    k = 8; tv = wt(k, "var") - 0.2
    s.B[0] = (51, 0); s.B[1] = (40, -12); s.B[2] = (41, -3); s.B[3] = (41.6, 5); s.B[4] = (40, 14)
    s.A[9] = path_at([(0, (41.9, 2)), (1.4, (48.5, 1.5))], t); s.A[6] = (30, -1)
    u = clamp(t / 1.2); s.ball = arc((30.8, -0.8, 0.11), (48.2, 1.6, 0.11), u, 1.0)
    if t > 1.5: s.ball = arc((48.2, 1.6, 0.11), (53.2, -2, 0.8), clamp((t - 1.5) / 0.35), 0.3)
    if t > 1.9: s.labels.append(((52.5, -2, 3.0), "GOL?", ACC, t - 1.9))
    s.pip = ("VAR · REVISÃO", tv) if t > tv else None
    return [(0, (32, -16, 7), (47, 0, 0.6), 48), (6.6, (35, -14, 6), (48, 0, 0.6), 46)]

def step9(t, s):
    k = 9; tg = wt(k, "segurou") - 0.2; te = wt(k, "escanteio") - 0.2
    s.B[0] = (50.5, 0.5); s.ball = (50.5, 0.25, 1.15); s.A[9] = (44, 7); s.A[8] = (36, -9)
    if t > tg:
        span = te - tg; left = max(0, 8 - 8 * (t - tg) / span)
        s.counter = ((50.5, 2.0, 1.9), left)
    s.flag = True
    if t > te:
        s.rings.append(((52.5, -34), ACC)); s.labels.append(((52.5, -34, 2.2), "ESCANTEIO PRO RIVAL", ACC, t - te))
        s.ball = (52.3, -33.6, 0.11)
    cams = [(0, (42, -7, 3.0), (50.5, 0.8, 1.3), 46), (max(0.1, te - 0.1), (43, -6.5, 2.8), (50.5, 0.8, 1.3), 44), (te + 1.0, (40, -48, 14), (51, -24, 0), 50), (7.9, (41, -47, 13), (51, -25, 0), 50)]
    return cams

def step10(t, s):
    R = 48
    return [(0, (R * math.cos(math.radians(-100)), R * math.sin(math.radians(-100)), 30), (0, 0, 0), 52),
            (6.7, (R * math.cos(math.radians(-100 + 12 * 6.7)), R * math.sin(math.radians(-100 + 12 * 6.7)), 38), (0, 0, 0), 52)]

STEPS = [step0, step1, step2, step3, step4, step5, step6, step7, step8, step9, step10]

def cam_keys_at(keys, t):
    if t <= keys[0][0]: k = keys[0]; return k[1], k[2], k[3]
    for a, b in zip(keys[:-1], keys[1:]):
        if t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]); u = u if (b[0] - a[0]) > 3 else smooth(u)
            return lerp(a[1], b[1], u), lerp(a[2], b[2], u), a[3] + (b[3] - a[3]) * u
    k = keys[-1]; return k[1], k[2], k[3]

def get_state(T):
    k = seg_at(T); t = T - SC[k]["start"]
    s = St(); s.pip = None; s.counter = None
    keys = STEPS[k](t, s)
    pos, tgt, fov = cam_keys_at(keys, t)
    if k > 0 and t < 1.0:
        sp = St(); sp.pip = None; sp.counter = None
        pk = STEPS[k - 1](SC[k - 1]["dur"], sp)
        p0, g0, f0 = cam_keys_at(pk, SC[k - 1]["dur"]); u = smooth(t / 1.0)
        pos, tgt, fov = lerp(p0, pos, u), lerp(g0, tgt, u), f0 + (fov - f0) * u
        # players glide from previous layout
        s.A = [lerp2(a, b, u) for a, b in zip(sp.A, s.A)]; s.B = [lerp2(a, b, u) for a, b in zip(sp.B, s.B)]
        if t < 0.5: s.ball = tuple(lerp(sp.ball, s.ball, smooth(t / 0.5)))
    return k, t, s, (pos, tgt, fov)

def render_world(s, cam, Wc, Hc, t):
    img = Image.new("RGB", (Wc, Hc), (12, 13, 15)); d = ImageDraw.Draw(img, "RGBA")
    draw_pitch(d, cam)
    for pts, fill in s.zones: poly(d, cam, pts, fill)
    for pts, col, dashed_ in s.paths:
        polyline(d, cam, pts, col if len(col) == 4 else col + (230,), 0.13, 2, 12, dash=0.9 if dashed_ else None, phase=-t * 3)
    for (x, y), col in s.rings: ring(d, cam, x, y, col + (235,), 1.1, t)
    objs = []
    for team, lst in (("A", s.A), ("B", s.B)):
        for i, (x, y) in enumerate(lst):
            spr = (SPR_AGK if i == 0 else SPR_A) if team == "A" else (SPR_BGK if i == 0 else SPR_B)
            if (team, i) in s.fallen: spr = SPR_FALL
            c = cam.cam((x, y, 0.9)); objs.append((c[2], "p", (x, y, spr, team == "B")))
    objs.append((cam.cam(s.ball)[2] - 0.05, "ball", None))
    for sgn in (-1, 1): objs.append((cam.cam((sgn * HX, 0, 1.2))[2] + 0.5, "goal", sgn))
    if s.flag: objs.append((cam.cam((HX, -HY, 0.8))[2], "flag", None))
    for X, cardim, age in s.cards: objs.append((cam.cam(X)[2] - 0.1, "card", (X, cardim, age)))
    for (z, kind, data) in objs:
        if kind == "p": draw_shadow(d, cam, data[0], data[1])
    bx, by, bz = s.ball; draw_shadow(d, cam, bx, by, 0.13, 90)
    for z, kind, data in sorted(objs, key=lambda o: -o[0]):
        if z < cam.near: continue
        if kind == "p":
            x, y, spr, flip = data
            if spr is SPR_FALL: draw_billboard(img, cam, (x, y, 0), spr, 0.9)
            else: draw_billboard(img, cam, (x, y, 0), spr, 2.05, 1.0, flip)
        elif kind == "ball": draw_ball(img, d, cam, s.ball)
        elif kind == "goal": draw_goal(d, cam, data, s.bar if data > 0 else "bar", t)
        elif kind == "flag":
            polyline(d, cam, [(HX, -HY, 0), (HX, -HY, 1.6)], (230, 230, 230), 0.05, 1, 6)
            fp = [cam.proj((HX, -HY, 1.6)), cam.proj((HX - 0.1, -HY - 0.55 + 0.05 * math.sin(t * 8), 1.42)), cam.proj((HX, -HY, 1.25))]
            if all(fp): d.polygon([p[:2] for p in fp], fill=ACC)
        elif kind == "card":
            X, cardim, age = data
            sc = 0.3 + 0.7 * min(1, age / 0.25)
            draw_billboard(img, cam, (X[0], X[1], X[2]), cardim, 0.62 * sc)
    return img

def chip(text, col, size=26):
    f = mono(size); w = int(f.getlength(text)) + 28; h = size + 18
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 6, fill=col + (235,)); d.text((w / 2, h / 2), text, font=f, fill=(12, 12, 14), anchor="mm")
    return im

def title_block(img, k, t):
    tag, title, sub = META[k]
    a = ease(t / 0.25)
    d = ImageDraw.Draw(img)
    y0 = 215
    d.rectangle((60, y0 - 9, 76, y0 + 7), fill=ACC)
    d.text((92, y0), tag, font=mono(30), fill=ACC, anchor="lm")
    tf = font(BLK, 112)
    while tf.size > 60 and tf.getlength(title) > 960: tf = font(BLK, tf.size - 4)
    tim = txt(title, tf, WHITE, shadow=10)
    reveal = clamp(t / 0.3)
    if reveal < 1: tim = tim.crop((0, 0, max(1, int(tim.width * ease(reveal))), tim.height))
    img.alpha_composite(tim, (60 - 16 - 20, 245 - 16))
    sf = mono(27); spaced = " ".join(sub)
    while sf.getlength(spaced) > 960 and sf.size > 16: sf = mono(sf.size - 1)
    d.text((62, 402), spaced, font=sf, fill=GREY + (int(255 * clamp((t - 0.2) / 0.3)),), anchor="lm")

def frame(T):
    k, t, s, (pos, tgt, fov) = get_state(T)
    cam = Cam(pos, tgt, fov, W * S, H * S)
    big = render_world(s, cam, W * S, H * S, t)
    img = big.reduce(S).convert("RGBA")
    # vignette-ish top/bottom fade for legibility
    img.alpha_composite(FADE)
    # labels anchored in 3D
    for X, text, col, age in s.labels:
        p = cam.proj(X)
        if not p: continue
        x, y = p[0] / S, p[1] / S; c = chip(text, col)
        sc = 0.6 + 0.4 * ease(age / 0.2)
        put(img, c, x, y - 34, sc, clamp(age / 0.15))
        if age > 0.1: ImageDraw.Draw(img).line((x, y - 34 + c.height / 2, x, y - 6), fill=col + (200,), width=3)
    if s.counter:
        X, left = s.counter; p = cam.proj(X)
        if p:
            n = int(math.ceil(left)); col = ACC if left > 3 else RED
            r = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); dd = ImageDraw.Draw(r)
            dd.ellipse((8, 8, 142, 142), fill=(10, 10, 12, 210), outline=(255, 255, 255, 50), width=10)
            if left > 0: dd.arc((8, 8, 142, 142), -90, -90 + 360 * left / 8, fill=col, width=10)
            dd.text((75, 75), str(n), font=font(BLK, 70), fill=WHITE, anchor="mm")
            put(img, r, p[0] / S, p[1] / S - 70)
    if s.pip:
        label, tp = s.pip; a = ease((T - SC[k]["start"] - tp) / 0.3)
        pw, ph = 940, 520
        if k == 3:
            sp = St(); sp.bar = "tape"; sp.B[0] = (52, 0.3); sp.A = []; sp.B = [(52, 0.3)]; sp.ball = (43.3, -1.6, 0.11)
            pc = Cam((44, -2.5, 1.7), (52.5, 0, 1.4), 40, pw, ph)
        else:
            sp = St(); sp.A = []; sp.B = [(51, 0), (40, -12), (41, -3), (41.6, 5), (40, 14)]; sp.A = [(41.9, 2)]; sp.ball = (41.9, 2.6, 0.11)
            sp.paths.append(([(41.6, -HY, 0.03), (41.6, HY, 0.03)], ACC, False)); sp.paths.append(([(41.9, -HY, 0.03), (41.9, HY, 0.03)], RED, False))
            sp.rings.append(((41.9, 2), RED)); sp.rings.append(((41.6, 5), ACC))
            pc = Cam((41.8, -26, 16), (41.8, 2, 0), 42, pw, ph)
        sp.pip = None
        pim = render_world(sp, pc, pw, ph, t).convert("RGBA")
        if k == 8 and T - SC[k]["start"] - tp > 0.8:
            p = pc.proj((41.9, 2, 2.2))
            if p: pim.alpha_composite(chip("IMPEDIDO POR 30CM", RED, 24), (int(p[0] - 140), int(p[1] - 50)))
        frame_ = Image.new("RGBA", (pw + 8, ph + 8), ACC + (255,)); frame_.paste(pim, (4, 4))
        ImageDraw.Draw(frame_).rectangle((4, 4, 4 + 18 + mono(24).getlength(label) + 18, 44), fill=ACC)
        ImageDraw.Draw(frame_).text((22, 24), label, font=mono(24), fill=(12, 12, 14), anchor="lm")
        put(img, frame_, W / 2, 470 + 270 + 30 * (1 - a), 1, a)
    title_block(img, k, t)
    if not os.environ.get("NOCAP"): vlib.caption(img, SC[k]["words"], t, y=1500)
    fin = clamp((T - (TOTAL - 0.5)) / 0.5)
    rgb = img.convert("RGB")
    if T < 0.2 or fin > 0: rgb = Image.blend(rgb, Image.new("RGB", (W, H), (0, 0, 0)), max(1 - T / 0.2 if T < 0.2 else 0, fin))
    return rgb

def make_fade():
    a = np.zeros((H, W), np.uint8)
    for y in range(H):
        if y < 520: a[y] = int(170 * (1 - y / 520) ** 1.4)
        elif y > 1380: a[y] = int(200 * ((y - 1380) / 540) ** 1.3)
    im = Image.new("RGBA", (W, H), (10, 11, 13, 0)); im.putalpha(Image.fromarray(a)); return im
FADE = make_fade()

def render(a, b, name):
    tmp = f"{HERE}/{os.environ.get("CHDIR", "chunks")}/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(a, b): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0: os.replace(tmp, f"{HERE}/{os.environ.get("CHDIR", "chunks")}/{name}.mp4")
    print("done", name, flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for spec in sys.argv[2:]:
            frame(float(spec)).save(f"{HERE}/pv_{float(spec):06.2f}.jpg", quality=85)
    else:
        NF = int(round(TOTAL * FPS)); parts = int(sys.argv[2]); i = int(sys.argv[1])
        bounds = [NF * j // parts for j in range(parts + 1)]
        render(bounds[i], bounds[i + 1], f"c{i:02d}")
