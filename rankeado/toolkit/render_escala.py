import sys, json, random, math
import numpy as np
sys.path.insert(0, "/home/claude"); from rkcommon import *

D8 = "/home/claude/rk8/"; FOT = D8 + "fotos/"
WD = Words(D8, {"RANKEEI": "RANKEEI"})
# rank, nome, foto, precrop, diam_km, cor, sub
B = [
 (10, "LUA", "p10_x.jpg", None, 3474, (200, 200, 210), "o satélite da Terra"),
 (9, "MERCÚRIO", "p09_x.jpg", None, 4879, (170, 165, 160), "o menor planeta"),
 (8, "MARTE", "p08_0.jpg", (520, 0, 1024, 420), 6779, (240, 110, 60), "o planeta vermelho"),
 (7, "VÊNUS", "p07_1.jpg", None, 12104, (235, 180, 80), "quase gêmeo da Terra"),
 (6, "TERRA", "p06_0.jpg", None, 12756, (70, 150, 255), "a nossa casa"),
 (5, "NETUNO", "p05_0.jpg", None, 49528, (70, 120, 255), "o mais distante"),
 (4, "URANO", "p04_0.jpg", (0, 0, 512, 866), 51118, (110, 220, 230), "o planeta deitado"),
 (3, "SATURNO", "p03_x.jpg", None, 120536, (230, 200, 140), "sem contar os anéis"),
 (2, "JÚPITER", "p02_x.jpg", None, 142984, (230, 170, 120), "o maior planeta"),
 (1, "SOL", "p01_0.jpg", None, 1392700, (255, 150, 30), "a nossa estrela"),
]
EARTH = 12756
def fmt(n): return f"{n:,}".replace(",", ".")
def xr(r):
    v = r / EARTH
    return f"{v:.0f}x" if v >= 10 else (f"{v:.1f}x".replace(".", ",") if v >= 1.05 else (f"{v:.2f}x".replace(".", ",") if v < 0.99 else "1x"))

_disc = {}
def disc(i):
    """RGBA of the body, square, diameter = image size; for Saturn width>height (rings)"""
    if i in _disc: return _disc[i]
    r = B[i]; im = Image.open(FOT + r[2]).convert("RGB")
    if r[3]: im = im.crop(r[3])
    a = np.asarray(im.convert("L")).astype(np.float32)
    mask = a > 28
    from scipy import ndimage
    lab, n = ndimage.label(ndimage.binary_closing(mask, iterations=3))
    if n > 1 and r[1] not in ("SATURNO", "SOL"):
        sizes = ndimage.sum(mask, lab, range(1, n + 1)); mask = lab == (1 + int(np.argmax(sizes)))
    ys, xs = np.where(mask)
    if r[1] == "SATURNO":
        x0, x1 = np.percentile(xs, 0.2), np.percentile(xs, 99.8); y0, y1 = np.percentile(ys, 0.5), np.percentile(ys, 99.5)
        im = im.crop((int(x0) - 4, int(y0) - 4, int(x1) + 4, int(y1) + 4))
        al = im.convert("L").point(lambda v: min(255, max(0, (v - 8) * 6)))
        out = im.convert("RGBA"); out.putalpha(al)
        # body diameter ~ globe height; globe height == crop height
        _disc[i] = (out, out.height); return _disc[i]
    x0, x1 = np.percentile(xs, 0.3), np.percentile(xs, 99.7); y0, y1 = np.percentile(ys, 0.3), np.percentile(ys, 99.7)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; R = max(x1 - x0, y1 - y0) / 2
    if r[1] == "SOL": R = min(x1 - x0, y1 - y0) / 2 * 1.0
    im = im.crop((int(cx - R), int(cy - R), int(cx + R), int(cy + R)))
    S = im.width; m = Image.new("L", (S * 4, S * 4), 0); ImageDraw.Draw(m).ellipse((4, 4, S * 4 - 4, S * 4 - 4), fill=255)
    m = m.resize((S, S), Image.LANCZOS)
    out = im.convert("RGBA"); out.putalpha(m); _disc[i] = (out, S); return _disc[i]

