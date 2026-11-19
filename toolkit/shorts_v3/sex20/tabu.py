from com import *
from scripts import TB

def s0(img, t, T):  # 9 anos sem vencer em casa
    img.alpha_composite(rays(W, H, cx, 700, T, (255, 230, 150), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("9 ANOS", 230, AMB, 14), cx, 470, 1, sc, -3)
    paste(img, txt("SEM VENCER O", 92, WHITE, 10), cx, 650, 1, sc, -3)
    paste(img, txt("FLAMENGO EM CASA!", 92, WHITE, 10), cx, 760, 1, sc, -3)
    paste(img, logo("PAL", 230), 330, 1060, 1); paste(img, logo("FLA", 230), 750, 1060, 1)
    if t > 0.7: paste(img, stamp("TABU", 120, RED), cx, 1300, 1, 1 + 0.25 * max(0, 1 - (t - 0.7) / 0.15), -6)

def s1(img, t, T):  # última vitória 2017, 2 a 0
    pop(img, chip("ÚLTIMA VITÓRIA", 66, INK, WHITE), cx, 420, t, 0.0)
    pop(img, txt("NOV 2017", 170, AMB), cx, 620, t, 0.4)
    pop(img, scorebox("PAL", "FLA", 2, 0, 140), cx, 920, t, 2.4, 0.3)
    pop(img, chip("ALLIANZ PARQUE", 50, INK, WHITE), cx, 1120, t, 2.8)

RES = [("2018", "1x1", "E"), ("2019", "1x3", "D"), ("2020", "1x1", "E"), ("2021", "1x3", "D"), ("2022", "1x1", "E"), ("2023", "1x1", "E"), ("2024", "0x0", "E"), ("2025", "0x2", "D")]
def s2(img, t, T):  # 8 jogos 5E 3D
    for k, (y, sc, r) in enumerate(RES):
        t0 = k * 0.13; x = 290 if k % 2 == 0 else 790; yy = 420 + (k // 2) * 150
        pop(img, chip(f"{y}  {sc}", 58, WHITE if r == "D" else INK, RED if r == "D" else WHITE), x, yy, t, t0, 0.2)
    pop(img, chip("5 EMPATES", 80, INK, AMB), cx, 1080, t, 1.4, 0.25, -3)
    pop(img, chip("3 DERROTAS", 80, WHITE, RED), cx, 1240, t, 2.1, 0.25, 3)

def s3(img, t, T):  # empate = campeão no Nubank Parque
    pitch3d(img, T, 200, 9, hgt=40, dim=50)
    pop(img, chip("SE EMPATAR NO SÁBADO", 62, INK, WHITE), cx, 430, t, 0.0)
    pop(img, logo("FLA", 300), cx, 760, t, 1.2)
    if t > 1.4: img.alpha_composite(rays(W, H, cx, 760, T, (255, 220, 140), 14, 40))
    pop(img, stamp("CAMPEÃO", 140, RED), cx, 1010, t, 1.8, 0.25, -6)
    pop(img, chip("DENTRO DO NUBANK PARQUE", 52, INK, AMB), cx, 1230, t, 2.8)
    if t > 2.0: img.alpha_composite(confetti(W, H, t - 2.0))

def s4(img, t, T):  # contas
    pop(img, chip("PALMEIRAS PRECISA", 58, WHITE, GREEN), cx, 400, t, 0.4)
    for k, lg in enumerate(["FLA", "CHA", "CFC"]):
        x = 250 + k * 290; t0 = 0.9 + k * 0.3
        pop(img, logo(lg, 150), x, 590, t, t0); pop(img, check(90, True), x + 70, 660, t, t0 + 0.15)
    pop(img, txt("VENCER 3 DE 3", 74, AMB), cx, 770, t, 1.9)
    pop(img, chip("E O FLAMENGO...", 58, WHITE, RED), cx, 930, t, 2.8)
    for k, lg in enumerate(["CFC", "CHA"]):
        x = 380 + k * 320; t0 = 3.2 + k * 0.3
        pop(img, logo(lg, 150), x, 1110, t, t0); pop(img, check(90, False), x + 70, 1180, t, t0 + 0.15)
    pop(img, txt("NÃO PODE VENCER MAIS!", 64), cx, 1300, t, 3.9)

def s5(img, t, T):  # 3 a 0 no Maracanã
    pitch3d(img, T, 60, 10, hgt=38, dim=40)
    pop(img, chip("PRESTA ATENÇÃO", 66, INK, AMB), cx, 420, t, 0.0, 0.25, -3)
    pop(img, chip("1º TURNO • MARACANÃ", 56, INK, WHITE), cx, 560, t, 1.0)
    pop(img, scorebox("FLA", "PAL", 0, 3, 150), cx, 860, t, 2.2, 0.3)
    if t > 2.4: img.alpha_composite(confetti(W, H, t - 2.4))

def s6(img, t, T):  # CTA
    pop(img, txt("QUEBRA O TABU?", 110, AMB), cx, 470, t, 0.0)
    pop(img, scorebox("PAL", "FLA", "?", "?", 140), cx, 800, t, 0.3)
    pop(img, chip("COMENTA O SEU PLACAR", 60, INK, WHITE), cx, 1060, t, 0.8)

S = Short("/home/claude/sex20/tabu", TB, [s0, s1, s2, s3, s4, s5, s6], "O TABU DE 9 ANOS",
          ["dark", "night", "dark", "dark", "blue", "dark", "green"], "Interloper", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("tambor_impacto", S.segs[1][0] + 2.4, 0.3), ("torcida_aww", S.segs[2][0] + 2.1, 0.2), ("whoosh_boom", S.segs[3][0] + 1.8, 0.35), ("torcida_comemora", S.segs[5][0] + 2.2, 0.2)])
