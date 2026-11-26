import sys, json, subprocess, os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

W, H, FPS = 1080, 1920, 30
FD = "/home/claude/fonts/"
_fc = {}
def F(kind, sz):
    sz = max(8, int(sz)); k = (kind, sz)
    if k in _fc: return _fc[k]
    if kind == "an": f = ImageFont.truetype(FD + "Anton-Regular.ttf", sz)
    elif kind == "mono": f = ImageFont.truetype(FD + "ShareTechMono-Regular.ttf", sz)
    elif kind == "os": f = ImageFont.truetype(FD + "Oswald[wght].ttf", sz); f.set_variation_by_name("SemiBold")
    _fc[k] = f; return f

WHITE = (255, 255, 255); BLACK = (0, 0, 0); BG = (6, 8, 16)
CAT = {"TERRA": (255, 138, 0), "AR": (0, 229, 255), "ESPAÇO": (190, 110, 255)}
FOT = "/home/claude/rk5/fotos/"
B = [  # rank, name, sub, photo, fx, kmh, trigger, cat, display
 (10, "YANGWANG U9 XTREME", "carro de produção mais rápido", "v10_1.jpg", 0.5, 503, "503", "TERRA", "503"),
 (9, "MAGLEV L0", "o trem que flutua · Japão", "v09_1.jpg", 0.45, 603, "603", "TERRA", "603"),
 (8, "THRUSTSSC", "quebrou a barreira do som", "v08_0.jpg", 0.5, 1228, "1", "TERRA", "1.228"),
 (7, "SR-71 BLACKBIRD", "o jato mais rápido da história", "v07_1.jpg", 0.5, 3529, "3", "AR", "3.529"),
 (6, "X-15", "avião-foguete · 2x uma bala", "v06_1.jpg", 0.5, 7274, "7", "AR", "7.274"),
 (5, "ÔNIBUS ESPACIAL", "na volta do espaço", "v05_5.jpg", 0.5, 27000, "27", "ESPAÇO", "~27.000"),
 (4, "APOLLO 10", "os humanos mais rápidos", "v04_1.jpg", 0.5, 39897, "40", "ESPAÇO", "39.897"),
 (3, "CÁPSULA STARDUST", "a reentrada mais rápida", "v03_0.jpg", 0.5, 46100, "46", "ESPAÇO", "46.100"),
 (2, "SONDA HELIOS 2", "recorde de 1976", "v02_2.jpg", 0.5, 246960, "247", "ESPAÇO", "246.960"),
 (1, "SONDA PARKER", "NASA · rasante no Sol", "v01_0.jpg", 0.5, 692000, "692", "ESPAÇO", "692.000"),
]
FIX = {"10": "DÉCIMO", "6º": "SEXTO", "KMH": "KM/H", "RANKEI": "RANKEEI"}
WORDS = json.load(open("/home/claude/rk5/words.json"))

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def word_time(k, key, default):
    for w in WORDS[k]:
        if w["w"].strip(".,!?") == key: return w["t0"]
    for w in WORDS[k]:
        if key in w["w"]: return w["t0"]
    return default
def mix(a, b, u): return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))

# ---------- stars + warp ----------
random.seed(11)
STARS = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.2, 1.0)) for _ in range(420)]
def warp(img, t, speed, col):
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 640
    for (x, y, z) in STARS:
        zz = (z - t * speed * 0.35) % 1.0 + 0.02
        px, py = cx + x / zz * 260, cy + y / zz * 260
        ln = min(300, 6 + speed * 60 * (1 / zz))
        ang = math.atan2(py - cy, px - cx)
        qx, qy = px - math.cos(ang) * ln * 0.25, py - math.sin(ang) * ln * 0.25
        if -50 < px < W + 50 and -50 < py < H + 50:
            b = int(80 + 175 * (1 - zz))
            c = mix((b, b, b), col, 0.35)
            d.line([(qx, qy), (px, py)], fill=c, width=2 if zz < 0.3 else 1)

def background(lvl, t, col):
    img = Image.new("RGB", (W, H), BG)
    g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse([W / 2 - 700, 640 - 700, W / 2 + 700, 640 + 700], fill=int(60 + 12 * lvl))
    g = g.filter(ImageFilter.GaussianBlur(220))
    img = Image.composite(Image.new("RGB", (W, H), mix(BG, col, 0.5)), img, g)
    warp(img, t, 0.4 + lvl * 0.45, col)
    return img

