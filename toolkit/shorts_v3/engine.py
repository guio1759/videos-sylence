"""Motor de Shorts v3: cenas por frase (segs), legenda alinhada ao roteiro, render 1080x1920."""
import sys, os, json, re, math, difflib, subprocess, unicodedata, functools
sys.path.insert(0, "/home/claude/ep1/v2")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from gfx import *  # noqa

W, H, FPS = 1080, 1920, 30
LOG = "/home/claude/work/logos/"


def norm(s): return re.sub(r"[^a-z0-9%]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())


@functools.lru_cache(64)
def logo(k, h):
    im = Image.open(LOG + k + ".png").convert("RGBA"); im = im.crop(im.getchannel("A").getbbox()); h = int(h)
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def txt(s, size, col=WHITE, stroke=8, weight="blk"): return text_el(s, font(weight, size), col, stroke)


def pop(img, el, x, y, t, t0=0.0, dur=0.3, rot=0, alpha=1.0):
    if t < t0: return
    paste(img, el, x, y, alpha, 0.2 + 0.8 * back((t - t0) / dur), rot)


def fade(img, el, x, y, t, t0=0.0, dur=0.5, dy=30):
    if t < t0: return
    u = ease((t - t0) / dur); paste(img, el, x, y + dy * (1 - u), u)


def slide(img, el, x, y, t, t0=0.0, dx=-500, dur=0.35):
    if t < t0: return
    u = ease((t - t0) / dur); paste(img, el, x + dx * (1 - u), y, u)


def lines(img, ls, y, t, t0=0.0, size=110, col=WHITE, gap=1.15, step=0.18, cols=None):
    for i, l in enumerate(ls):
        fade(img, txt(l, size, (cols or [col] * len(ls))[i]), W / 2, y + i * size * gap, t, t0 + i * step, 0.35)


def jersey(num, name, w=420, col=(20, 120, 60), fg=WHITE):
    w = int(w); h = int(w * 1.05); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s = w / 100
    poly = [(30 * s, 5 * s), (42 * s, 10 * s), (58 * s, 10 * s), (70 * s, 5 * s), (98 * s, 22 * s), (88 * s, 42 * s), (78 * s, 36 * s),
            (78 * s, 102 * s), (22 * s, 102 * s), (22 * s, 36 * s), (12 * s, 42 * s), (2 * s, 22 * s)]
    d.polygon(poly, fill=col, outline=INK, width=6)
    d.text((w / 2, 30 * s), name, font=font("blk", 10 * s), fill=fg, anchor="mm")
    d.text((w / 2, 66 * s), str(num), font=font("blk", 38 * s), fill=fg, anchor="mm", stroke_width=3, stroke_fill=INK)
    return im


def person(h, col=(235, 235, 235)):
    h = int(h); w = int(h * 0.5); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((w * 0.28, 0, w * 0.72, h * 0.27), fill=col)
    d.rounded_rectangle((w * 0.08, h * 0.3, w * 0.92, h), int(w * 0.3), fill=col)
    return im


def trophy(h, col=(255, 205, 60)):
    h = int(h); w = int(h * 0.8); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.pieslice((w * 0.12, -h * 0.25, w * 0.88, h * 0.62), 0, 180, fill=col, outline=INK, width=6)
    d.arc((0, h * 0.05, w * 0.26, h * 0.38), 90, 270, fill=INK, width=8); d.arc((w * 0.74, h * 0.05, w, h * 0.38), -90, 90, fill=INK, width=8)
    d.rectangle((w * 0.43, h * 0.6, w * 0.57, h * 0.78), fill=col, outline=INK, width=5)
    d.rounded_rectangle((w * 0.25, h * 0.78, w * 0.75, h * 0.96), 10, fill=(40, 120, 60), outline=INK, width=5)
    return im


def candle(h, t):
    h = int(h); w = int(h * 0.45); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((w * 0.3, h * 0.38, w * 0.7, h), 10, fill=(245, 240, 225))
    fl = 1 + 0.08 * math.sin(t * 13) + 0.05 * math.sin(t * 7.3)
    cx, top = w / 2, h * 0.38
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((cx - w * 0.5, top - h * 0.32, cx + w * 0.5, top + h * 0.05), fill=(255, 190, 80, 90))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(w * 0.12)))
    d.ellipse((cx - w * 0.12, top - h * 0.26 * fl, cx + w * 0.12, top - h * 0.02), fill=(255, 200, 70))
    d.ellipse((cx - w * 0.06, top - h * 0.16 * fl, cx + w * 0.06, top - h * 0.03), fill=(255, 245, 200))
    return im


