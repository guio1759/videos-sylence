from com import *
from scripts import NP
EST = lambda h: logo("EST", h)

def s0(img, t, T):  # empatou, Fla campeão, agora é a final
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 220, 140), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, scorebox("PAL", "FLA", 1, 1, 110), cx, 380, 1, 1)
    paste(img, trophy(300), cx, 700, 1, sc)
    paste(img, txt("AGORA SÓ", 105, WHITE, 12), cx, 960, 1, sc, -3)
    paste(img, txt("IMPORTA A FINAL!", 98, AMB, 12), cx, 1100, 1, sc, -3)
    if t > 0.6: pop(img, chip("FLAMENGO CAMPEÃO BRASILEIRO", 46, WHITE, RED), cx, 1270, t, 0.6, 0.25, -2)

def s1(img, t, T):  # 1x1, gols
    pitch3d(img, T, 0, 7, dist=40, hgt=16, tgt=(-40, 0, 0), dim=50)
    pop(img, chip("NUBANK PARQUE • 36ª RODADA", 54, INK, WHITE), cx, 400, t, 0.0)
    pop(img, scorebox("PAL", "FLA", 1, 1, 140), cx, 640, t, 0.3, 0.3)
    pop(img, chip("ARIAS • DE CABEÇA • 11' 1ºT", 54, WHITE, GREEN), cx, 900, t, 1.0, 0.25, -2)
    pop(img, chip("SAMUEL LINO • 30' 2ºT", 54, WHITE, RED), cx, 1040, t, 2.3, 0.25, 2)

def s2(img, t, T):  # o que muda pra final
    pop(img, txt("O QUE MUDA", 120, AMB), cx, 420, t, 0.0)
    pop(img, txt("PRA FINAL?", 110, WHITE), cx, 550, t, 0.2)
    items = [("QUASE TODOS OS TITULARES", 1.6), ("NINGUÉM EXPULSO", 3.0), ("CARTÃO DO BR NÃO VALE", 4.3)]
    for k, (s, t0) in enumerate(items):
        pop(img, check(110), 170, 780 + k * 190, t, t0, 0.25)
        slide(img, chip(s, 50, INK, WHITE), 600, 780 + k * 190, t, t0, 300)

def s3(img, t, T):  # Barboza livre, Paulinho dúvida
    pop(img, person(380, (230, 245, 235)), 300, 760, t, 0.0)
    pop(img, chip("BARBOZA", 60, WHITE, INK), 300, 1010, t, 0.2)
    pop(img, stamp("LIBERADO", 70, GREEN), 300, 1130, t, 1.4, 0.25, -8)
    pop(img, person(380, (235, 235, 235)), 780, 760, t, 2.2)
    pop(img, chip("PAULINHO", 60, WHITE, INK), 780, 1010, t, 2.4)
    pop(img, stamp("DÚVIDA", 70, AMB), 780, 1130, t, 3.0, 0.25, 8)

def s4(img, t, T):  # faltam 7 dias
    img.alpha_composite(rays(W, H, cx, 640, T, (255, 220, 140), 14, 50))
    paste(img, txt("FALTAM", 100, WHITE), cx, 420, 1, 0.8 + 0.2 * back(t / 0.3))
    paste(img, txt("7 DIAS", 220, AMB, 16), cx, 620, 1, (0.6 + 0.4 * back(t / 0.35)) * (1 + 0.03 * math.sin(T * 8)), shake(t, 0.35, 6))
    for k, s in enumerate(["SÁBADO • 28/11 • 17H", "CENTENÁRIO • MONTEVIDÉU"]):
        pop(img, chip(s, 60, INK, AMB if k == 0 else WHITE), cx, 900 + k * 150, t, 1.0 + k * 1.2)
    pop(img, trophy(220), cx, 1260, t, 2.6)

def s5(img, t, T):  # CTA placar
    img.alpha_composite(rays(W, H, cx, 700, T, (150, 255, 170), 14, 45))
    slide(img, logo("PAL", 270), 290, 650, t, 0.0, -400); slide(img, EST(270), 790, 650, t, 0.15, 400)
    pop(img, txt("X", 110, AMB), cx, 650, t, 0.3)
    pop(img, stamp("FINAL!", 120, GREEN), cx, 900, t, 0.6, 0.25, -6)
    pop(img, txt("SEU PLACAR?", 120, AMB), cx, 1110, t, 1.6)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1260, t, 2.2)

S = Short("/home/claude/sab21b/pos", NP, [s0, s1, s2, s3, s4, s5], "AGORA É A FINAL",
          ["night", "dark", "dark", "green", "night", "dark"], "Rising_Game", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("apito_juiz", S.segs[1][0] + 0.1, 0.2), ("chute_bola_1", S.segs[1][0] + 0.95, 0.3), ("torcida_reacao_gol", S.segs[1][0] + 1.0, 0.2),
                   ("chute_bola_2", S.segs[1][0] + 2.25, 0.3), ("torcida_aww", S.segs[1][0] + 2.3, 0.18), ("tambor_impacto", S.segs[4][0] + 0.35, 0.35), ("torcida_comemora", S.segs[5][0] + 0.6, 0.22)])
