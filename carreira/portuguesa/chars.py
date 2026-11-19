"""Bonecos desenhados (sem IA): Thiago Tee e garotos."""
from PIL import Image, ImageDraw, ImageFilter
SK = (232, 180, 140); SKD = (205, 150, 112); RED = (200, 30, 40); GRN = (20, 120, 60); INK = (25, 22, 24)

def _soft(im): return im.filter(ImageFilter.GaussianBlur(0.6))

def thiago(h=900, mouth="smile", t=0.0):
    W = int(h * 0.85); im = Image.new("RGBA", (W, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = h / 100
    cx = W / 2
    # corpo gordinho (polo vermelha com gola verde)
    d.ellipse((cx - 40 * s, 52 * s, cx + 40 * s, 132 * s), fill=RED, outline=INK, width=int(1.2 * s))
    d.polygon([(cx - 9 * s, 52 * s), (cx + 9 * s, 52 * s), (cx, 62 * s)], fill=GRN, outline=INK)
    d.line([(cx, 62 * s), (cx, 72 * s)], fill=INK, width=int(0.8 * s))
    for yy in (66, 70): d.ellipse((cx - 1 * s, yy * s - 1 * s, cx + 1 * s, yy * s + 1 * s), fill=(240, 240, 240))
    d.arc((cx - 40 * s, 60 * s, cx + 40 * s, 140 * s), 200, 340, fill=(160, 20, 30), width=int(1.2 * s))
    # pescoço + papada
    d.ellipse((cx - 15 * s, 44 * s, cx + 15 * s, 58 * s), fill=SKD)
    # cabeça careca redonda
    d.ellipse((cx - 22 * s, 6 * s, cx + 22 * s, 52 * s), fill=SK, outline=INK, width=int(1.1 * s))
    d.ellipse((cx - 26 * s, 24 * s, cx - 18 * s, 36 * s), fill=SK, outline=INK, width=int(0.8 * s))  # orelhas
    d.ellipse((cx + 18 * s, 24 * s, cx + 26 * s, 36 * s), fill=SK, outline=INK, width=int(0.8 * s))
    d.ellipse((cx - 12 * s, 9 * s, cx + 2 * s, 16 * s), fill=(250, 220, 195))  # brilho da careca
    d.ellipse((cx - 14 * s, 40 * s, cx + 14 * s, 54 * s), fill=SK)  # papada
    d.arc((cx - 12 * s, 42 * s, cx + 12 * s, 52 * s), 20, 160, fill=SKD, width=int(0.8 * s))
    # rosto
    blink = 1.5 < (t % 3.1) < 1.62
    for ex in (-8, 8):
        if blink: d.line([(cx + ex * s - 3 * s, 27 * s), (cx + ex * s + 3 * s, 27 * s)], fill=INK, width=int(s))
        else: d.ellipse((cx + ex * s - 2.6 * s, 24.5 * s, cx + ex * s + 2.6 * s, 29.5 * s), fill=INK)
        d.line([(cx + ex * s - 4 * s, 21 * s), (cx + ex * s + 4 * s, 20.5 * s)], fill=(90, 60, 40), width=int(1.2 * s))
    d.ellipse((cx - 3 * s, 29 * s, cx + 3 * s, 35 * s), fill=SKD)  # nariz
    d.ellipse((cx - 17 * s, 31 * s, cx - 11 * s, 36 * s), fill=(240, 150, 140))
    d.ellipse((cx + 11 * s, 31 * s, cx + 17 * s, 36 * s), fill=(240, 150, 140))
    if mouth == "smile": d.chord((cx - 8 * s, 34 * s, cx + 8 * s, 43 * s), 0, 180, fill=(120, 30, 40), outline=INK)
    elif mouth == "open":
        o = 3 + 2.5 * abs(__import__("math").sin(t * 14))
        d.ellipse((cx - 5 * s, 37 * s, cx + 5 * s, (37 + o) * s), fill=(110, 25, 35), outline=INK)
    else: d.arc((cx - 7 * s, 40 * s, cx + 7 * s, 46 * s), 200, 340, fill=INK, width=int(s))
    # prancheta
    d.rounded_rectangle((cx + 18 * s, 72 * s, cx + 40 * s, 100 * s), int(2 * s), fill=(150, 105, 60), outline=INK, width=int(0.8 * s))
    d.rectangle((cx + 21 * s, 77 * s, cx + 37 * s, 97 * s), fill=(245, 245, 240))
    for yy in (81, 85, 89, 93): d.line([(cx + 23 * s, yy * s), (cx + 35 * s, yy * s)], fill=(150, 150, 160), width=int(0.6 * s))
    d.ellipse((cx + 14 * s, 82 * s, cx + 24 * s, 92 * s), fill=SK, outline=INK)  # mão
    return _soft(im.crop(im.getchannel("A").getbbox()))

def kid(h=900, skin=(170, 115, 80), hair=(30, 22, 20), shirt=(200, 30, 40), style="short"):
    W = int(h * 0.7); im = Image.new("RGBA", (W, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = h / 100; cx = W / 2
    d.rounded_rectangle((cx - 28 * s, 56 * s, cx + 28 * s, 110 * s), int(14 * s), fill=shirt, outline=INK, width=int(s))
    d.rectangle((cx - 6 * s, 50 * s, cx + 6 * s, 60 * s), fill=skin)
    d.ellipse((cx - 17 * s, 14 * s, cx + 17 * s, 54 * s), fill=skin, outline=INK, width=int(s))
    if style == "short": d.chord((cx - 18 * s, 10 * s, cx + 18 * s, 36 * s), 180, 360, fill=hair)
    else:
        for k in range(9): d.ellipse((cx + (k - 4) * 4 * s - 5 * s, 8 * s, cx + (k - 4) * 4 * s + 5 * s, 22 * s), fill=hair)
    for ex in (-6, 6): d.ellipse((cx + ex * s - 2.2 * s, 30 * s, cx + ex * s + 2.2 * s, 35 * s), fill=INK)
    d.chord((cx - 6 * s, 39 * s, cx + 6 * s, 46 * s), 0, 180, fill=(120, 30, 40))
    return _soft(im.crop(im.getchannel("A").getbbox()))

if __name__ == "__main__":
    bg = Image.new("RGBA", (1400, 950), (40, 44, 60, 255))
    bg.alpha_composite(thiago(900), (20, 20)); bg.alpha_composite(kid(800), (800, 120))
    bg.convert("RGB").save("/tmp/claude-0/chars.jpg")
