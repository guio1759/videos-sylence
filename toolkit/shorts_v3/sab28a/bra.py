from extra import *
from scripts import BRA
EST = lambda h: logo("EST", h)
GOLD = (255, 205, 60)
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def flag_br(w):
    w = int(w); h = int(w * 0.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 16, fill=(0, 150, 60), outline=INK, width=6)
    d.polygon([(w * 0.08, h / 2), (w / 2, h * 0.09), (w * 0.92, h / 2), (w / 2, h * 0.91)], fill=(255, 215, 0))
    r = h * 0.25; d.ellipse((w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), fill=(20, 40, 130))
    d.arc((w / 2 - r * 1.3, h / 2 - r * 0.6, w / 2 + r * 1.3, h / 2 + r * 2.2), 225, 315, fill=WHITE, width=max(4, int(h * 0.04)))
    return im
def flag_ar(w):
    w = int(w); h = int(w * 0.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 16, fill=WHITE)
    d.rectangle((3, 3, w - 3, h / 3), fill=(116, 172, 223)); d.rectangle((3, h * 2 / 3, w - 3, h - 3), fill=(116, 172, 223))
    r = h * 0.11; d.ellipse((w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), fill=(246, 180, 14), outline=(133, 52, 13), width=3)
    d.rounded_rectangle((0, 0, w, h), 16, outline=INK, width=6)
    return im
def vs_box(la, lb, ga, gb, sz=150, colb=WHITE):
    w = int(sz * 6); h = int(sz * 1.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 30, fill=(15, 18, 26, 240), outline=WHITE, width=5)
    im.alpha_composite(la, (int(sz * 1.0 - la.width / 2), int(h / 2 - la.height / 2)))
    im.alpha_composite(lb, (int(w - sz * 1.0 - lb.width / 2), int(h / 2 - lb.height / 2)))
    d.text((w / 2, h / 2), f"{ga} x {gb}", font=font("blk", sz * 0.8), fill=colb, anchor="mm")
    return im
def cups(img, years, y, t, t0s, h=170, col=GOLD):
    n = len(years); gap = min(250, 960 / n)
    for k, (yr, t0) in enumerate(zip(years, t0s)):
        x = cx + (k - (n - 1) / 2) * gap
        pop(img, trophy(h, col), x, y, t, t0, 0.25, (-5, 5)[k % 2])
        pop(img, chip(yr, 46, INK, WHITE), x, y + h * 0.72, t, t0 + 0.1, 0.25)
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 1070, T, (255, 400, 120), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, chip("HOJE • 17H • FINAL", 60, INK, AMB), cx, 470, 1, sc, -3)
    paste(img, flag_br(400), 290 + shake(t, 0.05, 14), 810, 1, sc, -6)
    paste(img, flag_ar(400), 790 - shake(t, 0.05, 14), 810, 1, sc, 6)
    paste(img, txt("VS", 120, AMB, 12), cx, 810, 1, sc)
    paste(img, txt("O BRASIL", 140, WHITE, 14), cx, 1070, 1, sc, -2)
    paste(img, txt("PODE PASSAR!", 120, GREEN, 12), cx, 1215, 1, sc, 2)
    pop(img, logo("PAL", 160), cx, 1395, t, wt(0, "palmeiras") - 0.15)
def s1(img, t, T):
    pop(img, chip("TÍTULOS DA LIBERTADORES", 58, INK, WHITE), cx, 490, t, 0.0)
    t0 = wt(1, "empatados") - 0.2
    if t > 0.2:
        u = min(1.0, (t - 0.2) / 1.2); n = int(round(25 * ease(u)))
        pop(img, vs_box(flag_br(200), flag_ar(200), n, n, 150, AMB if u >= 1 else WHITE), cx + shake(t, wt(1, "vinte") , 10), 810, t, 0.2)
    pop(img, stamp("EMPATE!", 110, RED), cx, 1130, t, t0, 0.25, -6)
    pop(img, txt("25 PRA CADA LADO", 80, WHITE), cx, 1320, t, wt(1, "cada") - 0.3)
    if t > wt(1, "olha"): paste(img, emoji.get("olhos", 170, t), 900, 1170, 1)
