from com import *
from scripts import ZO

def s0(img, t, T):  # Libertadores vale muito mais
    img.alpha_composite(rays(W, H, cx, 640, T, (255, 220, 140), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, trophy(300), cx, 560, 1, sc)
    paste(img, txt("LIBERTADORES", 140, AMB, 14), cx, 820, 1, sc, -3)
    paste(img, txt("VALE MUITO MAIS", 92, WHITE, 10), cx, 960, 1, sc, -3)
    paste(img, txt("QUE O BRASILEIRÃO", 70, WHITE, 8), cx, 1060, 1, sc, -3)
    if t > 1.7:
        pop(img, logo("FLA", 180), 300, 1290, t, 1.7, 0.25, shake(t, 1.9, 10))
        pop(img, chip("E O FLAMENGO SABE", 50, WHITE, RED), 690, 1290, t, 1.9, 0.25, -3)

def s1(img, t, T):  # Copa do Brasil, Vitória 2x0
    pop(img, chip("MAIO • COPA DO BRASIL", 60, INK, WHITE), cx, 420, t, 0.0)
    slide(img, logo("VIT", 260), 300, 700, t, 0.3, -400); slide(img, logo("FLA", 260), 780, 700, t, 0.45, 400)
    pop(img, scorebox("VIT", "FLA", 2, 0, 140), cx, 980, t, 1.8, 0.3)
    pop(img, chip("BARRADÃO", 54, INK, AMB), cx, 1150, t, 2.3)
    pop(img, stamp("ELIMINADO", 100, RED), cx, 760, t, 3.0, 0.2, -10 + shake(t, 3.0, 8))

def s2(img, t, T):  # Libertadores, Estudiantes, Maracanã, 3 pênaltis
    pitch3d(img, T, 0, 7, dist=40, hgt=16, tgt=(40, 0, 0), dim=60)
    pop(img, chip("OUTUBRO • LIBERTADORES", 60, INK, WHITE), cx, 400, t, 0.0)
    pop(img, logo("EST", 260), cx, 650, t, 0.8)
    pop(img, chip("DENTRO DO MARACANÃ!", 66, INK, AMB), cx, 880, t, 1.6, 0.25, -3)
    for k in range(3):
        pop(img, check(150, False), 290 + k * 250, 1100, t, 3.0 + k * 0.3, 0.2)
    pop(img, chip("3 PÊNALTIS PERDIDOS", 58, WHITE, RED), cx, 1270, t, 3.9)

def s3(img, t, T):  # campeão hoje = obrigação
    img.alpha_composite(rays(W, H, cx, 720, T, (255, 150, 150), 14, 35))
    pop(img, chip("SE FOR CAMPEÃO HOJE...", 60, INK, WHITE), cx, 400, t, 0.0)
    pop(img, logo("FLA", 280), cx, 700, t, 0.3)
    pop(img, chip("PARABÉNS 👏".replace(" 👏", ""), 70, INK, AMB), cx, 940, t, 1.0)
    pop(img, stamp("OBRIGAÇÃO", 130, RED), cx, 1150, t, 2.4, 0.2, -6 + shake(t, 2.4, 10))
    pop(img, chip("COM ESSE ELENCO", 50, WHITE, INK), cx, 1320, t, 2.0)

def s4(img, t, T):  # Palmeiras na final contra o mesmo Estudiantes
    img.alpha_composite(rays(W, H, cx, 760, T, (150, 255, 170), 14, 50))
    pop(img, chip("PRESTA ATENÇÃO", 64, INK, AMB), cx, 400, t, 0.0, 0.25, -3)
    slide(img, logo("PAL", 280), 290, 760, t, 1.0, -400); slide(img, logo("EST", 280), 790, 760, t, 1.2, 400)
    pop(img, txt("X", 110, AMB), cx, 760, t, 1.4)
    pop(img, stamp("FINAL!", 130, GREEN), cx, 1040, t, 1.8, 0.25, -6)
    pop(img, chip("O MESMO ESTUDIANTES", 58, INK, WHITE), cx, 1230, t, 3.2)
    if t > 1.9: img.alpha_composite(confetti(W, H, t - 1.9))

def s5(img, t, T):  # CTA
    pop(img, txt("VOCÊ TROCARIA?", 110, AMB), cx, 440, t, 0.0)
    pop(img, chip("BRASILEIRÃO", 80, WHITE, BLUE), cx, 660, t, 0.4, 0.25, -3)
    pop(img, txt("POR", 70), cx, 780, t, 0.8)
    pop(img, chip("LIBERTADORES", 90, INK, AMB), cx, 900, t, 1.0, 0.25, 3)
    pop(img, chip("SIM", 90, WHITE, GREEN), 330, 1140, t, 2.0, 0.25, -4)
    pop(img, chip("NÃO", 90, WHITE, RED), 750, 1140, t, 2.2, 0.25, 4)

S = Short("/home/claude/sab21/zoe", ZO, [s0, s1, s2, s3, s4, s5], "LIBERTADORES x BRASILEIRÃO",
          ["night", "red", "dark", "red", "green", "dark"], "Volatile_Reaction", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", S.segs[1][0] + 1.8, 0.3), ("tambor_impacto", S.segs[1][0] + 3.0, 0.3),
                   ("torcida_aww", S.segs[2][0] + 3.0, 0.22), ("tambor_impacto", S.segs[3][0] + 2.4, 0.35), ("torcida_comemora", S.segs[4][0] + 1.8, 0.22)])
