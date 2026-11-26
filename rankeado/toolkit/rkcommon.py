import json, subprocess, os, random, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops, ImageOps

W, H, FPS = 1080, 1920, 30
FD = "/home/claude/fonts/"
_fc = {}
def F(kind, sz):
    sz = max(8, int(sz)); k = (kind, sz)
    if k in _fc: return _fc[k]
    if kind == "an": f = ImageFont.truetype(FD + "Anton-Regular.ttf", sz)
    elif kind == "mono": f = ImageFont.truetype(FD + "ShareTechMono-Regular.ttf", sz)
    elif kind == "os": f = ImageFont.truetype(FD + "Oswald[wght].ttf", sz); f.set_variation_by_name("SemiBold")
    elif kind == "osb": f = ImageFont.truetype(FD + "Oswald[wght].ttf", sz); f.set_variation_by_name("Bold")
    elif kind == "pf": f = ImageFont.truetype(FD + "PlayfairDisplay[wght].ttf", sz); f.set_variation_by_name("Black")
    elif kind == "pfb": f = ImageFont.truetype(FD + "PlayfairDisplay[wght].ttf", sz); f.set_variation_by_name("Bold")
    elif kind == "pfi": f = ImageFont.truetype(FD + "PlayfairDisplay-Italic[wght].ttf", sz); f.set_variation_by_axes([500])
    _fc[k] = f; return f

WHITE = (255, 255, 255); BLACK = (0, 0, 0); GOLD = (255, 214, 90)
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def ease2(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def lerp(a, b, u): return a + (b - a) * u
def mixc(a, b, u): return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))

NUMS = set("dois duas três quatro cinco seis sete oito nove dez onze doze treze vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento duzentos duzentas trezentos trezentas quatrocentos quinhentos seiscentos setecentos setecentas oitocentos novecentos mil milhão milhões vírgula".split())

class Words:
    def __init__(self, d, fix=None):
        self.W = json.load(open(f"{d}/words.json")); self.fix = fix or {}
        self.G = [self.groups(k) for k in range(len(self.W))]
    def time_of(self, k, key, default=2.0):
        for w in self.W[k]:
            if w["w"].lower().strip(".,!?:") == key.lower(): return w["t0"]
        for w in self.W[k]:
            if key.lower() in w["w"].lower(): return w["t0"]
        return default
    def first_num(self, k, default=2.5):
        for j, w in enumerate(self.W[k]):
            if j >= 2 and w["w"].lower().strip(".,!?:") in NUMS: return w["t0"]
        return default
    def groups(self, k):
        gs = []; buf = None
        for w in self.W[k]:
            txt = w["w"].upper().strip(",!?:")
            if txt.endswith("..."): txt = txt[:-3]
            if (txt.startswith("-") or txt.startswith(",") or txt.startswith(".")) and gs:
                gs[-1]["txt"] += txt.strip(".,"); gs[-1]["t1"] = w["t1"]; continue
            txt = txt.rstrip(".")
            if buf is not None: g = {"txt": (buf["txt"] + " " + txt).strip(), "t0": buf["t0"], "t1": w["t1"]}; buf = None
            else: g = {"txt": txt, "t0": w["t0"], "t1": w["t1"]}
            orig = w["w"].strip(".,!?:")
            if len(g["txt"]) <= 2 and not any(c.isdigit() for c in g["txt"]) and not (orig.isupper() and len(orig) >= 2): buf = g; continue
            g["num"] = any(x.lower() in NUMS for x in g["txt"].split())
            gs.append(g)
        if buf is not None: buf["num"] = False; gs.append(buf)
        for g in gs: g["txt"] = self.fix.get(g["txt"], g["txt"])
        return gs
    def caption(self, img, k, t, y, size=92, col=WHITE, numcol=GOLD, stroke=BLACK):
        d = ImageDraw.Draw(img); cur = None
        for g in self.G[k]:
            if g["t0"] - 0.05 <= t: cur = g
        if cur is None or t > cur["t1"] + 0.5: return
        a = (t - cur["t0"] + 0.05) / 0.12; sz = size * (1 + 0.22 * (1 - ease(a)))
        f = F("an", sz)
        while d.textlength(cur["txt"], font=f) > W - 90 and sz > 46: sz -= 6; f = F("an", sz)
        d.text((W / 2, y), cur["txt"], font=f, fill=numcol if cur["num"] else col, anchor="mm", stroke_width=9, stroke_fill=stroke)

def cover(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height); nw, nh = int(im.width * s + 1), int(im.height * s + 1)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = int((nw - w) * fx); y = int((nh - h) * fy); return im.crop((x, y, x + w, y + h))

def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255); return m

def shadow(img, box, r=30, blur=30, alpha=150, off=(0, 18)):
    x0, y0, x1, y1 = [int(v) for v in box]
    pad = blur * 2; sh = Image.new("L", (x1 - x0 + pad * 2, y1 - y0 + pad * 2), 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), r, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    img.paste((0, 0, 0), (x0 - pad + off[0], y0 - pad + off[1]), sh)

def render_scene(fn, k, D, out):
    n = int(round(D * FPS)); tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n):
        random.seed(k * 10000 + i); p.stdin.write(fn(i / FPS, D).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, out)

def lic(m):
    l = m["license"].upper(); v = m.get("lv") or ""
    return "domínio público" if l in ("CC0", "PDM") else f"CC {l} {v}".strip()

def credit_lines(meta, items, head, music):
    parts = [f"#{r} {meta[f].get('creator') or 'autor desconhecido'} ({lic(meta[f])})" for r, f in items]
    lines, cur = [head], ""
    for p_ in parts:
        if len(cur) + len(p_) > 98: lines.append(cur); cur = ""
        cur += ("  ·  " if cur else "") + p_
    lines.append(cur); lines.append(music); return lines

def main(scene_fn, durs_path, nscenes, prefix, stills):
    mode = sys.argv[1]; durs = json.load(open(durs_path))
    if mode == "stills":
        for k, t in stills(durs):
            random.seed(1); scene_fn(k)(t, durs[k]).convert("RGB").save(f"{prefix}_{k}_{round(t,1)}.png")
    else:
        ks = [int(x) for x in sys.argv[2:]] or range(nscenes)
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(4) as ex:
            list(ex.map(_rs, [(scene_fn, k, durs[k], f"{prefix}_{k:02d}.mp4") for k in ks]))

def _rs(a):
    fn, k, D, out = a; render_scene(fn(k), k, D, out)
