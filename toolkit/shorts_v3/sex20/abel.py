from com import *
from scripts import AB

def s0(img, t, T):  # O Abel jogou a toalha!
    rays_im = rays(W, H, cx, 820, T, (255, 120, 120), 14, 60); img.alpha_composite(rays_im)
    sc = 1.0 + 0.06 * math.sin(min(t, 0.4) * 8)
    y = 300 + 850 * ease(t / 0.9); paste(img, towel(360, t), cx + 160 + 30 * math.sin(t * 6), y, 1, 1, 25 * math.sin(t * 5))
    paste(img, txt("O ABEL", 165, WHITE, 12), cx, 470, 1, sc, -3)
    paste(img, txt("JOGOU A", 165, WHITE, 12), cx, 650, 1, sc, -3)
    paste(img, txt("TOALHA!", 190, AMB, 12), cx, 850, 1, sc, -3)
    if t > 0.85: paste(img, stamp("DESISTIU?", 100, RED), cx, 1300, 1, 1 + 0.2 * max(0, 1 - (t - 0.85) / 0.15), 7)

def s1(img, t, T):  # Presta atenção ... derrota pro Cruzeiro
    pop(img, chip("PRESTA ATENÇÃO", 76, INK, AMB), cx, 430, t, 0.0, 0.25, -3)
    pop(img, scorebox("CRU", "PAL", 2, 1, 140), cx, 780, t, 0.6, 0.3)
    pop(img, chip("MINEIRÃO • 18/11", 52, INK, WHITE), cx, 1000, t, 1.0)
    pop(img, stamp("VIRADA", 120, RED), cx, 1220, t, 1.7, 0.25, -6)

def s2(img, t, T):  # Este título está entregue.
    dx = shake(t, 0.55, 22)
    paste(img, panel(960, 560, (255, 255, 255, 245), border=(0, 0, 0, 0)), cx + dx, 820, 1)
    fade(img, text_el("“ESTE TÍTULO", font("blk", 98), INK, 0, shadow=False), cx + dx, 660, t, 0.0, 0.2)
    fade(img, text_el("ESTÁ", font("blk", 98), INK, 0, shadow=False), cx + dx, 790, t, 0.2, 0.2)
    pop(img, text_el("ENTREGUE.”", font("blk", 130), RED, 0, shadow=False), cx + dx, 940, t, 0.5, 0.25)
    pop(img, chip("ABEL FERREIRA", 52, WHITE, GREEN), cx, 1180, t, 0.3)

def s3(img, t, T):  # Flamengo abriu 6 ... empate dá o título
    pitch3d(img, T, 20, 8, hgt=42, dim=50)
    pop(img, logo("FLA", 210), 290, 470, t, 0.0); pop(img, logo("PAL", 210), 790, 470, t, 0.15)
    paste(img, odometer(79, 2, 150, t, 0.7, 60), 290, 720) if t > 0 else None
    paste(img, odometer(73, 2, 150, t, 0.7, 60), 790, 720)
    pop(img, chip("+6 PONTOS", 80, WHITE, RED), cx, 930, t, 0.9, 0.25, -4)
    if t > 2.2:
        pop(img, chip("SÁBADO • NA CASA DO PALMEIRAS", 48, INK, WHITE), cx, 1090, t, 2.2)
        pop(img, stamp("EMPATE = TÍTULO", 96, AMB), cx, 1270, t, 3.0, 0.25, -5)
        pop(img, trophy(170), 900, 1120, t, 3.4)

def s4(img, t, T):  # três dias pra preparar a final
    paste(img, odometer(3, 1, 260, t, 0.5, 9), cx, 560)
    pop(img, txt("DIAS", 120, AMB), cx, 790, t, 0.3)
    rows = [("SÁB 21", "FLA"), ("TER 24", "CHA"), ("SÁB 28", None)]
    for k, (dd, lg) in enumerate(rows):
        t0 = 0.8 + k * 0.55; y = 960 + k * 150
        slide(img, chip(dd, 58, INK, WHITE if lg else AMB), 330, y, t, t0, -400)
        if lg: slide(img, logo(lg, 110), 640, y, t, t0 + 0.1, 400)
        else: slide(img, chip("FINAL DA LIBERTADORES", 46, INK, AMB), 700, y, t, t0 + 0.1, 400)

def s5(img, t, T):  # o que for melhor pro Palmeiras
    img.alpha_composite(rays(W, H, cx, 700, T, (140, 255, 170), 14, 55))
    paste(img, logo("PAL", 380), cx, 700, 1, 0.9 + 0.1 * back(t / 0.3))
    pop(img, txt("“O QUE FOR MELHOR", 74), cx, 1010, t, 0.6)
    pop(img, txt("PRO PALMEIRAS”", 96, AMB), cx, 1110, t, 0.9)
    pop(img, chip("POUPAR PRA FINAL?", 60, WHITE, RED), cx, 1290, t, 1.8, 0.25, -4)

def s6(img, t, T):  # CTA
    pop(img, logo("PAL", 190), 300, 470, t, 0.0); pop(img, txt("x", 100), cx, 470, t, 0.05); pop(img, logo("FLA", 190), 780, 470, t, 0.1)
    pop(img, txt("TIME RESERVA", 110, AMB), cx, 720, t, 0.2)
    pop(img, txt("CONTRA O FLAMENGO?", 70), cx, 840, t, 0.35)
    pop(img, chip("SIM", 120, WHITE, GREEN), 330, 1080, t, 1.4); pop(img, chip("NÃO", 120, WHITE, RED), 750, 1080, t, 1.55)
    pop(img, chip("COMENTA AÍ", 56, INK, WHITE), cx, 1270, t, 1.9)

S = Short("/home/claude/sex20/abel", AB, [s0, s1, s2, s3, s4, s5, s6], "TÍTULO ENTREGUE?",
          ["red", "dark", "night", "dark", "blue", "green", "dark"], "Hitman", 50.95)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_grave", 0.4, 0.3), ("tambor_impacto", S.segs[2][0] + 0.5, 0.35), ("torcida_aww", S.segs[3][0] + 3.0, 0.2)])
