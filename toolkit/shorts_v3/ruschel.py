import sys; sys.path.insert(0, "/home/claude/qui")
from engine import *
from scripts import R

cx = W / 2
GOLD = (255, 205, 80)


def r0(img, t, T):
    paste(img, chip("10 ANOS ATRÁS", 64, INK, WHITE), cx, 430, 1)
    paste(img, txt("ELE", 150), cx, 640, 1, 0.94 + 0.06 * back(t / 0.3))
    paste(img, txt("SOBREVIVEU", 150, GOLD, 10), cx, 810, 1, 0.94 + 0.06 * back(t / 0.3), -2)
    fade(img, txt("À QUEDA DE UM AVIÃO", 70), cx, 990, t, 1.2)


def r1(img, t, T):
    pop(img, jersey(28, "RUSCHEL", 440), cx, 640, t, 0.0)
    pop(img, chip("ÚLTIMO JOGO • 14/11", 64, INK, AMB), cx, 960, t, 0.6)
    fade(img, txt("NOS BRAÇOS DA TORCIDA", 70), cx, 1120, t, 2.0)


def r2(img, t, T):
    lines(img, ["ALAN", "RUSCHEL"], 520, t, 0.0, 160, WHITE, 1.0, 0.2, [WHITE, GOLD])
    pop(img, chip("LATERAL-ESQUERDO", 60, INK, WHITE), cx, 930, t, 1.3)
    pop(img, chip("REVELADO NO JUVENTUDE", 60, WHITE, GREEN), cx, 1060, t, 2.1)


def r3(img, t, T):
    pop(img, logo("CHA", 300), cx, 600, t, 0.2)
    pop(img, chip("A PEQUENA CHAPECOENSE", 60, INK, WHITE), cx, 860, t, 1.4)
    pop(img, trophy(200), 230, 1080, t, 2.6)
    pop(img, txt("FINAL DA", 66), 640, 1040, t, 2.7); pop(img, txt("SUL-AMERICANA", 66, GOLD), 640, 1120, t, 2.8)


def r4(img, t, T):
    pop(img, chip("ÚLTIMO JOGO ANTES DA VIAGEM", 52, INK, WHITE), cx, 420, t, 0.0)
    pop(img, logo("PAL", 210), 200, 680, t, 1.3); pop(img, logo("CHA", 210), 880, 680, t, 1.45)
    pop(img, txt("1 x 0", 120), cx, 680, t, 1.7)
    pop(img, chip("27/11/2016 • TÍTULO DO PALMEIRAS", 46, INK, AMB), cx, 920, t, 2.6)


def r5(img, t, T):
    paste(img, candle(420, T), cx, 640, ease(t / 0.8))
    fade(img, txt("28 DE NOVEMBRO", 100), cx, 990, t, 0.3)
    fade(img, txt("DE 2016", 80, (200, 200, 200)), cx, 1100, t, 0.6)
    fade(img, chip("PERTO DE MEDELLÍN", 50, INK, WHITE), cx, 1230, t, 2.4)


def r6(img, t, T):
    fade(img, txt("71 VÍTIMAS", 150), cx, 520, t, 0.0, 0.6)
    for k in range(6):
        x = 190 + k * 140; hi = k == 2 and t > 3.2
        if t > 1.9 + k * 0.12:
            fade(img, person(200, GOLD if hi else (220, 220, 220)), x, 900, t, 1.9 + k * 0.12, 0.3)
    fade(img, txt("6 SOBREVIVENTES", 80, WHITE), cx, 1100, t, 2.2)
    if t > 3.2: fade(img, chip("ALAN", 50, INK, GOLD), 190 + 2 * 140, 740, t, 3.2, 0.3)


def r7(img, t, T):
    pop(img, stamp("FRATURA NA COLUNA", 86, RED), cx, 640, t, 0.0, 0.3, -4)
    fade(img, txt("RISCO DE FICAR", 80), cx, 900, t, 1.3)
    fade(img, txt("TETRAPLÉGICO", 110, GOLD), cx, 1020, t, 1.6)


def r8(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, alpha=45))
    pop(img, txt("8 MESES DEPOIS", 110, WHITE), cx, 520, t, 0.0)
    pop(img, chip("CAMP NOU", 110, INK, GOLD), cx, 760, t, 1.4)
    pop(img, txt("x BARCELONA • 07/08/2017", 56), cx, 920, t, 2.2)


def r9(img, t, T):
    pop(img, chip("NOVEMBRO DE 2017", 60, INK, WHITE), cx, 420, t, 0.0)
    pop(img, txt("JOGO OFICIAL", 90, GOLD), cx, 560, t, 0.6)
    pop(img, logo("CHA", 220), 280, 820, t, 1.5); pop(img, txt("x", 100), cx, 820, t, 1.6); pop(img, logo("FLA", 220), 800, 820, t, 1.7)
    pop(img, chip("APLAUDIDO PELAS DUAS TORCIDAS", 50, INK, AMB), cx, 1080, t, 3.0)


def r10(img, t, T):
    pop(img, txt("+9 ANOS", 170, GOLD, 12), cx, 700, t, 0.0)
    pop(img, txt("JOGANDO", 90), cx, 900, t, 0.3)


def r11(img, t, T):
    pop(img, txt("ÚLTIMO JOGO", 90), cx, 420, t, 0.0)
    pop(img, txt("2 x 0", 170, WHITE), cx, 620, t, 0.9)
    pop(img, chip("ACESSO À SÉRIE A", 80, INK, AMB), cx, 850, t, 1.9)
    pop(img, stamp("SAIU CARREGADO", 90, WHITE), cx, 1080, t, 3.2, 0.3, -5)
    if t > 1.9: img.alpha_composite(confetti(W, H, t - 1.9))


def r12(img, t, T):
    lines(img, ["“OBRIGADO,", "FUTEBOL.", "EU FARIA TUDO", "OUTRA VEZ.”"], 450, t, 0.4, 112, WHITE, 1.12, 0.45, [WHITE, WHITE, GOLD, GOLD])
    fade(img, txt("— ALAN RUSCHEL", 58, (210, 210, 210)), cx, 1010, t, 2.6)


def r13(img, t, T):
    paste(img, logo("CHA", 240), 330, 560, ease(t / 0.5)); paste(img, candle(330, T), 760, 560, ease(t / 0.5))
    fade(img, txt("29/11 • 10 ANOS", 96, GOLD), cx, 860, t, 0.4)
    fade(img, chip("DEIXE SUA HOMENAGEM", 64, INK, WHITE), cx, 1020, t, 2.6)
    fade(img, txt("GUERREIROS DA CHAPE", 72), cx, 1170, t, 3.6)


S = Short("/home/claude/qui/ruschel", R, [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13], "SOBREVIVENTE",
          ["night", "green", "dark", "green", "dark", "night", "night", "dark", "blue", "green", "green", "green", "dark", "night"],
          "Heartbreaking", 0, sfx_soft=True)
if __name__ == "__main__":
    main(S, extra=[("torcida_comemora", S.segs[11][0] + 1.9, 0.12), ("torcida_aww", S.segs[9][0] + 3.0, 0.1)])