def envelope(w, open_=0.0):
    w = int(w); h = int(w * 0.65); im = Image.new("RGBA", (w, h + int(h * 0.5)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); oy = int(h * 0.5)
    d.rectangle((0, oy, w, oy + h), fill=(245, 238, 220), outline=INK, width=6)
    d.line((0, oy + h, w / 2, oy + h * 0.5, w, oy + h), fill=INK, width=5)
    if open_ < 0.5: d.polygon([(0, oy), (w, oy), (w / 2, oy + h * 0.55 * (1 - 2 * open_))], fill=(230, 220, 195), outline=INK)
    else: d.polygon([(0, oy), (w, oy), (w / 2, oy - h * 0.55 * (2 * open_ - 1))], fill=(230, 220, 195), outline=INK)
    d.ellipse((w / 2 - 22, oy + h * 0.45, w / 2 + 22, oy + h * 0.45 + 44), fill=(30, 120, 60))
    return im


def heartbeat(w, h, t, col=(60, 220, 120)):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); pts = []
    for x in range(0, int(w), 4):
        u = ((x / w) * 3 - t * 0.8) % 1
        y = h / 2 - (h * 0.4 if 0.45 < u < 0.48 else -h * 0.25 if 0.48 < u < 0.51 else 0)
        pts.append((x, y))
    d.line(pts, fill=col, width=6); return im


