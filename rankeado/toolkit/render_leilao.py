import sys, json, subprocess, os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

W, H, FPS = 1080, 1920, 30
FD = "/home/claude/fonts/"
_fc = {}
def F(kind, sz):
    sz = max(8, int(sz)); k = (kind, sz)
    if k in _fc: return _fc[k]
    if kind == "pf":   f = ImageFont.truetype(FD + "PlayfairDisplay[wght].ttf", sz); f.set_variation_by_name("Black")
    elif kind == "pfb": f = ImageFont.truetype(FD + "PlayfairDisplay[wght].ttf", sz); f.set_variation_by_name("Bold")
    elif kind == "pfi": f = ImageFont.truetype(FD + "PlayfairDisplay-Italic[wght].ttf", sz); f.set_variation_by_name("Italic") if False else f.set_variation_by_axes([500])
    elif kind == "an":  f = ImageFont.truetype(FD + "Anton-Regular.ttf", sz)
    elif kind == "mono": f = ImageFont.truetype(FD + "ShareTechMono-Regular.ttf", sz)
    elif kind == "os":  f = ImageFont.truetype(FD + "Oswald[wght].ttf", sz); f.set_variation_by_name("SemiBold")
    _fc[k] = f; return f

GOLD = (232, 186, 82); GOLDL = (255, 226, 150); CREAM = (244, 237, 221); INK = (32, 22, 18); WINE = (120, 14, 30)
AMBER = (255, 168, 38); RED = (196, 18, 32); WHITE = (255, 255, 255); BLACK = (0, 0, 0)
FOT = "/home/claude/rk3/fotos/"
B = [  # rank, name, sub, photo, fx, price (US$ mi), trigger, year
 (10, "Ferrari 290 MM", "1956 · só 4 fabricadas", "c10_2.jpg", 0.5, 28.0, "28", 2015),
 (9, "McLaren F1 GTR", "1996 · lenda dos anos 90", "c09_1.jpg", 0.5, 34.7, "34", 2026),
 (8, "Ferrari 335 S", "1957 · carroceria Scaglietti", "c08_0.jpg", 0.33, 35.7, "35", 2016),
 (7, "Ferrari 250 LM", "1964 · vendida em Paris", "c07_0.jpg", 0.5, 36.3, "36", 2025),
 (6, "Ferrari Luce", "2026 · elétrica, zero km", "c06_0.jpg", 0.5, 40.0, "40", 2026),
 (5, "Shelby Cobra Daytona", "1964 · o americano mais caro", "c05_3.jpg", 0.5, 42.9, "42", 2026),
 (4, "Ferrari 250 GTO", "1962 · a lendária", "c04_0.jpg", 0.5, 48.4, "48", 2018),
 (3, "Ferrari 330 LM", "1962 · também uma 250 GTO", "c03_1.jpg", 0.5, 51.7, "51", 2023),
 (2, "Mercedes W196 R", "1954 · o carro do Fangio", "c02_1.jpg", 0.5, 53.9, "53", 2025),
 (1, "Mercedes 300 SLR", "1955 · só existem duas", "c01_0.jpg", 0.5, 143.0, "143", 2022),
]
FIX = {"RANKEI": "RANKEEI", "10º": "DÉCIMO", "8º": "OITAVO", "6º": "SEXTO", "2º": "SEGUNDO"}
WORDS = json.load(open("/home/claude/rk3/words.json"))

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def lerp(a, b, u): return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
def brl(n): return f"{int(round(n)):,}".replace(",", ".")
def fmt_mi(p): return ("%.0f" % p) if p == int(p) else ("%.1f" % p).replace(".", ",")

def word_time(k, key, default):
    for w in WORDS[k]:
        if key.lower() in w["w"].lower(): return w["t0"]
    return default

