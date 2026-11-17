import os, sys, math, subprocess
sys.path.insert(0, "/home/claude/work/palp")
import numpy as np
from PIL import Image, ImageDraw
import vlib
from vlib import font, txt, put, ease, glow, card, fitf, BLK, BD, WHITE, dust, flag
from make_palp import chip, mono, BG, ACC, RED, GREY
import words_bra as WM

HERE = "/home/claude/work/bra"
W, H, FPS = 1080, 1920, 30
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

YEL = (254, 223, 0)
def fl(kind, w=260, h=174):
    if kind == "BRA": return flag("BRA", w, h)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "NOR":
        d.rectangle((0, 0, w, h), fill=(186, 12, 47)); cx = w * 0.36
        d.rectangle((cx - h * 0.125, 0, cx + h * 0.125, h), fill=WHITE); d.rectangle((0, h * 0.375, w, h * 0.625), fill=WHITE)
        d.rectangle((cx - h * 0.0625, 0, cx + h * 0.0625, h), fill=(0, 32, 91)); d.rectangle((0, h * 0.4375, w, h * 0.5625), fill=(0, 32, 91))
    elif kind == "JPN":
        d.rectangle((0, 0, w, h), fill=WHITE); r = h * 0.3; d.ellipse((w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), fill=(188, 0, 45))
    elif kind == "SIN":
        d.rectangle((0, 0, w, h / 2), fill=(239, 51, 64)); d.rectangle((0, h / 2, w, h), fill=WHITE)
        r = h * 0.17; cx, cy = w * 0.2, h * 0.25
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE); d.ellipse((cx - r + r * 0.35, cy - r, cx + r + r * 0.35, cy + r), fill=(239, 51, 64))
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5; sx, sy = cx + r * 1.05 + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a); s = r * 0.13
            d.ellipse((sx - s, sy - s, sx + s, sy + s), fill=WHITE)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=255)
    from PIL import ImageChops
    im.putalpha(ImageChops.multiply(im.split()[3], m)); return im

def clock(size=300, t=0, ring=False):
    S = 3; s = size * S; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for sx in (-1, 1): d.ellipse((s / 2 + sx * s * 0.28 - s * 0.14, s * 0.02, s / 2 + sx * s * 0.28 + s * 0.14, s * 0.3), fill=(230, 60, 60))
    d.ellipse((s * 0.1, s * 0.12, s * 0.9, s * 0.92), fill=(240, 240, 235), outline=(30, 30, 34), width=int(s * 0.05))
    c = (s / 2, s * 0.52)
    for k in range(12):
        a = k * math.pi / 6; r0, r1 = s * 0.3, s * 0.34
        d.line((c[0] + r0 * math.sin(a), c[1] - r0 * math.cos(a), c[0] + r1 * math.sin(a), c[1] - r1 * math.cos(a)), fill=(40, 40, 44), width=int(s * 0.02))
    a7 = 7 * math.pi / 6; d.line((c[0], c[1], c[0] + s * 0.18 * math.sin(a7), c[1] - s * 0.18 * math.cos(a7)), fill=(30, 30, 34), width=int(s * 0.04))
    d.line((c[0], c[1], c[0], c[1] - s * 0.28), fill=(30, 30, 34), width=int(s * 0.025))
    d.line((s * 0.25, s * 0.9, s * 0.18, s * 0.98), fill=(30, 30, 34), width=int(s * 0.04)); d.line((s * 0.75, s * 0.9, s * 0.82, s * 0.98), fill=(30, 30, 34), width=int(s * 0.04))
    im = im.resize((size, size), Image.LANCZOS)
    if ring: im = im.rotate(8 * math.sin(t * 45), resample=Image.BICUBIC)
    return im

