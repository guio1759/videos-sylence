import sys; sys.path.insert(0, "/home/claude/qui")
from engine import *
from scripts import A

cx = W / 2


def s0(img, t, T):  # Piquerez machucado... e agora?
    paste(img, txt("PIQUEREZ", 150, WHITE, 10), cx, 560, 1, 0.9 + 0.1 * back(t / 0.25), -3)
    paste(img, stamp("FORA", 170, RED), cx, 800, 1, 1.0 + 0.15 * max(0, 1 - t / 0.2), 8)
    pop(img, txt("E AGORA?", 130, AMB, 10), cx, 1100, t, 0.85)


def s1(img, t, T):  # Calma... garoto de 21 anos subestimado
    pop(img, txt("CALMA, PALMEIRENSE", 80), cx, 380, t, 0.0)
    pop(img, jersey(56, "ARTHUR", 440), cx, 800, t, 0.6, 0.35)
    pop(img, chip("21 ANOS", 70, INK, AMB), 300, 1080, t, 1.3, 0.25, -6)
    pop(img, stamp("SUBESTIMADO", 90, AMB), cx, 1240, t, 2.4, 0.3, -5)


def s2(img, t, T):  # lesão na coxa ... Arthur assume
    if t < 2.1:
        pop(img, chip("LESÃO NA COXA", 80, WHITE, RED), cx, 520, t, 0.0)
        pop(img, txt("AMISTOSO DO URUGUAI", 60), cx, 680, t, 0.6)
        pop(img, txt("13/11", 140, AMB), cx, 860, t, 0.9)
    else:
        u = t - 2.1
        slide(img, logo("PAL", 260), 260, 620, u, 0.0, -400)
        slide(img, jersey(56, "ARTHUR", 380), 760, 640, u, 0.15, 400)
        pop(img, chip("NOVO DONO DA LATERAL ESQUERDA", 50, INK, AMB), cx, 1000, u, 0.9)


def s3(img, t, T):  # sub-11 até profissional
    steps = [("SUB-11", "2017"), ("SUB-13", ""), ("SUB-15", ""), ("SUB-17", ""), ("SUB-20", ""), ("PROFISSIONAL", "2026")]
    for k, (a, b) in enumerate(steps):
        y = 1300 - k * 150; t0 = 0.25 + k * 0.45
        if t < t0: continue
        col = AMB if k in (0, 5) else WHITE
        slide(img, chip(a + ("  •  " + b if b else ""), 60, INK, col), cx, y, t, t0, -300, 0.3)
    pop(img, txt("11 ANOS", 110, AMB), cx, 330, t, 0.0)


def s4(img, t, T):  # mãe Guarulhos -> treino, esperava no parque
    p = panel(900, 620, (15, 18, 30, 230)); paste(img, p, cx, 760, 1)
    ax, ay, bx, by = 230, 900, 850, 620
    d = ImageDraw.Draw(img); u = ease(t / 1.6)
    for k in range(int(30 * u)):
        f0, f1 = k / 30, (k + 0.55) / 30
        d.line((ax + (bx - ax) * f0, ay + (by - ay) * f0, ax + (bx - ax) * f1, ay + (by - ay) * f1), fill=AMB, width=10)
    paste(img, chip("GUARULHOS", 44, INK, WHITE), ax, ay + 80, 1); paste(img, chip("TREINO", 44, INK, WHITE), bx, by - 80, 1)
    for x, y in ((ax, ay), (bx, by)): d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=GREEN, outline=WHITE, width=5)
    pop(img, txt("A MÃE ESPERAVA NO PARQUE", 62, WHITE), cx, 1180, t, 1.7)
    pop(img, person(170, (255, 210, 120)), bx - 40, by + 170, t, 1.9)


def s5(img, t, T):  # bicampeão sub-20
    pop(img, trophy(330), 330, 720, t, 0.1); pop(img, trophy(330), 750, 720, t, 0.45)
    pop(img, chip("2024", 64, INK, AMB), 330, 960, t, 0.2); pop(img, chip("2025", 64, INK, AMB), 750, 960, t, 0.55)
    pop(img, txt("BICAMPEÃO BRASILEIRO SUB-20", 62), cx, 1150, t, 0.9)
    if t > 0.5: img.alpha_composite(confetti(W, H, t - 0.5))


def s6(img, t, T):  # estreia, campeão paulista, Abel
    pop(img, chip("ESTREIA • JAN 2026", 70, INK, WHITE), cx, 420, t, 0.0)
    pop(img, trophy(260), 300, 700, t, 1.2); pop(img, txt("CAMPEÃO", 76, AMB), 700, 650, t, 1.3); pop(img, txt("PAULISTA 2026", 62), 700, 750, t, 1.4)
    if t > 2.6:
        fade(img, panel(920, 300, (255, 255, 255, 240), border=(0, 0, 0, 0)), cx, 1090, t, 2.6, 0.3)
        fade(img, text_el("“Ele dá PASSE,", font("blk", 70), INK, 0, shadow=False), cx, 1040, t, 2.7, 0.3)
        fade(img, text_el("não cruzamento.”", font("blk", 70), INK, 0, shadow=False), cx, 1125, t, 2.9, 0.3)
        fade(img, chip("ABEL FERREIRA", 40, WHITE, GREEN), cx, 1240, t, 3.2, 0.3)


def s7(img, t, T):  # números
    if t > 0.9: paste(img, odometer(33, 2, 190, t - 0.9, 0.6, 0), 290, 640)
    pop(img, txt("JOGOS EM 2026", 44), 290, 860, t, 1.0)
    if t > 2.0: paste(img, odometer(7, 2, 190, t - 2.0, 0.5, 0), 790, 640)
    pop(img, txt("NA LIBERTADORES", 44), 790, 860, t, 2.1)
    pop(img, stamp("RESERVA?", 130, RED), cx, 1150, t, 3.6, 0.3, -8)


def s8(img, t, T):  # Flamengo sábado + final Libertadores dia 28
    pop(img, logo("PAL", 220), 300, 520, t, 0.0); pop(img, txt("x", 110), cx, 520, t, 0.1); pop(img, logo("FLA", 220), 780, 520, t, 0.2)
    pop(img, chip("SÁBADO • 16:30", 60, INK, WHITE), cx, 720, t, 0.4)
    pop(img, trophy(300), cx, 1000, t, 1.6)
    pop(img, chip("FINAL DA LIBERTADORES • 28/11", 52, INK, AMB), cx, 1230, t, 1.8)


def s9(img, t, T):  # CTA
    paste(img, jersey(56, "ARTHUR", 300), cx, 520, 1)
    pop(img, txt("O ARTHUR DÁ CONTA?", 84, AMB), cx, 820, t, 0.0)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1060, t, 0.3); pop(img, chip("NÃO", 110, WHITE, RED), 750, 1060, t, 0.45)
    pop(img, chip("COMENTA AÍ", 56, INK, WHITE), cx, 1250, t, 0.6)


S = Short("/home/claude/qui/arthur", A, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9], "A JOIA DA LATERAL",
          ["dark", "green", "dark", "green", "night", "green", "blue", "dark", "night", "green"], "Rising_Game", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("apito_curto", S.segs[8][0] + 0.1, 0.2)])
