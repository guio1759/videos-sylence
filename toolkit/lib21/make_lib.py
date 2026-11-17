import os, sys, math, subprocess
sys.path.insert(0, "/home/claude/work/palp"); sys.path.insert(1, "/home/claude/work/tat")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import vlib
from vlib import font, txt, put, ease, clamp, glow, card, fitf, BLK, BD, WHITE, trophy, confetti, rays, dust
from make_palp import badge, chip as pchip, mono, BG, ACC, RED, GREY, TEAMS
import eng3d as E
from eng3d import Cam, draw_pitch, draw_goal, draw_ball, draw_shadow, draw_billboard, make_player, ring, HX, HY, smooth, lerp
import words_lib as WM

HERE = "/home/claude/work/lib21"
W, H, FPS, S = 1080, 1920, 30, 2
LEAD = 0.2
WORDS = []
for i, (w, s) in enumerate(WM.W):
    e = WM.W[i + 1][1] if i + 1 < len(WM.W) else WM.END
    WORDS.append([w, s / 1000 + LEAD, min(e, s + 900) / 1000 + LEAD])
TOTAL = WM.END / 1000 + LEAD + 1.8
vlib.CF = font(BLK, 60)
def T(word, nth=0):
    c = 0
    for w, a, b in WORDS:
        if w.lower().strip(".,:;!?") == word.lower():
            if c == nth: return a
            c += 1
    raise KeyError(word)

GREEN = (0, 125, 62); FRED = (205, 25, 35)
SPR_P = make_player(GREEN, (245, 245, 245), (245, 245, 245))
SPR_PGK = make_player((60, 60, 70), (40, 40, 45))
SPR_F = make_player(FRED, (245, 245, 245), (20, 20, 20))
SPR_FGK = make_player((240, 200, 40), (30, 30, 30))
# Flamengo stripes
def stripes(im):
    im = im.copy(); d = ImageDraw.Draw(im); u = im.height / 100; cx = im.width / 2
    for y in (27, 36, 45):
        d.rectangle((cx - 13 * u, y * u, cx + 13 * u, (y + 4) * u), fill=(20, 20, 22))
    return im
SPR_F = stripes(SPR_F)

def tr(keys, t):
    """keys: [(t, *vals)] -> smooth piecewise"""
    if t <= keys[0][0]: return np.array(keys[0][1:], float)
    for a, b in zip(keys[:-1], keys[1:]):
        if t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 1
            return lerp(a[1:], b[1:], smooth(u))
    return np.array(keys[-1][1:], float)
def trl(keys, t):  # linear (ball rolling)
    if t <= keys[0][0]: return np.array(keys[0][1:], float)
    for a, b in zip(keys[:-1], keys[1:]):
        if t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 1
            return lerp(a[1:], b[1:], u)
    return np.array(keys[-1][1:], float)
def arcball(t, t0, t1, p0, p1, h):
    u = clamp((t - t0) / (t1 - t0)); p = lerp(p0, p1, u); return (p[0], p[1], 0.11 + h * 4 * u * (1 - u))

# ---------- base formations (PAL attacks +x) ----------
PAL0 = {"WEV": (-50, 0), "MAY": (-20, -25), "GOM": (-24, -6), "LUA": (-24, 6), "PIQ": (-20, 22), "DAN": (-8, -4), "ZER": (-8, 6),
        "VEI": (2, -2), "DUD": (8, 18), "RON": (10, -16), "RAP": (4, 6)}
FLA0 = {"DIE": (50, 0), "ISL": (32, 20), "RCA": (36, 5), "DLU": (36, -5), "FIL": (32, -20), "ARA": (24, 0), "AND": (22, 8),
        "EVE": (15, 15), "ARR": (14, -8), "BRU": (5, -15), "GAB": (6, 3)}
NAMES = {"GOM": "GÓMEZ", "MAY": "MAYKE", "VEI": "VEIGA", "GAB": "GABIGOL", "DLU": "DAVID LUIZ", "AND": "ANDREAS", "DEY": "DEYVERSON", "DIE": "DIEGO ALVES", "ARR": "ARRASCAETA"}