def scorecard(lay, t, t0, a_kind, a_name, sa, b_kind, b_name, sb, info, y=640, hl=None, t_score=None):
    u = ease((t - t0) / 0.35)
    put(lay, card(980, 400, (18, 21, 24, 240), 34, (255, 255, 255, 30), 2), W / 2, y, 1, u)
    put(lay, txt(info, mono(28), GREY), W / 2, y - 160, 1, u)
    for k, (kind, nm, x) in enumerate(((a_kind, a_name, W / 2 - 300), (b_kind, b_name, W / 2 + 300))):
        put(lay, fl(kind, 220, 146), x, y - 20, 1, u); put(lay, txt(nm, font(BLK, 42), WHITE), x, y + 100, 1, u)
    ts = t0 if t_score is None else t_score
    if t > ts:
        v = ease((t - ts) / 0.3)
        put(lay, txt(f"{sa} x {sb}", font(BLK, 120), hl or WHITE, shadow=10), W / 2, y - 20, 1.3 - 0.3 * v, v)

def redcard(lay, x, y, v, rot=-10):
    c = Image.new("RGBA", (110, 150), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle((4, 4, 106, 146), 12, fill=(220, 30, 40))
    put(lay, c, x, y, 1.4 - 0.4 * v, v, rot=rot)

def pitch2d(lay, t, t0, players):
    u = ease((t - t0) / 0.4)
    pw, ph = 860, 1000; px, py = W / 2 - pw / 2, 420
    p = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    for i in range(10): d.rectangle((0, i * ph / 10, pw, (i + 1) * ph / 10), fill=(30, 92, 50, 235) if i % 2 else (34, 102, 56, 235))
    lc = (255, 255, 255, 120)
    d.rectangle((10, 10, pw - 10, ph - 10), outline=lc, width=4); d.line((10, ph / 2, pw - 10, ph / 2), fill=lc, width=4)
    d.ellipse((pw / 2 - 90, ph / 2 - 90, pw / 2 + 90, ph / 2 + 90), outline=lc, width=4)
    d.rectangle((pw / 2 - 200, ph - 170, pw / 2 + 200, ph - 10), outline=lc, width=4); d.rectangle((pw / 2 - 200, 10, pw / 2 + 200, 170), outline=lc, width=4)
    put(lay, p, W / 2, py + ph / 2, 1, u)
    for name, (fx, fy), tn in players:
        if t < tn - 0.1: continue
        v = ease((t - tn + 0.1) / 0.3)
        x, y = px + fx * pw, py + fy * ph
        dot = Image.new("RGBA", (84, 84), (0, 0, 0, 0)); dd = ImageDraw.Draw(dot)
        dd.ellipse((4, 4, 80, 80), fill=YEL, outline=(0, 120, 60), width=7)
        put(lay, dot, x, y, 1.3 - 0.3 * v, v)
        put(lay, chip(name, (12, 12, 14), 24, WHITE), x, y + 62, 1, v)

def frame(t):
    img = BG.copy(); dust(img, t, (255, 230, 170)); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); flash = 0
    sB, sC, sD, sE, sF = T("na") - 0.25, T("e", 3) - 0.2, T("time") - 0.3, T("meu") - 0.2, T("agora") - 0.2
    def fade(s, e): return ease((t - s) / 0.35) * (1 - ease((t - e) / 0.3))
    if t < sB + 0.3:
        a = fade(-1, sB)
        put(lay, txt("AMANHÃ", mono(40), ACC), W / 2, 380, 1, a)
        put(lay, fl("SIN"), W / 2 - 260, 600, 1, a); put(lay, fl("BRA"), W / 2 + 260, 600, 1, a)
        put(lay, txt("x", font(BD, 80), GREY), W / 2, 600, 1, a)
        put(lay, txt("SINGAPURA", font(BLK, 44), WHITE), W / 2 - 260, 730, 1, a); put(lay, txt("BRASIL", font(BLK, 44), WHITE), W / 2 + 260, 730, 1, a)
        ts = T("sete")
        if t > ts - 0.2: put(lay, glow(txt("7H DA MANHÃ", font(BLK, 110), ACC, shadow=10), ACC, 14, 0.6), W / 2, 900, 1.2 - 0.2 * ease((t - ts + 0.2) / 0.3), ease((t - ts + 0.2) / 0.3) * a)
        tp = T("pior")
        if t > tp - 0.3: put(lay, chip("A FASE NÃO PODIA SER PIOR", RED, 40, (255, 255, 255)), W / 2, 1040, 1, ease((t - tp + 0.3) / 0.3) * a)
    if sB < t < sC + 0.3:
        a = fade(sB, sC); l2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(l2, txt("COPA DO MUNDO 2026", font(BLK, 76), WHITE, shadow=8), W / 2, 360, 1, 1)
        scorecard(l2, t, sB, "NOR", "NORUEGA", 2, "BRA", "BRASIL", 1, "OITAVAS DE FINAL · ELIMINADO", 640, None, T("noruega") - 0.1)
        for i, (text, col, tn) in enumerate([("2 GOLS DO HAALAND", WHITE, T("haaland")), ("PÊNALTI PERDIDO: BRUNO GUIMARÃES", RED, T("pênalti")),
                                              ("PIOR CAMPANHA DESDE 1990", RED, T("pior", 1)), ("24 ANOS SEM COPA", ACC, T("24"))]):
            if t > tn - 0.1: put(l2, chip(text, col, 36, (255, 255, 255) if col == RED else (12, 12, 14)), W / 2, 920 + i * 90, 1, ease((t - tn + 0.1) / 0.3))
        if a < 1: l2.putalpha(l2.split()[3].point(lambda q: int(q * a)))
        lay.alpha_composite(l2)
    if sC < t < sD + 0.3:
        a = fade(sC, sD); l2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(l2, txt("SÁBADO PASSADO", font(BLK, 76), WHITE, shadow=8), W / 2, 360, 1, 1)
        tv, tt, tpd = T("virou"), T("terceiro"), T("perdeu")
        sc = (2, 3) if t > tpd - 0.2 else ((2, 2) if t > tt else ((2, 1) if t > tv else (0, 1)))
        scorecard(l2, t, sC, "BRA", "BRASIL", sc[0], "JPN", "JAPÃO", sc[1], "AMISTOSO · SINGAPURA", 640, RED if sc == (2, 3) else None, tv - 0.3)
        if t > T("vini") - 0.1: put(l2, chip("2 GOLS DO VINI JR.", ACC, 36), W / 2, 920, 1, ease((t - T("vini") + 0.1) / 0.3))
        if t > tt - 0.1: put(l2, chip("3º GOL NOS ACRÉSCIMOS", RED, 36, (255, 255, 255)), W / 2, 1010, 1, ease((t - tt + 0.1) / 0.3))
        te = T("expulsos") - 0.3
        if t > te:
            v = ease((t - te) / 0.3)
            redcard(l2, W / 2 - 420, 1165, v, -12); redcard(l2, W / 2 + 420, 1165, ease((t - te - 0.15) / 0.3), 12)
            put(l2, txt("EXPULSOS:", font(BLK, 44), RED), W / 2, 1130, 1, v)
            put(l2, txt("ANCELOTTI E RAPHINHA", font(BLK, 48), WHITE), W / 2, 1195, 1, v)
        tm = T("auxiliar") - 0.2
        if t > tm: put(l2, chip("NO BANCO: FRANCESCO MAURI (AUXILIAR)", GREY, 30), W / 2, 1300, 1, ease((t - tm) / 0.3))
        if a < 1: l2.putalpha(l2.split()[3].point(lambda q: int(q * a)))
        lay.alpha_composite(l2)
    if sD < t < sE + 0.3:
        a = fade(sD, sE); l2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(l2, txt("PROVÁVEL BRASIL", font(BLK, 76), WHITE, shadow=8), W / 2, 330, 1, 1)
        P = [("LUCAS PERRI", (0.5, 0.9), T("lucas")), ("VANDERSON", (0.86, 0.72), T("vanderson")), ("J. JESUS", (0.62, 0.76), T("jonathan")),
             ("GABRIEL", (0.38, 0.76), T("gabriel")), ("DOUGLAS", (0.14, 0.72), T("douglas")), ("JOÃO GOMES", (0.64, 0.52), T("joão")),
             ("BRUNO G.", (0.36, 0.52), T("bruno", 1)), ("RAYAN", (0.86, 0.26), T("rayan")), ("ESTÊVÃO", (0.62, 0.2), T("estêvão")),
             ("VINI JR.", (0.14, 0.26), T("vini", 1)), ("ENDRICK", (0.38, 0.2), T("endrick"))]
        pitch2d(l2, t, sD, P)
        if a < 1: l2.putalpha(l2.split()[3].point(lambda q: int(q * a)))
        lay.alpha_composite(l2)
    if sE < t < sF + 0.3:
        a = fade(sE, sF); l2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(l2, txt("MEU PALPITE", font(BLK, 84), WHITE, shadow=8), W / 2, 380, 1, 1)
        scorecard(l2, t, sE, "BRA", "BRASIL", 2, "SIN", "SINGAPURA", 0, "TERÇA · 7H · ESTÁDIO NACIONAL", 660, ACC, T("2") - 0.1)
        if t > T("fraca") - 0.4: put(l2, chip("SINGAPURA É MUITO MAIS FRACA", WHITE, 36), W / 2, 940, 1, ease((t - T("fraca") + 0.4) / 0.3))
        if t > T("vergonha") - 0.4: put(l2, chip("NINGUÉM AGUENTA OUTRA VERGONHA", RED, 36, (255, 255, 255)), W / 2, 1030, 1, ease((t - T("vergonha") + 0.4) / 0.3))
        if a < 1: l2.putalpha(l2.split()[3].point(lambda q: int(q * a)))
        lay.alpha_composite(l2)
        if 0 <= t - (T("2") - 0.1) < 0.12: flash = 0.2
    if t > sF:
        v = ease((t - sF) / 0.35); ring = T("acordar") - 0.2 < t < T("comenta") + 0.4
        put(lay, clock(320, t, ring), W / 2 + (6 * math.sin(t * 60) if ring else 0), 560, 1.1 - 0.1 * v, v)
        put(lay, txt("TERÇA · 7H DA MANHÃ", font(BLK, 64), ACC, shadow=8), W / 2, 790, 1, v)
        tc = T("comenta")
        if t > tc - 0.2: put(lay, txt("VAI ACORDAR PRA VER?", font(BLK, 76), WHITE, shadow=8), W / 2, 900, 1, ease((t - tc + 0.2) / 0.3))
        tk = T("corajoso") - 0.3
        if t > tk:
            v2 = ease((t - tk) / 0.3)
            put(lay, chip("MAIS CORAJOSO QUE A NOSSA DEFESA", RED, 38, (255, 255, 255)), W / 2, 1020, 1.2 - 0.2 * v2, v2)
            put(lay, chip("NOS ACRÉSCIMOS", RED, 38, (255, 255, 255)), W / 2, 1100, 1.2 - 0.2 * v2, v2)
            put(lay, txt("COMENTA ↓", font(BLK, 76), WHITE, 4, (0, 0, 0), 6), W / 2, 1230 + 10 * math.sin(t * 7), 1, ease((t - tk - 0.5) / 0.3))
    for s in (sB, sC, sD, sE, sF):
        if 0 <= t - s < 0.1: flash = max(flash, 0.12 * (1 - (t - s) / 0.1))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img); d.rectangle((60, 196, 76, 212), fill=ACC); d.text((92, 204), "SELEÇÃO · PRÉ-JOGO", font=mono(30), fill=ACC, anchor="lm")
    vlib.caption(img, WORDS, t, y=1500)
    vlib.progress(img, t, TOTAL)
    dark = max(1 - t / 0.2 if t < 0.2 else 0, (t - (TOTAL - 0.5)) / 0.5)
    return vlib.post(img, int(t * FPS), flash, dark)

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
