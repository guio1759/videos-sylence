from com import *
from scripts import SEQ
EST = lambda h: logo("EST", h)
SEQL = [("FLA", "2019"), ("PAL", "2020"), ("PAL", "2021"), ("FLA", "2022"), ("FLU", "2023"), ("BOT", "2024"), ("FLA", "2025")]

def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 220, 140), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("7 ANOS", 170, AMB, 14), cx, 400, 1, sc, -3)
    paste(img, txt("SÓ DÁ BRASIL", 110, WHITE, 12), cx, 560, 1, sc, -3)
    paste(img, trophy(280), cx, 840, 1, sc)
    if t > 2.6: pop(img, EST(200), cx, 1150, t, 2.6, 0.25)
    if t > 3.2: pop(img, stamp("AMEAÇA", 80, RED), cx, 1300, t, 3.2, 0.25, -6 + shake(t, 3.2, 8))

def s1(img, t, T):
    pop(img, chip("CAMPEÕES DA LIBERTADORES", 54, INK, WHITE), cx, 380, t, 0.0)
    for k, (c, y) in enumerate(SEQL):
        t0 = 0.4 + k * 0.5; col, row = k % 2, k // 2
        x = 300 + col * 480 if k < 6 else cx; yy = 600 + row * 230
        pop(img, logo(c, 150), x - 90, yy, t, t0)
        pop(img, chip(y, 56, INK, AMB), x + 90, yy, t, t0 + 0.1)

def s2(img, t, T):
    pop(img, chip("ÚLTIMO ARGENTINO CAMPEÃO", 54, WHITE, INK), cx, 420, t, 0.0)
    pop(img, trophy(260), cx, 700, t, 0.3); pop(img, chip("RIVER PLATE", 80, WHITE, RED), cx, 900, t, 0.6, 0.25, -3)
    pop(img, txt("2018", 170, AMB, 14), cx, 1110, t, 1.6, 0.3, -3)

def s3(img, t, T):
    pop(img, EST(260), cx, 580, t, 0.0)
    for k in range(4): pop(img, trophy(150), 240 + k * 200, 870, t, 0.6 + k * 0.25)
    pop(img, chip("1968 • 69 • 70 • 2009", 50, INK, WHITE), cx, 1020, t, 1.4)
    pop(img, stamp("QUER A 5ª", 90, RED), cx, 1180, t, 2.2, 0.25, -6)

def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (150, 255, 170), 14, 50))
    pop(img, chip("PRESTA ATENÇÃO", 64, INK, AMB), cx, 380, t, 0.0, 0.25, -3)
    pop(img, logo("PAL", 230), 300, 640, t, 0.8); pop(img, txt("4", 150, AMB), 300, 860, t, 1.6)
    pop(img, txt("=", 130, WHITE), cx, 700, t, 2.6)
    pop(img, logo("FLA", 230), 780, 640, t, 3.0); pop(img, txt("4", 150, AMB), 780, 860, t, 3.2)
    pop(img, chip("BRASILEIROS COM MAIS TÍTULOS", 50, WHITE, GREEN), cx, 1080, t, 3.8)

def s5(img, t, T):
    pop(img, txt("A SEQUÊNCIA", 110, WHITE), cx, 440, t, 0.0)
    pop(img, txt("CONTINUA?", 130, AMB), cx, 580, t, 0.2)
    slide(img, logo("PAL", 220), 300, 840, t, 0.4, -400); slide(img, EST(220), 780, 840, t, 0.55, 400)
    pop(img, txt("X", 90, AMB), cx, 840, t, 0.7)
    pop(img, chip("SIM", 90, INK, GREEN), 330, 1090, t, 1.2, 0.25, -3)
    pop(img, chip("NÃO", 90, WHITE, RED), 750, 1090, t, 1.4, 0.25, 3)

S = Short("/home/claude/dom22/seq", SEQ, [s0, s1, s2, s3, s4, s5], "BRASIL x ARGENTINA",
          ["night", "dark", "red", "red", "green", "night"], "Volatile_Reaction", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("tambor_impacto", S.segs[0][0] + 3.2, 0.3), ("tambor_impacto", S.segs[2][0] + 1.6, 0.35),
                   ("tambor_impacto", S.segs[4][0] + 3.2, 0.35), ("torcida_comemora", S.segs[4][0] + 3.8, 0.2)])
