import sys, json, subprocess, os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
_fc = {}
def font(sz, bold=True):
    k = (int(sz), bold)
    if k not in _fc: _fc[k] = ImageFont.truetype(FB if bold else FR, int(sz))
    return _fc[k]
YEL = (255, 204, 0); WHITE = (255, 255, 255); BLACK = (0, 0, 0); DARK = (14, 14, 18)
FOT = "/home/claude/rk/fotos/"
B = [  # rank, name, place, meters, photo, focus-x
 (10, "CITIC TOWER", "Pequim · China", 528, "b10_w.jpg", 0.5),
 (9, "TIANJIN CTF", "Tianjin · China", 530, "b09_0.jpg", 0.5),
 (8, "GUANGZHOU CTF", "Guangzhou · China", 530, "b08_w.jpg", 0.27),
 (7, "ONE WORLD TRADE CENTER", "Nova York · EUA", 541, "b07_1.jpg", 0.5),
 (6, "LOTTE WORLD TOWER", "Seul · Coreia do Sul", 555, "b06_f2.jpg", 0.55),
 (5, "PING AN FINANCE CENTER", "Shenzhen · China", 599, "b05_f1.jpg", 0.5),
 (4, "ABRAJ AL-BAIT", "Meca · Arábia Saudita", 601, "b04_1.jpg", 0.5),
 (3, "SHANGHAI TOWER", "Xangai · China", 632, "b03_w.jpg", 0.45),
 (2, "MERDEKA 118", "Kuala Lumpur · Malásia", 679, "b02_f1.jpg", 0.5),
 (1, "BURJ KHALIFA", "Dubai · Emirados Árabes", 828, "b01_1.jpg", 0.5),
]
FIX = {"RANQUEI": "RANKEEI", "CEU": "SEUL", "5º": "QUINTO", "-BAIT": "AL-BAIT", "TORRES": "TORRES"}
WORDS = json.load(open("/home/claude/rk/words.json"))

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- photos: prepared tall cover image for a tilt-up pan ----------
PW, PH = 1188, 2400
_ph = {}
def photo(i):
    if i in _ph: return _ph[i]
    _, _, _, _, f, fx = B[i]
    im = Image.open(FOT + f).convert("RGB")
    s = max(PW / im.width, PH / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    cx = int(im.width * fx); x0 = max(0, min(im.width - PW, cx - PW // 2))
    y0 = (im.height - PH) // 2
    im = im.crop((x0, y0, x0 + PW, y0 + PH))
    im = ImageEnhance.Contrast(im).enhance(1.12); im = ImageEnhance.Color(im).enhance(1.15)
    _ph[i] = im; return im

def pan(im, p, zoom):
    # p: 0 bottom -> 1 top ; zoom >= 1
    cw, ch = W / zoom * (PW / W) * (W / PW), H / zoom
    cw = W / zoom; ch = H / zoom
    sx = (PW - cw) / 2
    sy = (PH - ch) * (1 - p)
    return im.resize((W, H), Image.BILINEAR, box=(sx, sy, sx + cw, sy + ch))

def grad():
    g = Image.new("L", (1, H))
    for y in range(H):
        a = 0
        if y < 520: a = 170 * (1 - y / 520) ** 1.4
        if y > 1150: a = max(a, 235 * ((y - 1150) / (H - 1150)) ** 1.1)
        g.putpixel((0, y), int(a))
    return g.resize((W, H))
GRAD = grad()
BLACKIM = Image.new("RGB", (W, H), BLACK)

def shade(img):
    return Image.composite(BLACKIM, img, GRAD)

def stroke_text(d, xy, s, f, fill, sw=8, anchor="la"):
    d.text(xy, s, font=f, fill=fill, stroke_width=sw, stroke_fill=BLACK, anchor=anchor)

def caption(d, k, t):
    ws = WORDS[k]
    # merge short words with next
    groups, buf = [], None
    for w in ws:
        txt = w["w"].upper().strip(".,!?")
        txt = FIX.get(txt, txt)
        if txt == "AL" : buf = buf or dict(w, txt="", t0=w["t0"]); continue
        if buf is not None:
            txt = (buf["txt"] + " " + txt).strip(); g = {"txt": txt, "t0": buf["t0"], "t1": w["t1"]}; buf = None
        else:
            g = {"txt": txt, "t0": w["t0"], "t1": w["t1"]}
        if txt == "PING" or (len(txt) <= 2 and not any(c.isdigit() for c in txt)):
            buf = g; continue
        groups.append(g)
    cur = None
    for g in groups:
        if g["t0"] - 0.05 <= t: cur = g
    if cur is None or t > cur["t1"] + 0.6: return
    a = (t - cur["t0"] + 0.05) / 0.12
    sz = 112 * (1 + 0.25 * (1 - ease(a)))
    num = any(c.isdigit() for c in cur["txt"])
    f = font(sz)
    while d.textlength(cur["txt"], font=f) > W - 80 and sz > 50: sz -= 6; f = font(sz)
    stroke_text(d, (W / 2, 1010), cur["txt"], f, YEL if num else WHITE, sw=10, anchor="mm")

def first_num_time(k):
    for w in WORDS[k]:
        if any(c.isdigit() for c in w["w"]): return w["t0"]
    return 1.2

def pips(d, k):
    x = W - 60 - 10 * 34
    for j in range(10):
        on = j < k
        d.rounded_rectangle([x + j * 34, 74, x + j * 34 + 24, 98], 6, fill=YEL if on else (255, 255, 255), outline=None)
    d.text((60, 70), "RANKEADO BR", font=font(32), fill=YEL)

def minichart(d, k, grow):
    x0, y1, h = 690, 1840, 300
    d.rounded_rectangle([x0 - 20, y1 - h - 40, W - 30, y1 + 16], 18, fill=(0, 0, 0))
    bw = 30; gap = 4
    ey = y1 - h * 330 / 828
    for x in range(x0, W - 50, 14): d.line([(x, ey), (x + 7, ey)], fill=(170, 170, 180), width=2)
    d.text((x0, ey - 26), "EIFFEL", font=font(18), fill=(170, 170, 180))
    for j in range(k):
        m = B[j][3]; hh = h * m / 828 * (ease(grow) if j == k - 1 else 1)
        bx = x0 + j * (bw + gap)
        d.rectangle([bx, y1 - hh, bx + bw, y1], fill=YEL if j == k - 1 else (90, 92, 104))

def frame_item(i, t, D):
    k = i + 1
    r, name, place, m, _, _ = B[i]
    p = ease(t / D) * 0.85 + 0.1 if r != 1 else min(1, t / (D * 0.6))
    zoom = 1.10 - 0.06 * (t / D)
    img = shade(pan(photo(i), p, zoom))
    d = ImageDraw.Draw(img)
    pips(d, k)
    # rank slam
    a = t / 0.22; sc = 1 + 1.6 * (1 - ease(a))
    stroke_text(d, (60, 345), f"#{r}", font(250 * sc if t < 0.22 else 250), YEL, sw=12, anchor="ls")
    caption(d, k, t - 0.12)
    # name box slides in
    a = ease((t - 0.25) / 0.3); off = int(-W * (1 - a))
    nf = font(64)
    while d.textlength(name, font=nf) > W - 140: nf = font(nf.size - 4)
    tw = d.textlength(name, font=nf)
    d.rounded_rectangle([50 + off, 1380, 50 + off + tw + 44, 1470], 14, fill=YEL)
    d.text((72 + off, 1425), name, font=nf, fill=BLACK, anchor="lm")
    d.text((60 + off, 1500), place, font=font(44, False), fill=WHITE)
    # height counter tied to the spoken number
    tn = first_num_time(k) + 0.12
    g = (t - tn + 0.25) / 0.55
    if g > 0:
        val = int(round(m * ease(g)))
        stroke_text(d, (55, 1600), f"{val}", font(170), WHITE, sw=6)
        vw = d.textlength(f"{val}", font=font(170))
        d.text((70 + vw, 1700), "m", font=font(80), fill=YEL)
    minichart(d, k, g)
    if r == 1:
        isso = next((w["t0"] for w in WORDS[k] if w["w"].lower().startswith("isso")), D * 0.55) + 0.12
        if t > isso:
            a2 = ease((t - isso) / 0.25)
            s = "≈ 2,5 TORRES EIFFEL"
            f = font(70 * (0.6 + 0.4 * a2))
            tw = d.textlength(s, font=f)
            d.rounded_rectangle([(W - tw) / 2 - 30, 560, (W + tw) / 2 + 30, 660], 16, fill=YEL)
            d.text((W / 2, 610), s, font=f, fill=BLACK, anchor="mm")
    img = fx(img, t, big=(r == 1 and abs(t - tn) < 0.5), tn=tn)
    return img

def fx(img, t, big=False, tn=0):
    # flash + shake at cut, extra punch on #1 number
    amp = 0
    if t < 0.25: amp = 22 * (1 - t / 0.25)
    if big and t >= tn: amp = max(amp, 30 * max(0, 1 - (t - tn) / 0.45))
    if amp > 0:
        dx, dy = random.uniform(-amp, amp), random.uniform(-amp, amp)
        img = img.transform((W, H), Image.AFFINE, (1, 0, dx, 0, 1, dy), fillcolor=BLACK)
    fl = 0
    if t < 0.1: fl = 0.55 * (1 - t / 0.1)
    if big and 0 <= t - tn < 0.12: fl = max(fl, 0.7 * (1 - (t - tn) / 0.12))
    if fl > 0: img = Image.blend(img, Image.new("RGB", (W, H), WHITE), fl)
    return img

def frame_intro(t, D):
    j = min(9, int(t / 0.34))
    i = j  # 10 -> 1 quick montage
    if t > 3.4: i = 9
    loc = (t - j * 0.34) if t <= 3.4 else t - 3.4
    img = pan(photo(i), 0.4 + 0.3 * min(1, loc / 1.5), 1.25 - 0.08 * min(1, loc / 1.5))
    img = Image.blend(img, BLACKIM, 0.45)
    d = ImageDraw.Draw(img)
    a = back(t / 0.35)
    stroke_text(d, (W / 2, 560), "RANKEEI OS", font(86), WHITE, sw=8, anchor="mm")
    stroke_text(d, (W / 2, 720), "10 PRÉDIOS", font(150 * max(0.3, a)), YEL, sw=12, anchor="mm")
    stroke_text(d, (W / 2, 880), "MAIS ALTOS", font(130), WHITE, sw=10, anchor="mm")
    stroke_text(d, (W / 2, 1030), "DO MUNDO", font(130), WHITE, sw=10, anchor="mm")
    tn = next((w["t0"] for w in WORDS[0] if w["w"].lower().startswith("número")), 2.5)
    if t > tn:
        a2 = ease((t - tn) / 0.25)
        s = "O Nº 1 VAI TE DEIXAR TONTO"
        f = font(56)
        tw = d.textlength(s, font=f)
        d.rounded_rectangle([(W - tw) / 2 - 26, 1180, (W + tw) / 2 + 26, 1270], 14, fill=YEL)
        d.text((W / 2, 1225), s, font=f, fill=BLACK, anchor="mm")
    d.text((60, 70), "RANKEADO BR", font=font(32), fill=YEL)
    if j != int(max(0, t - 1 / FPS) / 0.34) and t < 3.4:
        img = Image.blend(img, Image.new("RGB", (W, H), WHITE), 0.35)
    return img

CRED = None
def frame_outro(t, D):
    img = Image.new("RGB", (W, H), DARK)
    cw, chh = W // 2, 300
    for j in range(10):
        r = 9 - j  # #1 first
        tile = photo(r).resize((cw, int(cw * PH / PW)))
        y0 = (tile.height - chh) // 2
        tile = tile.crop((0, y0, cw, y0 + chh))
        tile = ImageEnhance.Brightness(tile).enhance(0.65)
        x, y = (j % 2) * cw, 160 + (j // 2) * chh
        a = ease((t - j * 0.05) / 0.25)
        if a <= 0: continue
        img.paste(tile, (x, int(y + (1 - a) * 80)))
        dd = ImageDraw.Draw(img)
        stroke_text(dd, (x + 20, y + 16), f"#{B[r][0]}", font(54), YEL, sw=5)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 160], fill=DARK)
    d.text((60, 70), "RANKEADO BR", font=font(32), fill=YEL)
    a = back((t - 0.3) / 0.35)
    if t > 0.3:
        d.rounded_rectangle([60, 700, W - 60, 1180], 30, fill=(0, 0, 0))
        stroke_text(d, (W / 2, 800), "QUAL PRÉDIO", font(100), WHITE, sw=6, anchor="mm")
        stroke_text(d, (W / 2, 940), "FALTOU?", font(150 * max(0.3, a)), YEL, sw=8, anchor="mm")
        d.text((W / 2, 1090), "comenta aí 👇".replace("👇", ""), font=font(50, False), fill=WHITE, anchor="mm")
    if t > 1.2:
        d.rounded_rectangle([160, 1200, W - 160, 1290], 45, fill=YEL)
        d.text((W / 2, 1245), "SEGUE O @RANKEADOBR", font=font(52), fill=BLACK, anchor="mm")
    if t > D - 2.6:
        d.rectangle([0, 1660, W, H], fill=(0, 0, 0))
        y = 1672
        for line in CRED:
            d.text((30, y), line, font=font(17, False), fill=(190, 190, 200)); y += 21
    return img

def scene_fn(k):
    if k == 0: return frame_intro
    if k == 11: return frame_outro
    return lambda t, D: frame_item(k - 1, t, D)

def render_scene(k, D, out):
    random.seed(k)
    n = int(round(D * FPS)); tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "19",
        "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    fn = scene_fn(k)
    for i in range(n): p.stdin.write(fn(i / FPS, D).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, out)

def credits():
    meta = json.load(open(FOT + "meta.json"))
    parts = []
    for b in B:
        mm = meta[b[4]]; lic = mm["license"].replace("CC ", "")
        parts.append(f"#{b[0]} {mm['creator']} ({'CC ' + lic if 'CC' not in lic else lic})")
    lines, cur = ["Fotos via Wikimedia Commons / Flickr:"], ""
    for p_ in parts:
        if len(cur) + len(p_) > 105: lines.append(cur); cur = ""
        cur += ("  ·  " if cur else "") + p_
    lines.append(cur)
    lines.append('Trilha: "Volatile Reaction" Kevin MacLeod (incompetech.com) · CC BY 4.0')
    return lines

if __name__ == "__main__":
    CRED = credits()
    mode = sys.argv[1]; durs = json.load(open(sys.argv[2]))
    if mode == "stills":
        for k, t in [(0, 3.0), (4, 2.5), (10, 6.5), (11, durs[11] - 1)]:
            scene_fn(k)(t, durs[k]).save(f"s2_{k}.png")
    else:
        for k in [int(x) for x in sys.argv[3:]] or range(12):
            render_scene(k, durs[k], f"sc2_{k:02d}.mp4")
