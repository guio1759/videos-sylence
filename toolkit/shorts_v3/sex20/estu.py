from com import *
from scripts import ES
EST = lambda h: shield_stripes(h, label="EST")

def s0(img, t, T):  # O time que eliminou o Flamengo ... adversário na final
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 150, 150), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("ELIMINOU O", 120, WHITE, 12), cx, 420, 1, sc, -3)
    paste(img, txt("FLAMENGO", 180, AMB, 14), cx, 580, 1, sc, -3)
    paste(img, logo("FLA", 260), 330, 900, 1, 1, -8 * ease(t / 0.4))
    paste(img, EST(280), 760, 900, 1, 1.0 + 0.04 * math.sin(T * 6))
    paste(img, stamp("ELIMINADO", 76, RED), 330, 960, 1, 1, -12)
    if t > 1.6:
        pop(img, chip("RIVAL DO PALMEIRAS NA FINAL", 54, INK, AMB), cx, 1240, t, 1.6, 0.25, -3)
        pop(img, logo("PAL", 170), cx, 1400, t, 2.1)

def s1(img, t, T):  # 0 a 0, pênaltis 3 a 2
    pitch3d(img, T, 0, 7, dist=40, hgt=16, tgt=(40, 0, 0), dim=50)
    pop(img, chip("SEMIFINAL • MARACANÃ", 56, INK, WHITE), cx, 400, t, 0.0)
    pop(img, scorebox("FLA", EST(150), 0, 0, 140), cx, 640, t, 0.5, 0.3)
    pop(img, chip("PÊNALTIS", 70, WHITE, RED), cx, 870, t, 1.6)
    if t > 1.9: paste(img, scorebox("FLA", EST(150), 2, 3, 140), cx, 1080, 1, 0.85 + 0.15 * back((t - 1.9) / 0.3))

def s2(img, t, T):  # um a menos
    paste(img, redcard(360), cx, 700, 1, 0.3 + 0.7 * back(t / 0.3), 12 + shake(t, 0.3, 6))
    pop(img, txt("COM 1 A MENOS", 110, AMB), cx, 1020, t, 0.4)
    pop(img, chip("BOA PARTE DO 2º TEMPO", 52, INK, WHITE), cx, 1170, t, 0.9)

def s3(img, t, T):  # Palmeiras despachou o Fluminense nos pênaltis
    pop(img, chip("HORAS ANTES...", 62, INK, WHITE), cx, 400, t, 0.0)
    slide(img, logo("PAL", 280), 300, 720, t, 0.3, -400); slide(img, logo("FLU", 280), 780, 720, t, 0.45, 400)
    pop(img, chip("PÊNALTIS", 70, WHITE, RED), cx, 960, t, 1.6)
    pop(img, stamp("FINAL!", 130, GREEN), cx, 1160, t, 2.5, 0.25, -6)
    if t > 2.6: img.alpha_composite(confetti(W, H, t - 2.6))

def s4(img, t, T):  # final dia 28
    img.alpha_composite(rays(W, H, cx, 640, T, (255, 220, 140), 14, 50))
    pop(img, trophy(360), cx, 640, t, 0.0)
    for k, s in enumerate(["SÁBADO • 28/11", "17H", "CENTENÁRIO • MONTEVIDÉU"]):
        pop(img, chip(s, 60, INK, AMB if k == 0 else WHITE), cx, 940 + k * 140, t, 0.6 + k * 0.7)

def s5(img, t, T):  # Flamengo campeão BR / Palmeiras campeão da América
    pop(img, chip("OLHA QUE LOUCURA", 64, INK, AMB), cx, 380, t, 0.0, 0.25, -3)
    pop(img, logo("FLA", 220), 280, 640, t, 0.9); pop(img, chip("CAMPEÃO", 46, WHITE, RED), 280, 800, t, 1.3); pop(img, chip("BRASILEIRO?", 46, WHITE, RED), 280, 870, t, 1.4); pop(img, chip("SÁB 21", 50, INK, WHITE), 280, 960, t, 1.6)
    if t > 3.2:
        u = ease((t - 3.2) / 0.5); d = ImageDraw.Draw(img); d.line((440, 1060, 440 + 200 * u, 1060), fill=AMB, width=12)
        pop(img, chip("7 DIAS", 60, INK, AMB), 540, 1130, t, 3.4)
    pop(img, logo("PAL", 220), 800, 640, t, 3.9); pop(img, chip("CAMPEÃO", 46, WHITE, GREEN), 800, 800, t, 4.3); pop(img, chip("DA AMÉRICA?", 46, WHITE, GREEN), 800, 870, t, 4.4); pop(img, chip("SÁB 28", 50, INK, WHITE), 800, 960, t, 4.6)
    if t > 4.5: pop(img, trophy(200), 800, 1260, t, 4.5)

def s6(img, t, T):  # CTA
    pop(img, txt("O QUE VALE MAIS?", 110, AMB), cx, 480, t, 0.0)
    pop(img, chip("BRASILEIRÃO", 90, WHITE, BLUE), cx, 780, t, 0.6, 0.25, -3)
    pop(img, txt("OU", 90), cx, 920, t, 0.9)
    pop(img, chip("LIBERTADORES", 90, INK, AMB), cx, 1060, t, 1.2, 0.25, 3)
    pop(img, chip("COMENTA AÍ", 56, INK, WHITE), cx, 1260, t, 1.8)

S = Short("/home/claude/sex20/estu", ES, [s0, s1, s2, s3, s4, s5, s6], "FINAL DA LIBERTADORES",
          ["red", "dark", "dark", "green", "night", "blue", "dark"], "Volatile_Reaction", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("apito_curto", S.segs[1][0] + 1.6, 0.2), ("torcida_reacao_gol", S.segs[1][0] + 1.9, 0.2), ("tambor_impacto", S.segs[2][0], 0.3), ("torcida_comemora", S.segs[3][0] + 2.5, 0.2)])
