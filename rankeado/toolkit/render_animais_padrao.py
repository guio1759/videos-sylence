import sys, json, subprocess, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
_fc = {}
def font(sz, bold=True):
    k = (int(sz), bold)
    if k not in _fc: _fc[k] = ImageFont.truetype(FB if bold else FR, int(sz))
    return _fc[k]
YEL = (255, 204, 0); RED = (235, 40, 40); WHITE = (255, 255, 255); BLACK = (0, 0, 0); DARK = (12, 12, 14)
FOT = "/home/claude/rk2/fotos/"
# rank, name, sub, photo, fx, stat
# stat: ("num", value, prefix, suffix, label, trigger_word)  or ("chip", text, trigger_word)
B = [
 (10, "PIRANHA", "rios do Brasil", "a10_1.jpg", 0.5, ("chip", "DENTES COMO LÂMINA", "dentes")),
 (9, "ONÇA-PINTADA", "Amazônia · Pantanal", "a09_2.jpg", 0.52, ("chip", "MORDIDA MAIS FORTE DOS FELINOS", "mordida")),
 (8, "SUCURI", "a maior cobra do Brasil", "a08_3.jpg", 0.45, ("num", 5, "", "+ m", "de comprimento", "5")),
 (7, "TUBARÃO", "litoral de Pernambuco", "a07_0.jpg", 0.35, ("num", 84, "", "", "ataques em PE desde 1992", "84")),
 (6, "TATURANA", "lagarta Lonomia", "a06_1.jpg", 0.5, ("chip", "VENENO CAUSA HEMORRAGIA", "veneno")),
 (5, "ARANHA-MARROM", "dentro de casa", "a05_0.jpg", 0.5, ("chip", "PODE NECROSAR A PELE", "necrosar")),
 (4, "ARANHA-ARMADEIRA", "Phoneutria", "a04_1.jpg", 0.5, ("num", 43, "+", " MIL", "picadas de aranha em 2023", "43")),
 (3, "JARARACA", "todo o Brasil", "a03_1.jpg", 0.7, ("chip", "A COBRA QUE MAIS PICA", "cobra")),
 (2, "ESCORPIÃO-AMARELO", "cidades do Brasil", "a02_3.jpg", 0.5, ("num", 200, "~", " MIL", "acidentes com escorpião em 2023", "200")),
 (1, "MOSQUITO DA DENGUE", "Aedes aegypti", "a01_0.jpg", 0.45, ("num", 6, "~", " MIL", "mortes por dengue em 2024", "6")),
]
FIX = {"RANQUEI": "RANKEEI", "9": "NONO", "AÇUCURI": "A SUCURI", "A GENTE": "GENTE", "E QUINTO": "QUINTO"}
WORDS = json.load(open("/home/claude/rk2/words.json"))

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

BLACKIM = Image.new("RGB", (W, H), BLACK)
_bg, _fg = {}, {}
def bg(i):
    if i not in _bg:
        im = Image.open(FOT + B[i][3]).convert("RGB")
        s = max(W / im.width, H / im.height) * 1.1
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
        x0 = (im.width - W) // 2; y0 = (im.height - H) // 2
        im = im.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(28))
        _bg[i] = ImageEnhance.Brightness(im).enhance(0.38)
    return _bg[i]
