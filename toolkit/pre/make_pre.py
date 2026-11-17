import os, sys, math, subprocess
sys.path.insert(0, "/home/claude/work/palp"); sys.path.insert(1, "/home/claude/work/tat"); sys.path.insert(2, "/home/claude/work/lib21")
import numpy as np
from PIL import Image, ImageDraw
import vlib
from vlib import font, txt, put, ease, clamp, glow, card, fitf, BLK, BD, WHITE, dust
from make_palp import badge, chip as pchip, mono, BG, ACC, RED, GREY
from eng3d import Cam, draw_pitch, draw_goal, draw_shadow, draw_billboard, make_player, polyline, poly, circle_pts, HX, HY, smooth, lerp
import words_pre as WM

HERE = "/home/claude/work/pre"
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

GREEN = (0, 125, 62); BLUE = (25, 75, 185)
SP = make_player(GREEN, (245, 245, 245), (245, 245, 245)); SPG = make_player((60, 60, 70), (40, 40, 45))
SC = make_player(BLUE, (245, 245, 245), (245, 245, 245)); SCG = make_player((240, 200, 40), (30, 30, 30))
def ghost(im, a=0.32):
    g = im.copy(); g.putalpha(g.split()[3].point(lambda v: int(v * a))); return g
SC_GH = ghost(SC)

# Palmeiras 4-3-3 (attacks +x)
PAL = [("CARLOS MIGUEL", (-48, 0), "carlos", 0), ("KHELLVEN", (-30, -24), "khellven", 0), ("FUCHS", (-33, -8), "fuchs", 0), ("BARBOZA", (-33, 8), "barboza", 0),
       ("ARTHUR", (-30, 24), "arthur", 0), ("MARLON", (-18, 0), "marlon", 0), ("EVANGELISTA", (-12, -12), "evangelista", 0), ("ANDREAS", (-12, 12), "andreas", 0),
       ("F. ANDERSON", (0, -22), "felipe", 0), ("VITOR ROQUE", (2, 2), "vitor", 0), ("SOSA", (0, 22), "sosa", 0)]
# Cruzeiro (defends +x)
CRU = [((48, 0), "GK"), ((32, 22), None), ((34, 7), "CB1"), ((34, -7), "CB2"), ((32, -22), None), ((22, -10), None), ((22, 10), None), ((20, 0), None),
       ((10, 22), "ARROYO"), ((8, 0), "KAIO"), ((10, -20), None)]

def camkeys(t):
    tA, tC, tD, tE, tF, tG = T("provável") - 0.3, T("cruzeiro", 1) - 0.2, T("perigo") - 0.2, T("chave") - 0.3, T("meu") - 0.3, 0
    keys = [(0, (-30, -70, 60), (5, 0, 0), 46), (tA, (-82, -18, 46), (-12, 0, 0), 50), (tC - 0.3, (-82, -18, 46), (-12, 0, 0), 50),
            (tC + 0.8, (10, -48, 34), (34, 0, 0), 46), (tD - 0.2, (12, -46, 34), (34, 0, 0), 46),
            (tD + 0.8, (34, 40, 36), (2, 8, 0), 50), (tE - 0.2, (32, 42, 36), (-2, 10, 0), 50),
            (tE + 0.9, (-66, 0.5, 72), (8, 0, 0), 60), (tF, (-64, 0.5, 72), (9, 0, 0), 60)]
    if t <= keys[0][0]: k = keys[0]; return k[1], k[2], k[3]
    for a, b in zip(keys[:-1], keys[1:]):
        if t <= b[0]:
            u = smooth((t - a[0]) / (b[0] - a[0])); return lerp(a[1], b[1], u), lerp(a[2], b[2], u), a[3] + (b[3] - a[3]) * u
    k = keys[-1]; return k[1], k[2], k[3]

