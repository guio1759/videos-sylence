from fx2 import *
nov_shield = crest
from scripts import FURIA
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 880, T, (255, 220, 60), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("O NOVORIZONTINO", 100, WHITE, 12), cx, 380, 1, sc, -3)
    paste(img, txt("VIROU FURIA!", 140, AMB, 14), cx, 520, 1, sc, 2)
    paste(img, nov_shield(330), 300 + shake(t, 0.1, 10), 880, 1, 0.85 + 0.15 * back(t / 0.25), -6)
    pop(img, txt("+", 120), cx, 880, t, 0.15)
    paste(img, furia_badge(400), 770, 880, 1, 0.85 + 0.15 * back(t / 0.25), 5)
    pop(img, stamp("NA SÉRIE A", 110, GREEN), cx, 1200, t, wt(0, "série") - 0.15, 0.25, -6)
def s1(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (180, 210, 255), 14, 35))
    pop(img, icon_pad(380), cx, 560, t, 0.0, 0.25, -5)
    pop(img, furia_badge(360), cx, 820, t, wt(1, "furia") - 0.2)
    pop(img, chip("GIGANTE DOS GAMES", 64, INK, AMB), cx, 980, t, wt(1, "gigante") - 0.2, 0.25, -3)
    tp = wt(1, "campeão") - 0.3
    pop(img, trophy(260), 300, 1220, t, tp, 0.25, -5)
    pop(img, chip("CAMPEÃO DA SÉRIE B", 56, WHITE, INK), 690, 1220, t, tp + 0.15, 0.25, 3)
def s2(img, t, T):
    pitch3d(img, T, 0, 7, dist=44, hgt=18, dim=60)
    pop(img, chip("JANEIRO 2027 • PAULISTÃO", 60, INK, WHITE), cx, 400, t, 0.0)
    tj = wt(2, "furia") - 0.3
    pop(img, jersey("10", "FURIA", 360, (20, 20, 20), (250, 205, 20)), cx, 760, t, tj, 0.25, -3)
    pop(img, chip("FURIA NOVORIZONTINO", 74, INK, AMB), cx, 1060, t, tj + 0.25, 0.25, 2)
def s3(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 150, 150), 14, 35))
    pop(img, stamp("NÃO É COMPRA", 110, RED), cx, 480, t, wt(3, "compra") - 0.2, 0.25, -5)
    pop(img, txt("...AINDA!", 110, AMB), cx, 640, t, wt(3, "ainda") - 0.2)
    to = wt(3, "opção") - 0.25
    pop(img, envelope(420, min(1, max(0, (t - to) / 0.5))), cx, 930, t, to - 0.2)
    pop(img, chip("OPÇÃO DE COMPRA", 74, INK, AMB), cx, 1190, t, to, 0.25, -2)
    emo(img, "dinheiro", 880, 870, t, to + 0.3, 170)
def s4(img, t, T):
    pitch3d(img, T, 80, 6, dist=46, hgt=20, dim=90)
    pop(img, chip("NOVO HORIZONTE (SP)", 60, INK, WHITE), cx, 400, t, 0.0)
    tn = wt(4, "trinta") - 0.3
    if t > tn:
        u = t - tn; paste(img, odometer(38000, 5, 140, round(min(u, 1.0), 2), 0.8), cx, 640, 1, back(min(1, u / 0.3)))
        pop(img, chip("HABITANTES", 60, INK, AMB), cx, 790, u, 0.3)
    tg = wt(4, "série") - 0.3
    pop(img, nov_shield(230), 330, 1080, t, tg, 0.25, -5); pop(img, icon_pad(260), 760, 1080, t, tg + 0.2, 0.25, 5)
    emo(img, "explodindo", cx, 1300, t, wt(4, "games") - 0.2, 180)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 60), 14, 40))
    pop(img, nov_shield(230), 330, 560, t, 0.0, 0.25, -5); pop(img, furia_badge(330), 760, 560, t, 0.1, 0.25, 5)
    pop(img, txt("DÁ CERTO?", 130, WHITE), cx, 880, t, wt(5, "certo") - 0.3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1100, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1100, t, wt(5, "não") - 0.2, 0.25, 4)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1290, t, wt(5, "comenta") - 0.1)
    FX.credit(img, EM.CREDIT, y=H - 110)
S = Short("/home/claude/x26/furia", FURIA, [s0, s1, s2, s3, s4, s5], "NOVORIZONTINO • SÉRIE A", ["amber", "dark", "amber", "red", "dark", "amber"], "Exhilarate", 8)
wt = mkwt(S)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "série"), 0.3), ("tambor_impacto", S.segs[3][0] + wt(3, "compra"), 0.3),
                   ("camera_click", S.segs[3][0] + wt(3, "opção"), 0.25), ("torcida_comemora", S.segs[1][0] + wt(1, "campeão"), 0.12)])