def world_state(t):
    """returns dict pal/fla positions, ball, cam (pos,tgt,fov), labels [(key,team,start,end)], goal flag"""
    pal = {k: np.array(v, float) for k, v in PAL0.items()}; fla = {k: np.array(v, float) for k, v in FLA0.items()}
    labels = []; rings = []
    tG, tM, tR, tB = T("gómez"), T("mayke"), T("rolou"), T("bateu")
    tE = T("empatou")
    tLance, tRec, tErr, tDey, tRou, tCara, tFez = T("lance"), T("recuou"), T("errou"), T("deyverson"), T("roubou"), T("cara"), T("fez")
    if t < T("mas") - 0.2:  # intro: formation, ball centre
        ball = (0.5, 0.3, 0.11)
        a = t * 0.05
        cam = ((-6 + 70 * math.cos(-1.9 + a), 70 * math.sin(-1.9 + a), 46), (0, 0, 0), 46)
    elif t < T("segundo") - 0.25:  # Veiga goal
        k = t
        pal["GOM"] = tr([(tG - 1.5, -24, -6), (tG, -19, -7)], k)
        pal["MAY"] = tr([(tG - 1.5, -6, -27), (tM + 0.6, 18, -27), (tR + 0.2, 31, -25)], k)
        pal["VEI"] = tr([(tG - 1.5, 6, -3), (tR, 26, -5), (tR + 0.9, 36, -4)], k)
        pal["RON"] = tr([(tG - 1.5, 14, -14), (tB, 38, -14)], k); pal["DUD"] = tr([(tG - 1.5, 10, 16), (tB, 34, 12)], k)
        pal["RAP"] = tr([(tG - 1.5, 4, 6), (tB, 30, 6)], k)
        fla["FIL"] = tr([(tG - 1.5, 24, -18), (tR + 0.5, 30, -22)], k); fla["DLU"] = tr([(tG - 1.5, 34, -6), (tB, 38, -7)], k)
        fla["RCA"] = tr([(tG - 1.5, 34, 4), (tB, 40, 0)], k); fla["ARA"] = tr([(tG - 1.5, 22, 0), (tB, 32, -2)], k)
        fla["DIE"] = tr([(tB, 50, 0), (tB + 0.5, 51, -2.2)], k)
        if k < tG + 0.05: ball = (pal["GOM"][0] + 0.6, pal["GOM"][1], 0.11)
        elif k < tM + 0.6: ball = arcball(k, tG + 0.05, tM + 0.6, (-18.4, -7), (18, -26.5), 13)
        elif k < tR + 0.2: p = pal["MAY"]; ball = (p[0] + 0.7, p[1] + 0.3, 0.11)
        elif k < tR + 0.9: ball = arcball(k, tR + 0.2, tR + 0.9, (31.7, -24.7), (35.6, -4), 0)
        elif k < tB + 0.1: ball = (35.6, -4, 0.11)
        else: ball = arcball(k, tB + 0.1, tB + 0.55, (36.3, -4), (52.8, -2.4), 0.8)
        labels = [("GOM", "P", tG - 1.2, tG + 0.8), ("MAY", "P", tM - 0.2, tR + 0.6), ("VEI", "P", tR, tB + 1.2)]
        bx, by = ball[0], ball[1]
        cam = (lerp((-40, -40, 30), (bx - 26, by - 34, 24), smooth(clamp((t - (T("mas") - 0.2)) / 1.2))), (bx + 4, by + 2, 0), 48)
        if t > tB + 0.6: cam = ((36.3 - 22, -4 - 30, 20), (46, -3, 1), 46)
    elif t < T("e", 4) - 0.2:  # Gabigol (FLA attacks -x)
        k = t
        pal = {kk: v - np.array([24, 0]) for kk, v in pal.items()}; pal["WEV"] = np.array([-50.5, 0.0])
        fla = {kk: np.array([-v[0] * 0.55 - 8, v[1]]) for kk, v in FLA0.items()}; fla["DIE"] = np.array([48.0, 0.0])
        fla["ARR"] = tr([(tE - 2.5, -28, 12), (tE - 1.0, -30, 10)], k); fla["GAB"] = tr([(tE - 2.5, -32, -4), (tE - 0.4, -39, 1)], k)
        if k < tE - 0.9: p = fla["ARR"]; ball = (p[0] - 0.7, p[1], 0.11)
        elif k < tE - 0.35: ball = arcball(k, tE - 0.9, tE - 0.35, (-30.7, 10), (-39.5, 1.2), 0)
        else: ball = arcball(k, tE - 0.2, tE + 0.25, (-39.6, 1.2), (-52.8, 1.8), 0.7)
        labels = [("GAB", "F", tE - 2.0, tE + 1.5)]
        cam = ((-14, 22, 22), (-42, 2, 0), 48)
    else:  # o lance
        k = t
        pal = {kk: np.array(v, float) + np.array([18, 0]) for kk, v in PAL0.items()}; pal["WEV"] = np.array([-40.0, 0])
        pal["VEI"] = np.array([28, 4.0]); pal["RON"] = np.array([30, -24.0]); pal["DUD"] = np.array([32, 16.0])
        fla["DLU"] = tr([(tRec - 2, 28, -2), (tRec, 30, -5), (tCara, 38, -4)], k)
        fla["AND"] = tr([(tRec, 38, -13), (tErr, 38.5, -12.5), (tCara, 41, -9)], k)
        fla["RCA"] = np.array([40, 6.0]); fla["FIL"] = np.array([30, -24.0]); fla["ISL"] = np.array([34, 20.0]); fla["ARA"] = np.array([22, 0.0])
        fla["DIE"] = tr([(tCara - 0.3, 50, 0), (tFez - 0.1, 47.6, -3.6)], k)
        dey = tr([(tRec, 29, -12), (tErr + 0.5, 31.5, -11), (tRou, 39.6, -9.4), (tCara + 0.2, 44.2, -6.6), (tFez, 45.6, -5.5)], k)
        pal["DEY"] = dey
        if k < tRec: p = fla["DLU"]; ball = (p[0] + 0.7, p[1], 0.11)
        elif k < tRec + 1.2: ball = arcball(k, tRec, tRec + 1.2, (30.7, -5), (38.6, -12.6), 0)
        elif k < tErr: ball = (38.6, -12.6, 0.11)
        elif k < tRou: ball = tuple(trl([(tErr, 38.6, -12.6, 0.11), (tErr + 0.4, 39.2, -10.8, 0.4), (tErr + 0.8, 39.6, -9.9, 0.11), (tRou, 39.9, -9.3, 0.11)], k))
        elif k < tFez: ball = (dey[0] + 0.8, dey[1] + 0.3, 0.11)
        else: ball = arcball(k, tFez, tFez + 0.5, (dey[0] + 0.8, dey[1] + 0.3), (52.8, -1.2), 0.5)
        labels = [("DLU", "F", tRec - 0.8, tErr), ("AND", "F", tRec + 0.6, tRou + 0.4), ("DEY", "P", tDey - 0.1, tFez + 1.0), ("DIE", "F", T("diego") - 0.2, tFez + 0.2)]
        if tErr < k < tRou: rings.append(((ball[0], ball[1]), RED))
        cam = (tuple(tr([(tLance - 0.5, 10, -42, 34), (tRec - 0.4, 24, -32, 20), (tErr, 30, -27, 13), (tRou, 30, -27, 13), (tCara, 34, -24, 13), (tFez + 0.4, 38, -22, 12)], k)),
               tuple(tr([(tLance - 0.5, 34, -6, 0), (tRec - 0.4, 35, -8, 0), (tErr, 38, -11, 0), (tRou, 39, -10, 0), (tCara, 45, -6, 0), (tFez + 0.4, 50, -3, 1)], k)), 46)
    return pal, fla, ball, cam, labels, rings

