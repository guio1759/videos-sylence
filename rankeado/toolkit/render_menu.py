import sys, json, random, math
sys.path.insert(0, "/home/claude"); from rkcommon import *

D7 = "/home/claude/rk7/"; FOT = D7 + "fotos/"
WD = Words(D7, {"RANKEEI": "RANKEEI", "ATUM-RABILHO": "ATUM-RABILHO"})
# rank, prato, onde, foto, preço, chip, usd, fx, fy
B = [
 (10, "Batata frita", "Serendipity 3 · Nova York", "f10_2.jpg", "US$ 200", "", 200, 0.3, 0.5),
 (9, "Pizza de luxo", "Industry Kitchen · Nova York", "f09_2.jpg", "US$ 2.700", "", 2700, 0.5, 0.5),
 (8, "Hambúrguer de ouro", "Golden Boy · Holanda", "f08_0.jpg", "€ 5.000", "≈ US$ 5.400", 5400, 0.5, 0.5),
 (7, "Mel Centauri", "Turquia", "f07_1.jpg", "US$ 10.800", "POR QUILO", 10800, 0.5, 0.4),
 (6, "Uvas Ruby Roman", "um único cacho · Japão", "f06_1.jpg", "¥ 1.300.000", "≈ US$ 12.200", 12200, 0.5, 0.5),
 (5, "Caviar Almas", "esturjão albino · Irã", "f05_1.jpg", "US$ 34.500", "POR QUILO", 34500, 0.5, 0.5),
 (4, "Melões Yubari", "um par · Japão", "f04_0.jpg", "¥ 5.800.000", "POR DUAS FRUTAS", 38000, 0.5, 0.5),
 (3, "Queijo Cabrales", "curado em caverna · Espanha", "f03_0.jpg", "€ 37.500", "≈ US$ 40.000", 40000, 0.5, 0.5),
 (2, "Trufa branca", "1,5 kg · Itália", "f02_2.jpg", "US$ 330.000", "", 330000, 0.45, 0.5),
 (1, "Atum-rabilho", "leilão de Tóquio · Japão", "f01_1.jpg", "¥ 510.300.000", "≈ US$ 3,2 MILHÕES", 3290000, 0.4, 0.5),
]
GOLDD = (212, 175, 95); GOLDL = (245, 215, 140); INK = (10, 18, 15)
_ph = {}
def photo(n):
    if n not in _ph: _ph[n] = Image.open(FOT + n).convert("RGB")
    return _ph[n]

