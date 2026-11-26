import sys, json, random, math
sys.path.insert(0, "/home/claude"); from rkcommon import *

D9 = "/home/claude/rk9/"; FOT = D9 + "fotos/"
WD = Words(D9, {"RANKEEI": "RANKEEI", "ONU": "ONU"})
# rank, cidade, país, foto, pop (mi), chip, fx, fy
B = [
 (10, "SEUL", "COREIA DO SUL", "c10_1.jpg", 22.5, "", 0.5, 0.5),
 (9, "CALCUTÁ", "ÍNDIA", "c09_1.jpg", 22.6, "", 0.5, 0.5),
 (8, "MANILA", "FILIPINAS", "c08_0.jpg", 24.7, "", 0.5, 0.5),
 (7, "CAIRO", "EGITO", "c07_2.jpg", 25.6, "ÚNICA FORA DA ÁSIA", 0.5, 0.5),
 (6, "GUANGZHOU", "CHINA", "c06_1.jpg", 27.6, "", 0.5, 0.5),
 (5, "XANGAI", "CHINA", "c05_0.jpg", 29.6, "", 0.5, 0.5),
 (4, "NOVA DÉLHI", "ÍNDIA", "c04_1.jpg", 30.2, "", 0.5, 0.6),
 (3, "TÓQUIO", "JAPÃO", "c03_2.jpg", 33.4, "JÁ FOI A Nº 1", 0.5, 0.5),
 (2, "DACA", "BANGLADESH", "c02_1.jpg", 36.6, "PODE SER A Nº 1 EM 2050", 0.5, 0.5),
 (1, "JACARTA", "INDONÉSIA", "c01_1.jpg", 41.9, "MAIS DE 2x A GRANDE SP", 0.5, 0.5),
]
NAVY = (18, 32, 66); PAPER = (244, 240, 230); RED = (228, 0, 43); GREEN = (0, 166, 80)
LINES = [(228, 0, 43), (0, 114, 206), (255, 184, 28), (0, 166, 80), (150, 80, 190), (255, 120, 0)]
def pfmt(v): return f"{v:.1f}".replace(".", ",")
def lcol(i): return GREEN if B[i][1] == "CAIRO" else RED
_ph = {}
def photo(n):
    if n not in _ph: _ph[n] = Image.open(FOT + n).convert("RGB")
    return _ph[n]

# ---------- transit-map paper ----------
def make_map():
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(234, 229, 216))
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(234, 229, 216))
    rnd = random.Random(4)
    for j, c in enumerate(LINES * 2):
        x, y = rnd.randint(-100, W + 100), rnd.choice([-50, H + 50]); pts = [(x, y)]
        for s in range(6):
            dx, dy = rnd.choice([(1, 0), (0, 1), (1, 1), (-1, 1), (0, -1), (1, -1)])
            if y > H / 2 and dy > 0: dy = -dy
            L = rnd.randint(150, 450); x += dx * L; y += dy * L; pts.append((x, y))
        cc = mixc(c, PAPER, 0.72); d.line(pts, fill=cc, width=26, joint="curve")
        for p in pts[1:-1]: d.ellipse((p[0] - 20, p[1] - 20, p[0] + 20, p[1] + 20), fill=PAPER, outline=cc, width=7)
    return img
MAP = make_map()

def header(img):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 200), fill=NAVY)
    d.ellipse((50, 50, 150, 150), fill=WHITE); d.text((100, 102), "M", font=F("an", 70), fill=NAVY, anchor="mm")
    d.text((180, 78), "LINHA MEGACIDADES", font=F("osb", 52), fill=WHITE, anchor="lm")
    d.text((182, 140), "AS MAIS POPULOSAS DO MUNDO · ONU 2025", font=F("os", 30), fill=(170, 185, 215), anchor="lm")