def s2(img, t, T):
    pop(img, logo("PAL", 230), cx, 590, t, 0.0)
    pop(img, txt("3 TÍTULOS", 110, GREEN), cx, 810, t, wt(2, "três") - 0.2)
    cups(img, ["1999", "2020", "2021"], 1090, t, [wt(2, "noventa") - 0.15, wt(2, "vinte") - 0.3, wt(2, "um") - 0.3])
def s3(img, t, T):
    pop(img, EST(230), cx, 570, t, 0.0)
    pop(img, txt("4 TÍTULOS", 110, (240, 90, 90)), cx, 790, t, wt(3, "quatro") - 0.2)
    cups(img, ["1968", "1969", "1970", "2009"], 1030, t, [wt(3, "quatro") - 0.1 + 0.12 * k for k in range(4)], 150, (230, 230, 230))
    pop(img, chip("QUER O 5º", 66, WHITE, RED), cx, 1300, t, wt(3, "quinto") - 0.2, 0.25, -3)
    pop(img, chip("17 ANOS DEPOIS", 52, INK, AMB), cx, 1420, t, wt(3, "dezessete") - 0.2, 0.25, 3)
def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 970, T, (150, 425, 170), 14, 45))
    pop(img, stamp("TETRA!", 150, GREEN), cx + shake(t, wt(4, "tetra"), 12), 360, t, wt(4, "tetra") - 0.2, 0.25, -6)
    ta = wt(4, "alcança") - 0.2
    if t < ta: pop(img, logo("PAL", 300), cx, 820, t, 0.0, 0.3)
    if t > ta and t < wt(4, "brasil") - 0.25:
        pop(img, vs_box(logo("PAL", 150), logo("FLA", 150), 4, 4, 130), cx, 870, t, ta)
        pop(img, chip("ALCANÇA O FLAMENGO", 56, INK, AMB), cx, 1070, t, ta + 0.2)
    tb = wt(4, "brasil") - 0.25
    if t > tb:
        pop(img, vs_box(flag_br(190), flag_ar(190), 26, 25, 140, AMB), cx, 890, t, tb)
        pop(img, txt("SOZINHO NO TOPO", 96, WHITE), cx, 1130, t, wt(4, "sozinho") - 0.2)
        img.alpha_composite(confetti(W, H, t - tb))
        paste(img, emoji.get("trofeu", 180, t - tb), 900, 1320, 1)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 970, T, (255, 400, 120), 14, 40))
    pop(img, chip("HOJE • 17H • CENTENÁRIO", 56, INK, AMB), cx, 500, t, 0.0)
    pop(img, flag_br(380), 290, 810, t, wt(5, "brasil") - 0.2, 0.25, -5)
    pop(img, flag_ar(380), 790, 810, t, wt(5, "argentina") - 0.2, 0.25, 5)
    pop(img, chip("BRASIL", 90, WHITE, GREEN), 290, 1100, t, wt(5, "brasil") - 0.1, 0.25, -4)
    pop(img, chip("ARGENTINA", 76, INK, (116, 342, 223)), 790, 1100, t, wt(5, "argentina") - 0.1, 0.25, 4)
    pop(img, txt("COMENTA!", 130, AMB), cx, 1320, t, wt(5, "comenta") - 0.2)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 405, 235), 3), W / 2, H - 125, 0.85)
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
S = Short("/home/claude/sab28a/bra", BRA, [s0, s1, s2, s3, s4, s5], "FINAL DA LIBERTADORES", ["green", "dark", "green", "red", "night", "blue"], "Impact_Prelude", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", S.segs[1][0] + wt(1, "empatados"), 0.3), ("camera_click", S.segs[2][0] + wt(2, "noventa"), 0.2),
                   ("tambor_impacto", S.segs[4][0] + wt(4, "tetra"), 0.35), ("torcida_comemora", S.segs[4][0] + wt(4, "brasil"), 0.2), ("torcida_grita_gol", S.segs[5][0] + 0.1, 0.08)])
