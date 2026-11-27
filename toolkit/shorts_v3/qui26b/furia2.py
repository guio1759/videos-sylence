from fx2 import *
from scripts import FURIA
def dur(i): return S.segs[i][1] - S.segs[i][0] + 0.1
def s0(img, t, T):
    img.alpha_composite(FX.kb(FX.load(P["novest"]), t, dur(0) + 0.5, (1.0, 1.12), (0.5, 0.62), (0.5, 0.55), vig=170))
    img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    sc = 1.0 + 0.04 * math.sin(min(t, 0.4) * 8)
    paste(img, big("O NOVORIZONTINO", 120, WHITE), cx, 330, 1, sc, -3)
    paste(img, big("VIROU FURIA!", 180, AMB), cx, 500, 1, sc, 2)
    paste(img, crest(380), 300 + shake(t, 0.1, 10), 900, 1, 0.85 + 0.15 * back(t / 0.25), -6)
    pop(img, big("+", 130), cx + 20, 900, t, 0.15)
    paste(img, furia_badge(400), 780, 900, 1, 0.85 + 0.15 * back(t / 0.25), 5)
    pop(img, stamp("NA SÉRIE A", 110, GREEN), cx, 1240, t, wt(0, "série") - 0.15, 0.25, -6)
    cr(img, "novest")
def s1(img, t, T):
    img.alpha_composite(FX.kb(FX.load(P["furia1"]), t, dur(1) + 0.3, (1.0, 1.15), (0.5, 0.5), (0.52, 0.45), vig=150))
    pop(img, furia_badge(420), cx, 380, t, wt(1, "fúria") - 0.2 if wt(1, "fúria") > 0.3 else 0.3)
    pop(img, chip("GIGANTE DOS GAMES", 64, INK, AMB), cx, 560, t, wt(1, "gigante") - 0.2, 0.25, -3)
    tp = wt(1, "campeão") - 0.3
    pop(img, crest(300), 300, 1180, t, tp, 0.25, -5)
    pop(img, trophy(230), 760, 1130, t, tp + 0.15, 0.25, 5)
    pop(img, chip("CAMPEÃO DA SÉRIE B", 56, WHITE, INK), 760, 1310, t, tp + 0.3, 0.25, 3)
    cr(img, "furia1")
def s2(img, t, T):
    img.alpha_composite(blurbg("novest", t, dur(2), (0, 0, 0, 120), 8, f0=(0.5, 0.7), f1=(0.5, 0.6)))
    pop(img, chip("JANEIRO 2027 • PAULISTÃO", 60, INK, WHITE), cx, 380, t, 0.0)
    tj = wt(2, "fúria") - 0.3
    pop(img, jersey("10", "FURIA", 380, (20, 20, 20), (250, 205, 20)), cx, 780, t, tj, 0.25, -3)
    pop(img, chip("FURIA NOVORIZONTINO", 78, INK, AMB), cx, 1090, t, tj + 0.25, 0.25, 2)
    cr(img, "novest")
def s3(img, t, T):
    img.alpha_composite(blurbg("furia1", t, dur(3), (120, 0, 0, 150), 12))
    pop(img, stamp("NÃO É COMPRA", 110, RED), cx, 460, t, wt(3, "compra") - 0.2, 0.25, -5)
    pop(img, big("...AINDA!", 140, AMB), cx, 630, t, wt(3, "ainda") - 0.2)
    to = wt(3, "opção") - 0.25
    pop(img, envelope(420, min(1, max(0, (t - to) / 0.5))), cx, 930, t, to - 0.2)
    pop(img, chip("OPÇÃO DE COMPRA", 74, INK, AMB), cx, 1190, t, to, 0.25, -2)
    emo(img, "dinheiro", 880, 870, t, to + 0.3, 170)
    cr(img, "furia1")
def s4(img, t, T):
    img.alpha_composite(FX.kb(FX.load(P["novest"]), t, dur(4), (1.25, 1.05), (0.5, 0.75), (0.5, 0.6), vig=170))
    img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 80)))
    pop(img, chip("NOVO HORIZONTE (SP)", 60, INK, WHITE), cx, 380, t, 0.0)
    tn = wt(4, "trinta") - 0.3
    if t > tn:
        u = t - tn; paste(img, odometer(38000, 5, 140, round(min(u, 1.0), 2), 0.8), cx, 620, 1, back(min(1, u / 0.3)))
        pop(img, chip("HABITANTES", 60, INK, AMB), cx, 770, u, 0.3)
    tg = wt(4, "série") - 0.3
    pop(img, crest(260), 330, 1080, t, tg, 0.25, -5); pop(img, icon_pad(280), 760, 1080, t, tg + 0.2, 0.25, 5)
    emo(img, "explodindo", cx, 1300, t, wt(4, "games") - 0.2, 170)
    cr(img, "novest")
def s5(img, t, T):
    img.alpha_composite(blurbg("novest", t, dur(5), (0, 0, 0, 140), 14))
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 60), 14, 35))
    pop(img, crest(300), 330, 600, t, 0.0, 0.25, -5); pop(img, furia_badge(340), 760, 600, t, 0.1, 0.25, 5)
    pop(img, big("DÁ CERTO?", 160, AMB), cx, 900, t, wt(5, "certo") - 0.3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1100, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1100, t, wt(5, "não") - 0.2, 0.25, 4)
    FX.credit(img, CRJ["novest"], y=H - 190); FX.credit(img, EM.CREDIT, y=H - 150)
S = Short("/home/claude/x26/furia", FURIA, [s0, s1, s2, s3, s4, s5], "NOVORIZONTINO • SÉRIE A", "dark", "Exhilarate", 8)
wt = mkwt(S)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "série"), 0.3), ("tambor_impacto", S.segs[3][0] + wt(3, "compra"), 0.3),
                   ("camera_click", S.segs[3][0] + wt(3, "opção"), 0.25), ("torcida_comemora", S.segs[1][0] + wt(1, "campeão"), 0.12)])