SX0, SX1, SY = 90, W - 90, 290
def sx(j): return SX0 + j * (SX1 - SX0) / 9
def strip(img, cur, t):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((30, 225, W - 30, 365), 24, fill=WHITE, outline=(210, 205, 195), width=2)
    d.line((sx(0), SY, sx(9), SY), fill=(200, 195, 185), width=14)
    if cur >= 0: d.line((sx(0), SY, sx(cur), SY), fill=RED, width=14)
    for j in range(10):
        c = lcol(j) if j <= cur else (190, 185, 175); r = 17 if j != cur else 24
        d.ellipse((sx(j) - r, SY - r, sx(j) + r, SY + r), fill=WHITE, outline=c, width=7)
        d.text((sx(j), SY + 48), str(B[j][0]), font=F("osb", 28), fill=NAVY if j <= cur else (170, 165, 155), anchor="mm")
    if cur >= 0:
        u = ease2((t - 0.05) / 0.7); x = lerp(sx(max(0, cur - 1)), sx(cur), u if cur > 0 else 1)
        d.rounded_rectangle((x - 46, SY - 62, x + 46, SY - 28), 14, fill=NAVY)
        for k in range(3): d.rectangle((x - 34 + k * 26, SY - 54, x - 16 + k * 26, SY - 40), fill=(150, 200, 255))

def poster(img, i, t, D):
    r = B[i]; x0, y0, w, h = 50, 400, W - 100, 700
    u = ease((t - 0.1) / 0.5)
    yy = y0 + (1 - u) * 80
    shadow(img, (x0, yy, x0 + w, yy + h), 26, 22, 110, (0, 14))
    ImageDraw.Draw(img).rounded_rectangle((x0, yy, x0 + w, yy + h), 26, fill=WHITE)
    z = 1.08 - 0.06 * (t / D)
    ph = cover(photo(r[3]), int((w - 28) * z), int((h - 28) * z), r[6], r[7])
    ph = ph.crop((int((ph.width - w + 28) * 0.5), int((ph.height - h + 28) * 0.5), int((ph.width - w + 28) * 0.5) + w - 28, int((ph.height - h + 28) * 0.5) + h - 28))
    ph = ImageEnhance.Contrast(ph).enhance(1.1); ph = ImageEnhance.Color(ph).enhance(1.15)
    img.paste(ph, (x0 + 14, int(yy) + 14), rounded_mask(ph.width, ph.height, 16))
    if u < 1: img.paste(PAPER, (0, 0), Image.new("L", (W, H), 0))

def sign(img, i, t):
    r = B[i]; d = ImageDraw.Draw(img); u = back((t - 0.3) / 0.45)
    if u <= 0: return
    y0 = 1135; x1 = max(300, lerp(-W, W - 50, min(1, u)))
    d.rounded_rectangle((50, y0, x1, y0 + 150), 20, fill=NAVY)
    c = lcol(i); d.ellipse((80, y0 + 25, 180, y0 + 125), fill=c)
    d.text((130, y0 + 78), str(r[0]), font=F("an", 64), fill=WHITE, anchor="mm")
    f = F("osb", 84)
    while d.textlength(r[1], font=f) > 620: f = F("osb", f.size - 4)
    d.text((215, y0 + 58), r[1], font=f, fill=WHITE, anchor="lm")
    d.text((218, y0 + 120), r[2], font=F("os", 32), fill=(170, 185, 215), anchor="lm")
    d.line((x1 - 210, y0 + 30, x1 - 210, y0 + 120), fill=(60, 80, 120), width=2)
    d.text((x1 - 120, y0 + 52), "ESTAÇÃO", font=F("os", 26), fill=(170, 185, 215), anchor="mm")
    d.text((x1 - 120, y0 + 100), f"Nº {r[0]:02d}", font=F("osb", 44), fill=WHITE, anchor="mm")

def person(d, x, y, s, fill, outline=None):
    d.ellipse((x - 0.22 * s, y, x + 0.22 * s, y + 0.44 * s), fill=fill, outline=outline, width=2)
    d.rounded_rectangle((x - 0.34 * s, y + 0.5 * s, x + 0.34 * s, y + 1.15 * s), int(0.25 * s), fill=fill, outline=outline, width=2)