# ---------- photo in HUD frame ----------
PW, PH = 900, 560
_ph = {}
def photo(i):
    if i not in _ph:
        im = Image.open(FOT + B[i][3]).convert("RGB")
        im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.12)
        ar = PW / PH
        if im.width / im.height > ar:
            nw = int(im.height * ar); cx = int(im.width * B[i][4]); x0 = max(0, min(im.width - nw, cx - nw // 2)); im = im.crop((x0, 0, x0 + nw, im.height))
        else:
            nh = int(im.width / ar); y0 = int((im.height - nh) * 0.35); im = im.crop((0, y0, im.width, y0 + nh))
        _ph[i] = im.resize((int(PW * 1.15), int(PH * 1.15)), Image.LANCZOS)
    return _ph[i]
SCAN = Image.new("L", (PW, PH), 0)
_sd = ImageDraw.Draw(SCAN)
for y in range(0, PH, 4): _sd.line([(0, y), (PW, y)], fill=40)

def hud_photo(img, i, t, D, col, x0, y0, sc=1.0, shake=0):
    src = photo(i); z = 1 + 0.14 * min(1, t / D)
    cw, ch = src.width / z, src.height / z; sx, sy = (src.width - cw) / 2, (src.height - ch) / 2
    ph = src.resize((PW, PH), Image.BILINEAR, box=(sx, sy, sx + cw, sy + ch))
    # chromatic split on entry
    if t < 0.35:
        off = int(18 * (1 - t / 0.35))
        r, g, b = ph.split(); r = ImageChops.offset(r, off, 0); b = ImageChops.offset(b, -off, 0); ph = Image.merge("RGB", (r, g, b))
    ph = Image.composite(Image.new("RGB", (PW, PH), BLACK), ph, SCAN)
    if sc != 1.0: ph = ph.resize((int(PW * sc), int(PH * sc)))
    w, h = ph.size; x0 = int(W / 2 - w / 2 + shake);
    img.paste(ph, (x0, y0))
    d = ImageDraw.Draw(img); L = 60
    for (cx, cy, dx, dy) in [(x0, y0, 1, 1), (x0 + w, y0, -1, 1), (x0, y0 + h, 1, -1), (x0 + w, y0 + h, -1, -1)]:
        d.line([(cx - dx * 10, cy - dy * 10), (cx + dx * L, cy - dy * 10)], fill=col, width=6)
        d.line([(cx - dx * 10, cy - dy * 10), (cx - dx * 10, cy + dy * L)], fill=col, width=6)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=mix(col, BLACK, 0.4), width=2)

# ---------- gauge (log scale 100 .. 1,000,000) ----------
GX, GY, GR = W / 2, 1520, 330
A0, A1 = 210, -30    # degrees: 210 (left) to -30 (right), clockwise
def ang_for(v):
    u = (math.log10(max(100, v)) - 2) / 4.0
    return math.radians(A0 + (A1 - A0) * u)
def gauge(img, val, col, done, t, cracked=0.0):
    d = ImageDraw.Draw(img)
    # glow arc
    glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow)
    gd.arc([GX - GR, GY - GR, GX + GR, GY + GR], start=-A0, end=-A1, fill=255, width=16)
    a_now = ang_for(val)
    gd.arc([GX - GR, GY - GR, GX + GR, GY + GR], start=-A0, end=-math.degrees(a_now), fill=255, width=16)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], start=-A0, end=-A1, fill=(40, 46, 60), width=14)
    gl = glow.filter(ImageFilter.GaussianBlur(14))
    img.paste(col, (0, 0), gl.point(lambda v: int(v * 0.5)))
    d = ImageDraw.Draw(img)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], start=-A0, end=-math.degrees(a_now), fill=col, width=14)
    # ticks
    for e in range(2, 7):
        for m in (1, 2, 5):
            v = m * 10 ** e
            if v > 1e6: continue
            a = ang_for(v); big = (m == 1)
            r1 = GR - 30; r2 = GR - (62 if big else 46)
            d.line([(GX + r1 * math.cos(a), GY - r1 * math.sin(a)), (GX + r2 * math.cos(a), GY - r2 * math.sin(a))], fill=WHITE if big else (150, 155, 170), width=4 if big else 2)
            if big:
                lab = {100: "100", 1000: "1 MIL", 10000: "10 MIL", 100000: "100 MIL", 1000000: "1 MI"}[v]
                rl = GR - 105
                d.text((GX + rl * math.cos(a), GY - rl * math.sin(a)), lab, font=F("mono", 28), fill=(200, 205, 220), anchor="mm")
    # ghost markers of previous records
    for (pv, pc) in done:
        a = ang_for(pv); r1, r2 = GR + 14, GR + 40
        d.line([(GX + r1 * math.cos(a), GY - r1 * math.sin(a)), (GX + r2 * math.cos(a), GY - r2 * math.sin(a))], fill=pc, width=6)
    # needle
    jit = 0.012 * math.sin(t * 40) if val > 0 else 0
    a = ang_for(val) + jit
    tip = (GX + (GR - 40) * math.cos(a), GY - (GR - 40) * math.sin(a))
    base_l = (GX + 18 * math.cos(a + math.pi / 2), GY - 18 * math.sin(a + math.pi / 2))
    base_r = (GX + 18 * math.cos(a - math.pi / 2), GY - 18 * math.sin(a - math.pi / 2))
    d.polygon([tip, base_l, base_r], fill=(255, 60, 60))
    d.ellipse([GX - 34, GY - 34, GX + 34, GY + 34], fill=(30, 34, 46), outline=col, width=4)
    if cracked > 0:
        random.seed(77); n = int(14 * cracked)
        for _ in range(n):
            ang = random.uniform(0, 6.28); r = 0; x, y = GX + 120 * math.cos(ang), GY - 140 - 120 * math.sin(ang)
            pts = [(x, y)]
            for s in range(6):
                ang += random.uniform(-0.6, 0.6); r = random.uniform(30, 70); x += r * math.cos(ang); y += r * math.sin(ang); pts.append((x, y))
            d.line(pts, fill=(230, 240, 255), width=3)

