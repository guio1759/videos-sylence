import sys, json, random, math
sys.path.insert(0, "/home/claude"); from rkcommon import *

D6 = "/home/claude/rk6/"; FOT = D6 + "fotos/"
WD = Words(D6, {"BEIRA-RIO": "BEIRA-RIO", "RANKEEI": "RANKEEI"})
# rank, nome, cidade, foto, capacidade, cor, setor
B = [
 (10, "BEIRA-RIO", "PORTO ALEGRE · RS", "e10_1.jpg", 50842, (215, 25, 32), "INTER"),
 (9, "PARQUE DO SABIÁ", "UBERLÂNDIA · MG", "e09_2.jpg", 52990, (0, 140, 70), "SABIÁ"),
 (8, "MANGUEIRÃO", "BELÉM · PA", "e08_3.jpg", 53000, (0, 120, 200), "PARÁ"),
 (7, "ARENA DO GRÊMIO", "PORTO ALEGRE · RS", "e07_0.jpg", 56500, (0, 150, 215), "GRÊMIO"),
 (6, "ARRUDA", "RECIFE · PE", "e06_0.jpg", 57000, (200, 20, 30), "SANTA CRUZ"),
 (5, "MINEIRÃO", "BELO HORIZONTE · MG", "e05_0.jpg", 61846, (30, 70, 160), "7 x 1"),
 (4, "CASTELÃO", "FORTALEZA · CE", "e04_0.jpg", 63903, (230, 120, 0), "CEARÁ"),
 (3, "MORUMBIS", "SÃO PAULO · SP", "e03_0.jpg", 66795, (200, 20, 30), "MAIOR PRIVADO"),
 (2, "MANÉ GARRINCHA", "BRASÍLIA · DF", "e02_1.jpg", 72788, (0, 150, 90), "CAPITAL"),
 (1, "MARACANÃ", "RIO DE JANEIRO · RJ", "e01_1.jpg", 78838, (212, 170, 40), "TEMPLO"),
]
def fmt(n): return f"{n:,}".replace(",", ".")
_ph = {}
def photo(name):
    if name not in _ph: _ph[name] = Image.open(FOT + name).convert("RGB")
    return _ph[name]
