import sys, json, subprocess, os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

W, H, FPS = 1080, 1920, 30
FD = "/home/claude/fonts/"
_fc = {}
def F(kind, sz):
    sz = max(8, int(sz)); k = (kind, sz)
    if k in _fc: return _fc[k]
    if kind == "pf": f = ImageFont.truetype(FD + "PlayfairDisplay[wght].ttf", sz); f.set_variation_by_name("Black")
    elif kind == "an": f = ImageFont.truetype(FD + "Anton-Regular.ttf", sz)
    elif kind == "mono": f = ImageFont.truetype(FD + "ShareTechMono-Regular.ttf", sz)
    elif kind == "os": f = ImageFont.truetype(FD + "Oswald[wght].ttf", sz); f.set_variation_by_name("SemiBold")
    elif kind == "osb": f = ImageFont.truetype(FD + "Oswald[wght].ttf", sz); f.set_variation_by_name("Bold")
    _fc[k] = f; return f

NAVY = (22, 36, 78); INKB = (28, 44, 96); RED = (200, 28, 40); GOLD = (214, 168, 64); WHITE = (255, 255, 255); BLACK = (0, 0, 0)
PAGE = (236, 240, 229)
FOT = "/home/claude/rk4/fotos/"
BR = 12397
# rank, name, iso, photo, fx, value, trigger, fact, stamp color
B = [
 (10, "HOLANDA", "NLD", "p10_1.jpg", 0.5, 78535, "78", "canais, bicicletas e flores", (40, 90, 170)),
 (9, "DINAMARCA", "DNK", "p09_0.jpg", 0.5, 82714, "82", "a terra do Lego", (170, 30, 50)),
 (8, "ESTADOS UNIDOS", "USA", "p08_1.jpg", 0.5, 95212, "95", "a maior economia do mundo", (30, 60, 140)),
 (7, "ISLÂNDIA", "ISL", "p07_0.jpg", 0.5, 107464, "107", "gelo, vulcões e auroras", (20, 110, 120)),
 (6, "SINGAPURA", "SGP", "p06_0.jpg", 0.5, 109117, "109", "menor que a cidade de SP", (180, 40, 60)),
 (5, "NORUEGA", "NOR", "p05_2.jpg", 0.5, 115188, "115", "turbinada pelo petróleo", (120, 30, 90)),
 (4, "SUÍÇA", "CHE", "p04_0.jpg", 0.5, 124478, "124", "bancos, relógios e chocolate", (190, 30, 40)),
 (3, "IRLANDA", "IRL", "p03_0.jpg", 0.5, 127837, "127", "sede de gigantes da tecnologia", (20, 120, 60)),
 (2, "LUXEMBURGO", "LUX", "p02_0.jpg", 0.5, 155733, "155", "menor que o Distrito Federal", (40, 120, 190)),
 (1, "LIECHTENSTEIN", "LIE", "p01_w2.jpg", 0.5, 230417, "230", "~40 mil habitantes", (170, 120, 20)),
]
FIX = {"DÉSIMO": "DÉCIMO", "SESTO": "SEXTO", "R $ 109": "109", "PAIZINHO": "PAISINHO", "OS 12": "12", "RANQUEI": "RANKEEI"}
WORDS = json.load(open("/home/claude/rk4/words.json"))

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def dots(n): return f"{int(n):,}".replace(",", ".")
def word_time(k, key, default):
    for w in WORDS[k]:
        if w["w"].strip(".,") == key or key.lower() in w["w"].lower(): return w["t0"]
    return default