# ---------------- backdrop: velvet + spotlight ----------------
def make_velvet():
    random.seed(3)
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        u = abs(y - 820) / 1100
        d.line([(0, y), (W, y)], fill=lerp((92, 10, 26), (22, 2, 8), min(1, u)))
    # vertical velvet folds
    folds = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(folds)
    for x in range(0, W, 6):
        v = int(28 + 26 * math.sin(x / 47.0) + 12 * math.sin(x / 13.0))
        fd.line([(x, 0), (x, H)], fill=max(0, v), width=6)
    folds = folds.filter(ImageFilter.GaussianBlur(10))
    im = Image.composite(Image.new("RGB", (W, H), (150, 30, 50)), im, folds.point(lambda v: v // 3))
    # spotlight cone
    spot = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(spot)
    sd.polygon([(W / 2 - 90, -50), (W / 2 + 90, -50), (W + 260, 1500), (-260, 1500)], fill=120)
    sd.ellipse([40, 1180, W - 40, 1560], fill=170)
    spot = spot.filter(ImageFilter.GaussianBlur(90))
    im = Image.composite(Image.new("RGB", (W, H), (255, 214, 170)), im, spot.point(lambda v: v // 3))
    # vignette
    vg = Image.new("L", (W, H), 0); vd = ImageDraw.Draw(vg)
    vd.rectangle([0, 0, W, H], fill=200); vd.ellipse([-260, -200, W + 260, H + 160], fill=0)
    vg = vg.filter(ImageFilter.GaussianBlur(140))
    im = Image.composite(Image.new("RGB", (W, H), BLACK), im, vg)
    # fine noise
    n = Image.effect_noise((W, H), 22).convert("RGB")
    im = Image.blend(im, ImageChops.multiply(im, n.point(lambda v: 150 + v // 3)), 0.25)
    return im
VELVET = None

# ---------------- catalog card ----------------
CW, CHt = 920, 1140
PHW, PHH = 840, 560
_photo = {}
def photo(i):
    if i not in _photo:
        im = Image.open(FOT + B[i][3]).convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.1); im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Sharpness(im).enhance(1.3)
        ar = PHW / PHH
        if im.width / im.height > ar:
            nw = int(im.height * ar); cx = int(im.width * B[i][4]); x0 = max(0, min(im.width - nw, cx - nw // 2)); im = im.crop((x0, 0, x0 + nw, im.height))
        else:
            nh = int(im.width / ar); y0 = (im.height - nh) // 2; im = im.crop((0, y0, im.width, y0 + nh))
        _photo[i] = im.resize((int(PHW * 1.15), int(PHH * 1.15)), Image.LANCZOS)
    return _photo[i]

PAPER = None
def make_paper():
    random.seed(7)
    p = Image.new("RGB", (CW, CHt), CREAM)
    n = Image.effect_noise((CW, CHt), 30).convert("L").filter(ImageFilter.GaussianBlur(0.6))
    p = Image.composite(Image.new("RGB", (CW, CHt), (226, 214, 190)), p, n.point(lambda v: max(0, v - 110)))
    return p

def card_img(i, t, D, sold_u, gold=False):
    r, name, sub, _, _, price, _, year = B[i]
    c = PAPER.copy(); d = ImageDraw.Draw(c)
    edge = GOLD if gold else (150, 120, 80)
    d.rectangle([14, 14, CW - 15, CHt - 15], outline=edge, width=4 if gold else 2)
    d.rectangle([24, 24, CW - 25, CHt - 25], outline=edge, width=1)
    d.text((CW / 2, 70), "RANKEADO BR  ·  LEILÕES HISTÓRICOS", font=F("os", 24), fill=(120, 95, 70), anchor="mm")
    d.line([(60, 100), (CW - 60, 100)], fill=(150, 120, 80), width=1)
    d.text((CW / 2, 150), f"LOTE Nº {r:02d}", font=F("pf", 58), fill=WINE, anchor="mm")
    # photo with slow push
    src = photo(i); z = 1.0 + 0.12 * min(1, t / max(D, 0.1))
    cw, ch = src.width / z, src.height / z; sx, sy = (src.width - cw) / 2, (src.height - ch) / 2
    ph = src.resize((PHW, PHH), Image.BILINEAR, box=(sx, sy, sx + cw, sy + ch))
    px, py = (CW - PHW) // 2, 205
    d.rectangle([px - 6, py - 6, px + PHW + 5, py + PHH + 5], fill=INK)
    c.paste(ph, (px, py))
    nf = F("pf", 76)
    while d.textlength(name, font=nf) > CW - 100: nf = F("pf", nf.size - 4)
    d.text((CW / 2, py + PHH + 85), name, font=nf, fill=INK, anchor="mm")
    d.text((CW / 2, py + PHH + 150), sub, font=F("pfi", 36), fill=(110, 80, 55), anchor="mm")
    d.line([(160, py + PHH + 200), (CW - 160, py + PHH + 200)], fill=(150, 120, 80), width=1)
    if sold_u <= 0:
        dots = "." * (1 + int(t * 3) % 3)
        d.text((CW / 2, py + PHH + 265), "lances em andamento" + dots, font=F("pfi", 40), fill=(140, 110, 85), anchor="mm")
    else:
        d.text((CW / 2, py + PHH + 240), "ARREMATADO POR", font=F("os", 26), fill=(120, 95, 70), anchor="mm")
        d.text((CW / 2, py + PHH + 300), f"US$ {fmt_mi(price)} milhões", font=F("pf", 64), fill=WINE, anchor="mm")
    return c

def stamp_on(card, u, text="VENDIDO"):
    if u <= 0: return card
    sc = 1 + 1.4 * (1 - ease(u / 0.6))
    s = Image.new("RGBA", (560, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(s)
    sd.rounded_rectangle([16, 16, 544, 184], 18, outline=RED + (255,), width=10)
    sd.rounded_rectangle([34, 34, 526, 166], 10, outline=RED + (255,), width=3)
    sd.text((280, 102), text, font=F("an", 108), fill=RED + (255,), anchor="mm")
    # ink texture
    n = Image.effect_noise((560, 200), 60).point(lambda v: 255 if v > 95 else 120)
    a = ImageChops.multiply(s.split()[3], n)
    s.putalpha(a.point(lambda v: int(v * 0.85 * min(1, u * 3))))
    s = s.rotate(-14, resample=Image.BICUBIC, expand=True)
    s = s.resize((int(s.width * sc), int(s.height * sc)), Image.BILINEAR)
    card = card.convert("RGBA")
    card.alpha_composite(s, (int(CW / 2 - s.width / 2 + 120), int(380 - s.height / 2)))
    return card

def place_card(img, card, ang, cx, cy, shadow=True):
    cr = card.convert("RGBA").rotate(ang, resample=Image.BICUBIC, expand=True)
    if shadow:
        sh = Image.new("RGBA", cr.size, (0, 0, 0, 0)); sh.putalpha(cr.split()[3].point(lambda v: int(v * 0.6)))
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        img.paste((0, 0, 0), (int(cx - cr.width / 2 + 18), int(cy - cr.height / 2 + 30)), sh.split()[3])
    img.paste(cr, (int(cx - cr.width / 2), int(cy - cr.height / 2)), cr)

# ---------------- LED bid board ----------------
def led(img, label, value, flash=0.0, y=150):
    d = ImageDraw.Draw(img)
    x0, x1, y0, y1 = 70, W - 70, y - 90, y + 90
    d.rounded_rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], 22, fill=GOLD)
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(10, 8, 6))
    for gx in range(x0 + 8, x1 - 4, 9):
        d.line([(gx, y0 + 6), (gx, y1 - 6)], fill=(22, 16, 10), width=1)
    d.text((W / 2, y0 + 34), label, font=F("mono", 32), fill=(200, 130, 30), anchor="mm")
    glow = Image.new("L", (W, 200), 0); gd = ImageDraw.Draw(glow)
    gd.text((W / 2, 112), value, font=F("mono", 92), fill=255, anchor="mm")
    g = glow.filter(ImageFilter.GaussianBlur(9))
    col = lerp(AMBER, (255, 240, 200), flash)
    img.paste(col, (0, y - 100), g.point(lambda v: int(v * 0.55)))
    img.paste(col, (0, y - 100), glow)

# ---------------- paddles & gavel ----------------
def paddle_sprite(num):
    s = Image.new("RGBA", (220, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle([95, 180, 125, 410], 12, fill=(92, 56, 30, 255))
    d.ellipse([10, 10, 210, 210], fill=(250, 248, 240, 255), outline=(30, 30, 30, 255), width=6)
    d.text((110, 112), str(num), font=F("an", 92), fill=(20, 20, 20, 255), anchor="mm")
    return s
_paddles = {}
def paddle(num):
    if num not in _paddles: _paddles[num] = paddle_sprite(num)
    return _paddles[num]

def gavel_sprite():
    s = Image.new("RGBA", (520, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle([245, 140, 275, 500], 12, fill=(96, 56, 28, 255))           # handle (pivot at bottom 260,500)
    d.rounded_rectangle([150, 70, 370, 170], 22, fill=(70, 38, 18, 255))           # head
    d.rectangle([180, 70, 200, 170], fill=GOLD + (255,)); d.rectangle([320, 70, 340, 170], fill=GOLD + (255,))
    d.rounded_rectangle([150, 70, 370, 95], 12, fill=(110, 66, 34, 255))
    return s
GAVEL = None
def draw_gavel(img, ang, px, py):
    g = GAVEL.rotate(ang, resample=Image.BICUBIC, center=(260, 500)).resize((416, 416), Image.BILINEAR)
    img.paste(g, (int(px - 208), int(py - 400)), g); return
    img.paste(g, (int(px - 260), int(py - 500)), g)

# ---------------- captions ----------------
def groups_for(k):
    gs = []; buf = None
    for w in WORDS[k]:
        txt = w["w"].upper().strip(".,!?")
        if (txt.startswith("-") or txt.startswith(",")) and gs:
            gs[-1]["txt"] += txt; gs[-1]["t1"] = w["t1"]; continue
        if buf is not None: g = {"txt": (buf["txt"] + " " + txt).strip(), "t0": buf["t0"], "t1": w["t1"]}; buf = None
        else: g = {"txt": txt, "t0": w["t0"], "t1": w["t1"]}
        orig = w["w"].strip(".,!?")
        if len(g["txt"]) <= 2 and not any(c.isdigit() for c in g["txt"]) and not (orig.isupper() and len(orig) >= 2):
            buf = g; continue
        gs.append(g)
    for g in gs: g["txt"] = FIX.get(g["txt"], g["txt"])
    return gs
GROUPS = [groups_for(k) for k in range(12)]
def caption(img, k, t, y=1720):
    d = ImageDraw.Draw(img); cur = None
    for g in GROUPS[k]:
        if g["t0"] - 0.05 <= t: cur = g
    if cur is None or t > cur["t1"] + 0.5: return
    a = (t - cur["t0"] + 0.05) / 0.12; sz = 104 * (1 + 0.22 * (1 - ease(a)))
    f = F("an", sz)
    while d.textlength(cur["txt"], font=f) > W - 90 and sz > 50: sz -= 6; f = F("an", sz)
    num = any(c.isdigit() for c in cur["txt"])
    d.text((W / 2, y), cur["txt"], font=f, fill=GOLDL if num else WHITE, anchor="mm", stroke_width=9, stroke_fill=BLACK)

def lots_bar(d, k):
    y = 1868; x0, x1 = 200, W - 200
    for j in range(10):
        x = x0 + (x1 - x0) * j / 9
        on = j < k
        d.rounded_rectangle([x - 22, y - 9, x + 22, y + 9], 4, fill=GOLD if on else (70, 40, 46))
    d.text((W / 2, y - 40), f"{k}º LOTE DE 10" if k else "", font=F("os", 26), fill=GOLD, anchor="mm")

# ---------------- bids schedule ----------------
def bids(i, t0, t1, price):
    random.seed(100 + i)
    n = 7; vals = []
    for j in range(n):
        u = j / (n - 1)
        v = price * (0.42 + 0.58 * (u ** 1.3))
        if j < n - 1: v = round(v * 4) / 4
        vals.append(v)
    vals[-1] = price
    times = [t0 + (t1 - t0) * (j / (n - 1)) ** 0.85 for j in range(n)]
    nums = [random.randint(11, 99) for _ in range(n)]
    return list(zip(times, vals, nums))
BIDS = {}

def frame_item(i, t, D):
    k = i + 1; r, name, sub, _, _, price, trig, year = B[i]
    tn = word_time(k, trig, D * 0.5) + 0.12
    if i not in BIDS: BIDS[i] = bids(i, 0.7, tn, price)
    bl = BIDS[i]
    img = VELVET.copy()
    # current bid
    cur = None
    for (bt, v, nm) in bl:
        if t >= bt: cur = (bt, v, nm)
    slam = tn + 0.45
    sold_u = (t - slam) if t >= slam else 0
    if cur is None: led(img, "LANCE INICIAL", "US$ ---", 0)
    else:
        fl = max(0, 1 - (t - cur[0]) / 0.2)
        lab = "ARREMATADO!" if t >= slam else "LANCE ATUAL"
        led(img, lab, "US$ " + brl(cur[1] * 1e6), fl if t < slam else (0.5 + 0.5 * math.sin(t * 18)) * 0.6)
    # paddles
    for j, (bt, v, nm) in enumerate(bl):
        u = (t - bt) / 0.75
        if 0 <= u <= 1:
            h = math.sin(math.pi * min(1, u)) ; side = j % 2
            p = paddle(nm).rotate(12 if side else -12, resample=Image.BICUBIC, expand=True)
            x = 40 + (j * 53) % 120 if side == 0 else W - 40 - p.width - (j * 37) % 120
            y = H - 120 - int(380 * ease(h * 1.0)) + 60
            img.paste(p, (x, y), p)
    # card toss in
    a = ease(t / 0.5); ang_final = (-2.2 if i % 2 else 2.0)
    ang = ang_final + (1 - a) * (-18 if i % 2 else 18)
    cx = W / 2 + (1 - a) * W * (1 if i % 2 == 0 else -1) * 0.9; cy = 860 + (1 - a) * 120
    card = card_img(i, t, D, sold_u, gold=(r <= 3))
    card = stamp_on(card, sold_u, "VENDIDO" if r != 1 else "RECORDE")
    shake = 0
    if 0 <= t - slam < 0.3: shake = 14 * (1 - (t - slam) / 0.3) * (2.2 if r == 1 else 1)
    place_card(img, card, ang, cx + random.uniform(-shake, shake), cy + random.uniform(-shake, shake))
    # gavel swing
    if t > tn - 0.2:
        gu = (t - (tn - 0.2)) / 0.65
        if gu < 1:
            ang_g = 55 * (1 - ease(gu / 0.7)) if gu < 0.7 else 0
            ang_g = ang_g - 8 * max(0, math.sin((gu - 0.7) / 0.3 * math.pi)) if gu >= 0.7 else ang_g
            draw_gavel(img, ang_g, W - 95, 1800)
        elif t - slam < 1.2:
            draw_gavel(img, 0, W - 95, 1800)
    d = ImageDraw.Draw(img)
    caption(img, k, t - 0.12)
    lots_bar(ImageDraw.Draw(img), k)
    if t < 0.07: img = Image.blend(img, Image.new("RGB", (W, H), WHITE), 0.3 * (1 - t / 0.07))
    if 0 <= t - slam < 0.1: img = Image.blend(img, Image.new("RGB", (W, H), GOLDL), 0.45 * (1 - (t - slam) / 0.1))
    if r == 1 and t > slam: confetti(img, t - slam)
    return img

CONF = None
def confetti(img, tt):
    global CONF
    if CONF is None:
        random.seed(9); CONF = [(random.uniform(0, W), random.uniform(-600, 0), random.uniform(250, 520), random.uniform(0, 6.28), random.choice([GOLD, GOLDL, (255, 255, 255), RED])) for _ in range(160)]
    d = ImageDraw.Draw(img)
    for (x, y, v, ph, c) in CONF:
        yy = y + v * tt; xx = x + 30 * math.sin(ph + tt * 3)
        if 0 < yy < H:
            w = 8 + 6 * abs(math.sin(ph + tt * 6)); d.rectangle([xx, yy, xx + w, yy + 16], fill=c)

def frame_intro(t, D):
    img = VELVET.copy()
    # three face-down catalog cards fanned
    for j, (ang, dx) in enumerate([(-12, -250), (0, 0), (12, 250)]):
        a = ease((t - 0.1 - j * 0.12) / 0.45)
        if a <= 0: continue
        c = PAPER.copy().resize((560, 700)); cd = ImageDraw.Draw(c)
        cd.rectangle([12, 12, 547, 687], outline=GOLD, width=3); cd.rectangle([24, 24, 535, 675], outline=(150, 120, 80), width=1)
        cd.text((280, 300), "LOTE", font=F("pf", 70), fill=WINE, anchor="mm")
        cd.text((280, 400), "?", font=F("pf", 160), fill=WINE, anchor="mm")
        place_card(img, c, ang + (1 - a) * 30, W / 2 + dx, 1180 + (1 - a) * 500)
    gu = t / 0.45
    if gu < 1.6: draw_gavel(img, 55 * (1 - ease(min(1, gu))), W - 150, 1640)
    d = ImageDraw.Draw(img)
    led(img, "O LEILÃO VAI COMEÇAR", "US$ ???.???.???", 0, y=150)
    a = back((t - 0.35) / 0.4)
    if t > 0.35:
        d.text((W / 2, 330), "RANKEEI OS 10", font=F("os", 54), fill=WHITE, anchor="mm")
        d.text((W / 2, 455), "CARROS", font=F("pf", 170 * max(0.3, a)), fill=GOLDL, anchor="mm", stroke_width=4, stroke_fill=(60, 30, 10))
        d.text((W / 2, 590), "mais caros já vendidos", font=F("pfi", 64), fill=WHITE, anchor="mm")
    tn = word_time(0, "número", 2.5)
    if t > tn:
        a2 = back((t - tn) / 0.3)
        d.rounded_rectangle([90, 1690, W - 90, 1800], 55, fill=RED)
        d.text((W / 2, 1745), "O Nº 1 CUSTOU QUASE 3X O 2º", font=F("an", 60 * max(0.3, a2)), fill=WHITE, anchor="mm")
    if 0.45 <= t < 0.55: img = Image.blend(img, Image.new("RGB", (W, H), GOLDL), 0.4 * (1 - (t - 0.45) / 0.1))
    return img

CRED = None
def frame_outro(t, D):
    img = VELVET.copy()
    # catalog grid
    tw_, th_ = 470, 300
    for j in range(10):
        r = 9 - j; a = ease((t - j * 0.05) / 0.3)
        if a <= 0: continue
        c = Image.new("RGB", (tw_, th_), CREAM); cd = ImageDraw.Draw(c)
        ph = photo(r).resize((tw_ - 24, int((tw_ - 24) * PHH / PHW)))
        c.paste(ph.crop((0, 0, tw_ - 24, 200)), (12, 12))
        cd.text((20, 236), f"LOTE {B[r][0]:02d}", font=F("pf", 30), fill=WINE, anchor="lm")
        cd.text((tw_ - 20, 236), f"US$ {fmt_mi(B[r][5])} mi", font=F("pf", 30), fill=INK, anchor="rm")
        cd.text((20, 274), B[r][1], font=F("pfi", 22), fill=(110, 80, 55), anchor="lm")
        x = 50 + (j % 2) * (tw_ + 40) + tw_ / 2; y = 260 + (j // 2) * (th_ + 26) + th_ / 2
        place_card(img, c, (j % 3 - 1) * 1.5, x, y + (1 - a) * 80, shadow=True)
    d = ImageDraw.Draw(img)
    if t > 0.4:
        a = back((t - 0.4) / 0.35)
        d.rounded_rectangle([60, 700, W - 60, 1150], 26, fill=(14, 4, 8), outline=GOLD, width=4)
        d.text((W / 2, 790), "QUAL LOTE VOCÊ", font=F("pf", 74), fill=WHITE, anchor="mm")
        d.text((W / 2, 915), "ARREMATARIA?", font=F("pf", 104 * max(0.3, a)), fill=GOLDL, anchor="mm")
        d.text((W / 2, 1060), "comenta aí", font=F("pfi", 50), fill=WHITE, anchor="mm")
    if t > 1.2:
        d.rounded_rectangle([170, 1190, W - 170, 1280], 45, fill=GOLD)
        d.text((W / 2, 1235), "SEGUE O @RANKEADOBR", font=F("an", 52), fill=BLACK, anchor="mm")
    if t > D - 2.6:
        d.rectangle([0, 1660, W, H], fill=BLACK); y = 1672
        for line in CRED: d.text((30, y), line, font=F("os", 17), fill=(190, 190, 200)); y += 21
    return img

def scene_fn(k):
    if k == 0: return frame_intro
    if k == 11: return frame_outro
    return lambda t, D: frame_item(k - 1, t, D)

def render_scene(k, D, out):
    n = int(round(D * FPS)); tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    fn = scene_fn(k)
    for i in range(n):
        random.seed(k * 10000 + i)
        p.stdin.write(fn(i / FPS, D).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, out)

def lic(m):
    l = m["license"].upper(); v = m.get("lv") or ""
    return "CC0" if l in ("CC0", "PDM") else f"CC {l} {v}".strip()
def credits():
    meta = json.load(open(FOT + "meta.json")); parts = []
    for b in B:
        m = meta[b[3]]; parts.append(f"#{b[0]} {m.get('creator') or 'autor desconhecido'} ({lic(m)})")
    lines, cur = ["Fotos via Wikimedia Commons / Flickr:"], ""
    for p_ in parts:
        if len(cur) + len(p_) > 110: lines.append(cur); cur = ""
        cur += ("  ·  " if cur else "") + p_
    lines.append(cur); lines.append('Trilha: "Volatile Reaction" Kevin MacLeod (incompetech.com) · CC BY 4.0')
    return lines

def bid_times():
    out = []
    for i in range(10):
        k = i + 1; tn = word_time(k, B[i][6], 3) + 0.12
        out.append({"bids": [bt for bt, _, _ in bids(i, 0.7, tn, B[i][5])], "slam": tn + 0.45})
    return out

if __name__ == "__main__":
    VELVET = make_velvet(); PAPER = make_paper(); GAVEL = gavel_sprite(); CRED = credits()
    mode = sys.argv[1]; durs = json.load(open(sys.argv[2]))
    if mode == "stills":
        for k, t in [(0, 0.3), (0, 3.4), (4, 1.6), (4, 5.6), (10, 10.2), (11, durs[11] - 1)]:
            random.seed(1); scene_fn(k)(t, durs[k]).convert("RGB").save(f"s6_{k}_{t}.png")
    elif mode == "times":
        json.dump(bid_times(), open("bidtimes.json", "w")); print("ok")
    else:
        for k in [int(x) for x in sys.argv[3:]] or range(12):
            render_scene(k, durs[k], f"s6_{k:02d}.mp4")