BOXW, BOXH, BOXY = 1080, 1000, 372
def fg(i):
    if i not in _fg:
        im = Image.open(FOT + B[i][3]).convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.1); im = ImageEnhance.Color(im).enhance(1.2)
        # cover-crop the photo to the box aspect, around focus x
        ar = BOXW / BOXH
        if im.width / im.height > ar:
            nw = int(im.height * ar); cx = int(im.width * B[i][4]); x0 = max(0, min(im.width - nw, cx - nw // 2))
            im = im.crop((x0, 0, x0 + nw, im.height))
        else:
            nh = int(im.width / ar); y0 = (im.height - nh) // 2; im = im.crop((0, y0, im.width, y0 + nh))
        _fg[i] = im.resize((int(BOXW * 1.25), int(BOXH * 1.25)), Image.LANCZOS)
    return _fg[i]

def card(i, t, D, zoom0=1.0, zoom1=1.18):
    src = fg(i); z = zoom0 + (zoom1 - zoom0) * (t / D)
    cw, ch = src.width / z / 1.25 * 1.25 / 1.0, src.height / z
    cw = src.width / z; ch = src.height / z
    sx = (src.width - cw) / 2; sy = (src.height - ch) / 2 + (src.height - ch) * 0.1 * (0.5 - t / D)
    im = src.resize((BOXW, BOXH), Image.BILINEAR, box=(sx, sy, sx + cw, sy + ch))
    mask = Image.new("L", (BOXW, BOXH), 255)
    return im, mask

_bk = {}
def backdrop(lvl):
    if lvl in _bk: return _bk[lvl].copy()
    import math
    img = Image.new("RGB", (W, H), (16, 16, 20)); d = ImageDraw.Draw(img)
    for y in range(H):
        c = int(14 + 10 * abs(y - H / 2) / (H / 2)); d.line([(0, y), (W, y)], fill=(c, c, c + 4))
    for x in range(-H, W, 46): d.line([(x, 0), (x + H, H)], fill=(26, 26, 32), width=10)
    glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow)
    gd.ellipse([-300, -420, W + 300, 520], fill=int(40 + 14 * lvl)); gd.ellipse([-300, H - 560, W + 300, H + 420], fill=int(40 + 14 * lvl))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    col = (255, int(200 - 15 * lvl), 0)
    img = Image.composite(Image.new("RGB", (W, H), col), img, glow.point(lambda v: v // 2))
    _bk[lvl] = img; return img.copy()

def tape(d, y, h, t, txt=True):
    d.rectangle([0, y, W, y + h], fill=YEL)
    off = (t * 140) % 60
    for x in range(-80, W + 80, 60):
        d.polygon([(x + off, y), (x + off + 28, y), (x + off + 28 - h, y + h), (x + off - h, y + h)], fill=(20, 20, 20))

def stroke_text(d, xy, s, f, fill, sw=8, anchor="la"):
    d.text(xy, s, font=f, fill=fill, stroke_width=sw, stroke_fill=BLACK, anchor=anchor)

def groups_for(k):
    gs = []; buf = None
    for w in WORDS[k]:
        txt = w["w"].upper().strip(".,!?")
        if txt.startswith("-") and gs:
            gs[-1]["txt"] += txt; gs[-1]["t1"] = w["t1"]; continue
        if buf is not None:
            g = {"txt": (buf["txt"] + " " + txt).strip(), "t0": buf["t0"], "t1": w["t1"]}; buf = None
        else:
            g = {"txt": txt, "t0": w["t0"], "t1": w["t1"]}
        if len(g["txt"]) <= 2 and not any(c.isdigit() for c in g["txt"]):
            buf = g; continue
        gs.append(g)
    for g in gs: g["txt"] = FIX.get(g["txt"], g["txt"])
    return gs
GROUPS = [groups_for(k) for k in range(12)]

def caption(d, k, t, y=1250):
    cur = None
    for g in GROUPS[k]:
        if g["t0"] - 0.05 <= t: cur = g
    if cur is None or t > cur["t1"] + 0.6: return
    a = (t - cur["t0"] + 0.05) / 0.12
    sz = 104 * (1 + 0.25 * (1 - ease(a)))
    num = any(c.isdigit() for c in cur["txt"])
    f = font(sz)
    while d.textlength(cur["txt"], font=f) > W - 80 and sz > 46: sz -= 6; f = font(sz)
    stroke_text(d, (W / 2, y), cur["txt"], f, YEL if num else WHITE, sw=10, anchor="mm")

def word_time(k, key, default):
    for w in WORDS[k]:
        if key.lower() in w["w"].lower(): return w["t0"]
    return default

def header(d, k):
    d.text((60, 58), "RANKEADO BR", font=font(32), fill=YEL)
    x = W - 60 - 10 * 34
    for j in range(10):
        d.rounded_rectangle([x + j * 34, 62, x + j * 34 + 24, 86], 6, fill=YEL if j < k else WHITE)

def meter(d, lvl, a, y=1820):
    d.text((60, y - 46), "NÍVEL DE PERIGO", font=font(30), fill=WHITE)
    n = 10; gw = (W - 120 - 9 * 8) / n
    filled = lvl * ease(a)
    for j in range(n):
        x = 60 + j * (gw + 8)
        col = (60, 60, 66)
        if j < int(filled + 0.001): col = (255, int(204 - 164 * j / 9), int(40 - 40 * j / 9))
        d.rounded_rectangle([x, y, x + gw, y + 34], 8, fill=col)

def fx(img, t, big=False, tn=0):
    amp = 0
    if t < 0.25: amp = 22 * (1 - t / 0.25)
    if big and t >= tn: amp = max(amp, 32 * max(0, 1 - (t - tn) / 0.45))
    if amp > 0:
        img = img.transform((W, H), Image.AFFINE, (1, 0, random.uniform(-amp, amp), 0, 1, random.uniform(-amp, amp)), fillcolor=BLACK)
    fl = 0
    if t < 0.1: fl = 0.55 * (1 - t / 0.1)
    if big and 0 <= t - tn < 0.12: fl = max(fl, 0.75 * (1 - (t - tn) / 0.12))
    if fl > 0: img = Image.blend(img, Image.new("RGB", (W, H), WHITE if not big else (255, 60, 60)), fl)
    return img

def frame_item(i, t, D):
    k = i + 1; r, name, sub, _, _, st = B[i]
    img = backdrop(11 - r)
    # card pops in
    a = back(t / 0.3); sc = 0.7 + 0.3 * a
    im, mask = card(i, t, D)
    if sc < 0.999:
        w2, h2 = int(BOXW * sc), int(BOXH * sc)
        im = im.resize((w2, h2)); mask = mask.resize((w2, h2))
    else: w2, h2 = BOXW, BOXH
    x0 = (W - w2) // 2; y0 = BOXY + (BOXH - h2) // 2
    img.paste(im, (x0, y0), mask)
    d = ImageDraw.Draw(img)
    # soft fade of photo into panels
    fade = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fade)
    for j in range(90): fd.line([(0, BOXY + j), (W, BOXY + j)], fill=int(255 * (1 - j / 90) ** 2))
    for j in range(260): fd.line([(0, BOXY + BOXH - 1 - j), (W, BOXY + BOXH - 1 - j)], fill=int(235 * (1 - j / 260) ** 1.6))
    img.paste(Image.new("RGB", (W, H), (14, 14, 18)), (0, 0), fade)
    d = ImageDraw.Draw(img)
    d.line([(0, BOXY), (W, BOXY)], fill=YEL if r > 3 else RED, width=6)
    d.line([(0, BOXY + BOXH), (W, BOXY + BOXH)], fill=YEL if r > 3 else RED, width=6)
    tape(d, 0, 22, t); tape(d, H - 22, 22, -t)
    header(d, k)
    rs = 1 + 1.6 * (1 - ease(t / 0.22))
    stroke_text(d, (60, 330), f"#{r}", font(200 * rs if t < 0.22 else 200), RED if r <= 3 else YEL, sw=12, anchor="ls")
    # name tag
    a = ease((t - 0.2) / 0.3); off = int(W * (1 - a))
    nf = font(60)
    while d.textlength(name, font=nf) > 640: nf = font(nf.size - 4)
    tw = d.textlength(name, font=nf)
    d.rounded_rectangle([W - 60 - tw - 44 + off, 200, W - 60 + off, 286], 14, fill=YEL)
    d.text((W - 60 - tw - 22 + off, 243), name, font=nf, fill=BLACK, anchor="lm")
    d.text((W - 60 + off, 300), sub, font=font(36, False), fill=WHITE, anchor="ra")
    caption(d, k, t - 0.12, y=1270)
    # stat
    tn = word_time(k, st[-1], D * 0.4) + 0.12
    g = (t - tn + 0.2) / 0.5
    if g > 0:
        if st[0] == "num":
            _, v, pre, suf, lab, _ = st
            val = int(round(v * ease(g)))
            s = f"{pre}{val}{suf}"
            f = font(150)
            stroke_text(d, (W / 2, 1530), s, f, YEL, sw=8, anchor="mm")
            d.text((W / 2, 1640), lab, font=font(40, False), fill=WHITE, anchor="mm")
        else:
            s = st[1]; a2 = back(g)
            f = font(72 * max(0.3, a2))
            while d.textlength(s, font=f) > W - 140: f = font(f.size - 3)
            tw = d.textlength(s, font=f)
            d.rounded_rectangle([(W - tw) / 2 - 30, 1480, (W + tw) / 2 + 30, 1590], 18, fill=RED)
            d.text((W / 2, 1535), s, font=f, fill=WHITE, anchor="mm")
    meter(d, 11 - r, (t - 0.3) / 0.8, y=1800)
    if r == 1:
        tc = word_time(k, "cabe", D * 0.75) + 0.12
        if t > tc:
            a3 = back((t - tc) / 0.3)
            s = "CABE NA PONTA DO DEDO"
            f = font(66 * max(0.3, a3)); tw = d.textlength(s, font=f)
            d.rounded_rectangle([(W - tw) / 2 - 28, BOXY + 40, (W + tw) / 2 + 28, BOXY + 130], 16, fill=YEL)
            d.text((W / 2, BOXY + 85), s, font=f, fill=BLACK, anchor="mm")
    return fx(img, t, big=(r == 1), tn=tn)

def frame_intro(t, D):
    j = min(9, int(t / 0.32)); i = (j % 9) if t <= 3.2 else 3
    img = backdrop(10)
    im, mask = card(i, (t % 0.32) + 0.5, 1.5, 1.15, 1.3)
    img.paste(ImageEnhance.Brightness(im).enhance(0.55), (0, BOXY))
    d = ImageDraw.Draw(img)
    d.line([(0, BOXY), (W, BOXY)], fill=RED, width=6); d.line([(0, BOXY + BOXH), (W, BOXY + BOXH)], fill=RED, width=6)
    tape(d, 0, 22, t); tape(d, H - 22, 22, -t)
    stroke_text(d, (W / 2, 240), "⚠", font(120), YEL, sw=6, anchor="mm") if False else None
    a = back(t / 0.35)
    stroke_text(d, (W / 2, 230), "RANKEEI OS 10", font(90), WHITE, sw=9, anchor="mm")
    stroke_text(d, (W / 2, 640), "ANIMAIS", font(190 * max(0.3, a)), YEL, sw=14, anchor="mm")
    stroke_text(d, (W / 2, 830), "MAIS PERIGOSOS", font(110), RED, sw=10, anchor="mm")
    stroke_text(d, (W / 2, 980), "DO BRASIL", font(110), WHITE, sw=10, anchor="mm")
    tn = word_time(0, "número", 2.5)
    if t > tn:
        a2 = back((t - tn) / 0.3); s = "O Nº 1 PODE ESTAR NO SEU QUARTO"
        f = font(54 * max(0.3, a2)); tw = d.textlength(s, font=f)
        d.rounded_rectangle([(W - tw) / 2 - 26, 1500, (W + tw) / 2 + 26, 1590], 14, fill=YEL)
        d.text((W / 2, 1545), s, font=f, fill=BLACK, anchor="mm")
    d.text((60, 58), "RANKEADO BR", font=font(32), fill=YEL)
    a4 = ease((t - 0.6) / 0.4)
    if a4 > 0:
        c = tuple(int(14 + (v - 14) * a4) for v in WHITE)
        d.text((W / 2, 1720), "ASSISTA ATÉ O Nº 1", font=font(46), fill=c, anchor="mm")
        meter(d, 10 * min(1, t / 3.2), 1, y=1790) if False else None
    if t < 3.2 and int(t / 0.32) != int(max(0, t - 1 / FPS) / 0.32):
        img = Image.blend(img, Image.new("RGB", (W, H), WHITE), 0.35)
    return img

CRED = None
def frame_outro(t, D):
    img = Image.new("RGB", (W, H), DARK)
    cw, chh = W // 2, 300
    for j in range(10):
        r = 9 - j
        tile = fg(r).resize((cw, int(cw * BOXH / BOXW)))
        y0 = (tile.height - chh) // 2; tile = ImageEnhance.Brightness(tile.crop((0, y0, cw, y0 + chh))).enhance(0.65)
        x, y = (j % 2) * cw, 160 + (j // 2) * chh
        a = ease((t - j * 0.05) / 0.25)
        if a <= 0: continue
        img.paste(tile, (x, int(y + (1 - a) * 80)))
        stroke_text(ImageDraw.Draw(img), (x + 20, y + 16), f"#{B[r][0]}", font(54), YEL, sw=5)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 160], fill=DARK); d.text((60, 70), "RANKEADO BR", font=font(32), fill=YEL)
    if t > 0.3:
        a = back((t - 0.3) / 0.35)
        d.rounded_rectangle([60, 700, W - 60, 1180], 30, fill=BLACK)
        stroke_text(d, (W / 2, 800), "QUAL ANIMAL", font(100), WHITE, sw=6, anchor="mm")
        stroke_text(d, (W / 2, 940), "FALTOU?", font(150 * max(0.3, a)), YEL, sw=8, anchor="mm")
        d.text((W / 2, 1090), "comenta aí", font=font(50, False), fill=WHITE, anchor="mm")
    if t > 1.2:
        d.rounded_rectangle([160, 1200, W - 160, 1290], 45, fill=YEL)
        d.text((W / 2, 1245), "SEGUE O @RANKEADOBR", font=font(52), fill=BLACK, anchor="mm")
    if t > D - 2.6:
        d.rectangle([0, 1660, W, H], fill=BLACK); y = 1672
        for line in CRED: d.text((30, y), line, font=font(17, False), fill=(190, 190, 200)); y += 21
    return img

def scene_fn(k):
    if k == 0: return frame_intro
    if k == 11: return frame_outro
    return lambda t, D: frame_item(k - 1, t, D)

def render_scene(k, D, out):
    random.seed(k); n = int(round(D * FPS)); tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    fn = scene_fn(k)
    for i in range(n): p.stdin.write(fn(i / FPS, D).tobytes())
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
        if len(cur) + len(p_) > 105: lines.append(cur); cur = ""
        cur += ("  ·  " if cur else "") + p_
    lines.append(cur); lines.append('Trilha: "Hitman" Kevin MacLeod (incompetech.com) · CC BY 4.0')
    return lines

if __name__ == "__main__":
    CRED = credits()
    mode = sys.argv[1]; durs = json.load(open(sys.argv[2]))
    if mode == "stills":
        for k, t in [(0, 3.0), (4, 3.5), (8, 3.0), (10, 7.8), (11, durs[11] - 1)]:
            scene_fn(k)(t, durs[k]).save(f"st_{k}.png")
    elif mode == "credits":
        print("\n".join(CRED))
    else:
        for k in [int(x) for x in sys.argv[3:]] or range(12):
            render_scene(k, durs[k], f"sc_{k:02d}.mp4")