# ---------- background: velvet + art deco fans ----------
def make_bg():
    g = Image.radial_gradient("L").resize((W, H)); bg = Image.composite(Image.new("RGB", (W, H), (4, 9, 7)), Image.new("RGB", (W, H), (16, 38, 30)), g)
    n = Image.effect_noise((W // 2, H // 2), 22).resize((W, H)).convert("L")
    bg = ImageChops.multiply(bg, Image.merge("RGB", [n.point(lambda v: 225 + v // 8)] * 3))
    L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L)
    for cx, cy in [(x * 270 + (135 if (y % 2) else 0), y * 150) for y in range(14) for x in range(-1, 6)]:
        for r in (120, 90, 60): d.arc((cx - r, cy - r, cx + r, cy + r), 200, 340, fill=20, width=2)
    bg.paste(GOLDD, (0, 0), L)
    return bg
BG = make_bg()

def frame_deco(img, rank):
    d = ImageDraw.Draw(img)
    for o, wdt in ((40, 3), (54, 1)):
        d.rectangle((o, o, W - o, H - o), outline=GOLDD, width=wdt)
    for cx, cy, sx, sy in [(40, 40, 1, 1), (W - 40, 40, -1, 1), (40, H - 40, 1, -1), (W - 40, H - 40, -1, -1)]:
        for r in (40, 64): d.arc((cx - r, cy - r, cx + r, cy + r), 0, 360, fill=GOLDD, width=2)
    d.text((W / 2, 130), "LE MENU", font=F("pf", 64), fill=GOLDL, anchor="mm")
    d.text((W / 2, 188), "as comidas mais caras já vendidas", font=F("pfi", 36), fill=(200, 190, 160), anchor="mm")
    d.line((180, 225, W / 2 - 60, 225), fill=GOLDD, width=2); d.line((W / 2 + 60, 225, W - 180, 225), fill=GOLDD, width=2)
    d.regular_polygon((W / 2, 225, 12), 4, fill=GOLDD)
    if rank:
        cx, cy = W - 150, 140
        d.ellipse((cx - 72, cy - 72, cx + 72, cy + 72), fill=INK, outline=GOLDD, width=4)
        d.text((cx, cy - 26), "Nº", font=F("pfi", 28), fill=GOLDL, anchor="mm")
        d.text((cx, cy + 16), str(rank), font=F("pf", 60), fill=GOLDL, anchor="mm")

# ---------- plate + cloche ----------
PCX, PCY, PR, FR = W // 2, 790, 430, 345
def make_plate():
    P = Image.new("RGBA", (PR * 2 + 120, PR * 2 + 120), (0, 0, 0, 0)); d = ImageDraw.Draw(P); c = PR + 60
    sh = Image.new("L", P.size, 0); ImageDraw.Draw(sh).ellipse((c - PR + 10, c - PR + 40, c + PR + 10, c + PR + 40), fill=200)
    P.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(30)))
    rim = Image.radial_gradient("L").resize((PR * 2, PR * 2)).point(lambda v: 255 - v // 3)
    pl = Image.merge("RGB", [rim.point(lambda v: int(v * 0.96)), rim.point(lambda v: int(v * 0.97)), rim])
    m = Image.new("L", (PR * 2, PR * 2), 0); ImageDraw.Draw(m).ellipse((0, 0, PR * 2 - 1, PR * 2 - 1), fill=255)
    P.paste(pl, (c - PR, c - PR), m)
    d.ellipse((c - PR + 22, c - PR + 22, c + PR - 22, c + PR - 22), outline=GOLDD, width=4)
    d.ellipse((c - FR - 14, c - FR - 14, c + FR + 14, c + FR + 14), outline=(205, 200, 190), width=6)
    return P
PLATE = make_plate()
_food = {}
def food(i):
    if i not in _food:
        r = B[i]; ph = cover(photo(r[3]), FR * 2, FR * 2, r[7], r[8])
        ph = ImageEnhance.Contrast(ph).enhance(1.1); ph = ImageEnhance.Color(ph).enhance(1.2)
        m = Image.new("L", (FR * 2, FR * 2), 0); ImageDraw.Draw(m).ellipse((0, 0, FR * 2 - 1, FR * 2 - 1), fill=255)
        inner = Image.radial_gradient("L").resize((FR * 2, FR * 2)).point(lambda v: 255 - max(0, v - 170) * 2)
        ph = ImageChops.multiply(ph, Image.merge("RGB", [inner] * 3))
        _food[i] = (ph, m)
    return _food[i]

def make_cloche():
    w, h = 920, 800; C = Image.new("RGBA", (w, h + 120), (0, 0, 0, 0))
    grad = Image.linear_gradient("L").rotate(90).resize((w, h + 120))
    metal = Image.merge("RGB", [grad.point(lambda v: int(120 + 120 * math.sin(v / 255 * 3.1) ** 0.6))] * 3)
    metal = ImageChops.multiply(metal, Image.new("RGB", metal.size, (235, 238, 245)))
    m = Image.new("L", C.size, 0); dm = ImageDraw.Draw(m)
    dm.pieslice((0, 120, w, 120 + h * 2), 180, 360, fill=255)
    dm.rounded_rectangle((w / 2 - 50, 50, w / 2 + 50, 140), 40, fill=255)
    C.paste(metal, (0, 0), m); d = ImageDraw.Draw(C)
    hl = Image.new("L", C.size, 0); ImageDraw.Draw(hl).arc((130, 190, w - 260, 120 + h * 2 - 140), 200, 250, fill=255, width=40)
    C.paste((255, 255, 255), (0, 0), ImageChops.multiply(hl.filter(ImageFilter.GaussianBlur(14)), m))
    d.rounded_rectangle((-10, 120 + h - 26, w + 10, 120 + h + 18), 20, fill=(185, 188, 195), outline=(120, 122, 130), width=3)
    d.ellipse((w / 2 - 50, 40, w / 2 + 50, 100), fill=(200, 204, 212), outline=(130, 132, 140), width=3)
    return C
CLOCHE = make_cloche()

def table(img, t, i, D, lift):
    img.paste(PLATE, (PCX - PR - 60, PCY - PR - 60), PLATE)
    if i is not None:
        ph, m = food(i); z = 1.0 + 0.05 * (t / max(D, 1))
        if z != 1.0:
            s = int(FR * 2 * z); ph2 = ph.resize((s, s)); o = (s - FR * 2) // 2; ph = ph2.crop((o, o, o + FR * 2, o + FR * 2))
        img.paste(ph, (PCX - FR, PCY - FR), m)
    if lift < 1:
        u = ease2(lift); C = CLOCHE
        if u > 0: C = C.rotate(-14 * u, resample=Image.BICUBIC, expand=True)
        x = PCX - C.width / 2 + 420 * u; y = PCY + 370 - (120 + 800) - 1100 * u
        sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).ellipse((PCX - 480, PCY + 330, PCX + 480, PCY + 440), fill=int(130 * (1 - u)))
        img.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(25)))
        img.paste(C, (int(x), int(y)), C)
        if 0 < u < 1:  # steam
            L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L)
            for j in range(9):
                yy = PCY - 120 - u * 500 - j * 50; xx = PCX + math.sin(j * 1.7 + t * 3) * 120
                rr = 60 + j * 10; d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=int(60 * (1 - u)))
            img.paste((255, 255, 255), (0, 0), L.filter(ImageFilter.GaussianBlur(30)))