def arrow(d, cam, pts, col, u, w=0.35):
    """draw path progressively (u in 0..1) with head"""
    if u <= 0: return
    pts = [np.array(p, float) for p in pts]
    L = [np.linalg.norm(b - a) for a, b in zip(pts[:-1], pts[1:])]; tot = sum(L); goal = tot * u; out = [pts[0]]; acc = 0
    for (a, b), l in zip(zip(pts[:-1], pts[1:]), L):
        if acc + l >= goal: out.append(a + (b - a) * ((goal - acc) / l)); break
        out.append(b); acc += l
    out3 = [(p[0], p[1], 0.05) for p in out]
    polyline(d, cam, out3, col, w, 3, 26)
    if len(out) >= 2:
        tip = out[-1]; dirv = out[-1] - out[-2]; n = np.linalg.norm(dirv)
        if n > 1e-6:
            dirv /= n; perp = np.array([-dirv[1], dirv[0]])
            poly(d, cam, [(*(tip + dirv * 2.2), 0.05), (*(tip + perp * 1.6), 0.05), (*(tip - perp * 1.6), 0.05)], col)

def render3d(t):
    pos, tgt, fov = camkeys(t)
    cam = Cam(np.array(pos, float), np.array(tgt, float), fov, W * S, H * S)
    img = Image.new("RGB", (W * S, H * S), (12, 13, 15)); d = ImageDraw.Draw(img, "RGBA")
    draw_pitch(d, cam)
    tC, tD, tE, tF = T("cruzeiro", 1) - 0.2, T("perigo") - 0.2, T("chave") - 0.3, T("meu") - 0.3
    tA = T("provável") - 0.3
    labels = []
    # zones / arrows
    if tE < t < tF + 0.3:
        u = ease((t - T("três", 1)) / 0.4)
        if u > 0: poly(d, cam, [(-18, 0, 0.03), (-12, -12, 0.03), (-12, 12, 0.03)], ACC + (int(70 * u),)); polyline(d, cam, [(-18, 0, 0.04), (-12, -12, 0.04), (-12, 12, 0.04), (-18, 0, 0.04)], ACC + (int(220 * u),), 0.18, 2, 14)
        uz = ease((t - T("zaga") + 0.2) / 0.4)
        if uz > 0: poly(d, cam, [(28, -14, 0.03), (40, -14, 0.03), (40, 14, 0.03), (28, 14, 0.03)], RED + (int(70 * uz),))
        ts = T("sosa", 1)
        arrow(d, cam, [(0, 22), (14, 18), (30, 8)], ACC + (240,), ease((t - ts + 0.2) / 0.9))
        arrow(d, cam, [(2, 2), (16, 0), (32, -4)], ACC + (240,), ease((t - T("vitor", 1) + 0.1) / 0.9))
    if tD + 0.5 < t < tE + 0.3:
        arrow(d, cam, [(10, 22), (-8, 25), (-26, 22)], (90, 150, 255, 240), ease((t - T("direita") + 0.3) / 1.0))
    objs = []
    for i, (name, (x, y), key, _) in enumerate(PAL):
        ta = (T(key) - 0.1) if key in ("carlos",) else T(key) - 0.1
        if t < tA: vis = 1.0 if t < T("palmeiras", 1) else 0.0
        else: vis = ease((t - ta) / 0.3) if t < tC else 1.0
        if t < T("palmeiras", 1): vis = 0
        if vis <= 0.01: continue
        objs.append((cam.cam((x, y, 0.9))[2], (x, y, SPG if i == 0 else SP, vis)))
        if tA < t < tC and t > ta: labels.append(((x, y), name, ACC, ease((t - ta) / 0.25) * (1 - ease((t - tC + 0.4) / 0.3))))
    if t > tC - 0.5:
        cv = ease((t - tC + 0.5) / 0.5)
        for (x, y), tag in CRU:
            spr = SCG if tag == "GK" else SC
            objs.append((cam.cam((x, y, 0.9))[2], (x, y, spr, cv)))
        # ghosts for absentees
        if tC < t < tD + 0.4:
            for (x, y), name, tn, col in [((34, 7), "JOÃO MARCELO · FORA DA TEMPORADA", T("joão"), RED), ((34, -7), "JONATHAN JESUS · SELEÇÃO", T("jonathan"), RED), ((32, 0), "FABRÍCIO BRUNO · DÚVIDA", T("fabrício"), ACC)]:
                if t > tn - 0.1:
                    a = ease((t - tn + 0.1) / 0.3) * (1 - ease((t - tD - 0.1) / 0.3))
                    labels.append(((x, y), name, col, a))
                    if col == RED: objs.append((cam.cam((x - 1.5, y, 0.9))[2], (x - 1.5, y, SC_GH, a)))
        if tD < t < tE + 0.3:
            tk = T("kaio")
            if t > tk - 0.1: labels.append(((8, 0), "KAIO JORGE", (120, 170, 255), ease((t - tk + 0.1) / 0.3)))
            ta2 = T("arroyo")
            if t > ta2 - 0.6: labels.append(((10, 22), "ARROYO", (120, 170, 255), ease((t - ta2 + 0.6) / 0.3)))
        if tE < t < tF + 0.3:
            for (x, y), nm, tn in [((0, 22), "SOSA", T("sosa", 1)), ((2, 2), "VITOR ROQUE", T("vitor", 1))]:
                if t > tn - 0.2: labels.append(((x, y), nm, ACC, ease((t - tn + 0.2) / 0.3)))
            if t > T("zaga") - 0.2: labels.append(((34, 0), "ZAGA IMPROVISADA", RED, ease((t - T("zaga") + 0.2) / 0.3)))
    for z, (x, y, spr, a) in objs: draw_shadow(d, cam, x, y, a=int(110 * a))
    for sg in (-1, 1): draw_goal(d, cam, sg)
    for z, (x, y, spr, a) in sorted(objs, key=lambda o: -o[0]):
        if z < cam.near: continue
        draw_billboard(img, cam, (x, y, 0), spr, 2.05, a)
    out = img.reduce(S).convert("RGBA")
    for (x, y), text, col, a in labels:
        if a <= 0.01: continue
        pr = cam.proj((x, y, 2.4))
        if not pr: continue
        px, py = pr[0] / S, pr[1] / S
        c = pchip(text, col, 24, (255, 255, 255) if col == RED else (12, 12, 14))
        put(out, c, px, py - 36, 0.75 + 0.25 * a, a)
        ImageDraw.Draw(out).line((px, py - 36 + c.height / 2, px, py - 6), fill=(255, 255, 255, int(150 * a)), width=3)
    return out

