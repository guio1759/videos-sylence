from extra import *
from scripts import BOL
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 820, T, GOLD, 14, 55))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("A 8ª BOLA DE OURO", 100, WHITE, 12), cx, 400, 1, sc, -3)
    paste(img, txt("DO MESSI", 130, GOLD, 12), cx, 540, 1, sc, -3)
    paste(img, goldball(420, T), cx, 880, 1, sc)
    pop(img, stamp("ROUBADA?", 140, RED), cx, 900, t, 0.5, 0.25, -10 + shake(t, 0.5, 10))
    pop(img, chip("OLHA OS NÚMEROS", 64, INK, WHITE), cx, 1230, t, wt(0, "olha") - 0.2, 0.25, 3)
def s1(img, t, T):
    pop(img, chip("BOLA DE OURO 2023 • PERÍODO", 56, INK, WHITE), cx, 420, t, 0.0)
    paste(img, calendar(980, ease(t / 2.5), t), cx, 760, 1, back(t / 0.3))
    pop(img, chip("COPA DO MUNDO • DEZ/2022", 60, INK, GOLD), cx, 1020, t, wt(1, "copa") - 0.3, 0.25, -3)
    pop(img, stamp("CONTA!", 110, GREEN), cx, 1220, t, wt(1, "dentro") - 0.2, 0.25, -6)
def s2(img, t, T):
    pitch3d(img, T, 0, 6, dist=45, hgt=18, tgt=(0, -20, 0), dim=70)
    pop(img, jersey("10", "MESSI", 360, ARG), cx, 600, t, 0.0)
    for k, (wd, lab, y) in enumerate([("sete", "7 GOLS", 880), ("três", "3 ASSISTÊNCIAS", 1000), ("melhor", "MELHOR DA COPA", 1130)]):
        pop(img, chip(lab, 70, INK, GOLD if k == 2 else WHITE), cx, y, t, wt(2, wd) - 0.2, 0.25, (-3, 2, -2)[k])
def s3(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, GOLD, 14, 50))
    pop(img, chip("FINAL • ARG 3 x 3 FRA • 4 x 2 NOS PÊNALTIS", 42, WHITE, INK), cx, 420, t, 0.0)
    pop(img, chip("2 GOLS NA FINAL", 74, INK, GOLD), cx, 600, t, wt(3, "dois") - 0.2, 0.25, -3)
    pop(img, chip("1º PÊNALTI DA DISPUTA", 60, INK, WHITE), cx, 730, t, wt(3, "pênalti") - 0.3, 0.25, 3)
    if t > wt(3, "campeão") - 0.3:
        u = t - wt(3, "campeão") + 0.3; img.alpha_composite(confetti(W, H, u))
        pop(img, trophy(330), cx, 1010, u, 0.0); pop(img, txt("CAMPEÃO DO MUNDO", 100, GOLD), cx, 1260, u, 0.2, 0.3, -3)
def s4(img, t, T):
    pop(img, chip("HAALAND: 52 GOLS PELO CITY • TRÍPLICE COROA", 40, WHITE, (60, 130, 200)), cx, 420, t, 0.0)
    tp = wt(4, "perdeu") - 0.3
    if t > tp:
        u = ease((t - tp) / 1.0); d = ImageDraw.Draw(img); base = 1300
        for k, (nm, v, x, col) in enumerate([("MESSI", 462, 330, GOLD), ("HAALAND", 357, 750, (120, 190, 240))]):
            hh = 620 * v / 462 * u; d.rounded_rectangle((x - 130, base - hh, x + 130, base), 24, fill=col + (255,), outline=INK, width=6)
            paste(img, txt(str(int(v * u)), 80, WHITE), x, base - hh - 60, 1); paste(img, chip(nm, 50, INK, WHITE), x, base + 60, 1)
        if t > tp + 1.1: paste(img, chip("+105 PONTOS", 70, INK, GREEN), cx, 560, 1, back((t - tp - 1.1) / 0.25), -4)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, GOLD, 14, 40))
    pop(img, goldball(260, T), cx, 520, t, 0.0)
    pop(img, txt("JUSTO", 150, GREEN), cx, 820, t, 0.3); pop(img, txt("OU", 90, WHITE), cx, 960, t, 0.5); pop(img, txt("ROUBO?", 150, RED), cx, 1100, t, 0.7)
    pop(img, chip("COMENTA AÍ", 70, INK, WHITE), cx, 1320, t, 1.2)
S = Short("/home/claude/qua25/bol", BOL, [s0, s1, s2, s3, s4, s5], "BOLA DE OURO", ["night", "dark", "dark", "night", "dark", "night"], "Exhilarate", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("whoosh_boom", 0.5, 0.3), ("tambor_impacto", S.segs[1][0] + wt(1, "dentro"), 0.3), ("torcida_comemora", S.segs[3][0] + wt(3, "campeão"), 0.2), ("tambor_impacto", S.segs[4][0] + wt(4, "perdeu") + 1.1, 0.35)])