def crowd_grid(img, i, val, col):
    d = ImageDraw.Draw(img); s = 40; cols = 15; gx = (W - cols * 62) / 2 + 31; gy = 1430
    for n in range(45):
        x = gx + (n % cols) * 62; y = gy + (n // cols) * 62
        if val >= n + 1: person(d, x, y, s, col)
        elif val > n:
            person(d, x, y, s, (215, 210, 200))
            fr = val - n; m = Image.new("L", (W, H), 0); md = ImageDraw.Draw(m); person(md, x, y, s, 255)
            cl = Image.new("L", (W, H), 0); ImageDraw.Draw(cl).rectangle((x - s, y - 5, x - 0.34 * s + 0.68 * s * fr, y + s * 1.3), fill=255)
            img.paste(col, (0, 0), ImageChops.multiply(m, cl)); d = ImageDraw.Draw(img)
        else: person(d, x, y, s, (225, 220, 210))
    d.text((W - 60, gy + 3 * 62 + 4), "CADA ÍCONE = 1 MILHÃO", font=F("os", 24), fill=(140, 135, 125), anchor="rm")

def frame_item(i, t, D):
    r = B[i]; k = i + 1; tn = WD.first_num(k)
    img = MAP.copy(); header(img); strip(img, i, t)
    poster(img, i, t, D); sign(img, i, t)
    d = ImageDraw.Draw(img); col = lcol(i)
    nu = ease((t - tn) / 1.1); v = r[4] * nu
    # big number over poster bottom-left
    if t > tn - 0.05:
        txt = pfmt(v); f = F("an", 190)
        bx, by = 80, 1060
        tw = d.textlength(txt, font=f)
        d.rounded_rectangle((60, by - 200, 60 + tw + 300, by + 20), 22, fill=(255, 255, 255))
        d.text((bx, by - 90), txt, font=f, fill=col, anchor="lm")
        d.text((bx + tw + 20, by - 120), "MILHÕES", font=F("osb", 54), fill=NAVY, anchor="lm")
        d.text((bx + tw + 22, by - 62), "DE PESSOAS", font=F("os", 34), fill=(120, 120, 130), anchor="lm")
    if r[5] and nu >= 1:
        cu = back((t - tn - 1.1) / 0.45); f = F("osb", 38); cw = d.textlength(r[5], font=f) + 60
        if cu > 0:
            cx = W - 70 - cw / 2; cy = 470
            S = Image.new("RGBA", (int(cw), 70), (0, 0, 0, 0)); sd = ImageDraw.Draw(S)
            sd.rounded_rectangle((0, 0, cw - 1, 69), 35, fill=(255, 205, 0)); sd.text((cw / 2, 36), r[5], font=f, fill=NAVY, anchor="mm")
            S = S.resize((max(1, int(cw * cu)), max(1, int(70 * cu))))
            img.paste(S, (int(cx - S.width / 2), int(cy - S.height / 2)), S)
    crowd_grid(img, i, v, col)
    WD.caption(img, k, t, 1785, size=84)
    a = 1 - ease(t / 0.15)
    if a > 0: img.paste(NAVY, (0, 0), Image.new("L", (W, H), int(160 * a)))
    return img

def frame_intro(t, D):
    img = MAP.copy(); header(img); strip(img, -1, t); d = ImageDraw.Draw(img)
    for j, (txt, f, c, y) in enumerate([("AS 10 CIDADES", F("an", 150), NAVY, 620), ("MAIS POPULOSAS", F("an", 150), RED, 790), ("DO MUNDO", F("an", 150), NAVY, 960)]):
        u = back((t - 0.1 - j * 0.12) / 0.45)
        if u > 0:
            x = lerp(-700 if j != 1 else W + 700, W / 2, u); tw = d.textlength(txt, font=f)
            d.rounded_rectangle((x - tw / 2 - 30, y - 95, x + tw / 2 + 30, y + 95), 20, fill=WHITE)
            d.text((x, y), txt, font=f, fill=c, anchor="mm")
    u = ease((t - 0.8) / 0.5)
    if u > 0:
        d.rounded_rectangle((W / 2 - 250, 1120, W / 2 + 250, 1200), 40, fill=NAVY)
        d.text((W / 2, 1160), "SEGUNDO A ONU · 2025", font=F("osb", 40), fill=WHITE, anchor="mm")
    # train crossing
    x = -300 + (W + 600) * ((t * 0.35) % 1)
    d.rounded_rectangle((x - 260, 1330, x + 260, 1450), 40, fill=NAVY)
    for k in range(6): d.rounded_rectangle((x - 220 + k * 76, 1355, x - 170 + k * 76, 1400), 8, fill=(150, 200, 255))
    d.rectangle((x - 260, 1425, x + 260, 1435), fill=RED)
    d.line((0, 1465, W, 1465), fill=(120, 115, 105), width=6)
    WD.caption(img, 0, t, 1650, size=84)
    return img

def frame_outro(t, D):
    img = MAP.copy(); header(img); d = ImageDraw.Draw(img)
    # list as a vertical line diagram
    lx = 150
    d.line((lx, 300, lx, 300 + 9 * 105), fill=RED, width=16)
    for j in range(10):
        r = B[9 - j]; y = 300 + j * 105; u = ease((t - j * 0.06) / 0.3)
        if u <= 0: continue
        c = GREEN if r[1] == "CAIRO" else RED
        d.ellipse((lx - 24, y - 24, lx + 24, y + 24), fill=WHITE, outline=c, width=8)
        d.text((lx + 60, y), f"{r[0]}. {r[1]}", font=F("osb", 52), fill=NAVY, anchor="lm")
        d.text((W - 80, y), pfmt(r[4]) + " mi", font=F("an", 56), fill=c, anchor="rm")
    # São Paulo transfer
    st = WD.time_of(11, "Paulo", 0.6)
    u = back((t - st) / 0.5)
    if u > 0:
        y = 300 + 10 * 105 + 40
        d.line((lx, 300 + 9 * 105, lx, y), fill=(200, 195, 185), width=16)
        d.rounded_rectangle((60, y - 60, W - 60, y + 60), 30, fill=(0, 140, 60))
        d.ellipse((lx - 30, y - 30, lx + 30, y + 30), fill=(255, 205, 0), outline=WHITE, width=6)
        d.text((lx + 60, y), "13. SÃO PAULO", font=F("osb", int(52 * min(1, u))), fill=WHITE, anchor="lm")
        d.text((W - 90, y), "18,9 mi", font=F("an", 56), fill=(255, 205, 0), anchor="rm")
    u = back((t - D + 2.6) / 0.5)
    if u > 0: d.text((W / 2, 1600), "SEGUE O RANKEADO BR", font=F("an", int(92 * min(1, u))), fill=RED, anchor="mm", stroke_width=6, stroke_fill=WHITE)
    WD.caption(img, 11, t, 1700, size=80)
    if t > D - 1.5:
        d.rectangle((0, 1700, W, H), fill=NAVY)
        for j, line in enumerate(CRED): d.text((W / 2, 1728 + j * 30), line, font=F("mono", 19), fill=(220, 225, 235), anchor="mm")
    return img

meta = json.load(open(FOT + "meta.json"))
CRED = credit_lines(meta, [(b[0], b[3]) for b in B], "Dados: ONU, World Urbanization Prospects 2025. Fotos via Flickr:",
                    'Trilha: "Hitman" Kevin MacLeod (incompetech.com) · CC BY 4.0')
def scene_fn(k):
    if k == 0: return frame_intro
    if k == 11: return frame_outro
    return lambda t, D, i=k - 1: frame_item(i, t, D)
if __name__ == "__main__":
    main(scene_fn, D9 + "durs.json", 12, "s9", lambda d: [(0, 2.5), (1, d[1] - 0.3), (4, d[4] - 0.3), (9, d[9] - 0.5), (10, d[10] - 0.5), (11, 4.0), (11, d[11] - 0.5)])
