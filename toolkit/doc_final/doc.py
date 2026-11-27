"""Engine do mini-documentário 16:9 (1920x1080). Uso: python3 doc.py <cap> prev t... | part k K | final K"""
import sys, os, json, math, re, functools, subprocess, difflib, unicodedata
sys.path.insert(0, "/home/claude/ep1/v2"); sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); sys.path.insert(0, "/home/claude/doc")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
from gfx import font, ease, back, paste, text_el, chip, stamp, rays, odometer, confetti, AMB, WHITE, RED, GREEN, INK
from fonts import F
import fotos_cc
W, H, FPS = 1920, 1080, 30
LOG = "/home/claude/work/logos/"
FC = "/home/claude/videos-sylence/assets/fotos_cc/"; DF = "/home/claude/doc/fotos/"
P = dict(cent=DF + "cent/cc_25ab1e64.jpg", pennant=DF + "est68/cc_f931b322.jpg", allianz=DF + "torcida/cc_04452f33.jpg", torcida=DF + "torcida/cc_49d3645c.jpg",
         campo=DF + "torcida/cc_bca833ce.jpg", laplata=DF + "veron/cc_085710b0.jpg", brujas=DF + "veron/cc_093efe19.jpg", veron=DF + "veron/cc_a24691a9.jpg",
         abel1=FC + "abel/cc_e1b75bde.jpg", abel2=FC + "abel/cc_e4571f8d.jpg", centw=FC + "est/cc_a8e55cb3.jpg", centw2=FC + "est/cc_b4477b36.jpg",
         centst=FC + "est/cc_fbfbb3a9.jpg", flaco=FC + "fl/cc_cf8f1bef.jpg", musgs=FC + "mus/cc_30d9a437.jpg", musuy=FC + "mus/cc_bc7b8486.jpg", musgol=FC + "mus/cc_c408ab38.jpg")
GOLD = (255, 205, 60); NAVY = (12, 18, 32); SEP = (214, 190, 150)


def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())


# ---------------- imagens ----------------
@functools.lru_cache(40)
def photo(key, mode="color"):
    im = Image.open(P.get(key, key)).convert("RGB")
    if mode == "sepia":
        g = ImageOps.grayscale(im); im = ImageOps.colorize(g, (30, 22, 12), (240, 222, 190))
    elif mode == "gray": im = ImageOps.grayscale(im).convert("RGB")
    else: im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.1)).enhance(1.06)
    return im


def cover(im, z=1.0, fx=0.5, fy=0.5):
    r = W / H; w, h = im.size
    if w / h > r: ch = h / z; cw = ch * r
    else: cw = w / z; ch = cw / r
    x0 = (w - cw) * fx; y0 = (h - ch) * fy
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)


def kb(img, key, t, dur, mode="color", z=(1.04, 1.16), f0=(0.5, 0.5), f1=(0.5, 0.45), dim=110, blur=0):
    u = min(1, t / max(dur, 0.1)); zz = z[0] + (z[1] - z[0]) * u
    fr = cover(photo(key, mode), zz, f0[0] + (f1[0] - f0[0]) * u, f0[1] + (f1[1] - f0[1]) * u)
    if blur: fr = fr.filter(ImageFilter.GaussianBlur(blur))
    img.paste(fr.convert("RGBA"), (0, 0))
    if dim: img.alpha_composite(vig(dim))
    S.cred = fotos_cc.credito(P.get(key, key))


@functools.lru_cache(8)
def vig(a):
    v = Image.new("L", (W, H), 0); d = ImageDraw.Draw(v); d.ellipse((-W * .25, -H * .35, W * 1.25, H * 1.35), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220)); m = Image.new("RGBA", (W, H), (0, 0, 0, a))
    m.putalpha(Image.eval(v, lambda x: int((255 - x) * a / 255 + a * 0.45))); return m


@functools.lru_cache(16)
def _grad(top, bot):
    a = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top)[None, None] * (1 - a) + np.array(bot)[None, None] * a).repeat(W, 1).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")


