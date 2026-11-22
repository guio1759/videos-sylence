from com import *
from scripts import ABL
EST = lambda h: logo("EST", h)

def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 220, 140), 14, 55))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("ABEL NA", 120, WHITE, 12), cx, 400, 1, sc, -3)
    paste(img, txt("HISTÓRIA?", 140, AMB, 14), cx, 550, 1, sc, -3)
    for k in range(3):
        tr = trophy(220) if k < 2 else trophy(220, (120, 120, 130))
        paste(img, tr, 250 + k * 290, 860, 1 if k < 2 or t > 0.5 else 0.4, sc * (1 + (0.08 * math.sin(T * 8) if k == 2 else 0)))
    if t > 0.5: paste(img, txt("?", 140, AMB, 12), 830, 850, 1, 1 + 0.08 * math.sin(T * 8))
    pop(img, chip("CLUBE DE SÓ 2 TÉCNICOS", 56, INK, AMB), cx, 1160, t, 1.4, 0.25, -2)

def s1(img, t, T):
    pop(img, chip("PRESTA ATENÇÃO", 64, INK, AMB), cx, 400, t, 0.0, 0.25, -3)
    pop(img, txt("3 TÍTULOS", 140, WHITE), cx, 620, t, 0.6)
    pop(img, txt("OU MAIS", 110, AMB), cx, 770, t, 0.9)
    for k in range(3): pop(img, trophy(170), 290 + k * 250, 1010, t, 1.4 + k * 0.3)
    pop(img, stamp("SÓ 2 TÉCNICOS", 80, RED), cx, 1230, t, 2.6, 0.25, -6 + shake(t, 2.6, 8))

def s2(img, t, T):  # Bianchi 4, Zubeldía 3
    pop(img, person(330, (235, 235, 240)), 290, 680, t, 0.0)
    pop(img, chip("CARLOS BIANCHI", 46, WHITE, INK), 290, 900, t, 0.1)
    pop(img, txt("4", 160, AMB), 290, 1070, t, 0.5)
    pop(img, person(330, (235, 235, 240)), 790, 680, t, 1.4)
    pop(img, chip("O. ZUBELDÍA", 46, WHITE, INK), 790, 900, t, 1.5)
    pop(img, txt("3", 160, AMB), 790, 1070, t, 1.9)
    pop(img, EST(130), 790, 1240, t, 2.6)
    pop(img, chip("VÉLEZ • BOCA", 40, INK, WHITE), 290, 1240, t, 0.8)

def s3(img, t, T):  # Abel 2 títulos, 4ª final
    pop(img, logo("PAL", 200), cx, 430, t, 0.0)
    pop(img, chip("ABEL FERREIRA", 64, WHITE, INK), cx, 600, t, 0.1)
    for k, y in enumerate(["2020", "2021"]):
        pop(img, trophy(170), 330 + k * 420, 820, t, 0.6 + k * 0.5); pop(img, chip(y, 50, INK, AMB), 330 + k * 420, 950, t, 0.7 + k * 0.5)
    pop(img, txt("4ª FINAL", 140, AMB, 12), cx, 1160, t, 2.6, 0.3, -3)
    pop(img, chip("PELO PALMEIRAS", 50, WHITE, GREEN), cx, 1300, t, 3.0)

def s4(img, t, T):  # coincidência Estudiantes
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 150, 150), 14, 35))
    pop(img, chip("OLHA A COINCIDÊNCIA", 60, INK, AMB), cx, 400, t, 0.0, 0.25, 3)
    pop(img, EST(340), cx, 760, t, 1.0)
    pop(img, chip("O TIME DO ZUBELDÍA", 64, WHITE, RED), cx, 1040, t, 2.6, 0.25, -3)
    pop(img, chip("TRI 1968 • 69 • 70", 54, INK, WHITE), cx, 1190, t, 3.2)

def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, (255, 220, 140), 14, 50))
    pop(img, txt("ABEL TRI?", 150, AMB, 14), cx, 520, t, 0.0)
    for k in range(3): pop(img, trophy(150), 330 + k * 210, 780, t, 0.3 + k * 0.2)
    pop(img, chip("SIM", 90, INK, GREEN), 330, 1030, t, 1.0, 0.25, -3)
    pop(img, chip("NÃO", 90, WHITE, RED), 750, 1030, t, 1.2, 0.25, 3)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1220, t, 1.8)

S = Short("/home/claude/dom22/abl", ABL, [s0, s1, s2, s3, s4, s5], "ABEL NA HISTÓRIA",
          ["night", "dark", "dark", "green", "red", "night"], "Hitman", 50.95)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("tambor_impacto", S.segs[1][0] + 2.6, 0.35), ("whoosh_boom", S.segs[2][0] + 0.5, 0.25),
                   ("whoosh_boom", S.segs[2][0] + 1.9, 0.25), ("tambor_impacto", S.segs[3][0] + 2.6, 0.35), ("tambor_impacto", S.segs[4][0] + 2.6, 0.3)])
