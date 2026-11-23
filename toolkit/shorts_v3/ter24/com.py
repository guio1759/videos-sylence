import sys; sys.path.insert(0, "/home/claude/ter24"); sys.path.insert(0, "/home/claude/work/tat")
from engine import *
import eng3d as E
cx = W / 2

def pitch3d(img, T, ang0=0.0, spd=6.0, dist=78, hgt=34, tgt=(0, 0, 0), fov=50, dim=0):
    a = math.radians(ang0 + spd * T)
    pos = (tgt[0] + dist * math.cos(a), tgt[1] + dist * math.sin(a), hgt)
    cam = E.Cam(np.array(pos, float), np.array(tgt, float), fov, W, H)
    d = ImageDraw.Draw(img, "RGBA"); E.draw_pitch(d, cam)
    if dim: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, dim)))
    return cam, d

def shield_stripes(h, cols=((220, 30, 40), WHITE), label=None):
    h = int(h); w = int(h * 0.82); im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    mask = Image.new("L", (w, h), 0); md = ImageDraw.Draw(mask)
    md.polygon([(0, 0), (w, 0), (w, h * 0.55), (w / 2, h), (0, h * 0.55)], fill=255)
    st = Image.new("RGBA", (w, h)); sd = ImageDraw.Draw(st); n = 7
    for k in range(n): sd.rectangle((k * w / n, 0, (k + 1) * w / n, h), fill=cols[k % 2])
    im.paste(st, (0, 0), mask)
    d = ImageDraw.Draw(im); d.line([(0, 0), (w, 0), (w, h * 0.55), (w / 2, h), (0, h * 0.55), (0, 0)], fill=INK, width=max(4, h // 40))
    if label: d.text((w / 2, h * 0.3), label, font=font("blk", h * 0.2), fill=WHITE, anchor="mm", stroke_width=max(3, h // 50), stroke_fill=INK)
    return im

def towel(w, t):
    w = int(w); h = int(w * 0.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 18, fill=(250, 250, 250), outline=INK, width=6)
    for y in (0.15, 0.85): d.rectangle((6, h * y - 10, w - 6, h * y + 10), fill=(40, 140, 80))
    for k in range(9): d.line((w * (k + 0.5) / 9, h - 4, w * (k + 0.5) / 9, h + 14), fill=(230, 230, 230), width=6)
    return im

def scorebox(a, b, ga, gb, sz=150):
    w = int(sz * 5.6); h = int(sz * 1.6); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 30, fill=(15, 18, 26, 240), outline=WHITE, width=5)
    la, lb = (logo(a, sz) if isinstance(a, str) else a), (logo(b, sz) if isinstance(b, str) else b)
    im.alpha_composite(la, (int(sz * 0.9 - la.width / 2), int(h / 2 - la.height / 2)))
    im.alpha_composite(lb, (int(w - sz * 0.9 - lb.width / 2), int(h / 2 - lb.height / 2)))
    d.text((w / 2, h / 2), f"{ga} x {gb}", font=font("blk", sz * 0.85), fill=WHITE, anchor="mm")
    return im

def shake(t, t0, amp=18, dur=0.25):
    if t < t0 or t > t0 + dur: return 0
    return amp * (1 - (t - t0) / dur) * math.sin((t - t0) * 90)

def redcard(h, rot=0):
    h = int(h); w = int(h * 0.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w, h), 14, fill=RED, outline=INK, width=6); return im

def check(sz, ok=True):
    sz = int(sz); im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, sz, sz), fill=GREEN if ok else RED, outline=INK, width=5)
    if ok: d.line([(sz * .25, sz * .52), (sz * .43, sz * .7), (sz * .76, sz * .32)], fill=WHITE, width=int(sz * .12))
    else:
        d.line([(sz * .3, sz * .3), (sz * .7, sz * .7)], fill=WHITE, width=int(sz * .12)); d.line([(sz * .7, sz * .3), (sz * .3, sz * .7)], fill=WHITE, width=int(sz * .12))
    return im
