from com import *
from scripts import VAL
EST = lambda h: logo("EST", h)

def money(v, t, t0, dur=1.0, size=120, col=AMB):
    u = ease(max(0, t - t0) / dur); return txt(f"US$ {int(v * u)} MI", size, col, 12)

def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 820, T, (255, 220, 140), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("VALE 4 VEZES", 130, WHITE, 12), cx, 390, 1, sc, -3)
    paste(img, txt("MAIS!", 190, AMB, 14), cx, 560, 1, sc, -3)
    paste(img, logo("PAL", 380), 330, 900, 1, sc)
    paste(img, EST(150), 800, 1000, 1, sc)
    paste(img, txt("x4", 110, AMB), 640, 860, 1, sc, 8)
    if t > 2.6: pop(img, stamp("PERIGO", 100, RED), cx, 1250, t, 2.6, 0.25, -6 + shake(t, 2.6, 8))

def s1(img, t, T):
    pop(img, chip("VALOR DE MERCADO DO ELENCO", 52, INK, WHITE), cx, 380, t, 0.0)
    # barras verticais
    base = 1120
    for k, (code, v, x, col) in enumerate([("PAL", 250, 320, GREEN), ("EST", 62.6, 760, RED)]):
        t0 = 0.4 + k * 1.6
        if t < t0: continue
        u = ease((t - t0) / 1.0); hgt = 480 * (v / 250) * u
        d = ImageDraw.Draw(img); d.rounded_rectangle((x - 120, base - hgt, x + 120, base), 24, fill=col + (255,), outline=INK, width=6)
        pop(img, logo(code, 150), x, base + 110, t, t0)
        paste(img, money(v, t, t0, 1.0, 80, WHITE), x, base - hgt - 70, 1)
    if t > 4.4: pop(img, chip("+ DE US$ 187 MI DE DIFERENÇA", 50, INK, AMB), cx, 1400, t, 4.4, 0.25, -2)

def s2(img, t, T):
    pop(img, chip("OS 9 MAIS VALIOSOS DA FINAL", 54, INK, WHITE), cx, 380, t, 0.0)
    for k in range(9):
        r, c = k // 3, k % 3
        pop(img, logo("PAL", 170), 250 + c * 290, 620 + r * 240, t, 0.3 + k * 0.17)
    pop(img, stamp("TODOS DO PALMEIRAS", 78, GREEN), cx, 1380, t, 2.2, 0.25, -5 + shake(t, 2.2, 8))

def s3(img, t, T):
    pitch3d(img, T, 0, 6, dist=45, hgt=18, tgt=(0, -20, 0), dim=70)
    pop(img, jersey("★", "VITOR ROQUE", 360), 290, 620, t, 0.0)
    pop(img, chip("US$ 43,7 MI", 58, INK, AMB), 270, 880, t, 0.6, 0.25, -3)
    pop(img, EST(260), 780, 620, t, 1.2)
    pop(img, chip("ELENCO TODO: 62,6", 44, WHITE, RED), 800, 960, t, 1.6, 0.25, 3)
    if t > 2.4:
        pop(img, chip("70% DO TIME INTEIRO", 64, INK, WHITE), cx, 1120, t, 2.4)
        paste(img, bar(760, 50, 0.7 * ease((t - 2.4) / 0.8), AMB), cx, 1240, 1)

def s4(img, t, T):
    img.alpha_composite(speedlines(W, H, T))
    pop(img, logo("FLA", 260), 300, 620, t, 0.0)
    pop(img, chip("+ DE US$ 240 MI", 56, WHITE, RED), 300, 860, t, 0.5, 0.25, -3)
    pop(img, txt("X", 120, AMB), cx, 620, t, 0.8)
    pop(img, EST(260), 780, 620, t, 1.0)
    pop(img, stamp("ELIMINADO", 100, RED), cx, 1060, t, 2.0, 0.25, -8 + shake(t, 2.0, 10))
    pop(img, chip("DENTRO DO MARACANÃ", 56, INK, AMB), cx, 1260, t, 2.6, 0.25, 2)

def s5(img, t, T):
    pop(img, txt("FAVORITISMO...", 110, WHITE), cx, 440, t, 0.0)
    slide(img, logo("PAL", 220), 300, 760, t, 0.3, -400); slide(img, EST(220), 780, 760, t, 0.45, 400)
    pop(img, txt("X", 90, AMB), cx, 760, t, 0.6)
    pop(img, chip("AJUDA", 76, INK, GREEN), 280, 1060, t, 1.2, 0.25, -3)
    pop(img, chip("ATRAPALHA", 64, WHITE, RED), 770, 1060, t, 1.5, 0.25, 3)

S = Short("/home/claude/ter24/val", VAL, [s0, s1, s2, s3, s4, s5], "FINAL DA LIBERTADORES",
          ["night", "dark", "green", "dark", "red", "night"], "Hitman", 50.95)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("tambor_impacto", 2.6, 0.3), ("camera_click", S.segs[1][0] + 2.0, 0.3),
                   ("tambor_impacto", S.segs[2][0] + 2.2, 0.35), ("whoosh_boom", S.segs[4][0] + 2.0, 0.3), ("torcida_aww", S.segs[4][0] + 2.2, 0.15)])