def readout(img, val_disp, col, y=1720):
    d = ImageDraw.Draw(img)
    glow = Image.new("L", (W, 220), 0); ImageDraw.Draw(glow).text((W / 2, 100), val_disp, font=F("mono", 120), fill=255, anchor="mm")
    img.paste(col, (0, y - 100), glow.filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7)))
    img.paste(WHITE, (0, y - 100), glow)
    d.text((W / 2, y + 85), "KM/H", font=F("os", 40), fill=col, anchor="mm")

def groups_for(k):
    gs = []; buf = None
    for w in WORDS[k]:
        txt = w["w"].upper().strip(",!?")
        if txt.endswith(".") and not any(c.isdigit() for c in txt[:-1]): txt = txt[:-1]
        if (txt.startswith("-") or txt.startswith(",") or txt.startswith(".")) and gs: gs[-1]["txt"] += txt; gs[-1]["t1"] = w["t1"]; continue
        if txt.endswith("."): txt = txt[:-1]
        if buf is not None: g = {"txt": (buf["txt"] + " " + txt).strip(), "t0": buf["t0"], "t1": w["t1"]}; buf = None
        else: g = {"txt": txt, "t0": w["t0"], "t1": w["t1"]}
        orig = w["w"].strip(".,!?")
        if len(g["txt"]) <= 2 and not any(c.isdigit() for c in g["txt"]) and not (orig.isupper() and len(orig) >= 2): buf = g; continue
        gs.append(g)
    for g in gs: g["txt"] = FIX.get(g["txt"], g["txt"])
    return gs
GROUPS = [groups_for(k) for k in range(12)]
def caption(img, k, t, y=1065):
    d = ImageDraw.Draw(img); cur = None
    for g in GROUPS[k]:
        if g["t0"] - 0.05 <= t: cur = g
    if cur is None or t > cur["t1"] + 0.5: return
    a = (t - cur["t0"] + 0.05) / 0.12; sz = 96 * (1 + 0.22 * (1 - ease(a)))
    f = F("an", sz)
    while d.textlength(cur["txt"], font=f) > W - 90 and sz > 50: sz -= 6; f = F("an", sz)
    num = any(c.isdigit() for c in cur["txt"])
    d.text((W / 2, y), cur["txt"], font=f, fill=(255, 220, 80) if num else WHITE, anchor="mm", stroke_width=9, stroke_fill=BLACK)