def make_fade():
    a = np.zeros((H, W), np.uint8)
    for y in range(H):
        if y < 560: a[y] = int(200 * (1 - y / 560) ** 1.3)
        elif y > 1300: a[y] = int(215 * ((y - 1300) / 620) ** 1.2)
    im = Image.new("RGBA", (W, H), (10, 11, 13, 0)); im.putalpha(Image.fromarray(a)); return im
FADE = make_fade()

def title(img, t, t0, l1, l2=None, y=330):
    v = ease((t - t0) / 0.3)
    put(img, txt(l1, fitf(BLK, l1, 980, 80), WHITE, shadow=8), W / 2, y, 1, v)
    if l2: put(img, txt(l2, mono(30), ACC), W / 2, y + 70, 1, v)

def frame(t):
    fl = 0
    s_pred, s_cta = T("meu") - 0.3, T("comenta") - 0.2
    tB, tA, tC, tD, tE = T("palmeiras", 1) - 0.2, T("provável") - 0.3, T("cruzeiro", 1) - 0.2, T("perigo") - 0.2, T("chave") - 0.3
    if t < s_pred:
        img = render3d(t); img.alpha_composite(FADE)
        if t < tB:
            u = ease(t / 0.35)
            put(img, txt("PRÉ-JOGO", mono(36), ACC), W / 2, 420, 1, u)
            put(img, badge("CRU", 240), W / 2 - 240, 640, 1, u); put(img, badge("PAL", 240), W / 2 + 240, 640, 1, u)
            put(img, txt("x", font(BD, 80), GREY), W / 2, 640, 1, u)
            put(img, pchip("HOJE · 20H30 · MINEIRÃO", WHITE, 32), W / 2, 850, 1, u)
            tr_ = T("remendadas")
            if t > tr_ - 0.3: put(img, pchip("AS DUAS DEFESAS REMENDADAS", RED, 38, (255, 255, 255)), W / 2, 940, 1, ease((t - tr_ + 0.3) / 0.3))
        elif t < tA:
            title(img, t, tB, "PALMEIRAS SEM")
            for i, (nm, key) in enumerate([("GÓMEZ", "gómez"), ("MURILO", "murilo"), ("PIQUEREZ", "piquerez")]):
                tn = T(key) - 0.15
                if t < tn: continue
                v = ease((t - tn) / 0.3); x = W / 2 + (i - 1) * 320
                put(img, SP.resize((150, 300)), x, 620, 1, v)
                d = ImageDraw.Draw(img); a = int(255 * v)
                d.line((x - 70, 530, x + 70, 710), fill=RED + (a,), width=14); d.line((x + 70, 530, x - 70, 710), fill=RED + (a,), width=14)
                put(img, txt(nm, font(BLK, 44), WHITE), x, 820, 1, v)
            tb = T("abandonar") - 0.2
            if t > tb:
                v = ease((t - tb) / 0.3)
                put(img, pchip("3 ZAGUEIROS", GREY, 36), W / 2 - 230, 960, 1, v); put(img, txt("→", font(BLK, 70), WHITE), W / 2, 960, 1, v)
                put(img, pchip("LINHA DE 4", ACC, 36), W / 2 + 210, 960, 1, ease((t - tb - 0.4) / 0.3))
        elif t < tC:
            title(img, t, tA, "PROVÁVEL PALMEIRAS", "4-3-3 · ZAGA INÉDITA")
        elif t < tD:
            title(img, t, tC, "CRUZEIRO TAMBÉM SOFRE ATRÁS", "TÉC. ARTUR JORGE")
        elif t < tE:
            title(img, t, tD, "O PERIGO DO CRUZEIRO")
            tk = T("dois")
            if t > tk - 0.2: put(img, pchip("KAIO JORGE: 2 GOLS NO ÚLTIMO JOGO", (120, 170, 255), 32), W / 2, 470, 1, ease((t - tk + 0.2) / 0.3))
        else:
            title(img, t, tE, "A CHAVE DO JOGO", "MEIO COM 3 + VELOCIDADE")
        for tg in (tB, tA, tC, tD, tE):
            if 0 <= t - tg < 0.1: fl = 0.12 * (1 - (t - tg) / 0.1)
    else:
        img = BG.copy(); dust(img, t, (255, 230, 170))
        if t < s_cta + 0.3:
            u = ease((t - s_pred) / 0.35); a = 1 - ease((t - s_cta) / 0.3) if t > s_cta else 1
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            put(lay, txt("MEU PALPITE", font(BLK, 84), WHITE, shadow=8), W / 2, 380, 1, u)
            put(lay, badge("CRU", 230), W / 2 - 280, 640, 1, u); put(lay, glow(badge("PAL", 230), ACC, 16, 0.7), W / 2 + 280, 640, 1, u)
            tr_ = T("dois", 1) - 0.1
            if t > tr_:
                v = ease((t - tr_) / 0.3); pop = 1 + 0.3 * (1 - v)
                put(lay, txt("1", font(BLK, 170), WHITE, shadow=10), W / 2 - 80, 640, pop, v)
                put(lay, txt("x", font(BD, 70), GREY), W / 2, 640, 1, v)
                put(lay, txt("2", font(BLK, 170), ACC, shadow=10), W / 2 + 80, 640, pop, v)
            for i, (text, col, tn) in enumerate([("PALMEIRAS PRECISA VENCER", ACC, T("precisa")), ("CRUZEIRO NÃO BRIGA POR MAIS NADA", WHITE, T("cruzeiro", 2))]):
                if t > tn - 0.1: put(lay, pchip(text, col, 34), W / 2, 900 + i * 100, 1, ease((t - tn + 0.1) / 0.3))
            if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
            img.alpha_composite(lay)
            if 0 <= t - tr_ < 0.12: fl = 0.22 * (1 - (t - tr_) / 0.12)
        if t > s_cta:
            v = ease((t - s_cta) / 0.35)
            put(img, txt("QUAL O SEU", font(BLK, 100), WHITE, shadow=8), W / 2, 720, 1, v)
            put(img, glow(txt("PLACAR?", font(BLK, 150), ACC, shadow=10), ACC, 16, 0.7), W / 2, 870, 1.15 - 0.15 * v, v)
            put(img, txt("COMENTA ↓", font(BLK, 76), WHITE, 4, (0, 0, 0), 6), W / 2, 1060 + 10 * math.sin(t * 7), 1, ease((t - s_cta - 0.4) / 0.3))
    d = ImageDraw.Draw(img); d.rectangle((60, 196, 76, 212), fill=ACC); d.text((92, 204), "CRUZEIRO x PALMEIRAS · 35ª RODADA", font=mono(30), fill=ACC, anchor="lm")
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
