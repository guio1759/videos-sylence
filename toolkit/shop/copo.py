import sys; sys.path.insert(0, "/home/claude/sex20"); sys.path.insert(0, "/home/claude/shop")
from com import *
from shopscripts import CP
from PIL import ImageFilter, ImageEnhance
P = Image.open("/home/claude/shop/copo/prod.jpg").convert("RGB"); P = P.crop((0, 0, int(P.width * 0.9), int(P.height * 0.9))).resize((960, 958), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
def framed(w):
    im = P.resize((int(w), int(w)), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width, im.height), 40, fill=255); im.putalpha(m)
    out = Image.new("RGBA", (im.width + 16, im.height + 16), (0, 0, 0, 0)); ImageDraw.Draw(out).rounded_rectangle((0, 0, out.width, out.height), 48, fill=WHITE)
    out.alpha_composite(im, (8, 8)); return out
FR = framed(820)

def plastic(h):
    h = int(h); w = int(h * 0.75); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (w, 0), (w * 0.82, h), (w * 0.18, h)], fill=(235, 240, 245, 200), outline=(150, 160, 170), width=6)
    for k in range(1, 6): d.line([(w * 0.03 + k * w * 0.15, 10), (w * 0.2 + k * w * 0.11, h - 10)], fill=(200, 210, 220), width=4)
    d.line([(0, 0), (w, h)], fill=RED, width=22); d.line([(w, 0), (0, h)], fill=RED, width=22); return im

def star(sz, fill):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = sz / 2
    pts = [(c + (c if k % 2 == 0 else c * 0.42) * math.cos(math.radians(-90 + 36 * k)), c + (c if k % 2 == 0 else c * 0.42) * math.sin(math.radians(-90 + 36 * k))) for k in range(10)]
    d.polygon(pts, fill=fill, outline=INK); return im

def gift(sz):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((sz * .1, sz * .4, sz * .9, sz * .95), fill=RED, outline=INK, width=5); d.rectangle((sz * .05, sz * .28, sz * .95, sz * .42), fill=RED, outline=INK, width=5)
    d.rectangle((sz * .44, sz * .28, sz * .56, sz * .95), fill=AMB); d.ellipse((sz * .25, sz * .08, sz * .5, sz * .3), outline=AMB, width=10); d.ellipse((sz * .5, sz * .08, sz * .75, sz * .3), outline=AMB, width=10)
    return im

def s0(img, t, T):
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, logo("PAL", 170), 300, 380, 1); paste(img, txt("x", 90), cx, 380, 1); paste(img, logo("FLA", 170), 780, 380, 1)
    paste(img, chip("SÁBADO • 16:30", 56, INK, AMB), cx, 540, 1)
    paste(img, txt("VAI ASSISTIR COM", 84, WHITE, 10), cx, 700, 1, sc, -2)
    paste(img, txt("COPO DE PLÁSTICO?", 88, AMB, 12), cx, 820, 1, sc, -2)
    paste(img, plastic(380), cx, 1180, 1, 1 + 0.15 * max(0, 1 - t / 0.2), 6 * math.sin(T * 3))

def s1(img, t, T):
    paste(img, FR, cx, 800, 1, 0.75 + 0.25 * back(t / 0.35) + 0.02 * t)
    pop(img, chip("COPO TÉRMICO DO PALMEIRAS", 54, WHITE, GREEN), cx, 300, t, 0.1)
    pop(img, stamp("SEU NOME A LASER", 84, AMB), cx, 1300, t, wt_(1, "nome"), 0.25, -5)

def s2(img, t, T):
    paste(img, FR, cx, 800, 1, 1.0 + 0.04 * t)
    img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 80)))
    pop(img, gift(300), cx, 760, t, 0.0, 0.25); pop(img, txt("+ BRINDE", 140, AMB), cx, 1030, t, 0.15)
    if t > 0.2: img.alpha_composite(confetti(W, H, t - 0.2))

def s3(img, t, T):
    for k in range(5):
        pop(img, star(150, AMB if k < 4 else (240, 200, 120)), 190 + k * 175, 520, t, k * 0.08, 0.2)
    pop(img, txt("4,8 ESTRELAS", 110), cx, 700, t, 0.4)
    tv = wt_(3, "mais")
    if t > tv:
        paste(img, odometer(2500, 4, 170, t - tv, 0.8, 0), cx, 1000)
        pop(img, txt("+ VENDIDOS", 90, AMB), cx, 1230, t, tv + 0.5)

def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 820, T, (255, 220, 140), 16, 70))
    paste(img, framed(520), cx, 640, 1, 0.9 + 0.1 * back(t / 0.3))
    pop(img, chip("R$ 34,89", 170, INK, AMB), cx, 1090, t, wt_(4, "trinta") - 0.1, 0.25, -3)
    pop(img, chip("2x SEM JUROS", 56, WHITE, RED), cx, 1280, t, wt_(4, "trinta") + 0.6)

def s5(img, t, T):
    paste(img, framed(560), cx, 620, 1)
    pop(img, txt("TOCA NO PRODUTO", 96, WHITE), cx, 1010, t, 0.0)
    y = 1180 + 30 * math.sin(T * 8)
    if t > 0.3:
        d = ImageDraw.Draw(img); x0 = 240
        d.rectangle((x0 - 28, y - 90, x0 + 28, y + 20), fill=AMB, outline=INK); d.polygon([(x0 - 80, y + 10), (x0 + 80, y + 10), (x0, y + 110)], fill=AMB, outline=INK)
    pop(img, chip("ANTES DO JOGO!", 70, INK, AMB), cx + 120, 1250, t, wt_(5, "antes") - 0.1, 0.25, 3)

def s6(img, t, T):
    paste(img, framed(480), cx, 620, 1)
    pop(img, txt("QUAL NOME", 120, AMB), cx, 1000, t, 0.0); pop(img, txt("VOCÊ GRAVARIA?", 96), cx, 1120, t, 0.15)
    pop(img, chip("COMENTA 👇".replace("👇", ""), 70, INK, WHITE), cx, 1290, t, 0.5)

def wt_(i, word):
    s0 = SH.segs[i][0]
    for w in SH.caps:
        if SH.segs[i][0] - 0.01 <= w["t0"] <= SH.segs[i][1] + 0.01 and norm(w["w"]).startswith(norm(word)): return w["t0"] - s0
    return 0.3

SH = Short("/home/claude/shop/copo", CP, [s0, s1, s2, s3, s4, s5, s6], "ACHADO DO TORCEDOR",
           ["green", "dark", "night", "dark", "green", "dark", "green"], "Rising_Game", 0)
if __name__ == "__main__":
    main(SH, extra=[("tambor_impacto", 0.0, 0.4), ("camera_click", SH.segs[1][0] + 0.3, 0.3), ("torcida_comemora", SH.segs[2][0], 0.15), ("tambor_impacto", SH.segs[4][0] + 0.5, 0.3)])