def render3d(t):
    pal, fla, ball, (pos, tgt, fov), labels, rings = world_state(t)
    cam = Cam(np.array(pos, float), np.array(tgt, float), fov, W * S, H * S)
    img = Image.new("RGB", (W * S, H * S), (12, 13, 15)); d = ImageDraw.Draw(img, "RGBA")
    draw_pitch(d, cam)
    for (x, y), col in rings: ring(d, cam, x, y, col + (235,), 1.2, t)
    objs = []
    for team, dd in (("P", pal), ("F", fla)):
        for k_, (x, y) in dd.items():
            spr = (SPR_PGK if k_ == "WEV" else SPR_P) if team == "P" else (SPR_FGK if k_ == "DIE" else SPR_F)
            objs.append((cam.cam((x, y, 0.9))[2], "p", (x, y, spr)))
    objs.append((cam.cam(ball)[2] - 0.05, "b", None))
    for sg in (-1, 1): objs.append((cam.cam((sg * HX, 0, 1.2))[2] + 0.5, "g", sg))
    for z, kind, dat in objs:
        if kind == "p": draw_shadow(d, cam, dat[0], dat[1])
    draw_shadow(d, cam, ball[0], ball[1], 0.13, 90)
    for z, kind, dat in sorted(objs, key=lambda o: -o[0]):
        if z < cam.near: continue
        if kind == "p": draw_billboard(img, cam, (dat[0], dat[1], 0), dat[2], 2.05)
        elif kind == "b": draw_ball(img, d, cam, ball)
        else: draw_goal(d, cam, dat)
    out = img.reduce(S).convert("RGBA")
    for key, team, a, b in labels:
        if not (a < t < b): continue
        p = (pal if team == "P" else fla)[key]; pr = cam.proj((p[0], p[1], 2.4))
        if not pr: continue
        x, y = pr[0] / S, pr[1] / S; age = t - a; v = ease(age / 0.25) * (1 - ease((t - b + 0.25) / 0.25))
        c = pchip(NAMES[key], ACC if team == "P" else (235, 235, 235), 26)
        put(out, c, x, y - 40, 0.7 + 0.3 * v, v)
        ImageDraw.Draw(out).line((x, y - 40 + c.height / 2, x, y - 8), fill=(255, 255, 255, int(160 * v)), width=3)
    return out