def header(img, k, r, name, sub, cat, col, t):
    d = ImageDraw.Draw(img)
    d.text((60, 60), "VELOCÍMETRO RANKEADO", font=F("mono", 28), fill=(150, 160, 190))
    x = W - 60 - 10 * 30
    for j in range(10): d.rectangle([x + j * 30, 66, x + j * 30 + 20, 86], fill=col if j < k else (50, 55, 70))
    a = back(t / 0.3)
    f = F("an", 150 * max(0.3, a) if t < 0.3 else 150)
    d.text((60, 120), f"#{r}", font=f, fill=col)
    an = ease((t - 0.2) / 0.3); off = int(60 * (1 - an))
    if an > 0:
        d.rounded_rectangle([300 + off, 130, 300 + off + 26 + d.textlength(cat, font=F("mono", 30)) + 26, 176], 8, outline=col, width=3)
        d.text((326 + off, 153), cat, font=F("mono", 30), fill=col, anchor="lm")
        nf = F("an", 74)
        while d.textlength(name, font=nf) > W - 360: nf = F("an", nf.size - 4)
        d.text((300 + off, 190), name, font=nf, fill=WHITE)
        d.text((300 + off, 190 + nf.size + 20), sub.upper(), font=F("os", 28), fill=(170, 178, 200))

def frame_item(i, t, D):
    k = i + 1; r, name, sub, _, _, v, trig, cat, disp = B[i]
    col = CAT[cat]; lvl = 11 - r
    tn = word_time(k, trig, D * 0.5) + 0.12
    g = (t - tn + 0.6) / 1.0   # needle sweep finishes ~0.4s after number spoken
    prev = B[i - 1][5] if i > 0 else 100
    val = prev + (v - prev) * ease(g) if g > 0 else prev
    # log-space sweep looks better
    if g > 0: val = 10 ** (math.log10(prev) + (math.log10(v) - math.log10(prev)) * ease(g))
    img = background(lvl, t, col)
    shake = 0
    if g >= 1 and t - (tn + 0.4) < 0.25: shake = random.uniform(-10, 10) * (3 if r == 1 else 1)
    hud_photo(img, i, t, D, col, 0, 400, 1.0, shake)
    header(img, k, r, name, sub, cat, col, t)
    caption(img, k, t - 0.12)
    done = [(B[j][5], CAT[B[j][7]]) for j in range(i)]
    gauge(img, val, col, done, t, cracked=(ease((t - tn - 0.4) / 0.3) if r == 1 else 0))
    if g > 0:
        if g >= 1: readout(img, disp, col)
        else:
            shown = f"{int(val):,}".replace(",", ".")
            readout(img, shown, col)
    # ratio chip vs previous
    if i > 0 and g >= 1 and t > tn + 0.6:
        ratio = v / B[i - 1][5]
        s = ("%.1fX O ANTERIOR" % ratio).replace(".", ",")
        if r == 1: s = "1.376X O CARRO Nº 10"
        ab = back((t - tn - 0.6) / 0.3); d = ImageDraw.Draw(img); f = F("an", 46 * max(0.3, ab)); tw = d.textlength(s, font=f)
        d.rounded_rectangle([W - 60 - tw - 40, 1250, W - 60, 1320], 14, fill=col)
        d.text((W - 80 - tw, 1285), s, font=f, fill=BLACK, anchor="lm")
    if t < 0.08: img = Image.blend(img, Image.new("RGB", (W, H), col), 0.35 * (1 - t / 0.08))
    if r == 1 and 0 <= t - tn - 0.4 < 0.15: img = Image.blend(img, Image.new("RGB", (W, H), WHITE), 0.7 * (1 - (t - tn - 0.4) / 0.15))
    return img

def frame_intro(t, D):
    col = CAT["ESPAÇO"]
    img = background(3 + 7 * min(1, t / D), t, mix(CAT["TERRA"], col, min(1, t / D)))
    d = ImageDraw.Draw(img)
    a = back(t / 0.4)
    d.text((W / 2, 240), "RANKEEI AS 10 COISAS", font=F("an", 74), fill=WHITE, anchor="mm")
    d.text((W / 2, 420), "MAIS RÁPIDAS", font=F("an", 170 * max(0.3, a)), fill=(255, 220, 80), anchor="mm", stroke_width=6, stroke_fill=BLACK)
    d.text((W / 2, 580), "JÁ CRIADAS PELO SER HUMANO", font=F("an", 70), fill=WHITE, anchor="mm")
    sweep = 100 * 10 ** (4 * min(1, t / (D * 0.9)))
    gauge(img, sweep, mix(CAT["TERRA"], col, min(1, t / D)), [], t)
    readout(img, f"{int(sweep):,}".replace(",", "."), col)
    tn = word_time(0, "mil", 4.0)
    if t > tn:
        ab = back((t - tn) / 0.3); d = ImageDraw.Draw(img); s = "O Nº 1 É +1.000X O CARRO MAIS RÁPIDO"
        f = F("an", 52 * max(0.3, ab)); tw = d.textlength(s, font=f)
        d.rounded_rectangle([(W - tw) / 2 - 26, 700, (W + tw) / 2 + 26, 790], 16, fill=(255, 60, 60))
        d.text((W / 2, 745), s, font=f, fill=WHITE, anchor="mm")
    return img

