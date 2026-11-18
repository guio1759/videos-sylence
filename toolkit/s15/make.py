import sys, os, json, math, re, functools, subprocess
sys.path.insert(0, "/home/claude/ep1/v2")
from PIL import Image, ImageDraw
from gfx import *

D = os.path.dirname(os.path.abspath(__file__))
WJ = json.load(open(os.path.join(D, "words.json"))); WORDS = WJ["words"]; TOTAL = WJ["total"] + 0.5
W, H, FPS = 1080, 1920, 30
LOG = "/home/claude/work/logos/"


@functools.lru_cache(64)
def logo(k, h):
    im = Image.open(LOG + k + ".png").convert("RGBA"); im = im.crop(im.getchannel("A").getbbox()); h = int(h)
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def norm(s): return re.sub(r"[^a-z0-9%]", "", s.lower())
SKIP = {"o", "a", "e", "de", "da", "do", "no", "na", "os", "em", "se", "um", "tem", "ser", "mas", "nos", "ai"}


def caption(img, T):
    cur = None
    for w in WORDS:
        if w["t0"] - 0.03 <= T < w["t1"] + 0.1: cur = w
        if w["t0"] > T: break
    if not cur: return
    if norm(cur["w"]) in SKIP or not norm(cur["w"]):
        i = WORDS.index(cur); prev = next((WORDS[k] for k in range(i - 1, max(-1, i - 4), -1) if norm(WORDS[k]["w"]) not in SKIP), None)
        if not prev or T - prev["t1"] > 0.6: return
        cur = prev
    s = re.sub(r"[.,!?:;]", "", cur["w"]).upper()
    if s == "%": s = "15%"
    sc = 0.75 + 0.25 * back((T - cur["t0"]) / 0.16)
    hot = any(k in s for k in ("15", "85", "76", "73", "VERDE", "TAÇA", "EMPATE", "CRUZEIRO", "FLAMENGO", "PALMEIRAS", "VERDÃO"))
    paste(img, chip(s, 96, INK, AMB if hot else WHITE, "blk", 0.5, 0.25), W / 2, H * 0.84, 1, sc, rot=-2 if hash(s) % 2 else 2)


def topic(img, t):
    paste(img, tag_box("CORRIDA PELO TÍTULO", 44, WHITE, INK), W / 2, 150, 1)


def pop(img, el, x, y, t, t0, dur=0.3, rot=0):
    if t < t0: return
    paste(img, el, x, y, 1, 0.2 + 0.8 * back((t - t0) / dur), rot)


def slide(img, el, x, y, t, t0, dx=-500, dur=0.35):
    if t < t0: return
    u = ease((t - t0) / dur); paste(img, el, x + dx * (1 - u), y, u)


def txt(s, size, col=WHITE, stroke=8): return text_el(s, font("blk", size), col, stroke)


def trophy(h):
    h = int(h); w = int(h * 0.8); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); g = (255, 205, 60)
    d.pieslice((w * 0.12, -h * 0.25, w * 0.88, h * 0.62), 0, 180, fill=g, outline=INK, width=8)
    for sx in (0, 1):
        x0 = w * 0.0 if sx == 0 else w * 0.74
        d.arc((x0, h * 0.05, x0 + w * 0.26, h * 0.38), 90 if sx == 0 else -90, 270 if sx == 0 else 90, fill=INK, width=10)
    d.rectangle((w * 0.43, h * 0.6, w * 0.57, h * 0.78), fill=g, outline=INK, width=6)
    d.rounded_rectangle((w * 0.25, h * 0.78, w * 0.75, h * 0.96), 10, fill=(40, 120, 60), outline=INK, width=6)
    return im


SC = [(0, 5.18, "s1"), (5.18, 6.76, "s2"), (6.76, 11.48, "s3"), (11.48, 16.04, "s4"), (16.04, 20.66, "s5"), (20.66, 22.94, "s6"), (22.94, 99, "s7")]