# ---------- flags ----------
def flag(iso, w, h):
    im = Image.new("RGB", (w, h), WHITE); d = ImageDraw.Draw(im)
    def hstripes(cols):
        for j, c in enumerate(cols): d.rectangle([0, h * j / len(cols), w, h * (j + 1) / len(cols)], fill=c)
    def vstripes(cols):
        for j, c in enumerate(cols): d.rectangle([w * j / len(cols), 0, w * (j + 1) / len(cols), h], fill=c)
    def nordic(bg, outer, inner=None):
        d.rectangle([0, 0, w, h], fill=bg); cx = w * 0.36; t = h * 0.22
        d.rectangle([cx - t / 2, 0, cx + t / 2, h], fill=outer); d.rectangle([0, h / 2 - t / 2, w, h / 2 + t / 2], fill=outer)
        if inner:
            t2 = t * 0.5; d.rectangle([cx - t2 / 2, 0, cx + t2 / 2, h], fill=inner); d.rectangle([0, h / 2 - t2 / 2, w, h / 2 + t2 / 2], fill=inner)
    if iso == "NLD": hstripes([(174, 28, 40), WHITE, (33, 70, 139)])
    elif iso == "LUX": hstripes([(237, 41, 57), WHITE, (0, 161, 222)])
    elif iso == "IRL": vstripes([(22, 155, 98), WHITE, (255, 136, 62)])
    elif iso == "DNK": nordic((200, 16, 46), WHITE)
    elif iso == "NOR": nordic((186, 12, 47), WHITE, (0, 32, 91))
    elif iso == "ISL": nordic((2, 82, 156), WHITE, (220, 30, 53))
    elif iso == "CHE":
        d.rectangle([0, 0, w, h], fill=(218, 41, 28)); s = h * 0.6; t = s * 0.32
        d.rectangle([w / 2 - t / 2, h / 2 - s / 2, w / 2 + t / 2, h / 2 + s / 2], fill=WHITE); d.rectangle([w / 2 - s / 2, h / 2 - t / 2, w / 2 + s / 2, h / 2 + t / 2], fill=WHITE)
    elif iso == "SGP":
        hstripes([(239, 51, 64), WHITE]); r = h * 0.17; cx, cy = w * 0.2, h * 0.25
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE); d.ellipse([cx - r + r * 0.35, cy - r, cx + r + r * 0.35, cy + r], fill=(239, 51, 64))
        for a in range(5):
            ang = -math.pi / 2 + a * 2 * math.pi / 5; sx, sy = w * 0.31 + r * 0.6 * math.cos(ang), cy + r * 0.6 * math.sin(ang)
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=WHITE)
    elif iso == "USA":
        for j in range(13): d.rectangle([0, h * j / 13, w, h * (j + 1) / 13], fill=(178, 34, 52) if j % 2 == 0 else WHITE)
        cw, ch = w * 0.4, h * 7 / 13; d.rectangle([0, 0, cw, ch], fill=(60, 59, 110))
        for yy in range(5):
            for xx in range(6): d.ellipse([cw * (xx + 0.5) / 6 - 2, ch * (yy + 0.5) / 5 - 2, cw * (xx + 0.5) / 6 + 2, ch * (yy + 0.5) / 5 + 2], fill=WHITE)
    elif iso == "LIE":
        hstripes([(0, 43, 127), (206, 17, 38)]); cx, cy = w * 0.25, h * 0.25
        d.rectangle([cx - 14, cy, cx + 14, cy + 8], fill=(255, 210, 0))
        d.polygon([(cx - 14, cy), (cx - 10, cy - 14), (cx - 4, cy - 4), (cx, cy - 18), (cx + 4, cy - 4), (cx + 10, cy - 14), (cx + 14, cy)], fill=(255, 210, 0))
    elif iso == "BRA":
        d.rectangle([0, 0, w, h], fill=(0, 156, 59)); d.polygon([(w * 0.08, h / 2), (w / 2, h * 0.1), (w * 0.92, h / 2), (w / 2, h * 0.9)], fill=(255, 223, 0))
        r = h * 0.24; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(0, 39, 118))
    ImageDraw.Draw(im).rectangle([0, 0, w - 1, h - 1], outline=(0, 0, 0), width=1)
    return im