PAL_ = {"navy": ((16, 26, 48), (6, 8, 16)), "green": ((18, 90, 52), (4, 22, 12)), "sepia": ((70, 56, 38), (20, 15, 10)), "red": ((110, 20, 26), (20, 4, 6)), "gray": ((48, 50, 56), (10, 10, 12))}
BGP = {"c1": ("centw", "sepia"), "c2": ("centw", "gray"), "c3": ("campo", "color"), "c4": ("laplata", "color"), "c5": ("allianz", "color"), "c6": ("cent", "color")}
TINT = {"navy": (14, 22, 44), "green": (10, 70, 40), "sepia": (60, 44, 24), "red": (100, 14, 20), "gray": (30, 30, 34)}


@functools.lru_cache(24)
def _bgphoto(key, mode, tint):
    im = cover(photo(key, mode), 1.08).filter(ImageFilter.GaussianBlur(24)).convert("RGBA")
    im = Image.blend(im, Image.new("RGBA", (W, H), TINT[tint] + (255,)), 0.72)
    return im


@functools.lru_cache(6)
def _grain(k):
    rng = np.random.default_rng(k); a = rng.integers(0, 14, (H // 3, W // 3), dtype=np.uint8)
    g = Image.fromarray(a, "L").resize((W, H)); m = Image.new("RGBA", (W, H), (255, 240, 210, 0)); m.putalpha(g); return m


def bgc(img, key, T):
    pk, mode = BGP.get(S.cid, ("cent", "color"))
    bp = _bgphoto(pk, mode, key); off = 20 * math.sin(T * 0.15)
    img.paste(bp, (int(off) - 20, 0)); img.paste(bp.crop((W - 40, 0, W, H)), (W - 40 + int(off) + 20, 0)) if off > 0 else None
    img.alpha_composite(vig(110))
    if mode == "sepia": img.alpha_composite(_grain(int(T * 12) % 6))


@functools.lru_cache(64)
def logo(k, h):
    im = Image.open(LOG + k + ".png").convert("RGBA"); im = im.crop(im.getchannel("A").getbbox()); h = int(h)
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


@functools.lru_cache(64)
def badge(txt, h, c1, c2, stripes=True):
    h = int(h); w = int(h * 0.82); im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon([(0, 0), (w, 0), (w, h * .58), (w / 2, h), (0, h * .58)], fill=255)
    s = Image.new("RGBA", (w, h), c1); sd = ImageDraw.Draw(s)
    if stripes:
        for k in range(1, 7, 2): sd.rectangle((k * w / 7, 0, (k + 1) * w / 7, h), fill=c2)
    im.paste(s, (0, 0), m); d = ImageDraw.Draw(im)
    d.line([(0, 0), (w, 0), (w, h * .58), (w / 2, h), (0, h * .58), (0, 0)], fill=INK, width=max(4, h // 35))
    d.text((w / 2, h * .36), txt, font=font("blk", int(h * (0.22 if len(txt) < 5 else 0.15))), fill=WHITE, anchor="mm", stroke_width=max(3, h // 45), stroke_fill=INK)
    return im


CREST = {"PEÑ": ("PEÑ", (250, 200, 0), (20, 20, 20)), "BOC": ("BOCA", (20, 40, 120), (250, 200, 0)), "CAL": ("CALI", (30, 120, 60), (240, 240, 240)),
         "CER": ("CERRO", (200, 20, 30), (20, 40, 140)), "LDU": ("LDU", (245, 245, 245), (200, 20, 40)), "UC": ("UC", (20, 60, 160), (245, 245, 245))}
def crest(k, h):
    if os.path.exists(LOG + k + ".png"): return logo(k, h)
    t, a, b = CREST[k]; return badge(t, h, a, b, k not in ("LDU", "UC"))


def tx(s, size, col=WHITE, f="anton", stroke=6):
    return text_el(s, F(f, size), col, stroke)


def pop(img, el, x, y, t, t0=0.0, dur=0.3, rot=0, alpha=1.0):
    if t < t0: return
    paste(img, el, x, y, alpha, 0.2 + 0.8 * back((t - t0) / dur), rot)


def slide(img, el, x, y, t, t0=0.0, dx=-600, dur=0.4):
    if t < t0: return
    u = ease((t - t0) / dur); paste(img, el, x + dx * (1 - u), y, u)


def shake(t, t0, amp=16, dur=0.3):
    return amp * (1 - (t - t0) / dur) * math.sin((t - t0) * 80) if t0 <= t <= t0 + dur else 0


def scorebox(a, b, ga, gb, sz=150, sub=None, grey=False):
    w = int(sz * 6.4); h = int(sz * 1.75) + (int(sz * 0.55) if sub else 0); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 34, fill=(12, 14, 20, 235), outline=(200, 200, 200) if grey else WHITE, width=5)
    hb = int(sz * 1.75); la, lb = crest(a, sz), crest(b, sz)
    im.alpha_composite(la, (int(sz * 1.0 - la.width / 2), int(hb / 2 - la.height / 2))); im.alpha_composite(lb, (int(w - sz * 1.0 - lb.width / 2), int(hb / 2 - lb.height / 2)))
    d.text((w / 2, hb / 2), f"{ga} x {gb}", font=F("anton", sz * 0.95), fill=(170, 170, 170) if grey else WHITE, anchor="mm")
    if sub: d.text((w / 2, hb + sz * 0.2), sub, font=font("blk", sz * 0.27), fill=AMB, anchor="mm")
    return im


def datestamp(s, sz=44):
    return chip(s, sz, INK, AMB)


def trophy(h, col=GOLD):
    h = int(h); w = int(h * 0.8); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.pieslice((w * 0.12, -h * 0.25, w * 0.88, h * 0.62), 0, 180, fill=col, outline=INK, width=6)
    d.arc((0, h * 0.05, w * 0.26, h * 0.38), 90, 270, fill=INK, width=8); d.arc((w * 0.74, h * 0.05, w, h * 0.38), -90, 90, fill=INK, width=8)
    d.rectangle((w * 0.43, h * 0.6, w * 0.57, h * 0.78), fill=col, outline=INK, width=5)
    d.rounded_rectangle((w * 0.25, h * 0.78, w * 0.75, h * 0.96), 10, fill=(40, 40, 40), outline=INK, width=5)
    return im


def xmark(sz, ok=False):
    sz = int(sz); im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, sz, sz), fill=GREEN if ok else RED, outline=INK, width=5)
    if ok: d.line([(sz * .25, sz * .52), (sz * .43, sz * .7), (sz * .76, sz * .32)], fill=WHITE, width=int(sz * .12))
    else: d.line([(sz * .3, sz * .3), (sz * .7, sz * .7)], fill=WHITE, width=int(sz * .12)); d.line([(sz * .7, sz * .3), (sz * .3, sz * .7)], fill=WHITE, width=int(sz * .12))
    return im


def namecard(name, sub, w=520, col=(20, 120, 60)):
    h = 150; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 20, fill=(14, 16, 22, 235), outline=WHITE, width=4); d.rectangle((0, 0, 16, h), fill=col)
    d.text((40, 52), name, font=F("anton", 62), fill=WHITE, anchor="lm"); d.text((40, 112), sub, font=font("blk", 30), fill=AMB, anchor="lm")
    return im


def polaroid(key, w, mode="color", rot=0):
    im = photo(key, mode).copy(); im.thumbnail((w, w * 1.4)); b = int(w * 0.04)
    c = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b + int(b * 2.5)), (245, 245, 240, 255)); c.paste(im, (b, b))
    s = Image.new("RGBA", (c.width + 60, c.height + 60), (0, 0, 0, 0)); ImageDraw.Draw(s).rectangle((30, 40, c.width + 30, c.height + 40), fill=(0, 0, 0, 140))
    s = s.filter(ImageFilter.GaussianBlur(14)); s.alpha_composite(c, (30, 30)); return s


