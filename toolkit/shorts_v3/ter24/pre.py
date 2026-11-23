from com import *
from scripts import PRE
EST = lambda h: logo("EST", h)

def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 140), 14, 55))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("90 MINUTOS", 140, WHITE, 12), cx, 380, 1, sc, -3)
    paste(img, txt("VALEM", 100, WHITE, 10), cx, 520, 1, sc, -3)
    paste(img, txt("+ DE R$ 130 MI", 124, AMB, 12), cx, 660, 1, sc, -3)
    paste(img, trophy(330), cx, 990, 1, sc)
    if t > 2.2: img.alpha_composite(confetti(W, H, t - 2.2))
    if t > 2.4: pop(img, chip("PRO PALMEIRAS", 64, WHITE, GREEN), cx, 1270, t, 2.4, 0.25, -3)

def s1(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 220, 140), 14, 45))
    pop(img, chip("PRÊMIO DO CAMPEÃO • CONMEBOL", 50, INK, WHITE), cx, 380, t, 0.0)
    pop(img, trophy(300), cx, 680, t, 0.2)
    if t > 0.8:
        paste(img, txt("US$", 90, WHITE), 260, 1010, 1)
        paste(img, odometer(25, 2, 150, t - 0.8, 1.2), 560, 1010, 1)
        paste(img, txt("MI", 110, AMB), 830, 1010, 1)
    if t > 2.6: img.alpha_composite(confetti(W, H, t - 2.6, 5))

def stack(img, x, n, t, t0, col, base=1150):
    for k in range(n):
        tk = t0 + k * 0.07
        if t < tk: break
        d = ImageDraw.Draw(img); y = base - k * 22
        d.rounded_rectangle((x - 130, y - 22, x + 130, y + 2), 8, fill=col + (255,), outline=INK, width=4)

def s2(img, t, T):
    pop(img, chip("CAMPEÃO", 64, INK, AMB), 300, 400, t, 0.0, 0.25, -2)
    pop(img, chip("VICE", 64, WHITE, INK), 780, 400, t, 0.2, 0.25, 2)
    stack(img, 300, 25, t, 0.3, (60, 190, 100)); stack(img, 780, 7, t, 1.2, (60, 190, 100))
    pop(img, txt("25", 120, AMB), 300, 1260, t, 0.5); pop(img, txt("7", 120, WHITE), 780, 1260, t, 1.3)
    if t > 2.2: pop(img, stamp("18 MI DE DIFERENÇA", 70, RED), cx, 1420, t, 2.2, 0.25, -6 + shake(t, 2.2, 8))

PH = [("GRUPOS + VITÓRIAS", "2,02"), ("OITAVAS", "1,25"), ("QUARTAS", "1,7"), ("SEMIFINAL", "2,3"), ("TÍTULO", "25")]
def s3(img, t, T):
    pop(img, chip("A CAMPANHA INTEIRA (US$ MI)", 50, INK, WHITE), cx, 360, t, 0.0)
    for k, (a, b) in enumerate(PH):
        y = 520 + k * 135; t0 = 0.3 + k * 0.35
        slide(img, chip(a, 50, WHITE, INK), 380, y, t, t0, -500)
        slide(img, chip(b, 56, INK, AMB if k == 4 else WHITE), 820, y, t, t0 + 0.1, 500)
    if t > 2.4: pop(img, chip("US$ 32 MILHÕES", 92, INK, AMB), cx, 1270, t, 2.4, 0.25, -3)

def s4(img, t, T):
    pitch3d(img, T, 20, 8, dist=70, hgt=30, dim=80)
    pop(img, txt("JOGO ÚNICO", 140, AMB, 12), cx, 420, t, 0.0, 0.3, -3)
    slide(img, logo("PAL", 230), 300, 760, t, 0.3, -400); slide(img, EST(230), 780, 760, t, 0.4, 400)
    pop(img, txt("X", 100, WHITE), cx, 760, t, 0.6)
    pop(img, chip("CENTENÁRIO • SÁB 28/11 • 17H", 50, INK, WHITE), cx, 1000, t, 0.9)
    pop(img, stamp("GANHOU, LEVA TUDO", 74, GREEN), cx, 1180, t, 2.0, 0.25, -5 + shake(t, 2.0, 8))

def s5(img, t, T):
    pop(img, txt("SE FOR CAMPEÃO...", 100, WHITE), cx, 420, t, 0.0)
    pop(img, txt("QUAL REFORÇO?", 118, AMB), cx, 560, t, 0.3)
    pop(img, jersey("?", "REFORÇO", 380), cx, 880, t, 0.6, 0.3, 3 * math.sin(T * 3))
    pop(img, chip("COMENTA O NOME", 64, INK, WHITE), cx, 1180, t, 1.4)

S = Short("/home/claude/ter24/pre", PRE, [s0, s1, s2, s3, s4, s5], "PRÊMIO DA FINAL",
          ["green", "night", "dark", "dark", "dark", "green"], "Volatile_Reaction", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("torcida_comemora", 2.2, 0.15), ("tambor_impacto", S.segs[1][0] + 2.0, 0.3),
                   ("whoosh_boom", S.segs[2][0] + 2.2, 0.3), ("tambor_impacto", S.segs[3][0] + 2.4, 0.35), ("apito_curto", S.segs[4][0] + 0.1, 0.25),
                   ("tambor_impacto", S.segs[4][0] + 2.0, 0.3)])