def make_fade():
    a = np.zeros((H, W), np.uint8)
    for y in range(H):
        if y < 560: a[y] = int(190 * (1 - y / 560) ** 1.3)
        elif y > 1300: a[y] = int(215 * ((y - 1300) / 620) ** 1.2)
    im = Image.new("RGBA", (W, H), (10, 11, 13, 0)); im.putalpha(Image.fromarray(a)); return im
FADE = make_fade()

def scorebug(img, t, sp, sf, hl=0):
    c = card(420, 100, (14, 16, 18, 235), 50, (255, 255, 255, 40), 2)
    c.alpha_composite(badge("PAL", 64).resize((84, 84)), (8, 8)); c.alpha_composite(badge("FLA", 64).resize((84, 84)), (420 - 92, 8))
    ImageDraw.Draw(c).text((210, 50), f"{sp}  x  {sf}", font=font(BLK, 56), fill=WHITE, anchor="mm")
    put(img, c, W / 2, 400, 1 + 0.15 * hl, 1)

def big_event(img, t, t0, l1, l2, col=ACC, dur=2.2):
    if not (t0 < t < t0 + dur): return
    v = ease((t - t0) / 0.25) * (1 - ease((t - t0 - dur + 0.3) / 0.3))
    put(img, glow(txt(l1, fitf(BLK, l1, 960, 150), col, shadow=10), col, 16, 0.7), W / 2, 760, 1.25 - 0.25 * ease((t - t0) / 0.3), v)
    if l2: put(img, txt(l2, font(BLK, 54), WHITE, shadow=8), W / 2, 880, 1, v)

