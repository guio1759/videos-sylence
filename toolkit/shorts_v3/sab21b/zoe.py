from com import *
from scripts import ZB
EST = lambda h: logo("EST", h)

def s0(img, t, T):  # fez a obrigação, mas a que vale mais...
    img.alpha_composite(rays(W, H, cx, 700, T, (255, 220, 140), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("LIBERTADORES", 118, AMB, 14), cx, 420, 1, sc, -3)
    paste(img, txt("VALE MUITO MAIS!", 100, WHITE, 10), cx, 560, 1, sc, -3)
    paste(img, logo("FLA", 220), 300, 860, 1, 1)
    paste(img, stamp("SÓ OBRIGAÇÃO", 56, RED), 300, 1040, 1, 1, -8)
    paste(img, trophy(260), 780, 860, 1, sc)
    if t > 1.8: pop(img, logo("PAL", 150), 780, 1080, t, 1.8, 0.25)

def s1(img, t, T):  # parabéns, era obrigação
    img.alpha_composite(rays(W, H, cx, 720, T, (255, 150, 150), 14, 35))
    pop(img, chip("CAMPEÃO BRASILEIRO", 60, INK, WHITE), cx, 400, t, 0.0)
    pop(img, logo("FLA", 280), cx, 680, t, 0.2)
    pop(img, chip("PARABÉNS!", 70, INK, AMB), cx, 920, t, 0.4)
    pop(img, chip("COM ESSE ELENCO...", 54, WHITE, INK), cx, 1080, t, 1.4)
    pop(img, stamp("OBRIGAÇÃO", 130, RED), cx, 1260, t, 2.6, 0.2, -6 + shake(t, 2.6, 10))

def s2(img, t, T):  # Copa do Brasil
    pop(img, chip("MAIO • COPA DO BRASIL", 60, INK, WHITE), cx, 400, t, 0.0)
    slide(img, logo("VIT", 260), 300, 680, t, 0.2, -400); slide(img, logo("FLA", 260), 780, 680, t, 0.35, 400)
    pop(img, scorebox("VIT", "FLA", 2, 0, 130), cx, 960, t, 1.4, 0.3)
    pop(img, chip("BARRADÃO", 54, INK, AMB), cx, 1130, t, 2.8)
    pop(img, stamp("ELIMINADO", 80, RED), 780, 700, t, 3.2, 0.2, -10 + shake(t, 3.2, 8))

def s3(img, t, T):  # Libertadores semifinal
    pitch3d(img, T, 0, 7, dist=40, hgt=16, tgt=(40, 0, 0), dim=60)
    pop(img, chip("OUTUBRO • SEMI DA LIBERTADORES", 54, INK, WHITE), cx, 400, t, 0.0)
    pop(img, EST(260), cx, 650, t, 0.6)
    pop(img, chip("DENTRO DO MARACANÃ!", 66, INK, AMB), cx, 880, t, 2.2, 0.25, -3)
    pop(img, chip("PÊNALTIS", 70, WHITE, RED), cx, 1040, t, 3.4)
    pop(img, stamp("ELIMINADO", 100, RED), cx, 1220, t, 3.9, 0.2, 8 + shake(t, 3.9, 8))

def s4(img, t, T):  # mesmo Estudiantes x Palmeiras na final
    img.alpha_composite(rays(W, H, cx, 760, T, (150, 255, 170), 14, 50))
    pop(img, chip("PRESTA ATENÇÃO", 64, INK, AMB), cx, 400, t, 0.0, 0.25, -3)
    slide(img, logo("PAL", 280), 290, 740, t, 1.0, -400); slide(img, EST(280), 790, 740, t, 1.2, 400)
    pop(img, txt("X", 110, AMB), cx, 740, t, 1.4)
    pop(img, stamp("FINAL!", 130, GREEN), cx, 1010, t, 1.8, 0.25, -6)
    pop(img, chip("SÁBADO 28/11 • MONTEVIDÉU", 54, INK, WHITE), cx, 1200, t, 2.8)
    if t > 1.9: img.alpha_composite(confetti(W, H, t - 1.9))

def s5(img, t, T):  # CTA
    pop(img, txt("QUAL VALE MAIS?", 110, AMB), cx, 460, t, 0.0)
    pop(img, chip("LIBERTADORES", 90, INK, AMB), cx, 720, t, 0.4, 0.25, -3)
    pop(img, txt("OU", 90), cx, 860, t, 0.8)
    pop(img, chip("BRASILEIRÃO", 90, WHITE, BLUE), cx, 1000, t, 1.0, 0.25, 3)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1220, t, 2.0)

S = Short("/home/claude/sab21b/zoe", ZB, [s0, s1, s2, s3, s4, s5], "LIBERTADORES x BRASILEIRÃO",
          ["night", "red", "red", "dark", "green", "dark"], "Volatile_Reaction", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("tambor_impacto", S.segs[1][0] + 2.6, 0.35), ("whoosh_boom", S.segs[2][0] + 1.4, 0.3),
                   ("torcida_aww", S.segs[2][0] + 3.2, 0.2), ("apito_juiz", S.segs[3][0] + 3.4, 0.2), ("torcida_aww", S.segs[3][0] + 3.9, 0.2), ("torcida_comemora", S.segs[4][0] + 1.8, 0.22)])
