"""Elementos gráficos animados (independentes de resolução) para o Modo Carreira v2."""
import os, math, random, functools, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
sys.path.insert(0, "/home/claude/carreira")
import card as C

FD = "/usr/share/fonts/opentype/inter/"
A = "/home/claude/carreira/assets"
IMG = "/home/claude/ep1/img"
AMB = (246, 178, 40); WHITE = (255, 255, 255); BG = (14, 14, 16); RED = (232, 58, 58); GREEN = (60, 200, 110)
BLUE = (60, 110, 240); PURPLE = (88, 52, 200); INK = (20, 20, 22)


@functools.lru_cache(None)
def font(name, size):
    return ImageFont.truetype(FD + {"blk": "InterDisplay-Black.otf", "xb": "InterDisplay-ExtraBold.otf", "bd": "InterDisplay-Bold.otf",
                                   "sb": "Inter-SemiBold.otf", "md": "InterDisplay-Medium.otf"}[name], int(size))


def ease(u): u = max(0.0, min(1.0, u)); return 1 - (1 - u) ** 3
def back(u):  # overshoot
    u = max(0.0, min(1.0, u)); c = 1.9; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
def clamp(u, a=0.0, b=1.0): return max(a, min(b, u))


def paste(img, el, x, y, alpha=1.0, scale=1.0, rot=0.0, center=True):
    if el is None or alpha <= 0.01: return
    if scale != 1.0:
        if scale <= 0.01: return
        el = el.resize((max(1, int(el.width * scale)), max(1, int(el.height * scale))), Image.BILINEAR)
    if rot: el = el.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1:
        el = el.copy(); el.putalpha(el.getchannel("A").point(lambda a: int(a * alpha)))
    if center: x, y = x - el.width / 2, y - el.height / 2
    img.alpha_composite(el, (int(x), int(y)))


