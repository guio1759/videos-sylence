from com import *
from scripts import CAM
EST = lambda h: logo("EST", h)
CER = lambda h: shield_stripes(h, ((200, 20, 40), (20, 50, 150)), "CER")
LDU = lambda h: shield_stripes(h, ((245, 245, 245), (20, 40, 120)), "LDU")

def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (150, 255, 170), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("CHEGOU", 130, WHITE, 12), cx, 400, 1, sc, -3)
    paste(img, txt("SOFRENDO...", 120, AMB, 12), cx, 540, 1, sc, -3)
    paste(img, logo("PAL", 300), cx, 820, 1, sc * (1 + 0.03 * math.sin(T * 9)))
    if t > 1.6: pop(img, stamp("PERIGOSO", 110, RED), cx, 1110, t, 1.6, 0.25, -7 + shake(t, 1.6, 10))

def s1(img, t, T):  # grupo
    pop(img, chip("FASE DE GRUPOS • GRUPO F", 56, INK, WHITE), cx, 400, t, 0.0)
    rows = [("CER", "CERRO PORTEÑO", 13), ("PAL", "PALMEIRAS", 11)]
    for k, (c, n, p) in enumerate(rows):
        y = 620 + k * 200; t0 = 0.5 + k * 0.6
        if t < t0: continue
        pn = panel(900, 160, (18, 18, 22, 235) if c != "PAL" else (20, 110, 60, 240)); paste(img, pn, cx, y, ease((t - t0) / 0.3))
        pop(img, txt(f"{k+1}º", 80), 200, y, t, t0)
        pop(img, CER(110) if c == "CER" else logo("PAL", 110), 320, y, t, t0)
        pop(img, txt(n, 44), 580, y, t, t0)
        pop(img, txt(f"{p} PTS", 52, AMB), 890, y, t, t0)
    pop(img, chip("3V • 2E • 1D", 60, INK, AMB), cx, 1100, t, 2.0)

def s2(img, t, T):  # oitavas cerro
    pitch3d(img, T, 20, 7, dist=40, hgt=16, tgt=(40, 0, 0), dim=60)
    pop(img, chip("OITAVAS", 66, INK, AMB), cx, 380, t, 0.0, 0.25, -3)
    slide(img, logo("PAL", 230), 300, 640, t, 0.2, -400); slide(img, CER(230), 780, 640, t, 0.35, 400)
    pop(img, chip("IDA 1x1 • VOLTA 1x0", 58, WHITE, INK), cx, 880, t, 1.0)
    pop(img, chip("GUSTAVO GÓMEZ ⚽", 66, WHITE, GREEN), cx, 1040, t, 2.2, 0.25, 2)
    pop(img, stamp("NO PARAGUAI", 70, AMB), cx, 1210, t, 3.0, 0.25, -6)

def s3(img, t, T):  # quartas LDU, Carlos Miguel 2 penaltis
    pop(img, chip("QUARTAS • QUITO", 60, INK, WHITE), cx, 380, t, 0.0)
    pop(img, scorebox(LDU(140), "PAL", 3, 2, 120), cx, 580, t, 0.2, 0.3)
    pop(img, chip("A LDU VIROU!", 60, WHITE, RED), cx, 760, t, 1.0, 0.25, -3)
    pop(img, jersey("GOL", "C. MIGUEL", 300, (30, 30, 34)), cx, 1010, t, 2.0)
    for k in range(2): pop(img, check(110), 330 + k * 420, 1010, t, 2.8 + k * 0.4)
    pop(img, chip("2 PÊNALTIS DEFENDIDOS", 54, INK, AMB), cx, 1240, t, 3.2)

def s4(img, t, T):  # semi Flu
    pitch3d(img, T, -20, 7, dist=40, hgt=16, tgt=(-40, 0, 0), dim=60)
    pop(img, chip("SEMIFINAL", 66, INK, AMB), cx, 380, t, 0.0, 0.25, 3)
    slide(img, logo("PAL", 220), 300, 620, t, 0.2, -400); slide(img, logo("FLU", 220), 780, 620, t, 0.35, 400)
    pop(img, chip("AGREGADO 2x2", 64, WHITE, INK), cx, 860, t, 1.0)
    pop(img, chip("PÊNALTIS: 5x3", 72, INK, WHITE), cx, 1010, t, 2.2, 0.25, -2)
    pop(img, chip("MARLON FREITAS BATEU O ÚLTIMO", 46, WHITE, GREEN), cx, 1160, t, 3.2)
    if t > 3.4: img.alpha_composite(confetti(W, H, t - 3.4))

def s5(img, t, T):  # CTA
    img.alpha_composite(rays(W, H, cx, 650, T, (150, 255, 170), 14, 45))
    pop(img, txt("2 DECISÕES", 120, WHITE), cx, 400, t, 0.0)
    pop(img, txt("NOS PÊNALTIS", 110, AMB), cx, 530, t, 0.2)
    slide(img, logo("PAL", 220), 300, 760, t, 0.6, -400); slide(img, EST(220), 780, 760, t, 0.75, 400)
    pop(img, txt("X", 90, AMB), cx, 760, t, 0.9)
    pop(img, chip("CASCA-GROSSA", 70, INK, AMB), cx, 990, t, 2.0, 0.25, -3)
    pop(img, txt("OU", 70), cx, 1110, t, 2.3)
    pop(img, chip("SORTE?", 70, WHITE, BLUE), cx, 1230, t, 2.5, 0.25, 3)

S = Short("/home/claude/dom22/cam", CAM, [s0, s1, s2, s3, s4, s5], "CAMINHO ATÉ A FINAL",
          ["night", "dark", "dark", "dark", "dark", "green"], "Five_Armies", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("chute_bola_1", S.segs[2][0] + 2.1, 0.3), ("torcida_reacao_gol", S.segs[2][0] + 2.2, 0.2),
                   ("torcida_aww", S.segs[3][0] + 1.0, 0.18), ("whoosh_boom", S.segs[3][0] + 2.8, 0.3), ("tambor_impacto", S.segs[4][0] + 2.2, 0.35),
                   ("torcida_comemora", S.segs[4][0] + 3.3, 0.22)])