def sparkles(img, t, n, area=(80, 300, W - 80, 1300)):
    d = ImageDraw.Draw(img)
    for j in range(n):
        x = random.uniform(area[0], area[2]); y = random.uniform(area[1], area[3]); s = random.uniform(4, 12)
        d.line((x - s, y, x + s, y), fill=GOLDL, width=2); d.line((x, y - s, x, y + s), fill=GOLDL, width=2)

# ---------- price meter ----------
def meter(img, usd_now, mark_prev):
    d = ImageDraw.Draw(img); x0, x1, y = 120, W - 120, 1770
    d.line((x0, y, x1, y), fill=(70, 70, 60), width=8)
    lo, hi = math.log10(100), math.log10(5e6)
    def px(v): return x0 + (math.log10(max(v, 100)) - lo) / (hi - lo) * (x1 - x0)
    for v, lab in [(100, "100"), (1e3, "1 MIL"), (1e4, "10 MIL"), (1e5, "100 MIL"), (1e6, "1 MI")]:
        d.line((px(v), y - 14, px(v), y + 14), fill=(110, 105, 90), width=3)
        d.text((px(v), y + 40), lab, font=F("mono", 26), fill=(150, 145, 125), anchor="mm")
    for v in mark_prev: d.ellipse((px(v) - 7, y - 7, px(v) + 7, y + 7), fill=(120, 105, 70))
    if usd_now > 100:
        xx = px(usd_now); d.line((x0, y, xx, y), fill=GOLDL, width=8)
        d.ellipse((xx - 16, y - 16, xx + 16, y + 16), fill=GOLDL, outline=INK, width=3)

def roll_price(s, u):
    out = []; digits = [c for c in s if c.isdigit()]; nd = len(digits); k = 0
    for c in s:
        if c.isdigit():
            lock = (k + 1) / nd
            out.append(c if u >= lock else str(random.randint(0, 9))); k += 1
        else: out.append(c)
    return "".join(out)

def frame_item(i, t, D):
    r, name, where, fn, price, chip, usd, fx, fy = B[i]; k = i + 1; gold = r == 1
    tn = WD.first_num(k)
    img = BG.copy()
    if gold:
        g = Image.radial_gradient("L").resize((W, H)).point(lambda v: int(max(0, 255 - v * 1.6) * 0.5 * ease((t - tn) / 0.6)))
        img.paste(GOLDD, (0, 0), g)
    frame_deco(img, r)
    table(img, t, i, D, (t - 0.25) / 0.7)
    d = ImageDraw.Draw(img)
    u = ease((t - 0.45) / 0.4)
    if u > 0:
        f = F("pfi", 96)
        while d.textlength(name, font=f) > W - 160: f = F("pfi", f.size - 4)
        d.text((W / 2, 1295 + 30 * (1 - u)), name, font=f, fill=(255, 250, 235), anchor="mm")
        d.text((W / 2, 1378), where.upper(), font=F("os", 32), fill=GOLDD, anchor="mm")
    pu = (t - tn) / 0.9
    if pu > 0:
        s = roll_price(price, pu); f = F("pf", 112)
        while d.textlength(s, font=f) > W - 200: f = F("pf", f.size - 6)
        sc = 1 + 0.15 * math.exp(-max(0, t - tn - 0.9) * 8) if pu >= 1 else 1
        f = F("pf", f.size * sc)
        tw = d.textlength(s, font=f)
        d.line((110, 1478, W / 2 - tw / 2 - 30, 1478), fill=GOLDD, width=2)
        d.line((W / 2 + tw / 2 + 30, 1478, W - 110, 1478), fill=GOLDD, width=2)
        d.text((W / 2, 1478), s, font=f, fill=GOLDL, anchor="mm", stroke_width=3, stroke_fill=INK)
        if chip and pu > 1.1:
            cu = back((pu - 1.1) / 0.5); cf = F("osb", 34); cw = d.textlength(chip, font=cf) + 50
            d.rounded_rectangle((W / 2 - cw / 2, 1555, W / 2 + cw / 2, 1605), 25, fill=GOLDD)
            d.text((W / 2, 1580), chip, font=F("osb", int(34 * min(1, cu))), fill=INK, anchor="mm")
        if pu >= 1: sparkles(img, t, 30 if gold else 6)
    meter(img, usd * ease(min(1, max(0, pu))) if pu > 0 else 0, [b[6] for b in B[:i]])
    WD.caption(img, k, t, 1655, size=80)
    a = 1 - ease(t / 0.15)
    if a > 0: img.paste((0, 0, 0), (0, 0), Image.new("L", (W, H), int(200 * a)))
    return img

