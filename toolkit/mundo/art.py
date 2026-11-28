"""Arte 2D chapada (estilo cartoon simples) para o quadro NESSE MUNDO. Tudo desenhado com PIL, sem imagem externa."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
SKIN = [(241, 194, 150), (198, 140, 95), (141, 92, 62), (224, 172, 125)]
INKC = (40, 32, 28)
VERDE = (22, 140, 72); BRANCO = (245, 245, 240)


def gray(c, k):
    if k <= 0: return c
    a = c[3] if len(c) == 4 else None
    l = int(0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]); l = int(l * 0.85 + 30)
    out = tuple(int(c[i] * (1 - k) + l * k) for i in range(3))
    return out + ((a,) if a is not None else ())


def limb(d, p0, ang, ln, w, col):
    x1 = p0[0] + ln * math.sin(math.radians(ang)); y1 = p0[1] + ln * math.cos(math.radians(ang))
    d.line((p0[0], p0[1], x1, y1), fill=col, width=int(w)); r = w / 2
    d.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=col); d.ellipse((p0[0] - r, p0[1] - r, p0[0] + r, p0[1] + r), fill=col)
    return (x1, y1)


def person(kind="fan", h=600, k=0.0, shirt=None, pants=None, skin=0, la=20, ra=-20, ll=8, rl=-8, expr="smile", sit=False, scarf=False, hair=None, look=0, seed=0):
    """kind: vo, caio, pai, fan, noiva, noivo. k = 0 colorido .. 1 cinza. la/ra ângulos dos braços (0 = para baixo, 90 = para o lado direito da tela, 180 = para cima)."""
    rnd = random.Random(seed)
    W_, H_ = int(h * 0.9), int(h * 1.05); im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    G = lambda c: gray(c, k)
    u = h / 100.0; cx = W_ / 2
    child = kind == "caio"; s = 0.82 if child else 1.0
    head_r = 13 * u * (1.08 if child else 1.0); top = H_ - 100 * u * s
    hy = top + head_r + 2 * u
    neck = hy + head_r
    body_h = 30 * u * s; body_w = 26 * u * (0.9 if child else 1.0)
    if kind == "vo": body_w *= 1.05
    sh = shirt or {"vo": (120, 85, 60), "caio": (90, 110, 150), "pai": (70, 90, 120), "noivo": (40, 40, 48), "noiva": (250, 250, 250)}.get(kind, (rnd.choice([200, 40, 230, 30]), rnd.choice([40, 120, 180, 90]), rnd.choice([40, 200, 60, 160])))
    pa = pants or {"noiva": (250, 250, 250), "noivo": (40, 40, 48)}.get(kind, (60, 60, 75))
    sk = SKIN[skin % 4]
    hip = neck + body_h
    leg = 30 * u * s
    if not sit:
        limb(d, (cx - body_w * 0.22, hip - 2 * u), ll, leg, 9 * u, G(pa)); limb(d, (cx + body_w * 0.22, hip - 2 * u), rl, leg, 9 * u, G(pa))
    else:
        p = limb(d, (cx - body_w * 0.22, hip - 2 * u), 80, leg * 0.5, 9 * u, G(pa)); limb(d, p, 0, leg * 0.5, 9 * u, G(pa))
        p = limb(d, (cx + body_w * 0.22, hip - 2 * u), 80, leg * 0.5, 9 * u, G(pa)); limb(d, p, 0, leg * 0.5, 9 * u, G(pa))
    if kind == "noiva":
        d.polygon([(cx - body_w * 0.4, neck + 8 * u), (cx + body_w * 0.4, neck + 8 * u), (cx + body_w * 0.95, hip + leg * 0.95), (cx - body_w * 0.95, hip + leg * 0.95)], fill=G((252, 252, 252)), outline=G((220, 220, 225)))
    # braços atrás do corpo
    sy = neck + 4 * u
    limb(d, (cx - body_w / 2 + 3 * u, sy), -la, 27 * u * s, 7.5 * u, G(sh)); limb(d, (cx + body_w / 2 - 3 * u, sy), -ra, 27 * u * s, 7.5 * u, G(sh))
    for (x0, a) in ((cx - body_w / 2 + 3 * u, -la), (cx + body_w / 2 - 3 * u, -ra)):
        x1 = x0 + 27 * u * s * math.sin(math.radians(a)); y1 = sy + 27 * u * s * math.cos(math.radians(a)); r = 4.6 * u
        d.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=G(sk))
    d.rounded_rectangle((cx - body_w / 2, neck, cx + body_w / 2, hip), int(7 * u), fill=G(sh))
    if kind == "noivo":
        d.polygon([(cx - 3 * u, neck), (cx + 3 * u, neck), (cx, neck + 14 * u)], fill=G((250, 250, 250))); d.polygon([(cx - 2 * u, neck + 3 * u), (cx + 2 * u, neck + 3 * u), (cx, neck + 12 * u)], fill=G((200, 30, 40)))
    if kind == "vo":
        d.line((cx, neck + 2 * u, cx, hip - 2 * u), fill=G((90, 60, 40)), width=int(1.4 * u))
        for j in range(3): d.ellipse((cx + 2 * u, neck + (6 + 8 * j) * u, cx + 4.4 * u, neck + (8.4 + 8 * j) * u), fill=G((230, 210, 170)))
    if scarf:
        for j in range(5):
            c = VERDE if j % 2 == 0 else BRANCO
            d.rectangle((cx - body_w * 0.36 + j * body_w * 0.144, neck - 1 * u, cx - body_w * 0.36 + (j + 1) * body_w * 0.144, neck + 5 * u), fill=G(c))
        for j in range(4):
            c = VERDE if j % 2 == 0 else BRANCO
            d.rectangle((cx + body_w * 0.12, neck + 4 * u + j * 5 * u, cx + body_w * 0.32, neck + 9 * u + j * 5 * u), fill=G(c))
    # cabeça
    hx = cx + look * u
    d.ellipse((hx - head_r, hy - head_r, hx + head_r, hy + head_r), fill=G(sk))
    d.ellipse((hx - head_r - 2.2 * u, hy - 2 * u, hx - head_r + 2.4 * u, hy + 3 * u), fill=G(sk)); d.ellipse((hx + head_r - 2.4 * u, hy - 2 * u, hx + head_r + 2.2 * u, hy + 3 * u), fill=G(sk))
    hc = hair or {"vo": (235, 235, 235), "caio": (50, 35, 25), "pai": (45, 32, 22), "noiva": (90, 55, 30)}.get(kind, rnd.choice([(40, 30, 20), (90, 60, 30), (20, 20, 20), (200, 160, 80)]))
    if kind == "vo":
        d.chord((hx - head_r - 1 * u, hy - head_r * 0.4, hx - head_r * 0.35, hy + head_r * 0.55), 90, 270, fill=G(hc)); d.chord((hx + head_r * 0.35, hy - head_r * 0.4, hx + head_r + 1 * u, hy + head_r * 0.55), -90, 90, fill=G(hc))
        d.rounded_rectangle((hx - head_r * 0.62, hy + head_r * 0.28, hx + head_r * 0.62, hy + head_r * 0.38), int(u), fill=G((235, 235, 235)))  # bigode
    elif kind == "noiva":
        d.chord((hx - head_r - 1.5 * u, hy - head_r - 1.5 * u, hx + head_r + 1.5 * u, hy + head_r * 0.6), 180, 360, fill=G(hc)); d.rectangle((hx - head_r - 1.5 * u, hy - 2 * u, hx - head_r + 2 * u, hy + head_r * 1.4), fill=G(hc)); d.rectangle((hx + head_r - 2 * u, hy - 2 * u, hx + head_r + 1.5 * u, hy + head_r * 1.4), fill=G(hc))
    else:
        d.chord((hx - head_r - 0.5 * u, hy - head_r - 1.5 * u, hx + head_r + 0.5 * u, hy + head_r * 0.5), 180, 360, fill=G(hc))
        if child: d.polygon([(hx - head_r * 0.5, hy - head_r * 0.9), (hx - head_r * 0.1, hy - head_r * 1.35), (hx + head_r * 0.2, hy - head_r * 0.85)], fill=G(hc))
    # rosto
    ey = hy + 0.5 * u; ex = 5.2 * u; er = 1.7 * u
    if kind == "vo":
        for sx in (-1, 1): d.ellipse((hx + sx * ex - 3.6 * u, ey - 3.4 * u, hx + sx * ex + 3.6 * u, ey + 3.4 * u), outline=G(INKC), width=int(0.9 * u))
        d.line((hx - ex + 3.6 * u, ey, hx + ex - 3.6 * u, ey), fill=G(INKC), width=int(0.9 * u))
    for sx in (-1, 1):
        if expr == "closed": d.arc((hx + sx * ex - er * 1.3, ey - er, hx + sx * ex + er * 1.3, ey + er * 1.4), 200, 340, fill=G(INKC), width=int(0.8 * u))
        else: d.ellipse((hx + sx * ex - er, ey - er, hx + sx * ex + er, ey + er), fill=G(INKC))
    by = ey - 4.6 * u
    if expr in ("sad", "bored"):
        d.line((hx - ex - 2.5 * u, by + 1.5 * u, hx - ex + 2.5 * u, by - 0.5 * u), fill=G(INKC), width=int(0.9 * u)); d.line((hx + ex - 2.5 * u, by - 0.5 * u, hx + ex + 2.5 * u, by + 1.5 * u), fill=G(INKC), width=int(0.9 * u))
    elif expr == "angry":
        d.line((hx - ex - 2.5 * u, by - 0.8 * u, hx - ex + 2.5 * u, by + 1.4 * u), fill=G(INKC), width=int(1.0 * u)); d.line((hx + ex - 2.5 * u, by + 1.4 * u, hx + ex + 2.5 * u, by - 0.8 * u), fill=G(INKC), width=int(1.0 * u))
    my = hy + 7 * u
    if expr in ("smile", "closed"): d.arc((hx - 4 * u, my - 3.5 * u, hx + 4 * u, my + 2.5 * u), 20, 160, fill=G(INKC), width=int(1.0 * u))
    elif expr == "sad": d.arc((hx - 3.6 * u, my + 0.2 * u, hx + 3.6 * u, my + 5 * u), 200, 340, fill=G(INKC), width=int(1.0 * u))
    elif expr == "shout": d.ellipse((hx - 3.4 * u, my - 2.8 * u, hx + 3.4 * u, my + 4.4 * u), fill=G((90, 30, 30))); d.ellipse((hx - 2.2 * u, my + 1.8 * u, hx + 2.2 * u, my + 4 * u), fill=G((220, 90, 90)))
    elif expr == "o": d.ellipse((hx - 1.8 * u, my - 1.4 * u, hx + 1.8 * u, my + 2.4 * u), fill=G(INKC))
    else: d.line((hx - 3 * u, my + 0.5 * u, hx + 3 * u, my + 0.5 * u), fill=G(INKC), width=int(1.0 * u))
    if expr in ("smile", "shout", "closed"):
        for sx in (-1, 1): d.ellipse((hx + sx * 8.5 * u - 2 * u, my - 3 * u, hx + sx * 8.5 * u + 2 * u, my - 1 * u), fill=G((240, 140, 130, 255)))
    return im


def crest(h=300, k=0.0):
    h = int(h); w = int(h * 0.84); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    G = lambda c: gray(c, k)
    pts = [(6, 6), (w - 6, 6), (w - 6, h * 0.55), (w / 2, h - 6), (6, h * 0.55)]
    d.polygon(pts, fill=G(VERDE)); d.polygon([(w * 0.42, 6), (w * 0.58, 6), (w * 0.58, h * 0.93), (w * 0.42, h * 0.86)], fill=G(BRANCO))
    d.line(pts + [pts[0]], fill=G((250, 250, 250)), width=max(4, h // 40))
    from gfx import font
    d.text((w / 2, h * 0.38), "VE", font=font("blk", int(h * 0.3)), fill=G((250, 210, 60)), anchor="mm", stroke_width=max(3, h // 60), stroke_fill=G(INKC))
    d.regular_polygon((w / 2, h * 0.13, h * 0.06), 5, fill=G((250, 210, 60)), rotation=180)
    return im


def bg_paper(W, H, k=0.0, warm=(244, 232, 210)):
    im = Image.new("RGBA", (W, H), gray(warm, k) + (255,)); d = ImageDraw.Draw(im)
    for x in range(0, W, 54): d.line((x, 0, x, H), fill=gray((228, 214, 190), k), width=2)
    for y in range(0, H, 54): d.line((0, y, W, y), fill=gray((228, 214, 190), k), width=2)
    return im


def bg_street(W, H, k=0.0, t=0.0, sky=(250, 214, 160)):
    G = lambda c: gray(c, k)
    im = Image.new("RGBA", (W, H), G(sky) + (255,)); d = ImageDraw.Draw(im)
    rnd = random.Random(4); x = -40
    cols = [(230, 120, 100), (240, 200, 110), (140, 190, 160), (170, 160, 220), (240, 160, 120), (120, 170, 210)]
    while x < W + 40:
        w = rnd.randint(170, 260); hh = rnd.randint(330, 520); c = rnd.choice(cols)
        d.rectangle((x, 1180 - hh, x + w, 1180), fill=G(c)); d.polygon([(x - 10, 1180 - hh), (x + w / 2, 1180 - hh - 90), (x + w + 10, 1180 - hh)], fill=G((170, 80, 60)))
        for wy in range(1180 - hh + 50, 1120, 120):
            d.rectangle((x + 30, wy, x + 80, wy + 60), fill=G((255, 245, 210))); d.rectangle((x + w - 80, wy, x + w - 30, wy + 60), fill=G((255, 245, 210)))
        x += w + 10
    d.rectangle((0, 1180, W, H), fill=G((190, 180, 165))); d.rectangle((0, 1180, W, 1210), fill=G((150, 140, 128)))
    return im


def bg_stands(W, H, k=0.0, rows=9, wipe=None, seed=7, t=0.0, people=True):
    """Arquibancada cheia. wipe=(0..1): fração das fileiras (de cima pra baixo) já cinza."""
    im = Image.new("RGBA", (W, H), gray((70, 90, 120), k) + (255,)); d = ImageDraw.Draw(im)
    rnd = random.Random(seed); rh = H / rows
    for r in range(rows):
        kr = k
        if wipe is not None: kr = max(k, min(1.0, (wipe * (rows + 2) - r)))
        y = r * rh
        d.rectangle((0, y + rh * 0.62, W, y + rh), fill=gray((120, 125, 135), kr))
        if not people: continue
        x = -30 + (r % 2) * 50
        while x < W + 40:
            c = rnd.choice([VERDE, BRANCO, VERDE, (250, 210, 60)])
            bob = 6 * math.sin(t * 6 + x * 0.05 + r) * (1 - kr)
            d.rounded_rectangle((x, y + rh * 0.3 + bob, x + 70, y + rh * 0.7), 20, fill=gray(c, kr))
            d.ellipse((x + 12, y + rh * 0.08 + bob, x + 58, y + rh * 0.08 + 46 + bob), fill=gray(rnd.choice(SKIN), kr))
            x += rnd.randint(85, 110)
    im.info["stands"] = True
    return im


def seat(w=220, col=(30, 120, 70), k=0.0):
    w = int(w); h = int(w * 1.1); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = gray(col, k); c2 = gray(tuple(int(v * 0.75) for v in col), k)
    d.rounded_rectangle((w * 0.1, 0, w * 0.9, h * 0.62), int(w * 0.12), fill=c)
    d.rounded_rectangle((0, h * 0.55, w, h * 0.78), int(w * 0.08), fill=c2)
    d.rectangle((w * 0.42, h * 0.78, w * 0.58, h), fill=gray((90, 90, 95), k))
    return im


def ticket(w=520, k=0.0, n=""):
    from gfx import font
    w = int(w); h = int(w * 0.42); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 22, fill=gray((250, 240, 215), k), outline=gray(VERDE, k), width=8)
    d.line((w * 0.72, 12, w * 0.72, h - 12), fill=gray(VERDE, k), width=4)
    d.text((w * 0.36, h * 0.3), "VILA ESPERANÇA", font=font("blk", int(h * 0.16)), fill=gray(VERDE, k), anchor="mm")
    d.text((w * 0.36, h * 0.6), "ARQUIBANCADA B", font=font("bd", int(h * 0.12)), fill=gray(INKC, k), anchor="mm")
    d.text((w * 0.86, h * 0.5), n, font=font("blk", int(h * 0.26)), fill=gray(INKC, k), anchor="mm")
    return im


def hand(w=420, k=0.0, skin=0, flip=False):
    w = int(w); h = int(w * 1.2); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = gray(SKIN[skin], k)
    d.rounded_rectangle((w * 0.18, h * 0.38, w * 0.82, h * 0.86), int(w * 0.16), fill=c)
    for j, (x, ln) in enumerate(((0.22, 0.36), (0.38, 0.42), (0.54, 0.4), (0.7, 0.33))):
        d.rounded_rectangle((w * x, h * (0.42 - ln), w * (x + 0.13), h * 0.55), int(w * 0.065), fill=c)
    d.rounded_rectangle((w * 0.0, h * 0.5, w * 0.3, h * 0.64), int(w * 0.07), fill=c)
    d.rectangle((w * 0.24, h * 0.86, w * 0.76, h), fill=gray((120, 85, 60), k))
    for j in range(3): d.arc((w * 0.3, h * (0.6 + j * 0.06), w * 0.7, h * (0.7 + j * 0.06)), 200, 340, fill=gray(tuple(int(v * 0.85) for v in SKIN[skin]), k), width=3)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


def wipe_gray(col_img, gray_img, frac, vertical=True, from_bottom=True):
    """Mistura duas versões: frac 0 = tudo colorido, 1 = tudo cinza, com borda suave."""
    w, h = col_img.size; m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    if vertical:
        y = h * (1 - frac) if from_bottom else h * frac
        if from_bottom: d.rectangle((0, y, w, h), fill=255)
        else: d.rectangle((0, 0, w, y), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(18)); out = col_img.copy(); out.paste(gray_img, (0, 0), Image.composite(m, Image.new("L", (w, h), 0), gray_img.split()[3]))
    return out