def pitch(w, h, t, path=None, t0=0.0, dur=1.2, col=(255, 255, 255)):
    """campinho 2D (metade, gol à direita) com bola percorrendo 'path' [(x,y) normalizados]"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 24, fill=(24, 110, 58, 240))
    for k in range(8): d.rectangle((k * w / 8, 0, (k + .5) * w / 8, h), fill=(30, 122, 64, 240))
    lw = 5; d.rounded_rectangle((0, 0, w, h), 24, outline=WHITE, width=lw); d.line((w * .02, 0, w * .02, h), fill=WHITE, width=lw)
    d.rectangle((w * .78, h * .2, w - 3, h * .8), outline=WHITE, width=lw); d.rectangle((w * .92, h * .37, w - 3, h * .63), outline=WHITE, width=lw)
    d.rectangle((w - 14, h * .43, w, h * .57), fill=WHITE)
    if path and t > t0:
        u = ease((t - t0) / dur); pts = [(x * w, y * h) for x, y in path]
        n = len(pts) - 1; seg = min(n - 1, int(u * n)); f = u * n - seg
        drawn = pts[:seg + 1] + [(pts[seg][0] + (pts[seg + 1][0] - pts[seg][0]) * f, pts[seg][1] + (pts[seg + 1][1] - pts[seg][1]) * f)]
        for a, b in zip(drawn, drawn[1:]): d.line((a, b), fill=AMB, width=8)
        bx, by = drawn[-1]; d.ellipse((bx - 16, by - 16, bx + 16, by + 16), fill=WHITE, outline=INK, width=4)
    return im


def pens(names, res, n, w=1100):
    h = 120 + 110 * len(names); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 26, fill=(12, 14, 20, 235), outline=WHITE, width=4)
    for k, (nm, ok) in enumerate(zip(names, res)):
        if k >= n: break
        y = 90 + 110 * k; d.text((50, y), nm, font=F("anton", 60), fill=WHITE, anchor="lm")
        im.alpha_composite(xmark(86, ok), (w - 140, int(y - 43)))
        if not ok: d.text((w - 170, y), "DEFENDEU", font=font("blk", 34), fill=RED, anchor="rm")
    return im


def bars(img, items, t, t0, x0=360, y0=360, maxv=12, wmax=1100):
    for k, (lab, v, col) in enumerate(items):
        u = ease((t - t0 - 0.15 * k) / 0.8)
        if u <= 0: continue
        y = y0 + k * 150; d = ImageDraw.Draw(img)
        d.text((x0 - 30, y), lab, font=F("anton", 64), fill=WHITE, anchor="rm")
        d.rounded_rectangle((x0, y - 45, x0 + wmax * v / maxv * u, y + 45), 18, fill=col, outline=INK, width=5)
        d.text((x0 + wmax * v / maxv * u + 30, y), str(int(round(v * u))), font=F("anton", 72), fill=WHITE, anchor="lm")


# ---------------- motor ----------------
class Doc:
    def __init__(self, cid):
        from roteiro import CAPS
        c = next(x for x in CAPS if x[0] == cid)
        self.cid, self.music, self.moff, sents = c
        self.names = [s[0] for s in sents]; self.sents = [s[1] for s in sents]
        self.d = f"/home/claude/doc/{cid}"; j = json.load(open(self.d + "/words.json"))
        self.segs = j["segs"]; self.total = j["total"] + 0.6; self.caps = self.align(j["words"]); self.cred = None
        self.num = int(cid[1:]) if cid[1:].isdigit() else 0

    def align(self, ww):
        caps = []
        for i, (s0, s1) in enumerate(self.segs):
            sw = re.findall(r"\S+", self.sents[i]); wh = [w for w in ww if s0 - 0.15 <= w["t0"] < s1 + 0.05]
            a = [norm(x) for x in sw]; b = [norm(x["w"]) for x in wh]; tm = [None] * len(sw)
            for bl in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
                for k in range(bl.size): tm[bl.a + k] = (wh[bl.b + k]["t0"], wh[bl.b + k]["t1"])
            L = [max(1, len(norm(x))) for x in sw]; tot = sum(L); acc = 0
            for k in range(len(sw)):
                if tm[k] is None: st = s0 + (s1 - s0) * acc / tot; tm[k] = (st, st + (s1 - s0) * L[k] / tot)
                acc += L[k]
            for k in range(len(sw)): caps.append({"w": sw[k], "t0": max(s0, tm[k][0]), "t1": min(s1 + 0.2, tm[k][1]), "i": i})
        return caps

    def wt(self, i, w, nth=0, dflt=0.4):
        k = 0
        for c in self.caps:
            if c["i"] == i and norm(c["w"]).startswith(norm(w)):
                if k == nth: return c["t0"] - self.segs[i][0]
                k += 1
        return dflt

    def seg_at(self, T):
        for i in range(len(self.segs)):
            nxt = self.segs[i + 1][0] if i + 1 < len(self.segs) else 1e9
            if T < nxt - 0.12: return i
        return len(self.segs) - 1

    def caption(self, img, T):
        chunks, cur = [], []
        for k, w in enumerate(self.caps):
            cur.append(k)
            if len(cur) >= 4 or re.search(r"[.,!?:;…]$", w["w"]): chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        ch = next((c for c in chunks if self.caps[c[0]]["t0"] - 0.05 <= T < self.caps[c[-1]]["t1"] + 0.15), None)
        if not ch: return
        words = [re.sub(r"[.,!?:;…]+", "", self.caps[k]["w"]).upper() for k in ch]
        cur = max([k for k in ch if self.caps[k]["t0"] - 0.03 <= T] or [ch[0]])
        f = font("blk", 58); sp = 18; ws = [f.getlength(x) for x in words]; tot = sum(ws) + sp * (len(ws) - 1); x = W / 2 - tot / 2
        for k, wd, wl in zip(ch, words, ws):
            paste(img, text_el(wd, f, AMB if k == cur else WHITE, 7), x + wl / 2, H * 0.905, 1); x += wl + sp

    def frame(self, T):
        i = self.seg_at(T); s0 = self.segs[i][0] if i else 0.0
        dur = (self.segs[i + 1][0] if i + 1 < len(self.segs) else self.total) - s0
        img = Image.new("RGBA", (W, H), (0, 0, 0, 255)); self.cred = None; self.i = i
        SCN[self.names[i]](img, max(0, T - s0), dur, T)
        z = 1.0 + 0.035 * min(1, (T - s0) / max(dur, 1)); dx = 10 * math.sin(T * 0.6)
        cw, chh = W / z, H / z; img = img.crop((int((W - cw) / 2 + dx), int((H - chh) / 2), int((W + cw) / 2 + dx), int((H + chh) / 2))).resize((W, H), Image.BILINEAR)
        if i and T - s0 < 0.1: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(90 * (1 - (T - s0) / 0.1)))))
        if not self.names[i].startswith("cap") and self.num:
            paste(img, chip(f"CAP. {self.num}  •  {TITLES.get(self.cid, '')}", 28, WHITE, (12, 14, 20)), 40, 50, 0.9, center=False)
        if self.cred: paste(img, text_el(self.cred, font("sb", 22), (230, 230, 230), 3), 30, H - 36, 0.8, center=False)
        self.caption(img, T)
        return img.convert("RGB")

    def preview(self, ts, out):
        ims = [self.frame(T).resize((480, 270)) for T in ts]
        c = Image.new("RGB", (480 * 4, 270 * ((len(ims) + 3) // 4)))
        for k, im in enumerate(ims): c.paste(im, ((k % 4) * 480, (k // 4) * 270))
        c.save(out, quality=85)

    def render_part(self, a, b, out):
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
        for k in range(a, b): p.stdin.write(self.frame(k / FPS).tobytes())
        p.stdin.close(); p.wait(); os.rename(out + ".tmp.mp4", out)

    def mix(self):
        sys.path.insert(0, "/home/claude/work/sfx"); import sfxlib
        from scipy.io import wavfile
        SR = 44100; _, v = wavfile.read(self.d + "/narr.wav"); v = v.astype(np.float32) / 32768
        if v.ndim > 1: v = v.mean(1)
        N = int(self.total * SR); vo = np.zeros(N, np.float32); vo[:min(N, len(v))] = v[:N]
        subprocess.run(f"ffmpeg -loglevel error -y -ss {self.moff} -t {self.total + 1} -i /home/claude/ep1/music/{self.music}.mp3 -ac 1 -ar 44100 /tmp/mus_{self.cid}.wav", shell=True, check=True)
        _, m = wavfile.read(f"/tmp/mus_{self.cid}.wav"); m = m.astype(np.float32) / 32768; m = np.pad(m, (0, max(0, N - len(m))))[:N]
        m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.055
        env = np.sqrt(np.convolve(vo ** 2, np.ones(4410) / 4410, "same"))
        duck = np.convolve(np.where(env > 0.02, 0.5, 1.0).astype(np.float32), np.ones(8820) / 8820, "same"); m *= duck
        fi = int(0.8 * SR); m[:fi] *= np.linspace(0, 1, fi); fl = int(1.2 * SR); m[-fl:] *= np.linspace(1, 0, fl)
        fx = np.zeros(N, np.float32)
        def add(name, t, g):
            s = sfxlib.load(name) * g; k = int(max(0, t) * SR); e = min(N, k + len(s)); fx[k:e] += s[:e - k]
        for k, (s0, _) in enumerate(self.segs[1:]): add("whoosh_1" if k % 2 else "whoosh_2", s0 - 0.12, 0.09)
        for name, t, g in SFX.get(self.cid, []): add(name, t(self) if callable(t) else t, g)
        mix = vo + m + fx; mix /= max(1.0, np.abs(mix).max() / 0.98)
        wavfile.write(self.d + "/mix.wav", SR, (mix * 32767).astype(np.int16))


TITLES = {"c1": "A PRIMEIRA FERIDA", "c2": "O ESTÁDIO MALDITO", "c3": "O HOMEM QUE MUDOU TUDO", "c4": "O FANTASMA DE LA PLATA", "c5": "O CAMINHO MAIS SOFRIDO", "c6": "A FINAL"}
SFX = {}
SCN = {}
S = None


def sc(name):
    def deco(f): SCN[name] = f; return f
    return deco


def chapter_card(img, t, T, n, title, key, mode="color"):
    kb(img, key, t, 4, mode, (1.12, 1.2), dim=170, blur=3)
    pop(img, tx(f"CAPÍTULO {n}", 64, AMB, "anton", 5), W / 2, H * 0.36, t, 0.05, 0.35)
    if t > 0.35:
        u = ease((t - 0.35) / 0.5); ImageDraw.Draw(img).rectangle((W / 2 - 420 * u, H * 0.43, W / 2 + 420 * u, H * 0.43 + 6), fill=AMB)
    pop(img, tx(title, 150, WHITE, "anton", 8), W / 2, H * 0.56, t, 0.45, 0.35)


if __name__ == "__main__":
    S = Doc(sys.argv[1])
    import scenes  # noqa: E402,F401  (registra as cenas)
    cmd = sys.argv[2]
    if cmd == "prev":
        ts = [float(x) for x in sys.argv[3:]] or [s0 + 1.2 for s0, _ in S.segs]
        S.preview(ts, S.d + "/sheet.jpg")
    elif cmd == "part":
        n = int(S.total * FPS); k, K = int(sys.argv[3]), int(sys.argv[4]); S.render_part(n * k // K, n * (k + 1) // K, f"{S.d}/p{k}.mp4")
    elif cmd == "final":
        S.mix(); K = int(sys.argv[3])
        open(S.d + "/l.txt", "w").write("".join(f"file 'p{k}.mp4'\n" for k in range(K)))
        subprocess.run(f"cd {S.d} && ffmpeg -loglevel error -y -f concat -safe 0 -i l.txt -c copy v.mp4 && ffmpeg -loglevel error -y -i v.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest final.mp4", shell=True, check=True)
        print("ok", S.d + "/final.mp4")
