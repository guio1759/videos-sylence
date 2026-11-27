from common2 import *
import fotofx as FX, json
IMG = "/home/claude/x26/img/"
CRJ = json.load(open(IMG + "cred.json"))
P = {k: IMG + k + (".png" if k == "novcrest" else ".jpg") for k in CRJ}
def cr(img, k, y=H - 150): FX.credit(img, CRJ[k], y=y)
def big(s, size, col=WHITE, f="anton", st=10): return text_el(s, F(f, size), col, st)
def crest(h):
    im = Image.open(P["novcrest"]).convert("RGBA"); bb = im.getchannel("A").getbbox(); im = im.crop(bb)
    return im.resize((int(im.width * h / im.height), int(h)), Image.LANCZOS)
def blurbg(k, t, dur, tint=(0, 0, 0, 130), blur=10, z=(1.15, 1.3), f0=(0.5, 0.5), f1=(0.55, 0.45)):
    b = FX.kb(FX.load(P[k]), t, dur, z, f0, f1, vig=0).filter(ImageFilter.GaussianBlur(blur)); b.alpha_composite(Image.new("RGBA", (W, H), tint)); return b