class Short:
    def __init__(self, d, sents, scenes, topic, palette, music, music_off, sfx_soft=False):
        self.d = d; j = json.load(open(os.path.join(d, "words.json")))
        self.segs = j["segs"]; self.total = j["total"]; self.sents = sents; self.scenes = scenes
        self.topic = topic; self.pal = palette; self.music = music; self.moff = music_off; self.soft = sfx_soft
        self.caps = self.align(j["words"])

    def align(self, ww):
        caps = []
        for i, (s0, s1) in enumerate(self.segs):
            sw = [w for w in re.findall(r"\S+", self.sents[i][0])]
            wh = [w for w in ww if s0 - 0.15 <= w["t0"] < s1 + 0.05]
            a = [norm(x) for x in sw]; b = [norm(x["w"]) for x in wh]
            tm = [None] * len(sw)
            for bl in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
                for k in range(bl.size): tm[bl.a + k] = (wh[bl.b + k]["t0"], wh[bl.b + k]["t1"])
            # interpola os que faltam pelo tamanho
            L = [max(1, len(norm(x))) for x in sw]; tot = sum(L); acc = 0
            for k in range(len(sw)):
                if tm[k] is None:
                    st = s0 + (s1 - s0) * acc / tot; tm[k] = (st, st + (s1 - s0) * L[k] / tot)
                acc += L[k]
            for k in range(len(sw)): caps.append({"w": sw[k], "t0": max(s0, tm[k][0]), "t1": min(s1 + 0.2, tm[k][1])})
        return caps

    SKIP = {"o", "a", "e", "de", "da", "do", "no", "na", "os", "as", "em", "se", "um", "uma", "ele", "que", "pra", "pro", "com", "nos", "ao"}

    def caption(self, img, T):
        cur = None
        for w in self.caps:
            if w["t0"] - 0.03 <= T < w["t1"] + 0.1: cur = w
            if w["t0"] > T: break
        if not cur: return
        if norm(cur["w"]) in self.SKIP or not norm(cur["w"]):
            i = self.caps.index(cur); prev = next((self.caps[k] for k in range(i - 1, max(-1, i - 4), -1) if norm(self.caps[k]["w"]) not in self.SKIP), None)
            if not prev or T - prev["t1"] > 0.6: return
            cur = prev
        s = re.sub(r"[.,!?:;…]+", "", cur["w"]).upper().strip(".")
        if not s: return
        sc = 0.78 + 0.22 * back((T - cur["t0"]) / 0.16)
        hot = cur["w"].endswith("!") or any(ch.isdigit() for ch in s) or len(s) > 8
        paste(img, chip(s, 88, INK, AMB if hot else WHITE, "blk", 0.5, 0.25), W / 2, H * 0.845, 1, sc, rot=-2 if hash(s) % 2 else 2)

    def seg_at(self, T):
        for i, (s0, s1) in enumerate(self.segs):
            nxt = self.segs[i + 1][0] if i + 1 < len(self.segs) else 1e9
            if T < nxt: return i, T - s0
        return len(self.segs) - 1, T - self.segs[-1][0]

    def frame(self, T):
        i, t = self.seg_at(T)
        pal = self.pal[i] if isinstance(self.pal, list) else self.pal
        img = bg(W, H, pal, T)
        self.scenes[i](img, t, T)
        s0 = self.segs[i][0]
        if i and 0 <= T - s0 < 0.12:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int((60 if self.soft else 140) * (1 - (T - s0) / 0.12)))))
        paste(img, tag_box(self.topic, 44, WHITE, INK), W / 2, 150, 1)
        self.caption(img, T)
        return img.convert("RGB")

    def preview(self, ts, out):
        ims = [self.frame(T).resize((270, 480)) for T in ts]
        c = Image.new("RGB", (270 * min(5, len(ims)), 480 * ((len(ims) + 4) // 5)))
        for k, im in enumerate(ims): c.paste(im, ((k % 5) * 270, (k // 5) * 480))
        c.save(out, quality=85)

    def render_part(self, a, b, out):
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
        for k in range(a, b): p.stdin.write(self.frame(k / FPS).tobytes())
        p.stdin.close(); p.wait(); os.rename(out + ".tmp.mp4", out)

    def mix(self, extra=()):
        sys.path.insert(0, "/home/claude/work/sfx"); import sfxlib
        from scipy.io import wavfile
        SR = 44100; _, v = wavfile.read(os.path.join(self.d, "narr.wav")); v = v.astype(np.float32) / 32768
        if v.ndim > 1: v = v.mean(1)
        N = int(self.total * SR); vo = np.zeros(N, np.float32); vo[:min(N, len(v))] = v[:N]
        subprocess.run(f"ffmpeg -loglevel error -y -ss {self.moff} -t {self.total + 1} -i /home/claude/ep1/music/{self.music}.mp3 -ac 1 -ar 44100 /tmp/mus.wav", shell=True, check=True)
        _, m = wavfile.read("/tmp/mus.wav"); m = m.astype(np.float32) / 32768; m = np.pad(m, (0, max(0, N - len(m))))[:N]
        m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.05
        env = np.sqrt(np.convolve(vo ** 2, np.ones(4410) / 4410, "same"))
        duck = np.convolve(np.where(env > 0.02, 0.55, 1.0).astype(np.float32), np.ones(4410) / 4410, "same"); m *= duck
        fi = int(0.4 * SR); m[:fi] *= np.linspace(0, 1, fi); fl = int(0.8 * SR); m[-fl:] *= np.linspace(1, 0, fl)
        fx = np.zeros(N, np.float32)
        def add(name, t, g):
            s = sfxlib.load(name) * g; k = int(max(0, t) * SR); e = min(N, k + len(s)); fx[k:e] += s[:e - k]
        for k, (s0, _) in enumerate(self.segs[1:]): add("whoosh_1" if k % 2 else "whoosh_2", s0 - 0.12, 0.08 if self.soft else 0.16)
        for name, t, g in extra: add(name, t, g)
        mix = vo + m + fx; mix /= max(1.0, np.abs(mix).max() / 0.98)
        wavfile.write(os.path.join(self.d, "mix.wav"), SR, (mix * 32767).astype(np.int16))
        subprocess.run(f"ffmpeg -loglevel error -y -i {self.d}/mix.wav -af loudnorm=I=-14:TP=-1.5 -ar 44100 {self.d}/mixn.wav", shell=True, check=True)


def main(S, extra=()):
    cmd = sys.argv[1]
    if cmd == "prev":
        ts = [float(x) for x in sys.argv[2:]] or [s0 + 0.9 for s0, _ in S.segs]
        S.preview(ts, os.path.join(S.d, "sheet.jpg"))
    elif cmd == "part":
        n = int(S.total * FPS); k, K = int(sys.argv[2]), int(sys.argv[3])
        S.render_part(n * k // K, n * (k + 1) // K, os.path.join(S.d, f"p{k}.mp4"))
    elif cmd == "final":
        S.mix(extra); K = int(sys.argv[2])
        with open(os.path.join(S.d, "l.txt"), "w") as f:
            for k in range(K): f.write(f"file 'p{k}.mp4'\n")
        subprocess.run(f"cd {S.d} && ffmpeg -loglevel error -y -f concat -safe 0 -i l.txt -c copy v.mp4 && ffmpeg -loglevel error -y -i v.mp4 -i mixn.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest final.mp4", shell=True, check=True)
