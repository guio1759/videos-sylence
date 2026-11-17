"""Shared drawing helpers — 'balanced' style: chamativo sem estourar."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/"
import functools
@functools.lru_cache(maxsize=None)
def font(n, s): return ImageFont.truetype(F + n, s)
BLK, BLKI, XB, BD, SB, MD = "InterDisplay-Black.otf", "InterDisplay-BlackItalic.otf", "InterDisplay-ExtraBold.otf", "InterDisplay-Bold.otf", "Inter-SemiBold.otf", "InterDisplay-Medium.otf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
GOLD = (245, 200, 70); YEL = (252, 212, 60); WHITE = (248, 246, 240); MUT = (170, 182, 175)
GRN = (0, 135, 65); RED = (215, 55, 55); SKY = (110, 180, 235)

def ease(x): x = max(0., min(1., x)); return 1 - (1 - x) ** 3
def eback(x):
    x = max(0., min(1., x)); c = 1.2; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def clamp(x, a=0., b=1.): return max(a, min(b, x))

def trim(im): return im.crop(im.getbbox())
PAL = trim(Image.open("/home/claude/work/logos/_pal_crest.webp").convert("RGBA"))
def crest(h): return PAL.resize((int(PAL.width * h / PAL.height), h), Image.LANCZOS)

_cache = {}
def txt(s, f, fill=WHITE, stroke=0, sfill=(0, 0, 0), shadow=0):
    key = (s, id(f), fill, stroke, sfill, shadow)
    if key in _cache: return _cache[key]
    bb = f.getbbox(s, stroke_width=stroke); pad = 16 + shadow * 2
    im = Image.new("RGBA", (bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - bb[0], pad - bb[1] + shadow // 2), s, font=f, fill=(0, 0, 0, 190), stroke_width=stroke, stroke_fill=(0, 0, 0, 190))
        im = sh.filter(ImageFilter.GaussianBlur(shadow))
    ImageDraw.Draw(im).text((pad - bb[0], pad - bb[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    _cache[key] = im; return im

def glow(im, col, r=14, k=1.0):
    """soft, controlled glow (no blow-out): blurred colour halo at reduced opacity"""
    key = ("g", id(im), col, r, k)
    if key in _cache: return _cache[key]
    im = padim(im, r * 2)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(min(255, v * k * 0.75)))
    g = Image.new("RGBA", im.size, col + (0,)); g.putalpha(a)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(im)
    _cache[key] = out; return out
def padim(im, p):
    o = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p), (0, 0, 0, 0)); o.alpha_composite(im, (p, p)); return o
def put(img, im, cx, cy, sc=1.0, a=1.0, rot=0):
    if a <= 0.01 or sc <= 0.01: return
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if abs(sc - 1) > 0.005: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    if a < 0.99:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    l, tp = max(0, -x), max(0, -y); r, b = min(im.width, W - x), min(im.height, H - y)
    if r <= l or b <= tp: return
    if (l, tp, r, b) != (0, 0, im.width, im.height): im = im.crop((l, tp, r, b))
    img.alpha_composite(im, (x + l, y + tp))
def fitf(name, s, maxw, start):
    sz = start
    while sz > 18 and font(name, sz).getlength(s) > maxw: sz -= 2
    return font(name, sz)
def card(w, h, fill, r=28, outline=None, ow=3):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=outline, width=ow); return im

def radial(c0, c1, cx=0.5, cy=0.42):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W * cx) / W) ** 2 + ((y - H * cy) / H * 0.75) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    return Image.fromarray((np.array(c0) * (1 - k) + np.array(c1) * k).astype(np.uint8), "RGB").convert("RGBA")
def make_rays(n=16, col=(255, 215, 110), a=26):
    im = Image.new("RGBA", (1700, 1700), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(n):
        an = 2 * math.pi * k / n
        d.polygon([(850, 850), (850 + 1300 * math.cos(an - 0.06), 850 + 1300 * math.sin(an - 0.06)), (850 + 1300 * math.cos(an + 0.06), 850 + 1300 * math.sin(an + 0.06))], fill=col + (a,))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse((150, 150, 1550, 1550), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(200)); im.putalpha(ImageChops.multiply(im.split()[3], m))
    return im.filter(ImageFilter.GaussianBlur(5))
RAYS = make_rays()
_rot = {}
def rays(img, t, cx, cy, speed=6, a=1.0, sc=1.0):
    ang = int(t * speed) % 360
    if ang not in _rot: _rot[ang] = RAYS.rotate(ang, Image.BILINEAR)
    put(img, _rot[ang], cx, cy, sc, a)

yy, xx = np.mgrid[0:H, 0:W]
VIG = Image.fromarray((np.clip(1 - 0.6 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2), 0.4, 1) * 255).astype(np.uint8), "L")
del yy, xx
_r = np.random.default_rng(3)
GRAIN = [Image.fromarray(np.clip(128 + _r.normal(0, 20, (H // 2, W // 2)), 0, 255).astype(np.uint8), "L").resize((W, H)).convert("RGB") for _ in range(6)]
BLACK = Image.new("RGB", (W, H), (0, 0, 0)); WHITE_IM = Image.new("RGB", (W, H), (255, 255, 255))
DUST = [(_r.uniform(0, W), _r.uniform(0, H), _r.uniform(1.5, 3.5), _r.uniform(-8, 8), _r.uniform(-30, -8), _r.uniform(25, 70)) for _ in range(28)]
def dust(img, T, col=(255, 235, 170)):
    d = ImageDraw.Draw(img)
    for x, y, r, vx, vy, a in DUST:
        X = (x + vx * T) % W; Y = (y + vy * T) % H
        d.ellipse((X - r, Y - r, X + r, Y + r), fill=col + (int(a),))
CONF = [(_r.uniform(0, W), _r.uniform(-H, 0), _r.uniform(160, 320), _r.uniform(-40, 40), _r.uniform(0, 6.28), _r.uniform(2, 6), _r.integers(0, 3)) for _ in range(90)]
CCOL = [(0, 160, 80), (250, 248, 240), (245, 200, 70)]
def confetti(img, t, a=1.0):
    d = ImageDraw.Draw(img)
    for x, y, vy, vx, ph, sp, c in CONF:
        Y = y + vy * t; X = x + vx * t + 20 * math.sin(ph + t * sp)
        if not (-20 < Y < H + 20): continue
        w = 14 * abs(math.cos(ph + t * sp)) + 3
        d.rectangle((X - w / 2, Y - 6, X + w / 2, Y + 6), fill=CCOL[c] + (int(220 * a),))

def post(img, gi, flash=0.0, dark=0.0, shake=(0, 0), gray=0.0):
    rgb = img.convert("RGB")
    if gray > 0: rgb = Image.blend(rgb, rgb.convert("L").convert("RGB"), gray)
    if shake != (0, 0): rgb = ImageChops.offset(rgb, int(shake[0]), int(shake[1]))
    rgb = Image.composite(rgb, BLACK, VIG)
    rgb = Image.blend(rgb, ImageChops.overlay(rgb, GRAIN[gi % 6]), 0.18)
    if flash > 0: rgb = Image.blend(rgb, WHITE_IM, min(0.45, flash))
    if dark > 0: rgb = Image.blend(rgb, BLACK, min(1, dark))
    return rgb

CF = font(BLK, 72)
def _chunks(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w[0][-1] in ".,:;!?" or (len(cur) == 2 and len(" ".join(x[0] for x in cur)) > 15):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def caption(img, words, t, y=1440):
    for ch in _chunks(words):
        a, b = ch[0][1], ch[-1][2] + 0.12
        if not (a - 0.02 <= t < b): continue
        last = max([i for i, w in enumerate(ch) if w[1] <= t] + [0])
        ims = []
        for i, w in enumerate(ch):
            s = w[0].upper().strip(".,:;!?")
            cur = i == last
            im = txt(s, CF, YEL if cur else WHITE, 4, (0, 0, 0), 6)
            pop = 1 + 0.1 * (1 - ease((t - w[1]) / 0.14)) if cur else 1
            ims.append((im, pop))
        P = 2 * (16 + 12)
        tw = sum(i.width - P for i, _ in ims) + 20 * (len(ims) - 1)
        sc = min(1, 960 / tw); x = W / 2 - tw * sc / 2; ap = ease((t - a) / 0.1)
        for im, pop in ims:
            wpx = (im.width - P) * sc
            put(img, im, x + wpx / 2, y + (1 - ap) * 16, sc * pop, ap); x += wpx + 20 * sc
        return

def progress(img, T, total):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 9), fill=(0, 0, 0, 120)); d.rectangle((0, 0, int(W * T / total), 9), fill=YEL + (255,))

def trophy(h=560):
    S = 2; w = int(h * 0.8); im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = h * S / 100; cx = w * S / 2
    G1, G2, G3 = (255, 222, 120), (226, 170, 50), (150, 100, 10)
    d.ellipse((cx - 30 * u, 6 * u, cx + 30 * u, 14 * u), fill=G1)
    d.pieslice((cx - 30 * u, -26 * u, cx + 30 * u, 56 * u), 0, 180, fill=G2); d.rectangle((cx - 30 * u, 9 * u, cx + 30 * u, 15 * u), fill=G2)
    for s in (-1, 1):
        d.arc((cx + s * 30 * u - 12 * u, 14 * u, cx + s * 30 * u + 12 * u, 38 * u), 270 if s > 0 else 90, 90 if s > 0 else 270, fill=G2, width=int(3 * u))
    d.polygon([(cx - 5 * u, 55 * u), (cx + 5 * u, 55 * u), (cx + 3 * u, 70 * u), (cx - 3 * u, 70 * u)], fill=G2)
    d.ellipse((cx - 12 * u, 66 * u, cx + 12 * u, 74 * u), fill=G1)
    d.rectangle((cx - 20 * u, 76 * u, cx + 20 * u, 96 * u), fill=(40, 30, 20)); d.rectangle((cx - 20 * u, 76 * u, cx + 20 * u, 79 * u), fill=G3)
    d.rectangle((cx - 13 * u, 83 * u, cx + 13 * u, 90 * u), fill=G1)
    hl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(hl).ellipse((cx - 20 * u, 18 * u, cx - 10 * u, 44 * u), fill=(255, 250, 220, 140))
    im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(10)))
    return im.resize((w, h), Image.LANCZOS)

def flag(kind, w=120, h=80):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    v3 = lambda a, b, c: [d.rectangle((i * w / 3, 0, (i + 1) * w / 3, h), fill=col) for i, col in enumerate((a, b, c))]
    h3 = lambda a, b, c: [d.rectangle((0, i * h / 3, w, (i + 1) * h / 3), fill=col) for i, col in enumerate((a, b, c))]
    if kind == "ITA": v3((0, 140, 69), (244, 245, 240), (205, 33, 42))
    elif kind == "FRA": v3((0, 35, 149), (255, 255, 255), (237, 41, 57))
    elif kind == "AUT": h3((200, 16, 46), (255, 255, 255), (200, 16, 46))
    elif kind == "IUG": h3((0, 56, 147), (255, 255, 255), (206, 17, 38))
    elif kind == "POR":
        d.rectangle((0, 0, w * 0.4, h), fill=(0, 102, 0)); d.rectangle((w * 0.4, 0, w, h), fill=(255, 0, 0)); d.ellipse((w * 0.4 - 14, h / 2 - 14, w * 0.4 + 14, h / 2 + 14), fill=(255, 220, 0))
    elif kind == "URU":
        for i in range(9): d.rectangle((0, i * h / 9, w, (i + 1) * h / 9), fill=(255, 255, 255) if i % 2 == 0 else (0, 56, 168))
        d.rectangle((0, 0, w * 0.42, h * 5 / 9), fill=(255, 255, 255)); d.ellipse((w * 0.21 - 13, h * 5 / 18 - 13, w * 0.21 + 13, h * 5 / 18 + 13), fill=(252, 209, 22))
    elif kind == "BRA":
        d.rectangle((0, 0, w, h), fill=(0, 155, 58)); d.polygon([(w / 2, 8), (w - 10, h / 2), (w / 2, h - 8), (10, h / 2)], fill=(254, 223, 0)); d.ellipse((w / 2 - 17, h / 2 - 17, w / 2 + 17, h / 2 + 17), fill=(0, 39, 118))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 10, fill=255)
    im.putalpha(ImageChops.multiply(im.split()[3], m)); return im