# ---------- passport page ----------
def make_page():
    im = Image.new("RGB", (W, H), PAGE); d = ImageDraw.Draw(im)
    for j in range(0, H + 200, 26):
        pts = [(x, j + 14 * math.sin(x / 70 + j / 90) + 6 * math.sin(x / 23)) for x in range(0, W + 10, 10)]
        d.line(pts, fill=(214, 226, 214), width=2)
    for j in range(0, H + 200, 52):
        pts = [(x, j + 20 * math.sin(x / 110 - j / 60)) for x in range(0, W + 10, 10)]
        d.line(pts, fill=(222, 214, 232), width=2)
    # watermark globe
    cx, cy, r = W / 2, 1000, 380
    for k in range(7):
        rx = r * math.cos(k * math.pi / 14); d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=(220, 228, 220), width=3)
    for k in range(-3, 4):
        yy = cy + r * k / 4; xx = math.sqrt(max(0, r * r - (yy - cy) ** 2)); d.line([(cx - xx, yy), (cx + xx, yy)], fill=(220, 228, 220), width=3)
    n = Image.effect_noise((W, H), 18).convert("RGB")
    im = Image.blend(im, ImageChops.multiply(im, n.point(lambda v: 200 + v // 5)), 0.35)
    d = ImageDraw.Draw(im)
    # perforated page number on right edge
    d.text((60, 70), "REPÚBLICA DO RANKEADO", font=F("os", 30), fill=NAVY)
    d.text((60, 108), "PASSAPORTE · PASSPORT", font=F("mono", 24), fill=(90, 100, 130))
    d.line([(60, 150), (W - 60, 150)], fill=(150, 160, 185), width=2)
    return im
PAGEIM = None

def holo_frame(w, h, t):
    fr = Image.new("RGB", (w, h)); d = ImageDraw.Draw(fr)
    for x in range(w):
        hue = (x / w + t * 0.15) % 1.0
        r = int(200 + 55 * math.sin(6.28 * hue)); g = int(200 + 55 * math.sin(6.28 * hue + 2.1)); b = int(200 + 55 * math.sin(6.28 * hue + 4.2))
        d.line([(x, 0), (x, h)], fill=(r, g, b))
    return fr

PW, PH = 920, 580
_ph = {}
def photo(i):
    if i not in _ph:
        im = Image.open(FOT + B[i][3]).convert("RGB")
        im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.08)
        ar = PW / PH
        if im.width / im.height > ar:
            nw = int(im.height * ar); cx = int(im.width * B[i][4]); x0 = max(0, min(im.width - nw, cx - nw // 2)); im = im.crop((x0, 0, x0 + nw, im.height))
        else:
            nh = int(im.width / ar); y0 = (im.height - nh) // 2; im = im.crop((0, y0, im.width, y0 + nh))
        _ph[i] = im.resize((int(PW * 1.15), int(PH * 1.15)), Image.LANCZOS)
    return _ph[i]

def visa(i, t, D):
    src = photo(i); z = 1 + 0.13 * min(1, t / D)
    cw, ch = src.width / z, src.height / z; sx, sy = (src.width - cw) / 2, (src.height - ch) / 2
    ph = src.resize((PW, PH), Image.BILINEAR, box=(sx, sy, sx + cw, sy + ch))
    v = holo_frame(PW + 28, PH + 28, t); v.paste(ph, (14, 14))
    return v

def paste_rot(img, part, ang, cx, cy, shadow=12):
    p = part.convert("RGBA").rotate(ang, resample=Image.BICUBIC, expand=True)
    if shadow:
        a = p.split()[3].point(lambda v: int(v * 0.45)).filter(ImageFilter.GaussianBlur(shadow))
        img.paste((40, 40, 50), (int(cx - p.width / 2 + 8), int(cy - p.height / 2 + 14)), a)
    img.paste(p, (int(cx - p.width / 2), int(cy - p.height / 2)), p)

def stamp_img(i, big=False):
    r, name, iso, _, _, val, _, _, col = B[i]
    w, h = (560, 330) if big else (470, 280)
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    c = col + (255,)
    d.rounded_rectangle([8, 8, w - 8, h - 8], 60, outline=c, width=9)
    d.rounded_rectangle([24, 24, w - 24, h - 24], 48, outline=c, width=3)
    nf = F("osb", 70 if big else 60)
    while d.textlength(name, font=nf) > w - 90: nf = F("osb", nf.size - 4)
    d.text((w / 2, h * 0.40), name, font=nf, fill=c, anchor="mm")
    d.text((w / 2, h * 0.66), f"ENTRADA · #{r:02d} · {iso}", font=F("mono", 30 if big else 26), fill=c, anchor="mm")
    d.text((w / 2, h * 0.83), "★ RANKEADO BR ★", font=F("mono", 22), fill=c, anchor="mm")
    n = Image.effect_noise((w, h), 70).point(lambda v: 255 if v > 90 else 90)
    s.putalpha(ImageChops.multiply(s.split()[3], n))
    return s
_st = {}
def stamp(i, big=False):
    if (i, big) not in _st: _st[(i, big)] = stamp_img(i, big)
    return _st[(i, big)]

def groups_for(k):
    gs = []; buf = None
    for w in WORDS[k]:
        txt = w["w"].upper().strip(".,!?")
        if (txt.startswith("-") or txt.startswith(",")) and gs: gs[-1]["txt"] += txt; gs[-1]["t1"] = w["t1"]; continue
        if buf is not None: g = {"txt": (buf["txt"] + " " + txt).strip(), "t0": buf["t0"], "t1": w["t1"]}; buf = None
        else: g = {"txt": txt, "t0": w["t0"], "t1": w["t1"]}
        orig = w["w"].strip(".,!?")
        if len(g["txt"]) <= 2 and not any(c.isdigit() for c in g["txt"]) and not (orig.isupper() and len(orig) >= 2): buf = g; continue
        gs.append(g)
    for g in gs: g["txt"] = FIX.get(g["txt"], g["txt"])
    return gs
GROUPS = [groups_for(k) for k in range(12)]
def caption(img, k, t, y=1640):
    d = ImageDraw.Draw(img); cur = None
    for g in GROUPS[k]:
        if g["t0"] - 0.05 <= t: cur = g
    if cur is None or t > cur["t1"] + 0.5: return
    a = (t - cur["t0"] + 0.05) / 0.12; sz = 100 * (1 + 0.22 * (1 - ease(a)))
    f = F("an", sz)
    while d.textlength(cur["txt"], font=f) > W - 90 and sz > 50: sz -= 6; f = F("an", sz)
    num = any(c.isdigit() for c in cur["txt"])
    d.text((W / 2, y), cur["txt"], font=f, fill=(255, 214, 90) if num else WHITE, anchor="mm", stroke_width=10, stroke_fill=NAVY)

def mrz(d, i):
    r, name, iso = B[i][0], B[i][1], B[i][2]
    nm = name.replace(" ", "<").replace("Ç", "C").replace("Í", "I").replace("Â", "A")
    l1 = ("P<" + iso + "RANKEADO<<" + nm + "<" * 44)[:44]
    l2 = (f"{r:02d}TOP10<" + iso + f"{int(B[i][5])}<<PIB<PER<CAPITA<FMI<2026" + "<" * 44)[:44]
    d.text((W / 2, 1808), l1, font=F("mono", 34), fill=(70, 80, 110), anchor="mm")
    d.text((W / 2, 1850), l2, font=F("mono", 34), fill=(70, 80, 110), anchor="mm")

def frame_item(i, t, D):
    k = i + 1; r, name, iso, _, _, val, trig, fact, col = B[i]
    img = PAGEIM.copy(); d = ImageDraw.Draw(img)
    d.text((W - 60, 88), f"PÁG. {k:02d}/10", font=F("mono", 28), fill=(90, 100, 130), anchor="ra")
    # visa photo drops in
    a = back(t / 0.45)
    ang = (-1.6 if i % 2 else 1.4)
    if t > 0.02:
        v = visa(i, t, D)
        sc = 0.6 + 0.4 * a
        v2 = v.resize((max(10, int(v.width * sc)), max(10, int(v.height * sc))))
        paste_rot(img, v2, ang + (1 - a) * 10, W / 2, 530)
    # flag sticker
    af = back((t - 0.25) / 0.35)
    if af > 0:
        fl = flag(iso, int(210 * af) + 1, int(140 * af) + 1)
        bd = Image.new("RGB", (fl.width + 16, fl.height + 16), WHITE); bd.paste(fl, (8, 8))
        paste_rot(img, bd, -6, 175, 840, shadow=8)
    d = ImageDraw.Draw(img)
    # header block
    an = ease((t - 0.3) / 0.35); off = int(30 * (1 - an))
    if an > 0:
        d.text((300, 900 + off), f"VISTO Nº {r:02d}", font=F("mono", 34), fill=RED)
        nf = F("an", 112)
        while d.textlength(name, font=nf) > W - 360: nf = F("an", nf.size - 6)
        d.text((300, 940 + off), name, font=nf, fill=NAVY)
        d.text((300, 940 + off + nf.size + 18), fact.upper(), font=F("os", 32), fill=(90, 100, 130))
    # value typed
    tn = word_time(k, trig, D * 0.5) + 0.12
    vy = 1240
    d.text((60, vy), "PIB POR PESSOA (FMI 2026) ......", font=F("mono", 36), fill=(90, 100, 130))
    full = "US$ " + dots(val)
    if t > tn - 0.15:
        nchar = min(len(full), int((t - (tn - 0.15)) / 0.05) + 1)
        txt = full[:nchar]
        d.text((60, vy + 50), txt, font=F("an", 150), fill=INKB)
        if nchar < len(full) and int(t * 6) % 2 == 0:
            tw = d.textlength(txt, font=F("an", 150)); d.rectangle([60 + tw + 6, vy + 80, 60 + tw + 20, vy + 220], fill=INKB)
    # stamp slam
    ts = tn + 0.15 + 0.05 * len(full)
    if t > ts:
        u = (t - ts) / 0.16; sc = 1 + 1.6 * (1 - ease(u))
        st = stamp(i, big=(r == 1))
        st2 = st.resize((int(st.width * sc), int(st.height * sc)), Image.BILINEAR)
        al = st2.split()[3].point(lambda v: int(v * min(1, u * 2)))
        st2.putalpha(al)
        st2 = st2.rotate(-12 if i % 2 else 9, resample=Image.BICUBIC, expand=True)
        img.paste(st2, (int(W - 270 - st2.width / 2), int(760 - st2.height / 2)), st2)
        d = ImageDraw.Draw(img)
        ratio = val / BR
        if t > ts + 0.45:
            ab = back((t - ts - 0.45) / 0.3)
            s = ("≈ %.1fX O BRASIL" % ratio).replace(".", ",")
            f = F("an", 58 * max(0.3, ab)); tw = d.textlength(s, font=f)
            fl = flag("BRA", 72, 50)
            x0 = 60; y0 = 1470
            d.rounded_rectangle([x0, y0, x0 + tw + 130, y0 + 86], 18, fill=RED)
            img.paste(fl, (x0 + 18, y0 + 18)); d.text((x0 + 106, y0 + 43), s, font=f, fill=WHITE, anchor="lm")
    caption(img, k, t - 0.12)
    mrz(ImageDraw.Draw(img), i)
    # page slide-in
    ps = ease(t / 0.38)
    if ps < 1:
        bg = Image.new("RGB", (W, H), NAVY)
        x = int(W * (1 - ps))
        bg.paste(img.crop((0, 0, W - x, H)), (x, 0))
        bd = ImageDraw.Draw(bg)
        for j in range(40): bd.line([(x - j, 0), (x - j, H)], fill=tuple(int(c * (0.5 + 0.5 * j / 40)) for c in NAVY))
        img = bg
    # shake on stamp
    if 0 <= t - ts < 0.22:
        amp = (22 if r == 1 else 10) * (1 - (t - ts) / 0.22)
        img = img.transform((W, H), Image.AFFINE, (1, 0, random.uniform(-amp, amp), 0, 1, random.uniform(-amp, amp)), fillcolor=NAVY)
    return img

def cover():
    im = Image.new("RGB", (W, H), NAVY)
    n = Image.effect_noise((W, H), 40).convert("RGB")
    im = Image.blend(im, ImageChops.multiply(im, n.point(lambda v: 170 + v // 3)), 0.5)
    d = ImageDraw.Draw(im)
    d.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=3)
    cx, cy, r = W / 2, 1180, 230
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=6)
    for kk in range(5):
        rx = r * math.cos(kk * math.pi / 10); d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=GOLD, width=3)
    for kk in (-2, -1, 0, 1, 2):
        yy = cy + r * kk / 3; xx = math.sqrt(max(0, r * r - (yy - cy) ** 2)); d.line([(cx - xx, yy), (cx + xx, yy)], fill=GOLD, width=3)
    d.text((W / 2, 1490), "PASSAPORTE", font=F("pf", 78), fill=GOLD, anchor="mm")
    d.text((W / 2, 1570), "RANKEADO BR", font=F("os", 38), fill=GOLD, anchor="mm")
    return im
COVER = None

def frame_intro(t, D):
    img = COVER.copy(); d = ImageDraw.Draw(img)
    a = back(t / 0.4)
    d.text((W / 2, 200), "RANKEEI OS 10", font=F("os", 64), fill=WHITE, anchor="mm")
    d.text((W / 2, 380), "PAÍSES", font=F("an", 230 * max(0.3, a)), fill=(255, 214, 90), anchor="mm")
    d.text((W / 2, 560), "MAIS RICOS DO MUNDO", font=F("an", 96), fill=WHITE, anchor="mm")
    d.text((W / 2, 660), "PIB por pessoa · FMI 2026", font=F("mono", 40), fill=(190, 200, 230), anchor="mm")
    # flags fan (no #1 flag)
    for j, iso in enumerate(["NLD", "DNK", "USA", "ISL", "SGP", "NOR", "CHE", "IRL", "LUX"]):
        u = ease((t - 0.2 - j * 0.07) / 0.3)
        if u <= 0: continue
        fl = flag(iso, 150, 100); bd = Image.new("RGB", (166, 116), WHITE); bd.paste(fl, (8, 8))
        x = 130 + (j % 5) * 205 + (100 if j >= 5 else 0); y = 820 if j < 5 else 960
        paste_rot(img, bd, (j % 3 - 1) * 8, x, y + (1 - u) * 300, shadow=6)
    tn = word_time(0, "número", 2.5)
    if t > tn:
        u = (t - tn) / 0.16; sc = 1 + 1.4 * (1 - ease(u))
        s = Image.new("RGBA", (900, 230), (0, 0, 0, 0)); sd = ImageDraw.Draw(s)
        sd.rounded_rectangle([8, 8, 892, 222], 40, outline=RED + (255,), width=10)
        sd.text((450, 80), "O Nº 1 VOCÊ TALVEZ", font=F("an", 74), fill=RED + (255,), anchor="mm")
        sd.text((450, 160), "NEM SAIBA ONDE FICA", font=F("an", 74), fill=RED + (255,), anchor="mm")
        n = Image.effect_noise((900, 230), 70).point(lambda v: 255 if v > 90 else 110)
        s.putalpha(ImageChops.multiply(s.split()[3], n).point(lambda v: int(v * min(1, u * 2))))
        s = s.resize((int(900 * sc), int(230 * sc))).rotate(-6, resample=Image.BICUBIC, expand=True)
        bgw = Image.new("RGBA", s.size, (255, 255, 255, 0))
        img.paste(s, (int(W / 2 - s.width / 2), int(1720 - s.height / 2)), s)
    return img

CRED = None
def frame_outro(t, D):
    img = PAGEIM.copy(); d = ImageDraw.Draw(img)
    random.seed(5)
    pos = [(250, 330), (760, 300), (300, 560), (800, 560), (230, 800), (760, 820), (330, 1360), (790, 1370), (260, 1600), (780, 1610)]
    for j in range(10):
        i = 9 - j; u = (t - j * 0.12) / 0.15
        if u <= 0: continue
        sc = (1 + 1.2 * (1 - ease(u))) * 0.8
        st = stamp(i, big=(i == 9)); st2 = st.resize((int(st.width * sc), int(st.height * sc)))
        st2 = st2.rotate(random.uniform(-18, 18), resample=Image.BICUBIC, expand=True)
        img.paste(st2, (int(pos[j][0] - st2.width / 2), int(pos[j][1] - st2.height / 2)), st2)
    d = ImageDraw.Draw(img)
    if t > 0.6:
        a = back((t - 0.6) / 0.35)
        d.rounded_rectangle([60, 960, W - 60, 1270], 26, fill=NAVY)
        d.text((W / 2, 1040), "QUAL PAÍS VOCÊ", font=F("an", 84), fill=WHITE, anchor="mm")
        d.text((W / 2, 1150), "QUER CARIMBAR?", font=F("an", 104 * max(0.3, a)), fill=(255, 214, 90), anchor="mm")
        d.text((W / 2, 1235), "comenta aí", font=F("os", 36), fill=(200, 210, 235), anchor="mm")
    if t > 1.3:
        d.rounded_rectangle([170, 1290, W - 170, 1370], 40, fill=RED)
        d.text((W / 2, 1330), "SEGUE O @RANKEADOBR", font=F("an", 48), fill=WHITE, anchor="mm")
    if t > D - 2.6:
        d.rectangle([0, 1690, W, H], fill=BLACK); y = 1702
        for line in CRED: d.text((30, y), line, font=F("os", 17), fill=(200, 200, 210)); y += 21
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
        random.seed(k * 10000 + i); p.stdin.write(fn(i / FPS, D).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, out)

def lic(m):
    l = m["license"].upper(); v = m.get("lv") or ""
    return "CC0" if l in ("CC0", "PDM") else f"CC {l} {v}".strip()
def credits():
    meta = json.load(open(FOT + "meta.json")); parts = []
    for b in B:
        m = meta[b[3]]; parts.append(f"#{b[0]} {m.get('creator') or 'autor desconhecido'} ({lic(m)})")
    lines, cur = ["Dados: FMI, World Economic Outlook (out/2026), PIB per capita nominal. Fotos via Flickr:"], ""
    for p_ in parts:
        if len(cur) + len(p_) > 110: lines.append(cur); cur = ""
        cur += ("  ·  " if cur else "") + p_
    lines.append(cur); lines.append('Trilha: "Pamgaea" Kevin MacLeod (incompetech.com) · CC BY 4.0')
    return lines

def times():
    out = []
    for i in range(10):
        k = i + 1; tn = word_time(k, B[i][6], 3) + 0.12; full = "US$ " + dots(B[i][5])
        out.append({"type0": tn - 0.15, "nchar": len(full), "stamp": tn + 0.15 + 0.05 * len(full)})
    return out

if __name__ == "__main__":
    PAGEIM = make_page(); COVER = cover(); CRED = credits()
    mode = sys.argv[1]; durs = json.load(open(sys.argv[2]))
    if mode == "stills":
        for k, t in [(0, 0.5), (0, durs[0] - 0.3), (4, 0.2), (4, durs[4] - 0.3), (10, durs[10] - 0.3), (11, durs[11] - 1)]:
            random.seed(1); scene_fn(k)(t, durs[k]).convert("RGB").save(f"s7_{k}_{round(t,1)}.png")
    elif mode == "times":
        json.dump(times(), open("times.json", "w")); print("ok")
    else:
        for k in [int(x) for x in sys.argv[3:]] or range(12):
            render_scene(k, durs[k], f"s7_{k:02d}.mp4")