def put_body(img, i, cx, cy, dpx, glow=True):
    """draw body i with globe diameter dpx centred at cx,cy"""
    src, gd = disc(i); sc = dpx / gd
    w, h = max(1, int(src.width * sc)), max(1, int(src.height * sc))
    if w < 3:
        d = ImageDraw.Draw(img); rr = max(1, dpx / 2); d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=B[i][5]); return
    b = src.resize((w, h), Image.LANCZOS)
    if glow and dpx > 40:
        g = Image.new("L", (w + 200, h + 200), 0); ImageDraw.Draw(g).ellipse((100 + (w - dpx) / 2 - 10, 100 + (h - dpx) / 2 - 10, 100 + (w + dpx) / 2 + 10, 100 + (h + dpx) / 2 + 10), fill=90 if B[i][1] != "SOL" else 200)
        g = g.filter(ImageFilter.GaussianBlur(40 if B[i][1] != "SOL" else 60))
        img.paste(B[i][5], (int(cx - w / 2 - 100), int(cy - h / 2 - 100)), g)
    img.paste(b, (int(cx - w / 2), int(cy - h / 2)), b)

# ---------- space background ----------
random.seed(3)
STARS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1), random.uniform(0, 6.28)) for _ in range(500)]
_neb = {}
def space(col, t, drift=0.0):
    key = col
    if key not in _neb:
        n = Image.effect_noise((W // 16, H // 16), 90).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BICUBIC)
        n = n.point(lambda v: max(0, v - 120) * 0.55)
        base = Image.new("RGB", (W, H), (3, 4, 10)); base.paste(mixc(col, (40, 30, 90), 0.5), (0, 0), n.convert("L")); _neb[key] = base
    img = _neb[key].copy(); d = ImageDraw.Draw(img)
    for x, y, z, ph in STARS:
        xx = (x + drift * z * 60 * t) % W; br = int(140 + 115 * z * (0.7 + 0.3 * math.sin(t * 3 + ph)))
        s = 1.2 * z + 0.3; d.ellipse((xx - s, y - s, xx + s, y + s), fill=(br, br, min(255, br + 15)))
    return img

def header(img, rank, col):
    d = ImageDraw.Draw(img)
    d.text((70, 110), "SISTEMA SOLAR", font=F("an", 64), fill=WHITE, anchor="lm")
    d.text((72, 170), "DO MENOR PRO MAIOR · ESCALA REAL", font=F("mono", 30), fill=(150, 160, 190), anchor="lm")
    if rank:
        d.rounded_rectangle((W - 230, 72, W - 60, 202), 26, outline=col, width=4, fill=(8, 10, 20))
        d.text((W - 145, 140), f"#{rank}", font=F("an", 88), fill=col, anchor="mm")

def lineup(img, cur):
    d = ImageDraw.Draw(img); y = 1800; x = 110; xs = []
    for j in range(10):
        dd = 12 + math.log10(B[j][4] / 3000) * 20; xs.append(x + dd / 2); x += dd + 28
    off = (W - (x - 28) - 110) / 2
    d.line((110 + off, y, x - 28 + off, y), fill=(50, 55, 80), width=2)
    for j in range(10):
        dd = 12 + math.log10(B[j][4] / 3000) * 20; cx = xs[j] + off
        c = B[j][5] if j <= cur else (60, 65, 90)
        d.ellipse((cx - dd / 2, y - dd / 2, cx + dd / 2, y + dd / 2), fill=c)
        if j == cur: d.ellipse((cx - dd / 2 - 8, y - dd / 2 - 8, cx + dd / 2 + 8, y + dd / 2 + 8), outline=WHITE, width=3)

CY = 800
def frame_item(i, t, D):
    rk, name, fn, pc, km, col, sub = B[i]; k = i + 1; r = km / EARTH
    tn = WD.first_num(k, 2.0)
    img = space(col, t, 0.4)
    header(img, rk, col)
    grow = back((t - 0.05) / 0.6)
    if r < 0.999:
        s = 500; pd = r * s
        ex = W - 30 - s / 2; px = 30 + pd / 2 + (W - 60 - s - pd) * 0.35
        put_body(img, 4, ex + (1 - ease(t / 0.5)) * 500, CY, s)
        put_body(img, i, px, CY, max(2, pd * grow))
        d = ImageDraw.Draw(img)
        d.text((ex, CY + s / 2 + 40), "TERRA", font=F("os", 34), fill=(150, 190, 255), anchor="mm")
        d.text((px, CY + max(pd, 200) / 2 + 40), name, font=F("os", 34), fill=col, anchor="mm")
    elif r < 1.01:
        put_body(img, i, W / 2, CY, 640 * grow)
    else:
        P = 660 if rk != 3 else 430; s = P / r
        put_body(img, i, W / 2, CY, P * grow)
        # earth reference
        ex, ey = W - 130, CY + P / 2 + 10
        if rk == 1: ex, ey = W - 120, CY + P / 2 + 60
        u = ease((t - 0.5) / 0.4)
        if u > 0:
            put_body(img, 4, ex, ey, max(3, s), glow=False)
            d = ImageDraw.Draw(img); d.line((ex - 20 - s / 2, ey, ex - 90, ey + 50), fill=(150, 190, 255), width=3)
            d.text((ex - 100, ey + 62), "TERRA", font=F("os", 30), fill=(150, 190, 255), anchor="rm")
        # row of earths across the diameter
        n = int(r + 0.5) if rk != 1 else 109
        ru = (t - tn) / 1.2
        if ru > 0:
            shown = min(n, int(n * ease(ru)) + 1); d = ImageDraw.Draw(img)
            x0 = W / 2 - P / 2
            for j in range(shown):
                cx = x0 + s / 2 + j * (P / n)
                if s > 14: put_body(img, 4, cx, CY, s * 0.98, glow=False)
                else: d.ellipse((cx - s / 2, CY - s / 2, cx + s / 2, CY + s / 2), fill=(90, 160, 255), outline=(200, 230, 255))
            d.line((x0, CY + s / 2 + 14, x0 + P * shown / n, CY + s / 2 + 14), fill=WHITE, width=3)
    d = ImageDraw.Draw(img)
    # title + readout
    u = ease((t - 0.3) / 0.4)
    d.text((W / 2, 1255 + 20 * (1 - u)), name, font=F("an", 130), fill=WHITE, anchor="mm")
    d.text((W / 2, 1345), sub.upper(), font=F("os", 34), fill=col, anchor="mm")
    nu = ease((t - tn) / 0.9)
    val = fmt(int(km * nu)) + " km"
    if t >= tn: d.text((W / 2 - 20, 1440), "Ø " + val, font=F("mono", 70), fill=WHITE, anchor="mm")
    if nu >= 1:
        cu = back((t - tn - 0.9) / 0.4); chip = xr(km) + " A TERRA" if rk != 6 else "REFERÊNCIA"
        f = F("osb", int(40 * min(1, cu))); cw = d.textlength(chip, font=F("osb", 40)) + 60
        d.rounded_rectangle((W / 2 - cw / 2, 1495, W / 2 + cw / 2, 1555), 30, fill=col)
        d.text((W / 2, 1525), chip, font=f, fill=(5, 8, 15), anchor="mm")
    if rk == 1:
        st = WD.time_of(k, "Dentro", D - 2.5)
        su = back((t - st) / 0.5)
        if su > 0:
            f = F("an", int(76 * su)); txt = "CABEM 1,3 MILHÃO DE TERRAS"
            d.text((W / 2, 300), txt, font=f, fill=(255, 210, 90), anchor="mm", stroke_width=8, stroke_fill=BLACK)
    WD.caption(img, k, t, 1650)
    lineup(img, i)
    a = 1 - ease(t / 0.18)
    if a > 0: img.paste((255, 255, 255), (0, 0), Image.new("L", (W, H), int(120 * a)))
    return img

def frame_intro(t, D):
    img = space((80, 60, 200), t, 0.6); header(img, 0, WHITE); d = ImageDraw.Draw(img)
    # tiny earth growing then shrinking against giant sun limb
    sunR = 1500; cy = CY + sunR + 260 - 120 * ease(t / D)
    put_body(img, 9, W / 2, cy, sunR * 2)
    put_body(img, 4, W / 2, 760 - 40 * math.sin(t), 90)
    d = ImageDraw.Draw(img)
    for j, (txt, f, c, y) in enumerate([("DO MENOR", F("an", 170), WHITE, 400), ("PRO MAIOR", F("an", 170), (255, 200, 80), 560)]):
        u = back((t - 0.1 - j * 0.15) / 0.45)
        if u > 0: d.text((W / 2 + (1 - u) * (500 if j else -500), y), txt, font=f, fill=c, anchor="mm", stroke_width=8, stroke_fill=BLACK)
    d.text((W / 2, 850), "← TERRA", font=F("os", 36), fill=(150, 190, 255), anchor="lm") if False else None
    WD.caption(img, 0, t, 1060)
    return img

def frame_outro(t, D):
    img = space((255, 120, 30), t, 0.3); header(img, 0, WHITE); d = ImageDraw.Draw(img)
    s = 20; sunR = 109 * s / 2
    put_body(img, 9, W / 2, 1500 + sunR - 40 * ease(t / 1.0), sunR * 2)
    order = [8, 7, 6, 5, 3, 4, 2, 1, 0]
    ws = [max(6, B[j][4] / EARTH * s) * (2.2 if B[j][1] == "SATURNO" else 1) for j in order]
    gap = (W - 120 - sum(ws)) / (len(ws) - 1); x = 60
    for n, j in enumerate(order):
        dp = max(5, B[j][4] / EARTH * s); w = ws[n]; u = back((t - n * 0.08) / 0.4)
        if u > 0:
            cx = x + w / 2; put_body(img, j, cx, 1000 - (1 - u) * 300, dp * u, glow=False)
            if dp > 40 or B[j][1] == "TERRA": ImageDraw.Draw(img).text((cx, 1000 + max(dp, 60) / 2 + 30 + (60 if B[j][1] == "TERRA" else 0)), B[j][1].title(), font=F("os", 26), fill=(200, 205, 225), anchor="mm")
        x += w + gap
    d = ImageDraw.Draw(img)
    d.text((W / 2, 520), "TUDO NA MESMA ESCALA", font=F("an", 86), fill=WHITE, anchor="mm", stroke_width=6, stroke_fill=BLACK)
    u = back((t - 1.0) / 0.5)
    if u > 0: d.text((W / 2, 640), "SEGUE O RANKEADO BR", font=F("an", int(80 * u)), fill=(255, 200, 80), anchor="mm", stroke_width=6, stroke_fill=BLACK)
    WD.caption(img, 11, t, 1300)
    if t > D - 1.5:
        d.rectangle((0, 1700, W, H), fill=(5, 5, 10))
        for j, line in enumerate(CRED): d.text((W / 2, 1728 + j * 30), line, font=F("mono", 19), fill=(200, 200, 210), anchor="mm")
    return img

meta = json.load(open(FOT + "meta.json"))
CRED = credit_lines(meta, [(b[0], b[2]) for b in B], "Diâmetros: NASA. Imagens: NASA/ESA (domínio público) e Wikimedia Commons:",
                    'Trilha: "Volatile Reaction" Kevin MacLeod (incompetech.com) · CC BY 4.0')
def scene_fn(k):
    if k == 0: return frame_intro
    if k == 11: return frame_outro
    return lambda t, D, i=k - 1: frame_item(i, t, D)
if __name__ == "__main__":
    main(scene_fn, D8 + "durs.json", 12, "s8", lambda d: [(0, 2.5), (1, d[1] - 0.3), (4, d[4] - 0.3), (6, d[6] - 0.5), (8, d[8] - 0.5), (10, d[10] - 0.5), (11, d[11] - 0.5)])