def frame(Tm):
    t = Tm; fl = 0.0
    tGoal1, tGab, tGoal2 = T("bateu") + 0.55, T("empatou") + 0.25, T("fez") + 0.5
    s_ch = T("palmeiras", 1) - 0.2
    if t < s_ch:
        img = render3d(t); img.alpha_composite(FADE)
        d = ImageDraw.Draw(img); d.rectangle((60, 196, 76, 212), fill=ACC); d.text((92, 204), "FINAL · LIBERTADORES 2021", font=mono(30), fill=ACC, anchor="lm")
        if t < T("mas") - 0.2:
            u = ease(t / 0.4); a = 1 - ease((t - T("mas") + 0.5) / 0.3)
            put(img, txt("27/11/2021", font(BLK, 120), WHITE, shadow=10), W / 2, 420, 1, u * a)
            tp = T("palmeiras")
            if t > tp - 0.2:
                v = ease((t - tp + 0.2) / 0.3) * a
                put(img, badge("PAL", 210), W / 2 - 230, 640, 1, v); put(img, badge("FLA", 210), W / 2 + 230, 640, 1, v)
                put(img, txt("x", font(BD, 70), GREY), W / 2, 640, 1, v)
            tc = T("centenário")
            if t > tc - 0.2: put(img, pchip("ESTÁDIO CENTENÁRIO · MONTEVIDÉU", WHITE, 30), W / 2, 820, 1, ease((t - tc + 0.2) / 0.3) * a)
            tt = T("torcida")
            if t > tt:
                v = ease((t - tt) / 0.3) * a
                put(img, pchip("ARQUIBANCADA: MAIORIA RUBRO-NEGRA", FRED, 30, (255, 255, 255)), W / 2, 900, 1, v)
        else:
            sp = 1 if t > tGoal1 else 0; sf = 1 if t > tGab else 0
            if t > tGoal2: sp = 2
            hl = max(0, 1 - abs(t - tGoal1) / 0.3) if abs(t - tGoal1) < 0.3 else (max(0, 1 - abs(t - tGab) / 0.3) if abs(t - tGab) < 0.3 else (max(0, 1 - abs(t - tGoal2) / 0.3) if abs(t - tGoal2) < 0.3 else 0))
            scorebug(img, t, sp, sf, hl)
            tag = "1º TEMPO · 5'" if t < T("segundo") - 0.25 else ("2º TEMPO · 72'" if t < T("e", 4) - 0.2 else "PRORROGAÇÃO")
            put(img, txt(tag, mono(28), GREY), W / 2, 480, 1, 1)
            big_event(img, t, tGoal1, "GOL!", "RAPHAEL VEIGA")
            big_event(img, t, tGab, "1 x 1", "GABIGOL EMPATA", (235, 235, 235))
            big_event(img, t, T("prorrogação") - 0.1, "PRORROGAÇÃO", None, WHITE, 1.6)
            big_event(img, t, tGoal2, "GOL!", "DEYVERSON", ACC, 2.0)
            te = T("errou")
            if te < t < T("roubou"): put(img, pchip("ERRO DE DOMÍNIO", RED, 36, (255, 255, 255)), W / 2, 600, 1, ease((t - te) / 0.25))
            for tg in (tGoal1, tGab, tGoal2):
                if 0 <= t - tg < 0.12: fl = 0.25 * (1 - (t - tg) / 0.12)
    else:
        img = BG.copy(); dust(img, t, (255, 230, 170))
        d = ImageDraw.Draw(img); d.rectangle((60, 196, 76, 212), fill=ACC); d.text((92, 204), "FINAL · LIBERTADORES 2021", font=mono(30), fill=ACC, anchor="lm")
        s_tw, s_sat, s_cta = T("e", 6) - 0.2, T("neste") - 0.2, T("comenta") - 0.2
        if t < s_tw + 0.3:
            u = ease((t - s_ch) / 0.4); a = 1 - ease((t - s_tw) / 0.3)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rays(lay, t, W / 2, 760, a=0.6 * u)
            put(lay, glow(trophy(480), ACC, 20, 0.6), W / 2, 760, 1.15 - 0.15 * u, u)
            put(lay, glow(txt("CAMPEÃO", font(BLK, 140), ACC, shadow=10), ACC, 16, 0.7), W / 2, 1090, 1, u)
            ts = T("segunda")
            if t > ts - 0.1:
                v = ease((t - ts + 0.1) / 0.3)
                put(lay, pchip("2020", ACC, 40), W / 2 - 110, 1210, 1, v); put(lay, pchip("2021", ACC, 40), W / 2 + 110, 1210, 1, v)
                put(lay, txt("BICAMPEÃO SEGUIDO", font(BLK, 56), WHITE), W / 2, 1300, 1, v)
            confetti(lay, t - s_ch, u)
            if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
            img.alpha_composite(lay)
        if s_tw < t < s_sat + 0.3:
            u = ease((t - s_tw) / 0.35); a = 1 - ease((t - s_sat) / 0.3) if t > s_sat else 1
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            put(lay, txt("O MAIS CURIOSO", font(BLK, 84), WHITE, shadow=8), W / 2, 380, 1, u)
            ta = T("andreas", 1)
            if t > ta - 0.2:
                v = ease((t - ta + 0.2) / 0.35)
                put(lay, SPR_F.resize((240, 480)), W / 2 - 230, 800, 1, v); put(lay, badge("FLA", 120), W / 2 - 230, 1110, 1, v)
                put(lay, txt("2021", font(BLK, 64), GREY), W / 2 - 230, 520, 1, v)
                put(lay, txt("→", font(BLK, 120), WHITE), W / 2, 800, 1, v)
                tv = T("camisa")
                if t > tv - 0.2:
                    v2 = ease((t - tv + 0.2) / 0.35)
                    put(lay, glow(SPR_P.resize((240, 480)), ACC, 14, 0.5), W / 2 + 230, 800, 1.2 - 0.2 * v2, v2); put(lay, badge("PAL", 120), W / 2 + 230, 1110, 1, v2)
                    put(lay, txt("2026", font(BLK, 64), ACC), W / 2 + 230, 520, 1, v2)
                put(lay, txt("ANDREAS PEREIRA", font(BLK, 66), WHITE, shadow=8), W / 2, 1240, 1, v)
            if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
            img.alpha_composite(lay)
        if s_sat < t < s_cta + 0.3:
            u = ease((t - s_sat) / 0.35); a = 1 - ease((t - s_cta) / 0.3) if t > s_cta else 1
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            put(lay, txt("SÁBADO · 21/11 · 16H30", mono(40), ACC), W / 2, 520, 1, u)
            put(lay, badge("PAL", 280), W / 2 - 240, 760, 1, u); put(lay, badge("FLA", 280), W / 2 + 240, 760, 1, u)
            put(lay, txt("x", font(BD, 90), GREY), W / 2, 760, 1, u)
            td = T("decidir")
            if t > td - 0.2: put(lay, pchip("PODE DECIDIR O BRASILEIRÃO", RED, 40, (255, 255, 255)), W / 2, 1010, 1, ease((t - td + 0.2) / 0.3))
            if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
            img.alpha_composite(lay)
        if t > s_cta:
            v = ease((t - s_cta) / 0.35)
            put(img, txt("QUEM LEVA", font(BLK, 110), WHITE, shadow=8), W / 2, 720, 1, v)
            put(img, glow(txt("ESSA?", font(BLK, 160), ACC, shadow=10), ACC, 16, 0.7), W / 2, 880, 1.15 - 0.15 * v, v)
            put(img, txt("COMENTA ↓", font(BLK, 76), WHITE, 4, (0, 0, 0), 6), W / 2, 1060 + 10 * math.sin(t * 7), 1, ease((t - s_cta - 0.4) / 0.3))
        if 0 <= t - s_ch < 0.12: fl = 0.2
    vlib.caption(img, WORDS, t, y=1500)
    vlib.progress(img, t, TOTAL)
    dark = max(1 - t / 0.2 if t < 0.2 else 0, (t - (TOTAL - 0.5)) / 0.5)
    return vlib.post(img, int(t * FPS), fl, dark)

def render(a, b, name):
    od = f"{HERE}/chunks"; os.makedirs(od, exist_ok=True); tmp = f"{od}/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(a, b): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0: os.replace(tmp, f"{od}/{name}.mp4")
    print("done", name, flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for s in sys.argv[2:]: frame(float(s)).save(f"{HERE}/pv_{float(s):05.1f}.jpg", quality=85)
    else:
        NF = int(round(TOTAL * FPS)); parts = int(sys.argv[2]); i = int(sys.argv[1])
        bd = [NF * j // parts for j in range(parts + 1)]; render(bd[i], bd[i + 1], f"c{i:02d}")