CRED = None
def frame_outro(t, D):
    img = background(10, t * 0.3, CAT["ESPAÇO"]); d = ImageDraw.Draw(img)
    d.text((60, 60), "VELOCÍMETRO RANKEADO", font=F("mono", 28), fill=(150, 160, 190))
    for j in range(10):
        i = 9 - j; u = ease((t - j * 0.06) / 0.3)
        if u <= 0: continue
        r, name, sub, _, _, v, trig, cat, disp = B[i]; y = 140 + j * 92
        maxw = W - 120; w = maxw * (math.log10(v) - 2) / 4.0 * u
        d.rounded_rectangle([60, y, 60 + w, y + 70], 10, fill=mix(CAT[cat], BG, 0.35))
        d.text((80, y + 35), f"#{r}  {name}", font=F("os", 30), fill=WHITE, anchor="lm")
        d.text((60 + max(w, 520) - 16, y + 35), disp + " km/h", font=F("mono", 30), fill=WHITE, anchor="rm")
    if t > 0.8:
        a = back((t - 0.8) / 0.35)
        d.rounded_rectangle([60, 1100, W - 60, 1420], 26, fill=(14, 16, 30), outline=CAT["ESPAÇO"], width=4)
        d.text((W / 2, 1185), "QUAL DESSAS VOCÊ", font=F("an", 80), fill=WHITE, anchor="mm")
        d.text((W / 2, 1300), "QUERIA PILOTAR?", font=F("an", 104 * max(0.3, a)), fill=(255, 220, 80), anchor="mm")
        d.text((W / 2, 1385), "comenta aí", font=F("os", 36), fill=(200, 205, 225), anchor="mm")
    if t > 1.4:
        d.rounded_rectangle([170, 1450, W - 170, 1530], 40, fill=CAT["AR"])
        d.text((W / 2, 1490), "SEGUE O @RANKEADOBR", font=F("an", 48), fill=BLACK, anchor="mm")
    d.text((W / 2, 1580), "escala logarítmica: cada marca = 10x mais rápido", font=F("mono", 24), fill=(150, 160, 190), anchor="mm")
    if t > D - 2.6:
        d.rectangle([0, 1650, W, H], fill=BLACK); y = 1662
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
        m = meta[b[3]]; parts.append(f"#{b[0]} {m.get('creator') or 'NASA'} ({lic(m)})")
    lines, cur = ["Fontes: Guinness, FIA, NASA. Fotos via Wikimedia Commons / Flickr:"], ""
    for p_ in parts:
        if len(cur) + len(p_) > 110: lines.append(cur); cur = ""
        cur += ("  ·  " if cur else "") + p_
    lines.append(cur); lines.append('Trilha: "Volatile Reaction" Kevin MacLeod (incompetech.com) · CC BY 4.0')
    return lines

def times():
    return [{"tn": word_time(i + 1, B[i][6], 3) + 0.12} for i in range(10)]

if __name__ == "__main__":
    CRED = credits()
    mode = sys.argv[1]; durs = json.load(open(sys.argv[2]))
    if mode == "stills":
        for k, t in [(0, 0.3), (0, durs[0] - 0.3), (4, durs[4] - 0.3), (7, durs[7] - 0.3), (10, durs[10] - 0.3), (11, durs[11] - 1)]:
            random.seed(1); scene_fn(k)(t, durs[k]).convert("RGB").save(f"s8_{k}_{round(t,1)}.png")
    elif mode == "times":
        json.dump(times(), open("times.json", "w")); print("ok")
    else:
        for k in [int(x) for x in sys.argv[3:]] or range(12):
            render_scene(k, durs[k], f"s8_{k:02d}.mp4")
