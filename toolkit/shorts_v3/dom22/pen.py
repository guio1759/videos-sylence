from com import *
from scripts import PEN
EST = lambda h: logo("EST", h)

def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 150, 150), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("SE FOR PROS", 110, WHITE, 12), cx, 400, 1, sc, -3)
    paste(img, txt("PÊNALTIS...", 140, AMB, 14), cx, 550, 1, sc, -3)
    paste(img, jersey("GOL", "MUSLERA", 380, (30, 30, 34)), cx, 860, 1, sc)
    if t > 1.4: pop(img, stamp("PROBLEMA!", 110, RED), cx, 1150, t, 1.4, 0.25, -6 + shake(t, 1.4, 10))

def s1(img, t, T):
    pitch3d(img, T, 0, 7, dist=40, hgt=16, tgt=(40, 0, 0), dim=60)
    pop(img, chip("SEMI • MARACANÃ", 60, INK, WHITE), cx, 400, t, 0.0)
    pop(img, EST(220), 300, 640, t, 0.2); pop(img, logo("FLA", 220), 780, 640, t, 0.3)
    for k in range(3): pop(img, check(130), 300 + k * 240, 900, t, 1.3 + k * 0.4)
    pop(img, chip("3 PÊNALTIS DEFENDIDOS", 60, INK, AMB), cx, 1080, t, 2.6)
    pop(img, stamp("FLAMENGO FORA", 80, RED), cx, 1250, t, 3.3, 0.25, -6)

def s2(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, (150, 255, 170), 14, 50))
    pop(img, chip("O PALMEIRAS TEM O SEU", 54, INK, WHITE), cx, 400, t, 0.0)
    pop(img, jersey("GOL", "C. MIGUEL", 420, (20, 120, 60)), cx, 740, t, 0.3)
    pop(img, stamp("PAREDÃO", 120, GREEN), cx, 1080, t, 1.2, 0.25, -5)

def s3(img, t, T):
    pop(img, chip("CARLOS MIGUEL", 64, WHITE, INK), cx, 400, t, 0.0)
    pop(img, shield_stripes(170, ((245, 245, 245), (20, 40, 120)), "LDU"), 300, 640, t, 0.3)
    pop(img, check(100), 560, 600, t, 0.8); pop(img, check(100), 680, 600, t, 1.1)
    pop(img, logo("FLU", 170), 300, 880, t, 1.8); pop(img, check(100), 560, 860, t, 2.3)
    pop(img, txt("3 DEFESAS", 120, AMB), cx, 1090, t, 3.0)
    pop(img, chip("2 CLASSIFICAÇÕES", 60, WHITE, GREEN), cx, 1240, t, 3.6)

def s4(img, t, T):
    pop(img, chip("PRESTA ATENÇÃO", 64, INK, AMB), cx, 400, t, 0.0, 0.25, -3)
    pop(img, txt("JOGO ÚNICO", 130, WHITE), cx, 620, t, 0.9)
    pop(img, chip("EMPATOU?", 64, WHITE, INK), cx, 830, t, 1.9)
    pop(img, chip("PRORROGAÇÃO", 64, INK, WHITE), cx, 970, t, 2.4)
    pop(img, chip("PÊNALTIS", 80, WHITE, RED), cx, 1130, t, 3.0, 0.25, 3)

def s5(img, t, T):
    pop(img, txt("QUEM PEGA MAIS?", 105, AMB), cx, 420, t, 0.0)
    pop(img, jersey("GOL", "C. MIGUEL", 300, (20, 120, 60)), 300, 760, t, 0.3)
    pop(img, txt("X", 100, AMB), cx, 760, t, 0.5)
    pop(img, jersey("GOL", "MUSLERA", 300, (30, 30, 34)), 780, 760, t, 0.6)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1150, t, 1.4)

S = Short("/home/claude/dom22/pen", PEN, [s0, s1, s2, s3, s4, s5], "DUELO DE GOLEIROS",
          ["night", "dark", "green", "dark", "dark", "night"], "Crossing_the_Chasm", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("torcida_aww", S.segs[1][0] + 1.4, 0.15), ("tambor_impacto", S.segs[1][0] + 3.3, 0.3),
                   ("whoosh_boom", S.segs[2][0] + 1.2, 0.3), ("tambor_impacto", S.segs[3][0] + 3.0, 0.3), ("apito_juiz", S.segs[4][0] + 3.0, 0.2)])