_bg = {}
def bgfor(name):
    if name not in _bg:
        b = cover(photo(name), W // 4, H // 4).filter(ImageFilter.GaussianBlur(6)).resize((W, H))
        b = ImageEnhance.Brightness(b).enhance(0.32); b = ImageEnhance.Color(b).enhance(0.7); _bg[name] = b
    return _bg[name]

# ---- floodlights ----
def beams(t):
    L = Image.new("L", (W // 2, H // 2), 0); d = ImageDraw.Draw(L)
    for sx, base in [(-40, 0.35), (W // 2 + 40, -0.35)]:
        for j in range(3):
            a = base + 0.12 * math.sin(t * 0.7 + j * 2.1) + (j - 1) * 0.16
            ex = sx + math.sin(a) * 1500 * (1 if sx < 0 else -1) * -1
            x2 = sx + 1400 * math.sin(abs(a) + 0.4) * (1 if sx < 0 else -1)
            d.polygon([(sx, -20), (x2 - 90, H // 2), (x2 + 90, H // 2)], fill=26)
    return L.filter(ImageFilter.GaussianBlur(28)).resize((W, H))
_lamps = None
def lamps(img):
    global _lamps
    if _lamps is None:
        g = Image.new("L", (W, 220), 0); d = ImageDraw.Draw(g)
        for cx in (90, W - 90):
            for r in range(4):
                for c in range(4): d.ellipse((cx - 64 + c * 34, 40 + r * 30, cx - 44 + c * 34, 58 + r * 30), fill=255)
        _lamps = (g.filter(ImageFilter.GaussianBlur(14)), g)
    img.paste((255, 250, 220), (0, 0), _lamps[0]); img.paste((255, 255, 240), (0, 0), _lamps[1])

# ---- crowd silhouette band ----
random.seed(5)
FANS = [(random.uniform(-20, W + 20), random.uniform(0, 1), random.uniform(0, 6.28), random.choice([0, 0, 1, 2])) for _ in range(70)]
def crowd(img, t, hype=0.0, col=(12, 12, 18)):
    d = ImageDraw.Draw(img); top = 1700
    for x, depth, ph, arms in sorted(FANS, key=lambda f: f[1]):
        s = 0.75 + depth * 0.55; y = top + 40 + depth * 120
        jump = abs(math.sin(t * (5 + hype * 4) + ph)) * (8 + 30 * hype)
        y -= jump; hr = 26 * s
        c = mixc((40, 40, 55), col, depth)
        d.ellipse((x - hr, y - hr, x + hr, y + hr), fill=c)
        d.rounded_rectangle((x - 48 * s, y + hr * 0.7, x + 48 * s, H + 40), int(30 * s), fill=c)
        if arms or hype > 0.5:
            sw = math.sin(t * 6 + ph) * 0.35
            for side in (-1, 1):
                ax = x + side * 40 * s; ang = -math.pi / 2 + side * (0.45 + sw)
                bx, by = ax + math.cos(ang) * 110 * s, y + 20 * s + math.sin(ang) * 110 * s
                d.line((ax, y + 30 * s, bx, by), fill=c, width=int(20 * s))

def flashes(img, t, n=6):
    d = ImageDraw.Draw(img)
    for j in range(n):
        if random.random() < 0.5:
            x, y = random.uniform(30, W - 30), random.uniform(1640, 1780); r = random.uniform(3, 7)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 240))

# ---- scoreboard header ----
def scoreboard(img, rank, t, col):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 60, 70, W - 60, 230
    shadow(img, (x0, y0, x1, y1), 22, 20, 160, (0, 10))
    d.rounded_rectangle((x0, y0, x1, y1), 22, fill=(10, 10, 14), outline=(60, 60, 70), width=3)
    for yy in range(y0 + 8, y1 - 6, 6): d.line((x0 + 10, yy, x1 - 10, yy), fill=(18, 18, 24))
    d.text((x0 + 40, y0 + 46), "OS MAIORES ESTÁDIOS", font=F("os", 38), fill=(255, 190, 60), anchor="lm")
    d.text((x0 + 40, y0 + 104), "DO BRASIL · CAPACIDADE", font=F("mono", 34), fill=(150, 150, 160), anchor="lm")
    bx = x1 - 210; d.rounded_rectangle((bx, y0 + 18, x1 - 22, y1 - 18), 14, fill=col)
    txt = f"#{rank}" if rank else "TOP 10"
    d.text(((bx + x1 - 22) / 2, (y0 + y1) / 2 + 2), txt, font=F("an", 84 if rank else 56), fill=WHITE, anchor="mm")

# ---- ticket ----
TW, TH, PH = 940, 1240, 600
def barcode(d, x, y, w, h, seed):
    rnd = random.Random(seed); xx = x
    while xx < x + w:
        bw = rnd.choice([2, 3, 5, 7]); d.rectangle((xx, y, xx + bw, y + h), fill=(25, 25, 30)); xx += bw + rnd.choice([3, 4, 6])

_tk = {}
def ticket_base(i):
    if i in _tk: return _tk[i]
    r, name, city, fn, cap, col, setor = B[i]
    gold = r == 1
    paper = (246, 236, 205) if gold else (247, 244, 236)
    T = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    base = Image.new("RGB", (TW, TH), paper)
    if gold:
        g = Image.linear_gradient("L").resize((TW, TH)).rotate(30, expand=False)
        base = Image.composite(Image.new("RGB", (TW, TH), (255, 226, 130)), Image.new("RGB", (TW, TH), (214, 160, 40)), g)
    noise = Image.effect_noise((TW // 2, TH // 2), 18).resize((TW, TH)).convert("L")
    base = ImageChops.multiply(base, Image.merge("RGB", [noise.point(lambda v: 235 + v // 12)] * 3))
    ph = cover(photo(fn), TW - 40, PH - 20, 0.5, 0.55)
    ph = ImageEnhance.Contrast(ph).enhance(1.12); ph = ImageEnhance.Color(ph).enhance(1.15)
    base.paste(ph, (20, 20), rounded_mask(ph.width, ph.height, 26))
    d = ImageDraw.Draw(base)
    d.rectangle((20, PH, TW - 20, PH + 14), fill=col)
    # perforation
    py = PH + 70
    for x in range(70, TW - 60, 26): d.ellipse((x, py - 5, x + 10, py + 5), fill=(190, 180, 160) if not gold else (150, 110, 20))
    ink = (25, 24, 30); sub = (110, 105, 95) if not gold else (90, 60, 10)
    d.text((48, PH + 40), f"INGRESSO  ·  Nº {r:02d}", font=F("mono", 30), fill=sub, anchor="lm")
    d.text((TW - 48, PH + 40), f"SETOR {setor}", font=F("mono", 30), fill=sub, anchor="rm")
    f = F("an", 118)
    while d.textlength(name, font=f) > TW - 100: f = F("an", f.size - 6)
    d.text((48, PH + 175), name, font=f, fill=ink, anchor="lm")
    d.text((50, PH + 268), city, font=F("os", 40), fill=col if not gold else (120, 70, 0), anchor="lm")
    d.text((50, PH + 345), "CAPACIDADE", font=F("mono", 32), fill=sub, anchor="lm")
    barcode(d, 48, TH - 95, 520, 62, r)
    d.text((600, TH - 64), f"RKBR-{r:02d}-{cap}", font=F("mono", 30), fill=sub, anchor="lm")
    m = rounded_mask(TW, TH, 34); md = ImageDraw.Draw(m)
    for sx in (-34, TW - 34): md.ellipse((sx, py - 34, sx + 68, py + 34), fill=0)
    T.paste(base, (0, 0), m)
    _tk[i] = T; return T

def counter_digits(T, val, col, glow=0.0):
    d = ImageDraw.Draw(T); s = fmt(int(val))
    f = F("an", 170); x = 48; y = PH + 440
    d.text((x, y), s, font=f, fill=(25, 24, 30), anchor="lm")
    d.text((x + d.textlength(s, font=f) + 18, y + 40), "LUGARES", font=F("os", 44), fill=col, anchor="lm")

def place_ticket(img, T, cx, cy, ang, sc=1.0):
    if sc != 1.0: T = T.resize((int(TW * sc), int(TH * sc)), Image.LANCZOS)
    R = T.rotate(ang, resample=Image.BICUBIC, expand=True)
    a = R.split()[3]; sh = Image.new("L", R.size, 0); sh.paste(a.point(lambda v: v * 0.6), (0, 0))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    x, y = int(cx - R.width / 2), int(cy - R.height / 2)
    img.paste((0, 0, 0), (x + 10, y + 26), sh); img.paste(R, (x, y), R)

def stamp(img, text, cx, cy, u, col=(200, 20, 30), ang=-14, size=86):
    if u <= 0: return
    sc = 1 + 1.4 * (1 - ease(u / 0.35)); al = int(230 * min(1, u / 0.2))
    f = F("an", size); w = int(ImageDraw.Draw(img).textlength(text, font=f)) + 80; h = size + 60
    S = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(S)
    d.rounded_rectangle((6, 6, w - 6, h - 6), 16, outline=col + (al,), width=9)
    d.text((w / 2, h / 2 + 4), text, font=f, fill=col + (al,), anchor="mm")
    S = S.resize((int(w * sc), int(h * sc))).rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(S, (int(cx - S.width / 2), int(cy - S.height / 2)), S)

def frame_item(i, t, D):
    r, name, city, fn, cap, col, setor = B[i]
    k = i + 1; tn = WD.first_num(k) ; gold = r == 1
    img = bgfor(fn).copy()
    img.paste((255, 250, 220), (0, 0), beams(t + i)); lamps(img)
    scoreboard(img, r, t, col)
    # ticket entrance
    u = ease((t - 0.02) / 0.55)
    cy = lerp(H + 700, 960, u); ang = lerp(-18, -2 + 1.2 * math.sin(t * 0.8), u)
    T = ticket_base(i).copy()
    cu = ease((t - tn) / 1.2)
    counter_digits(T, cap * cu, col)
    if gold:
        # shine sweep
        sx = int(((t * 0.45) % 1.6 - 0.3) * TW * 1.6)
        sh = Image.new("L", T.size, 0); ImageDraw.Draw(sh).polygon([(sx, 0), (sx + 120, 0), (sx - 300, TH), (sx - 420, TH)], fill=110)
        sh = ImageChops.multiply(sh.filter(ImageFilter.GaussianBlur(20)), T.split()[3]); T.paste((255, 255, 240), (0, 0), sh)
    # zoom pop when number lands
    pop = 1 + 0.035 * math.exp(-max(0, t - tn - 1.2) * 6) * (1 if t > tn + 1.2 else 0)
    place_ticket(img, T, W / 2, cy, ang, 0.86 * pop)
    if r == 1:
        st = WD.time_of(k, "duzentas", D - 3)
        stamp(img, "RECORDE: ~200 MIL", W / 2 + 60, 690, t - st + 0.25, (200, 20, 30), -10, 78)
    elif r == 5:
        st = WD.time_of(k, "sete", D - 3)
        stamp(img, "7 x 1", W - 240, 650, t - st, (200, 20, 30), 12, 120)
    elif t > tn + 1.25:
        stamp(img, "ESGOTADO", W - 250, 640, t - tn - 1.25, (200, 20, 30), 12, 72)
    crowd(img, t, 1.0 if (gold and t > tn) else 0.15)
    flashes(img, t, 14 if gold else 5)
    WD.caption(img, k, t, 1585)
    fade(img, t, D)
    return img

def fade(img, t, D):
    a = 1 - ease(t / 0.16)
    if a > 0: img.paste((255, 255, 255), (0, 0), Image.new("L", (W, H), int(140 * a)))

def frame_intro(t, D):
    img = bgfor("e01_1.jpg").copy()
    ph = cover(photo("e01_1.jpg"), W, 1100, 0.5, 0.5)
    z = 1.12 - 0.08 * ease(t / D); ph = ph.resize((int(W * z), int(1100 * z)))
    ph = ph.crop(((ph.width - W) // 2, (ph.height - 1100) // 2, (ph.width - W) // 2 + W, (ph.height - 1100) // 2 + 1100))
    ph = ImageEnhance.Brightness(ph).enhance(0.75)
    g = Image.linear_gradient("L").resize((W, 1100))
    m = ImageChops.multiply(g.point(lambda v: min(255, v * 4)), g.rotate(180).point(lambda v: min(255, v * 3)))
    img.paste(ph, (0, 260), m)
    img.paste((255, 250, 220), (0, 0), beams(t)); lamps(img)
    scoreboard(img, 0, t, (200, 20, 30))
    d = ImageDraw.Draw(img)
    for j, (txt, f, c, y) in enumerate([("OS 10 MAIORES", F("an", 140), WHITE, 560), ("ESTÁDIOS", F("an", 230), GOLD, 760), ("DO BRASIL", F("an", 140), WHITE, 960)]):
        u = back((t - 0.1 - j * 0.12) / 0.45)
        if u <= 0: continue
        x = lerp(-600 if j % 2 == 0 else W + 600, W / 2, u)
        d.text((x, y), txt, font=f, fill=c, anchor="mm", stroke_width=10, stroke_fill=BLACK)
    # golden ticket teaser
    u = ease((t - 1.2) / 0.6)
    if u > 0:
        T = ticket_base(9).copy(); d2 = ImageDraw.Draw(T)
        d2.rectangle((20, 20, TW - 20, PH), fill=(30, 26, 20)); d2.text((TW / 2, PH / 2), "?", font=F("an", 420), fill=GOLD, anchor="mm")
        d2.rectangle((40, PH + 120, TW - 40, PH + 300), fill=(238, 200, 100)); d2.text((48, PH + 175), "???", font=F("an", 118), fill=(25, 24, 30), anchor="lm")
        counter_digits(T, 0, (120, 70, 0))
        place_ticket(img, T, W / 2 + 120, lerp(H + 500, 1290, u), lerp(30, 9 + math.sin(t * 2) * 2, u), 0.4)
    crowd(img, t, 0.5); flashes(img, t, 8)
    WD.caption(img, 0, t, 1585)
    return img

def frame_outro(t, D):
    img = bgfor("e01_1.jpg").copy(); img.paste((255, 250, 220), (0, 0), beams(t)); lamps(img)
    scoreboard(img, 0, t, (200, 20, 30)); d = ImageDraw.Draw(img)
    for j in range(10):
        r, name, city, fn, cap, col, setor = B[9 - j]
        u = back((t - j * 0.07) / 0.4)
        if u <= 0: continue
        y = 300 + j * 118; x = lerp(W + 500, 60, u)
        d.rounded_rectangle((x, y, x + W - 120, y + 100), 18, fill=(247, 244, 236) if r > 1 else (240, 200, 90))
        d.rectangle((x, y, x + 16, y + 100), fill=col)
        d.text((x + 44, y + 52), f"{r}", font=F("an", 66), fill=col, anchor="lm")
        d.text((x + 130, y + 52), name, font=F("an", 52), fill=(25, 24, 30), anchor="lm")
        d.text((x + W - 160, y + 52), fmt(cap), font=F("mono", 46), fill=(60, 55, 50), anchor="rm")
    u = back((t - 1.0) / 0.5)
    if u > 0:
        d.text((W / 2, 1540), "SEGUE O RANKEADO BR", font=F("an", int(96 * u)), fill=GOLD, anchor="mm", stroke_width=8, stroke_fill=BLACK)
    crowd(img, t, 0.8); flashes(img, t, 10)
    WD.caption(img, 11, t, 1660)
    if t > D - 1.5:
        d = ImageDraw.Draw(img); d.rectangle((0, 1690, W, H), fill=(8, 8, 12))
        for j, line in enumerate(CRED):
            d.text((W / 2, 1720 + j * 30), line, font=F("mono", 19), fill=(200, 200, 205), anchor="mm")
    return img

meta = json.load(open(FOT + "meta.json"))
CRED = credit_lines(meta, [(b[0], b[3]) for b in B], "Capacidades: Flashscore/CBF. Fotos via Wikimedia Commons / Flickr:",
                    'Trilha: "Hitman" Kevin MacLeod (incompetech.com) · CC BY 4.0')
def scene_fn(k):
    if k == 0: return frame_intro
    if k == 11: return frame_outro
    return lambda t, D, i=k - 1: frame_item(i, t, D)

if __name__ == "__main__":
    main(scene_fn, D6 + "durs.json", 12, "s6", lambda d: [(0, 2.5), (1, d[1] - 0.3), (6, d[6] - 0.5), (10, d[10] - 0.5), (11, d[11] - 0.5)])