def frame_intro(t, D):
    img = BG.copy(); frame_deco(img, 0)
    table(img, t, None, D, 0)
    d = ImageDraw.Draw(img)
    q = 1 + 0.06 * math.sin(t * 4)
    d.text((PCX, PCY - 60), "?", font=F("pf", int(200 * q)), fill=INK, anchor="mm")
    for j, (txt, f, c, y) in enumerate([("As 10 comidas", F("pfi", 110), (255, 250, 235), 1300), ("MAIS CARAS", F("pf", 150), GOLDL, 1440), ("já vendidas no mundo", F("pfi", 64), (220, 210, 180), 1555)]):
        u = ease((t - 0.1 - j * 0.15) / 0.5)
        if u <= 0: continue
        d.text((W / 2, y + 40 * (1 - u)), txt, font=f, fill=c, anchor="mm")
    sparkles(img, t, 5)
    WD.caption(img, 0, t, 1700, size=80)
    return img

def frame_outro(t, D):
    img = BG.copy(); frame_deco(img, 0); d = ImageDraw.Draw(img)
    d.text((W / 2, 300), "— A CONTA —", font=F("pf", 56), fill=GOLDL, anchor="mm")
    for j in range(10):
        r, name, where, fn, price, chip, usd, *_ = B[9 - j]
        u = ease((t - j * 0.08) / 0.35)
        if u <= 0: continue
        y = 400 + j * 100; col = GOLDL if r == 1 else (240, 235, 220)
        d.text((110 - 40 * (1 - u), y), f"{r}.", font=F("pf", 46), fill=GOLDD, anchor="lm")
        d.text((190, y), name, font=F("pfi", 50), fill=col, anchor="lm")
        tw = d.textlength(price, font=F("pfb", 46)); nx = 190 + d.textlength(name, font=F("pfi", 50)) + 20
        for x in range(int(nx), int(W - 110 - tw - 20), 16): d.ellipse((x, y + 8, x + 4, y + 12), fill=(120, 110, 80))
        d.text((W - 110, y), price, font=F("pfb", 46), fill=col, anchor="rm")
    u = back((t - 1.0) / 0.5)
    if u > 0: d.text((W / 2, 1520), "SEGUE O RANKEADO BR", font=F("an", int(96 * u)), fill=GOLDL, anchor="mm", stroke_width=6, stroke_fill=INK)
    WD.caption(img, 11, t, 1640, size=80)
    if t > D - 1.5:
        d.rectangle((60, 1690, W - 60, H - 60), fill=(4, 9, 7))
        for j, line in enumerate(CRED): d.text((W / 2, 1712 + j * 28), line, font=F("mono", 19), fill=(200, 195, 175), anchor="mm")
    return img

meta = json.load(open(FOT + "meta.json"))
CRED = credit_lines(meta, [(b[0], b[3]) for b in B], "Fontes: Guinness World Records e imprensa. Fotos ilustrativas via Flickr:",
                    'Trilha: "Pamgaea" Kevin MacLeod (incompetech.com) · CC BY 4.0')
def scene_fn(k):
    if k == 0: return frame_intro
    if k == 11: return frame_outro
    return lambda t, D, i=k - 1: frame_item(i, t, D)
if __name__ == "__main__":
    main(scene_fn, D7 + "durs.json", 12, "s7", lambda d: [(0, 2.5), (1, 0.6), (1, d[1] - 0.3), (6, d[6] - 0.5), (10, d[10] - 0.5), (11, d[11] - 0.5)])