def frame(T):
    for a, b, k in SC:
        if a <= T < b: break
    t = T - a
    img = bg(W, H, {"s1": "green", "s2": "dark", "s3": "night", "s4": "green", "s5": "red" if T < 18.62 else "green", "s6": "night", "s7": "green"}[k], T)
    cx = W / 2
    if k == "s1":
        r = rays(W, H, cx, 760, T)
        if r is not None: img.alpha_composite(r)
        # frame 1 já mostra o número
        s = 1.0 + 0.06 * math.sin(T * 9) if T > 0.4 else 0.85 + 0.15 * back(T / 0.35)
        paste(img, txt("15%", 380, AMB, 16), cx, 760, 1, s, -4)
        paste(img, txt("SÓ", 150, WHITE, 10), cx, 470, 1, 1, -4)
        pop(img, chip("CHANCE DE TÍTULO", 64, WHITE, RED), cx, 1060, T, 1.8)
        pop(img, logo("PAL", 300), cx, 1400, T, 2.62, 0.35)
        if T > 3.68: paste(img, chip("SEGUNDO A MATEMÁTICA", 46, INK, WHITE), cx, 1155, ease((T - 3.68) / 0.25))
    elif k == "s2":
        pop(img, stamp("A CONTA", 150, AMB), cx, 760, t, 0.15, 0.3, -6)
        pop(img, txt("PRESTA ATENÇÃO 👇".replace(" 👇", ""), 70), cx, 1020, t, 0.3)
    elif k == "s3":
        p = panel(900, 900); paste(img, p, cx, 820, 1)
        slide(img, logo("FLA", 260), 280, 560, t, 0.0, -400); slide(img, logo("PAL", 260), 280, 920, t, 1.8, -400)
        if t > 0.4: paste(img, odometer(76, 2, 150, t - 0.4, 0.5, 60), 720, 560)
        if t > 2.2: paste(img, odometer(73, 2, 150, t - 2.2, 0.5, 60), 720, 920)
        pop(img, chip("FALTAM 4 JOGOS", 70, INK, AMB), cx, 1180, t, 3.3)
    elif k == "s4":
        fx = [("CRU", "QUA"), ("FLA", "SÁB"), ("CHA", "TER"), ("CFC", "ÚLT")]
        times = [11.82, 12.26, 12.4, 12.55]
        for i, (tm, dia) in enumerate(fx):
            y = 430 + i * 240
            slide(img, panel(820, 200, (18, 18, 22, 230)), cx, y, T, 11.5 + i * 0.08, 600)
            if T > 11.6 + i * 0.08:
                paste(img, logo(tm, 140), 250, y); paste(img, txt(dia, 64), 470, y)
                if tm == "FLA" and T > 13.3: paste(img, chip("CONFRONTO DIRETO", 34, WHITE, RED), 640, y - 80, 1, 1, -4)
            if T > times[i]: pop(img, stamp("V", 90, GREEN), 830, y, T, times[i], 0.25, -8)
        pts = 73 + int(min(4, max(0, (T - 12.26) / 0.5 + 1))) * 3 if T > 12.26 else 73
        pts = 85 if T > 14.74 else min(pts, 82)
        paste(img, txt(f"{pts} PONTOS", 120, AMB if pts == 85 else WHITE, 10), cx, 1440, 1, 1.0 + (0.12 * (1 - ease((T - 15.02) / 0.3)) if T > 15.02 else 0))
    elif k == "s5":
        if T < 18.62:
            paste(img, logo("FLA", 300), cx, 620, 1, 1, 6 * math.sin(T * 14) if T > 16.94 else 0)
            pop(img, txt("NÃO PODE", 130), cx, 920, T, 16.62)
            pop(img, txt("TROPEÇAR", 150, AMB, 10), cx, 1080, T, 16.94, 0.3, -3)
        else:
            r = rays(W, H, cx, 700, T)
            if r is not None: img.alpha_composite(r)
            pop(img, txt("1 EMPATE", 150), cx, 420, T, 18.62)
            pop(img, trophy(420), cx, 800, T, 19.84, 0.35)
            pop(img, txt("TAÇA VERDE", 140, AMB, 10), cx, 1150, T, 20.1, 0.3, -3)
            if T > 20.34:
                c = confetti(W, H, T - 20.34)
                if c is not None: img.alpha_composite(c)
    elif k == "s6":
        pop(img, chip("AMANHÃ • 20:30", 74, INK, AMB), cx, 480, t, 0.3)
        slide(img, logo("CRU", 300), 290, 820, t, 0.9, -500); slide(img, logo("PAL", 300), 790, 820, t, 1.1, 500)
        pop(img, txt("x", 140), cx, 820, t, 1.2)
        pop(img, txt("TUDO COMEÇA AQUI", 74), cx, 1110, t, 1.4)
    elif k == "s7":
        pop(img, txt("VOCÊ ACREDITA", 110), cx, 470, t, 0.1)
        pop(img, txt("NOS 15%?", 190, AMB, 12), cx, 680, t, 1.3, 0.35, -4)
        pop(img, chip("SIM 💚".replace(" 💚", ""), 120, WHITE, GREEN), 330, 1050, t, 0.7)
        pop(img, chip("NÃO", 120, WHITE, RED), 750, 1050, t, 0.85)
        pop(img, chip("COMENTA AÍ 👇".replace(" 👇", ""), 60, INK, WHITE), cx, 1280, t, 0.4)
    # flash nos cortes
    for a_, b_, k_ in SC[1:]:
        if 0 <= T - a_ < 0.12: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - (T - a_) / 0.12)))))
    topic(img, T); caption(img, T)
    return img.convert("RGB")


if __name__ == "__main__":
    if sys.argv[1] == "prev":
        for T in map(float, sys.argv[2:]): frame(T).save(f"{D}/p_{T:05.2f}.jpg", quality=85)
    else:
        n = int(TOTAL * FPS); out = f"{D}/video_tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
        p.stdin.close(); p.wait(); os.rename(out, f"{D}/video.mp4")
