import os, sys, json, math, subprocess, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import vlib
from vlib import *

HERE = "/home/claude/work/palp"
LEAD = 0.2
RAW = json.loads(open(f"{HERE}/words.json").read())
FIX = {"Atlético.": "Athletico.", "G4.": "Z4.", "nos": "no", "para": "pra", "Deixe": "Deixa"}
WORDS = [[FIX.get(w["text"], w["text"]), w["start_ms"] / 1000 + LEAD, w["end_ms"] / 1000 + LEAD] for w in RAW]
TOTAL = 38.73 + LEAD + 1.6
vlib.CF = font(BLK, 60)
ACC = (255, 200, 60); RED = (235, 70, 70); GREY = (150, 156, 162)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
import functools
@functools.lru_cache(None)
def mono(s): return ImageFont.truetype(MONO, s)
def T(word, nth=0):
    c = 0
    for w, a, b in WORDS:
        if w.lower().strip(".,:;!?") == word.lower():
            if c == nth: return a
            c += 1
    raise KeyError(word)

TEAMS = {  # code: (name, primary, secondary)
    "CRU": ("CRUZEIRO", (20, 70, 170), (255, 255, 255)), "PAL": ("PALMEIRAS", (0, 120, 60), (255, 255, 255)),
    "FLA": ("FLAMENGO", (200, 20, 30), (20, 20, 20)), "CAP": ("ATHLETICO", (180, 20, 30), (20, 20, 20)),
    "COR": ("CORINTHIANS", (25, 25, 28), (255, 255, 255)), "BOT": ("BOTAFOGO", (40, 40, 44), (255, 255, 255)),
    "SAO": ("SÃO PAULO", (220, 30, 40), (255, 255, 255)), "FLU": ("FLUMINENSE", (130, 20, 50), (0, 120, 70)),
    "CFC": ("CORITIBA", (0, 110, 60), (255, 255, 255)), "SAN": ("SANTOS", (245, 245, 245), (20, 20, 20)),
    "REM": ("REMO", (10, 40, 110), (255, 255, 255)), "CHA": ("CHAPECOENSE", (0, 140, 70), (255, 255, 255)),
    "GRE": ("GRÊMIO", (0, 140, 210), (20, 20, 20)), "BAH": ("BAHIA", (0, 80, 170), (220, 30, 40)),
    "VAS": ("VASCO", (20, 20, 20), (255, 255, 255)), "INT": ("INTER", (210, 20, 30), (255, 255, 255)),
    "VIT": ("VITÓRIA", (200, 20, 30), (20, 20, 20)), "RBB": ("BRAGANTINO", (245, 245, 245), (210, 20, 40)),
    "GOI": ("GOIÁS", (0, 110, 50), (255, 255, 255)), "MIR": ("MIRASSOL", (250, 210, 30), (0, 110, 60)), "CAM": ("ATLÉTICO-MG", (20, 20, 20), (255, 255, 255)),
}
LOGO_DIR = "/home/claude/work/logos"
@functools.lru_cache(None)
def badge(code, d=200):
    fp = os.path.join(LOGO_DIR, code + ".png")
    if os.path.exists(fp):
        lg = Image.open(fp).convert("RGBA"); lg.thumbnail((d, d), Image.LANCZOS)
        im = Image.new("RGBA", (d, d), (0, 0, 0, 0)); im.alpha_composite(lg, ((d - lg.width) // 2, (d - lg.height) // 2))
        sh = Image.new("RGBA", (d + 40, d + 40), (0, 0, 0, 0))
        a = im.split()[3].point(lambda v: int(v * 0.55)); blk = Image.new("RGBA", (d, d), (0, 0, 0, 255)); blk.putalpha(a)
        sh.alpha_composite(blk, (20, 28)); sh = sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(im, (20, 20)); return sh
    name, p, s = TEAMS[code]
    S = 3; im = Image.new("RGBA", (d * S, d * S), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    dr.ellipse((0, 0, d * S - 1, d * S - 1), fill=s)
    dr.ellipse((d * S * 0.06, d * S * 0.06, d * S * 0.94, d * S * 0.94), fill=p)
    tc = s if sum(p) < 600 else (20, 20, 20)
    f = font(BLK, int(d * S * 0.3)); dr.text((d * S / 2, d * S / 2), code, font=f, fill=tc, anchor="mm")
    im = im.resize((d, d), Image.LANCZOS)
    sh = Image.new("RGBA", (d + 40, d + 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((20, 26, d + 20, d + 26), fill=(0, 0, 0, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(im, (20, 20)); return sh

BG = radial((26, 30, 34), (7, 8, 9))
def grid_bg(img, T_):
    d = ImageDraw.Draw(img); off = int(T_ * 18) % 90
    for y in range(-90, H, 90): d.line((0, y + off, W, y + off), fill=(255, 255, 255, 8), width=2)

def chip(text, col, size=30, fg=(12, 12, 14)):
    f = mono(size); w = int(f.getlength(text)) + 34; h = size + 22
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 8, fill=col + (240,)); d.text((w / 2, h / 2), text, font=f, fill=fg, anchor="mm"); return im

def header(img, t, tag="35ª RODADA · PALPITES"):
    d = ImageDraw.Draw(img)
    d.rectangle((60, 196, 76, 212), fill=ACC); d.text((92, 204), tag, font=mono(30), fill=ACC, anchor="lm")

def match_card(img, home, away, sh, sa, t_in, t_rev, info, tag=None, t_tag=0, t=0, t_out=None, glow_side=None):
    u = ease((t - t_in) / 0.4)
    dx = 600 * (1 - u)
    if t_out is not None and t > t_out: dx -= 1100 * ease((t - t_out) / 0.35)
    a = u
    cy = 860
    c = card(980, 620, (18, 21, 24, 240), 36, (255, 255, 255, 30), 2)
    put(img, c, W / 2 + dx, cy, 1, a)
    for k, (code, x) in enumerate(((home, W / 2 - 300), (away, W / 2 + 300))):
        b = badge(code, 230)
        if glow_side == k and t > t_rev: b = glow(b, ACC, 16, 0.8)
        put(img, b, x + dx, cy - 90, 1, a)
        put(img, txt(TEAMS[code][0], fitf(BLK, TEAMS[code][0], 380, 44), WHITE), x + dx, cy + 80, 1, a)
    put(img, txt("x", font(BD, 64), GREY), W / 2 + dx, cy - 90, 1, a)
    put(img, txt(info, mono(26), GREY), W / 2 + dx, cy + 150, 1, a)
    if t > t_rev:
        v = ease((t - t_rev) / 0.3); pop = 1 + 0.35 * (1 - v)
        for k, (n, x) in enumerate(((sh, W / 2 - 130), (sa, W / 2 + 130))):
            col = ACC if (k == 0 and sh > sa) or (k == 1 and sa > sh) else WHITE
            put(img, txt(str(n), font(BLK, 150), col, shadow=10), x + dx, cy + 245, pop, v)
        put(img, chip("PALPITE", ACC, 26), W / 2 + dx, cy - 270, 1, v)
    if tag and t > t_tag:
        v = ease((t - t_tag) / 0.3)
        put(img, chip(tag[0], tag[1], 40, (255, 255, 255) if tag[1] == RED else (12, 12, 14)), W / 2 + dx, cy + 410, 1.3 - 0.3 * v, v)

OTHERS = [("CFC", "SAN", 1, 1, "coritiba"), ("REM", "CHA", 2, 1, "remo"), ("GRE", "BAH", 1, 1, "grêmio"), ("VAS", "INT", 2, 1, "vasco"), ("VIT", "RBB", 1, 1, "vitória")]
def others(img, t, t0, t_out):
    u = ease((t - t0) / 0.4); dx = 600 * (1 - u) - (1100 * ease((t - t_out) / 0.35) if t > t_out else 0)
    put(img, txt("OS OUTROS JOGOS", font(BLK, 64), WHITE, shadow=8), W / 2 + dx, 330, 1, u)
    row0 = card(940, 96, (18, 21, 24, 200), 20); d = ImageDraw.Draw(row0)
    d.text((40, 48), "JÁ JOGADO", font=mono(24), fill=GREY, anchor="lm"); d.text((470, 48), "MIRASSOL 0 x 0 ATLÉTICO-MG", font=font(BD, 34), fill=GREY, anchor="mm")
    put(img, row0, W / 2 + dx, 440, 1, u * 0.9)
    for i, (h_, a_, sh, sa, key) in enumerate(OTHERS):
        ta = T(key) - 0.15
        if t < ta: continue
        v = ease((t - ta) / 0.3)
        r = card(940, 150, (18, 21, 24, 240), 24, (255, 255, 255, 30), 2)
        r.alpha_composite(badge(h_, 110), (14, 6)); r.alpha_composite(badge(a_, 110), (940 - 164, 6))
        d = ImageDraw.Draw(r)
        d.text((180, 75), TEAMS[h_][0], font=fitf(BLK, TEAMS[h_][0], 220, 36), fill=WHITE, anchor="lm")
        d.text((760, 75), TEAMS[a_][0], font=fitf(BLK, TEAMS[a_][0], 220, 36), fill=WHITE, anchor="rm")
        d.text((470, 75), f"{sh} x {sa}", font=font(BLK, 60), fill=ACC, anchor="mm")
        put(img, r, W / 2 + dx + 300 * (1 - v), 580 + i * 168, 1, v)

def standings(img, t, t0):
    u = ease((t - t0) / 0.4)
    put(img, txt("SE EU ACERTAR...", font(BLK, 72), WHITE, shadow=8), W / 2, 330, 1, u)
    rows = [("FLA", 76, 77), ("PAL", 73, 76)]
    tp = T("diferença") - 0.2
    p = ease((t - tp) / 0.8) if t > tp else 0
    for i, (code, a, b) in enumerate(rows):
        v = ease((t - t0 - 0.2 - i * 0.15) / 0.35)
        r = card(940, 170, (18, 21, 24, 240), 26, ACC + (200,) if code == "PAL" else (255, 255, 255, 30), 3 if code == "PAL" else 2)
        r.alpha_composite(badge(code, 130), (10, 10)); d = ImageDraw.Draw(r)
        d.text((60 + 120, 85), f"{i + 1}º  {TEAMS[code][0]}", font=font(BLK, 50), fill=WHITE, anchor="lm")
        pts = int(round(a + (b - a) * p))
        d.text((900, 85), f"{pts}", font=font(BLK, 80), fill=ACC if code == "PAL" else WHITE, anchor="rm")
        put(img, r, W / 2, 520 + i * 200, 1, v)
    if t > tp + 0.5:
        put(img, chip("DIFERENÇA: 1 PONTO", ACC, 40), W / 2, 960, 1, ease((t - tp - 0.5) / 0.3))
    tr = T("rodada", 1) - 0.2
    if t > tr:
        v = ease((t - tr) / 0.35)
        c = card(960, 300, (0, 70, 35, 240), 30, ACC + (230,), 4); d = ImageDraw.Draw(c)
        d.text((480, 60), "RODADA 36", font=mono(34), fill=ACC, anchor="mm")
        c.alpha_composite(badge("PAL", 140), (90, 90)); c.alpha_composite(badge("FLA", 140), (960 - 270, 90))
        d.text((480, 160), "x", font=font(BLK, 70), fill=WHITE, anchor="mm")
        d.text((480, 255), "VALENDO A LIDERANÇA", font=font(BLK, 42), fill=WHITE, anchor="mm")
        put(img, glow(c, ACC, 18, 0.6) if t > tr + 0.5 else c, W / 2, 1180 + 40 * (1 - v), 1.1 - 0.1 * v, v)

def frame(Tm):
    img = BG.copy(); grid_bg(img, Tm); dust(img, Tm, (255, 230, 170))
    t = Tm; fl = 0
    t_cru, t_fla, t_cor, t_sao, t_oth, t_std, t_cta = T("cruzeiro") - 0.4, T("maracanã") - 0.35, T("corinthians") - 0.35, T("são") - 0.35, T("outros") - 0.6, T("se") - 0.3, T("deixa") - 0.3
    if t < t_cru + 0.4:
        a = 1 - ease((t - t_cru) / 0.35)
        put(img, txt("PALPITES DA", font(BLK, 92), WHITE, shadow=8), W / 2, 700, 1, a * ease(t / 0.3))
        put(img, glow(txt("35ª RODADA", font(BLK, 150), ACC, shadow=10), ACC, 16, 0.7), W / 2, 850, 1.15 - 0.15 * ease(t / 0.4), a * ease(t / 0.3))
        put(img, txt("BRASILEIRÃO 2026", mono(36), GREY), W / 2, 970, 1, a * ease((t - 0.3) / 0.3))
        mt = card(700, 110, (18, 21, 24, 230), 55, (255, 255, 255, 40), 2); d = ImageDraw.Draw(mt)
        d.text((350, 55), "1º FLA 76   ·   2º PAL 73", font=font(BLK, 44), fill=WHITE, anchor="mm")
        put(img, mt, W / 2, 1120, 1, a * ease((t - 0.8) / 0.4))
    if t_cru < t < t_fla + 0.4:
        match_card(img, "CRU", "PAL", 1, 2, t_cru, T("2") - 0.05, "QUA 18/11 · 20H30 · MINEIRÃO", t=t, t_out=t_fla, glow_side=1)
    if t_fla < t < t_cor + 0.4:
        match_card(img, "FLA", "CAP", 1, 1, t_fla, T("1") - 0.05, "QUA 18/11 · 20H30 · MARACANÃ", ("TROPEÇO DO LÍDER", ACC), T("tropeça") - 0.1, t=t, t_out=t_cor)
    if t_cor < t < t_sao + 0.4:
        match_card(img, "COR", "BOT", 0, 1, t_cor, T("1", 2) - 0.05, "QUA 18/11 · 21H30 · NEO QUÍMICA ARENA", ("TIMÃO NO Z4", RED), T("afunda") - 0.1, t=t, t_out=t_sao)
    if t_sao < t < t_oth + 0.4:
        match_card(img, "SAO", "FLU", 1, 2, t_sao, T("2", 1) - 0.05, "QUI 19/11 · 21H30 · MORUMBIS", t=t, t_out=t_oth)
    if t_oth < t < t_std + 0.4:
        others(img, t, t_oth, t_std)
    if t_std < t < t_cta + 0.2:
        a = 1 - ease((t - t_cta) / 0.25)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); standings(lay, t, t_std)
        if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(lay)
    if t > t_cta:
        v = ease((t - t_cta) / 0.35)
        put(img, txt("E O SEU", font(BLK, 100), WHITE, shadow=8), W / 2, 720, 1, v)
        put(img, glow(txt("PALPITE?", font(BLK, 150), ACC, shadow=10), ACC, 16, 0.7), W / 2, 870, 1.15 - 0.15 * v, v)
        put(img, txt("COMENTA ↓", font(BLK, 76), WHITE, 4, (0, 0, 0), 6), W / 2, 1060 + 10 * math.sin(t * 7), 1, ease((t - t_cta - 0.4) / 0.3))
    for tr in (T("2") - 0.05, T("1") - 0.05, T("1", 2) - 0.05, T("2", 1) - 0.05):
        if 0 <= t - tr < 0.12: fl = 0.22 * (1 - (t - tr) / 0.12)
    header(img, t)
    caption(img, WORDS, t, y=1480)
    progress(img, Tm, TOTAL)
    dark = max(1 - Tm / 0.2 if Tm < 0.2 else 0, (Tm - (TOTAL - 0.5)) / 0.5)
    return post(img, int(Tm * FPS), fl, dark)

def render(a, b, name):
    os.makedirs(f"{HERE}/chunks", exist_ok=True); tmp = f"{HERE}/chunks/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(a, b): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0: os.replace(tmp, f"{HERE}/chunks/{name}.mp4")
    print("done", name, flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for s in sys.argv[2:]: frame(float(s)).save(f"{HERE}/pv_{float(s):05.1f}.jpg", quality=85)
    else:
        NF = int(round(TOTAL * FPS)); parts = int(sys.argv[2]); i = int(sys.argv[1])
        bd = [NF * j // parts for j in range(parts + 1)]; render(bd[i], bd[i + 1], f"c{i:02d}")
