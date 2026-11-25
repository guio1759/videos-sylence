from extra import *
from scripts import CHA
EST = lambda h: logo("EST", h)
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def plane(w):
    w = int(w); im = Image.new("RGBA", (w, w), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = w / 100
    d.polygon([(95*s,50*s),(10*s,42*s),(4*s,50*s),(10*s,58*s)], fill=WHITE, outline=INK)
    d.polygon([(55*s,46*s),(35*s,10*s),(26*s,10*s),(38*s,46*s)], fill=WHITE, outline=INK)
    d.polygon([(55*s,54*s),(35*s,90*s),(26*s,90*s),(38*s,54*s)], fill=WHITE, outline=INK)
    d.polygon([(16*s,46*s),(8*s,28*s),(3*s,28*s),(8*s,47*s)], fill=WHITE, outline=INK)
    return im
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 820, T, (255, 150, 150), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("TOMOU 3", 170, WHITE, 14), cx, 400, 1, sc, -3)
    paste(img, txt("DA CHAPE", 140, AMB, 12), cx, 560, 1, sc, -3)
    paste(img, scorebox("CHA", "PAL", 3, 0, 150), cx + shake(t, 0.15, 14), 820, 1, 0.85 + 0.15 * back(t / 0.25))
    pop(img, stamp("TÁ TUDO CERTO", 96, GREEN), cx, 1100, t, wt(0, "tudo") - 0.15, 0.25, -6 + shake(t, wt(0, "tudo"), 8))
def s1(img, t, T):
    pitch3d(img, T, 0, 7, dist=44, hgt=18, tgt=(0, 0, 0), dim=60)
    pop(img, chip("ARENA CONDÁ • 24/11", 58, INK, WHITE), cx, 400, t, 0.0)
    for k, x in enumerate((260, 540, 820)):
        pop(img, jersey(str((k * 7 + 13) % 40), "RESERVA", 250, (20, 120, 60)), x, 700, t, wt(1, "reservas") - 0.3 + k * 0.12, 0.25, (-4, 0, 4)[k])
    pop(img, chip("SÓ RESERVAS", 76, INK, AMB), cx, 960, t, wt(1, "reservas") - 0.1, 0.25, -3)
    pop(img, chip("+ GAROTOS DA BASE", 66, WHITE, GREEN), cx, 1100, t, wt(1, "garotos") - 0.2, 0.25, 3)
def s2(img, t, T):
    img.alpha_composite(rays(W, H, cx, 820, T, (255, 220, 140), 14, 50))
    pop(img, chip("TITULARES", 80, INK, WHITE), cx, 400, t, 0.0)
    pop(img, stamp("POUPADOS", 120, AMB), cx, 560, t, wt(2, "poupados") - 0.15, 0.25, -6)
    tf = wt(2, "final") - 0.3
    if t > tf:
        u = t - tf; pop(img, trophy(380), cx, 880, u, 0.0)
        pop(img, txt("FINAL DA", 90, WHITE), cx, 1130, u, 0.2); pop(img, txt("LIBERTADORES", 110, AMB), cx, 1240, u, 0.35)
def s3(img, t, T):
    pop(img, chip("BRASILEIRÃO • APÓS 37 RODADAS", 50, INK, WHITE), cx, 400, t, 0.0)
    pop(img, logo("PAL", 300), cx, 680, t, 0.2)
    pop(img, txt("2º LUGAR", 130, AMB), cx, 940, t, wt(3, "segundo") - 0.2)
    if t > wt(3, "setenta") - 0.3:
        u = t - wt(3, "setenta") + 0.3
        paste(img, odometer(74, 2, 150, round(min(u, 1.0), 2), 0.8), cx, 1140, 1, back(u / 0.3))
        pop(img, chip("PONTOS", 60, INK, WHITE), cx, 1310, u, 0.3)
def s4(img, t, T):
    d = ImageDraw.Draw(img); ax, ay, bx, by = 230, 560, 850, 900
    pop(img, chip("SÃO PAULO", 50, INK, WHITE), ax, ay - 90, t, 0.0); pop(img, chip("MONTEVIDÉU", 50, INK, AMB), bx, by + 90, t, 0.3)
    u = ease(t / 1.4)
    pts = [(ax + (bx - ax) * k / 40, ay + (by - ay) * k / 40 - 220 * math.sin(math.pi * k / 40)) for k in range(41)]
    for k in range(0, int(40 * u), 2): d.line([pts[k], pts[k + 1]], fill=WHITE, width=8)
    k = min(39, int(40 * u)); ang = math.degrees(math.atan2(pts[k + 1][1] - pts[k][1], pts[k + 1][0] - pts[k][0]))
    paste(img, plane(170), pts[k][0], pts[k][1], 1, 1, -ang)
    ts = wt(4, "sábado") - 0.3
    for j, s in enumerate(["SÁBADO • 28/11 • 17H", "CENTENÁRIO"]):
        pop(img, chip(s, 58, INK, AMB if j == 0 else WHITE), cx, 1100 + j * 120, t, ts + j * 0.5)
    te = wt(4, "estudiantes") - 0.3
    pop(img, logo("PAL", 170), 330, 1380, t, te); pop(img, txt("X", 90), cx, 1380, t, te + 0.1); pop(img, EST(170), 750, 1380, t, te + 0.2)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 140), 14, 40))
    pop(img, chip("PERDER PRA CHAPE", 70, WHITE, RED), cx, 420, t, 0.0, 0.25, -3)
    pop(img, txt("+", 100), cx, 540, t, 0.3)
    pop(img, chip("GANHAR A LIBERTADORES", 64, INK, AMB), cx, 660, t, wt(5, "ganhar") - 0.2, 0.25, 3)
    pop(img, txt("VOCÊ ACEITA?", 120, WHITE), cx, 860, t, wt(5, "aceita") - 0.3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1100, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1100, t, wt(5, "não") - 0.2, 0.25, 4)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1290, t, wt(5, "comenta") - 0.1)
S = Short("/home/claude/qui26/cha", CHA, [s0, s1, s2, s3, s4, s5], "PALMEIRAS • FINAL", ["red", "dark", "night", "green", "blue", "dark"], "Galactic_Rap", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("torcida_aww", 0.2, 0.15), ("whoosh_boom", wt(0, "tudo"), 0.3), ("tambor_impacto", S.segs[2][0] + wt(2, "poupados"), 0.3),
                   ("torcida_comemora", S.segs[2][0] + wt(2, "final"), 0.15), ("whoosh_3", S.segs[4][0] + 0.1, 0.2), ("apito_curto", S.segs[4][0] + wt(4, "sábado"), 0.15)])