def text_el(s, f, fill=WHITE, stroke=0, stroke_fill=(0, 0, 0), shadow=True):
    bb = f.getbbox(s, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 24, bb[3] - bb[1] + 24
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((12 - bb[0] + 3, 12 - bb[1] + 5), s, font=f, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    d.text((12 - bb[0], 12 - bb[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im


@functools.lru_cache(4096)
def chip(s, size=40, fg=INK, bg=AMB, weight="blk", padx=0.65, pady=0.32, outline=None):
    f = font(weight, size); bb = f.getbbox(s)
    px, py = int(size * padx), int(size * pady)
    w, h = bb[2] - bb[0] + 2 * px, bb[3] - bb[1] + 2 * py
    im = Image.new("RGBA", (w + 8, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 8, w + 3, h + 7), h // 2, fill=(0, 0, 0, 110))
    d.rounded_rectangle((2, 2, w + 1, h + 1), h // 2, fill=bg, outline=outline, width=4 if outline else 0)
    d.text((2 + px - bb[0], 2 + py - bb[1]), s, font=f, fill=fg)
    return im


def tag_box(s, size=46, fg=WHITE, bg=INK, outline=WHITE):
    """etiqueta de assunto (estilo 'MEIO MILHÃO DE VIEWS')"""
    f = font("blk", size); bb = f.getbbox(s); px, py = int(size * 0.5), int(size * 0.28)
    w, h = bb[2] - bb[0] + 2 * px, bb[3] - bb[1] + 2 * py
    im = Image.new("RGBA", (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((8, 8, w + 8, h + 8), fill=(0, 0, 0, 160))
    d.rectangle((0, 0, w, h), fill=bg, outline=outline, width=5)
    d.text((px - bb[0], py - bb[1]), s, font=f, fill=fg)
    return im


def panel(w, h, col=(18, 18, 22, 235), r=28, border=(255, 255, 255, 40)):
    p = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    ImageDraw.Draw(p).rounded_rectangle((0, 0, int(w) - 1, int(h) - 1), r, fill=col, outline=border, width=3)
    return p


# ---------- fundos ----------
PALETTE = {"amber": ((255, 196, 60), (214, 120, 20)), "purple": ((96, 60, 220), (40, 20, 110)), "blue": ((50, 110, 245), (20, 40, 130)),
           "red": ((220, 50, 50), (90, 10, 20)), "green": ((40, 170, 90), (10, 70, 40)), "night": ((30, 34, 60), (8, 8, 16)),
           "sepia": ((206, 170, 120), (110, 80, 50)), "dark": ((34, 34, 40), (10, 10, 12)), "teal": ((30, 190, 170), (10, 90, 90))}


@functools.lru_cache(64)
def _grad(W, H, key):
    top, bot = PALETTE[key]
    a = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top)[None, None] * (1 - a) + np.array(bot)[None, None] * a).repeat(W, 1).astype(np.uint8)
    im = Image.fromarray(arr, "RGB").convert("RGBA")
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((-W * 0.2, H * 0.55, W * 1.2, H * 1.6), fill=(0, 0, 0, 90))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(W // 10)))
    return im


@functools.lru_cache(16)
def _stripes(W, H):
    s = Image.new("RGBA", (W + 400, H), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    for x in range(-H, W + 400, 90): d.polygon([(x, 0), (x + 40, 0), (x + 40 + H, H), (x + H, H)], fill=(255, 255, 255, 14))
    return s


def bg(W, H, key, t):
    im = _grad(W, H, key).copy()
    off = int((t * 40) % 90)
    im.alpha_composite(_stripes(W, H).crop((off, 0, off + W, H)))
    return im


# ---------- personagens / ícones ----------
@functools.lru_cache(64)
def avatar(key, h):
    if key in ("gildo", "victor", "matic", "murrey", "rick"):
        im = C.clean_avatar(os.path.join(A, key + "_ai.png"))
    else:
        im = Image.open(os.path.join(IMG, key + ".png")).convert("RGBA"); im = im.crop(im.getchannel("A").getbbox())
    h = int(h); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


@functools.lru_cache(64)
def gray(key, h):
    a = avatar(key, h); g = ImageOps.grayscale(a.convert("RGB")).convert("RGBA"); g.putalpha(a.getchannel("A")); return g


@functools.lru_cache(64)
def crest(h):
    im = Image.open(os.path.join(A, "cambridge_united.png")).convert("RGBA"); h = int(h)
    return im.resize((h, h), Image.LANCZOS)


def icon_bus(w):
    w = int(w); h = int(w * 0.55); im = Image.new("RGBA", (w, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), int(w * 0.07), fill=AMB, outline=INK, width=8)
    for i in range(5):
        x = int(w * 0.06 + i * w * 0.17); d.rounded_rectangle((x, int(h * 0.12), x + int(w * 0.14), int(h * 0.48)), 12, fill=(150, 210, 240), outline=INK, width=5)
    d.rectangle((0, int(h * 0.62), w, int(h * 0.7)), fill=INK)
    d.text((int(w * 0.07), int(h * 0.74)), "LINHA 3", font=font("blk", h * 0.16), fill=INK)
    for x in (0.22, 0.78):
        cx = int(w * x); d.ellipse((cx - h * 0.17, h - h * 0.12, cx + h * 0.17, h + h * 0.22), fill=INK); d.ellipse((cx - h * 0.07, h - h * 0.02, cx + h * 0.07, h + h * 0.12), fill=(170, 170, 170))
    return im


def icon_pizza(w):
    w = int(w); im = Image.new("RGBA", (w, w), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, int(w * 0.3), w, int(w * 0.7)), 18, fill=(225, 190, 140), outline=INK, width=8)
    d.line((0, int(w * 0.42), w, int(w * 0.42)), fill=INK, width=6)
    d.text((w / 2, w * 0.56), "PIZZA", font=font("blk", w * 0.14), fill=RED, anchor="mm")
    return im


def icon_pad(w):
    w = int(w); h = int(w * 0.6); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, int(h * 0.1), w, int(h * 0.9)), int(h * 0.4), fill=(40, 40, 48), outline=WHITE, width=6)
    cx, cy = int(w * 0.27), int(h * 0.5); s = int(h * 0.12)
    d.rectangle((cx - s * 2, cy - s // 2, cx + s * 2, cy + s // 2), fill=WHITE); d.rectangle((cx - s // 2, cy - s * 2, cx + s // 2, cy + s * 2), fill=WHITE)
    for dx, dy, c in ((0.7, 0.36, GREEN), (0.79, 0.5, RED), (0.61, 0.5, BLUE), (0.7, 0.64, AMB)):
        x, y = int(w * dx), int(h * dy); d.ellipse((x - s, y - s, x + s, y + s), fill=c)
    return im


def icon_radio(w, t=0):
    w = int(w); h = int(w * 0.7); im = Image.new("RGBA", (w + 200, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 20, w, h + 20), 30, fill=(140, 70, 40), outline=INK, width=8)
    d.ellipse((w * 0.08, h * 0.25 + 20, w * 0.5, h * 0.25 + 20 + w * 0.42), fill=(60, 40, 30), outline=INK, width=6)
    d.rounded_rectangle((w * 0.58, h * 0.3 + 20, w * 0.92, h * 0.5 + 20), 10, fill=(250, 220, 140), outline=INK, width=5)
    for k in range(3):
        r = 40 + k * 45 + (t * 120) % 45
        d.arc((w + 20 - r, h / 2 + 20 - r, w + 20 + r, h / 2 + 20 + r), -40, 40, fill=WHITE, width=10)
    return im


def icon_phone(w, caller, t):
    w = int(w); h = int(w * 2.0); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), int(w * 0.14), fill=INK, outline=(90, 90, 100), width=8)
    d.rounded_rectangle((18, 18, w - 18, h - 18), int(w * 0.11), fill=(28, 30, 40))
    d.text((w / 2, h * 0.16), "chamada recebida", font=font("md", w * 0.07), fill=(190, 190, 200), anchor="mm")
    paste(im, crest(w * 0.42), w / 2, h * 0.36)
    for i, l in enumerate(caller.split("\n")):
        d.text((w / 2, h * 0.55 + i * w * 0.11), l, font=font("blk", w * 0.09), fill=WHITE, anchor="mm")
    for x, c in ((0.27, RED), (0.73, GREEN)):
        r = w * 0.11 * (1 + 0.08 * math.sin(t * 10)); cx, cy = w * x, h * 0.84
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
    return im


def newspaper(w, year, headline, sub="", sepia=False):
    w = int(w); h = int(w * 0.72); col = (238, 226, 200) if sepia else (246, 244, 236)
    im = Image.new("RGBA", (w, h), col + (255,)); d = ImageDraw.Draw(im)
    d.text((w / 2, h * 0.09), "CAMBRIDGE DAILY", font=font("blk", w * 0.075), fill=INK, anchor="mm")
    d.line((w * 0.05, h * 0.16, w * 0.95, h * 0.16), fill=INK, width=4); d.text((w * 0.06, h * 0.185), year, font=font("bd", w * 0.035), fill=INK)
    d.line((w * 0.05, h * 0.25, w * 0.95, h * 0.25), fill=INK, width=2)
    f = font("blk", w * 0.095); lines = wrap(headline, f, w * 0.9)
    while len(lines) > 3: f = font("blk", f.size - 4); lines = wrap(headline, f, w * 0.9)
    for i, l in enumerate(lines): d.text((w / 2, h * 0.36 + i * f.size * 1.08), l, font=f, fill=INK, anchor="mm")
    y0 = h * 0.36 + len(lines) * f.size * 1.08 + 10
    if sub: d.text((w / 2, y0 + 20), sub, font=font("sb", w * 0.04), fill=(70, 70, 70), anchor="mm")
    for k in range(4):
        y = y0 + 70 + k * 26
        if y < h - 20: d.line((w * 0.06, y, w * 0.94, y), fill=(180, 175, 165), width=10)
    im = im.filter(ImageFilter.GaussianBlur(0.4))
    return im


def wrap(s, f, maxw):
    out = [""]
    for w_ in s.split():
        if f.getlength((out[-1] + " " + w_).strip()) > maxw and out[-1]: out.append(w_)
        else: out[-1] = (out[-1] + " " + w_).strip()
    return out


def stamp(s, size=110, col=RED):
    f = font("blk", size); bb = f.getbbox(s); w, h = bb[2] - bb[0] + size, bb[3] - bb[1] + size * 0.6
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, w - 6, h - 6), 18, outline=col, width=12)
    d.text((w / 2, h / 2), s, font=f, fill=col, anchor="mm")
    return im


def bar(w, h, frac, col=AMB, bgc=(255, 255, 255, 50)):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=bgc)
    if frac > 0.01: d.rounded_rectangle((0, 0, max(h, (w - 1) * frac), h - 1), h // 2, fill=col)
    return im


def odometer(value, digits, size, t, dur=1.0, start=None):
    """contador de rolo estilo 'MEIO MILHÃO DE VIEWS'"""
    start = 0 if start is None else start
    v = start + (value - start) * ease(t / dur)
    s = f"{int(v):0{digits}d}"
    f = font("blk", size); cw = int(size * 0.78); ch = int(size * 1.25)
    im = Image.new("RGBA", (cw * digits + 20, ch + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, c in enumerate(s):
        x = 10 + i * cw
        d.rounded_rectangle((x + 3, 10, x + cw - 3, 10 + ch), 12, fill=(245, 245, 245), outline=INK, width=5)
        d.text((x + cw / 2, 10 + ch / 2), c, font=f, fill=INK, anchor="mm")
        d.line((x + 6, 10 + ch / 2, x + cw - 6, 10 + ch / 2), fill=(0, 0, 0, 60), width=3)
    return im


# ---------- cartas ----------
REAL = {"kaikai": ("Sullay Kaikai", "PD", 66, [80, 64, 63, 72, 30, 60]), "bauer": ("Patrick Bauer", "ZAG", 66, [48, 38, 52, 46, 68, 78]),
        "pelly": ("Pelly R. Mpanzu", "VOL", 64, [62, 52, 63, 64, 62, 70])}
SQUAD = [("Jake Eastwood", "GOL", 31, 64, "£350K"), ("Liam Bennett", "LD", 28, 63, "£300K"), ("Patrick Bauer", "ZAG", 34, 66, "£250K"),
         ("Kelland Watts", "ZAG", 27, 65, "£400K"), ("Zak Bradshaw", "ZAG", 22, 61, "£300K"), ("Pelly R. Mpanzu", "VOL", 32, 64, "£300K"),
         ("Dominic Ball", "VOL", 31, 63, "£280K"), ("Shane McLoughlin", "ALA", 29, 62, "£260K"), ("Ben Knight", "MEI", 24, 65, "£600K"),
         ("Sullay Kaikai", "PD", 31, 66, "£650K"), ("Louis Appéré", "ATA", 27, 63, "£350K"), ("Shayne Lavery", "ATA", 28, 64, "£450K"),
         ("Daniel Efobi", "ATA", 21, 57, "£120K"), ("Gabe Breeze", "GOL", 22, 60, "£150K")]


@functools.lru_cache(None)
def silhouette():
    im = Image.new("RGBA", (600, 600), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((210, 90, 390, 290), fill=(30, 30, 34, 255)); d.rounded_rectangle((110, 300, 490, 640), 120, fill=(30, 30, 34, 255))
    return im


@functools.lru_cache(None)
def card(key, w, ovr=None):
    w = int(w)
    if key in REAL:
        n, p, o, s = REAL[key]; return C.make_card(silhouette(), n, ovr or o, p, s, w=w)
    data = {"murrey": ("Murrey", 52, "MEI", [66, 50, 60, 62, 25, 40], True), "gildo": ("Gildo", 48, "PE", [98, 40, 42, 58, 20, 38], True),
            "f_kofi": ("Kofi Mensah-Hart", 50, "VOL", [55, 30, 48, 46, 52, 56], True), "f_ollie": ("Ollie Fenwick", 46, "ATA", [58, 50, 35, 44, 18, 45], True),
            "f_tomas": ("Tomás Ferreira", 68, "ZAG", [52, 40, 58, 50, 70, 74], False), "f_theo": ("Theo Okafor", 63, "ATA", [78, 63, 55, 66, 30, 64], False)}
    n, o, p, s, prom = data[key]
    av = avatar(key, 900)
    return C.make_card(av, n, ovr or o, p, s, w=w, promessa=prom)


def rays(W, H, cx, cy, t, col=(255, 220, 140), n=14, alpha=70):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); R = max(W, H) * 1.2
    for i in range(n):
        a0 = t * 0.4 + i * 2 * math.pi / n; a1 = a0 + math.pi / n * 0.5
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=col + (alpha,))
    return im.filter(ImageFilter.GaussianBlur(6))


def confetti(W, H, t, seed=3, n=90):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rng = random.Random(seed)
    for i in range(n):
        x = rng.random() * W + 40 * math.sin(t * 2 + i); y = (rng.random() * H * 0.3 - H * 0.3 + t * (300 + rng.random() * 300)) % (H + 60) - 30
        c = rng.choice([AMB, WHITE, INK, RED, GREEN]); s = 8 + rng.random() * 10
        d.rectangle((x, y, x + s, y + s * 0.6), fill=c)
    return im


def speedlines(W, H, t, n=40, col=(255, 255, 255, 90)):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rng = random.Random(int(t * 12))
    for i in range(n):
        y = rng.random() * H; L = 100 + rng.random() * 400; x = rng.random() * W
        d.line((x, y, x + L, y), fill=col, width=rng.choice([3, 4, 6]))
    return im
