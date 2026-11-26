from extra import *
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common")
import emoji as EM
from fonts import F
def mkwt(S):
    def wt(i, w):
        for c in S.caps:
            if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
        return 0.5
    return wt
def emo(img, name, x, y, t, t0, size=230):
    if t >= t0: paste(img, EM.get(name, size, t - t0), x, y, 1, 0.6 + 0.4 * back(min(1, (t - t0) / 0.25)))
def mic(h):
    h = int(h); w = int(h * 0.45); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((w * 0.1, 0, w * 0.9, h * 0.45), int(w * 0.4), fill=(70, 70, 80), outline=INK, width=6)
    for k in range(4): d.line((w * 0.2, h * (0.08 + k * 0.09), w * 0.8, h * (0.08 + k * 0.09)), fill=(140, 140, 150), width=4)
    d.rounded_rectangle((w * 0.32, h * 0.45, w * 0.68, h), 12, fill=(30, 30, 36), outline=INK, width=6)
    d.rectangle((w * 0.32, h * 0.55, w * 0.68, h * 0.68), fill=(255, 205, 0))
    d.text((w / 2, h * 0.615), "BAND", font=font("blk", int(w * 0.13)), fill=INK, anchor="mm")
    return im
def heli(w, t=0):
    w = int(w); h = int(w * 0.6); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((w * 0.15, h * 0.3, w * 0.65, h * 0.8), fill=(30, 30, 36), outline=WHITE, width=6)
    d.ellipse((w * 0.4, h * 0.38, w * 0.6, h * 0.6), fill=(140, 200, 255))
    d.rectangle((w * 0.6, h * 0.48, w * 0.95, h * 0.56), fill=(30, 30, 36), outline=WHITE, width=4)
    d.rectangle((w * 0.9, h * 0.36, w * 0.96, h * 0.62), fill=(30, 30, 36), outline=WHITE, width=3)
    d.line((w * 0.2, h * 0.92, w * 0.6, h * 0.92), fill=WHITE, width=8); d.line((w * 0.3, h * 0.8, w * 0.3, h * 0.92), fill=WHITE, width=6); d.line((w * 0.5, h * 0.8, w * 0.5, h * 0.92), fill=WHITE, width=6)
    d.line((w * 0.4, h * 0.3, w * 0.4, h * 0.18), fill=WHITE, width=8)
    L = w * 0.45 * abs(math.cos(t * 25)); d.line((w * 0.4 - L, h * 0.17, w * 0.4 + L, h * 0.17), fill=WHITE, width=10)
    return im
def furia_badge(w):
    w = int(w); h = int(w * 0.42); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), int(h * 0.2), fill=(12, 12, 14), outline=WHITE, width=8)
    d.text((w / 2, h / 2), "FURIA", font=F("bebas", int(h * 0.8)), fill=WHITE, anchor="mm")
    return im
def nov_shield(h):
    return shield_stripes(h, ((250, 205, 20), (20, 20, 20)), "NOV")
