from com import *
from scripts import DSF

def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 150, 150), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("FALTAM 5 DIAS", 115, WHITE, 12), cx, 400, 1, sc, -3)
    paste(img, txt("E O ABEL PODE", 95, WHITE, 10), cx, 540, 1, sc, -3)
    paste(img, txt("PERDER PEÇAS!", 120, AMB, 12), cx, 670, 1, sc, -3)
    paste(img, logo("PAL", 260), cx, 960, 1, sc)
    if t > 1.2: pop(img, chip("DEPARTAMENTO MÉDICO", 56, WHITE, RED), cx, 1200, t, 1.2, 0.25, -2)

def s1(img, t, T):  # Piquerez
    pop(img, jersey("LE", "PIQUEREZ", 400), cx, 640, t, 0.0)
    pop(img, chip("LESÃO NA COXA • DATA FIFA", 52, WHITE, INK), cx, 940, t, 1.0)
    pop(img, chip("EM TRATAMENTO", 60, INK, AMB), cx, 1090, t, 2.6, 0.25, -2)
    pop(img, stamp("SEM GARANTIA", 90, RED), cx, 1250, t, 3.8, 0.25, 6 + shake(t, 3.8, 8))

def s2(img, t, T):  # Arthur
    pitch3d(img, T, 0, 6, dist=45, hgt=18, tgt=(0, -20, 0), dim=60)
    pop(img, jersey("LE", "ARTHUR", 380), cx, 650, t, 0.0)
    pop(img, chip("CRIA DA ACADEMIA", 60, WHITE, GREEN), cx, 930, t, 1.0, 0.25, 2)
    pop(img, chip("FAVORITO PRA LATERAL", 60, INK, AMB), cx, 1080, t, 2.2, 0.25, -2)

def s3(img, t, T):  # Paulinho
    pop(img, jersey("ATA", "PAULINHO", 380), cx, 640, t, 0.0)
    pop(img, chip("PANTURRILHA", 64, WHITE, RED), cx, 920, t, 0.8)
    pop(img, chip("BANCO", 80, INK, WHITE), 330, 1100, t, 2.0, 0.25, -3)
    pop(img, chip("POUCOS MINUTOS", 54, INK, AMB), 730, 1100, t, 2.8, 0.25, 3)

def s4(img, t, T):  # Murilo
    img.alpha_composite(rays(W, H, cx, 700, T, (150, 255, 170), 14, 45))
    pop(img, chip("A BOA NOTÍCIA", 66, INK, AMB), cx, 400, t, 0.0, 0.25, -3)
    pop(img, jersey("ZAG", "MURILO", 380), cx, 700, t, 0.4)
    pop(img, chip("TRANSIÇÃO FÍSICA", 60, WHITE, INK), cx, 980, t, 1.6)
    pop(img, stamp("MAIS PERTO DE VOLTAR", 64, GREEN), cx, 1150, t, 2.8, 0.25, -5)

def s5(img, t, T):
    pop(img, txt("NA FINAL:", 120, WHITE), cx, 420, t, 0.0)
    pop(img, jersey("LE", "PIQUEREZ", 300), 300, 760, t, 0.3)
    pop(img, txt("OU", 90, AMB), cx, 760, t, 0.6)
    pop(img, jersey("LE", "ARTHUR", 300), 780, 760, t, 0.8)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1150, t, 1.6)

S = Short("/home/claude/dom22/dsf", DSF, [s0, s1, s2, s3, s4, s5], "DESFALQUES DA FINAL",
          ["red", "dark", "dark", "dark", "green", "night"], "Interloper", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("tambor_impacto", S.segs[1][0] + 3.8, 0.3), ("torcida_comemora", S.segs[4][0] + 2.8, 0.18)])
