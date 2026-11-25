from extra import *
from scripts import MUR
EST = lambda h: logo("EST", h)
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def wall(w, h, u=1.0, crack=0.0):
    w, h = int(w), int(h); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bw, bh = 150, 70; rows = h // bh
    for r in range(rows):
        if r > rows * u: break
        off = 0 if r % 2 else -bw // 2
        for c in range(-1, w // bw + 2):
            x = c * bw + off; y = h - (r + 1) * bh
            shade = 150 + (hash((r, c)) % 40)
            d.rectangle((x + 3, y + 3, x + bw - 3, y + bh - 3), fill=(shade, 60, 50), outline=(60, 25, 20), width=4)
    if crack > 0:
        pts = [(w / 2, h * 0.5)]; import random; rnd = random.Random(4)
        for a in range(6):
            ang = a * 60 + rnd.uniform(-20, 20); L = 0
            p = (w / 2, h * 0.5); q = []
            while L < 260 * crack:
                L += 50; ang += rnd.uniform(-25, 25)
                p = (p[0] + 50 * math.cos(math.radians(ang)), p[1] + 50 * math.sin(math.radians(ang))); q.append(p)
            if q: d.line([(w / 2, h * 0.5)] + q, fill=INK, width=8)
    return im
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 820, T, (255, 150, 150), 14, 40))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("+300 MINUTOS", 122, AMB, 14), cx, 400, 1, sc, -3)
    paste(img, txt("SEM TOMAR GOL", 110, WHITE, 12), cx, 550, 1, sc, -3)
    paste(img, wall(1000, 420, ease(t / 0.6) * 1.0 + 0.01), cx, 900, 1)
    paste(img, EST(300), cx, 900, 1, 0.85 + 0.15 * back(t / 0.3) + 0.03 * math.sin(T * 6))
    pop(img, stamp("MURALHA", 110, RED), cx, 1200, t, 1.2, 0.25, -6 + shake(t, 1.2, 8))
def s1(img, t, T):
    pitch3d(img, T, 0, 7, dist=40, hgt=16, tgt=(40, 0, 0), dim=60)
    rows = [("QUARTAS • NA CASA DO CORINTHIANS", "COR", EST(140), 0, 1, "um"), ("SEMI • LA PLATA", EST(140), "FLA", 0, 0, "zero"), ("SEMI • MARACANÃ", "FLA", EST(140), 0, 0, "maracanã")]
    tt = [wt(1, "um") - 0.2, wt(1, "flamengo") - 0.4, wt(1, "maracanã") - 0.6]
    for k, (lab, a, b, ga, gb, _) in enumerate(rows):
        y = 470 + k * 330
        pop(img, chip(lab, 40, INK, WHITE if k < 2 else AMB), cx, y - 120, t, tt[k])
        pop(img, scorebox(a, b, ga, gb, 120), cx, y + 30, t, tt[k] + 0.1)
def s2(img, t, T):
    pop(img, chip("LIBERTADORES 2026", 56, INK, WHITE), cx, 400, t, 0.0)
    pop(img, txt("12 JOGOS", 150, AMB), cx, 560, t, 0.1)
    for k in range(12):
        x = 180 + (k % 6) * 144; y = 780 + (k // 6) * 160
        pop(img, check(120, True), x, y, t, 0.4 + k * 0.12)
    pop(img, chip("NUNCA LEVOU 2 GOLS", 70, WHITE, RED), cx, 1170, t, wt(2, "nunca") - 0.2, 0.25, -3)
def s3(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, (200, 220, 255), 14, 40))
    pop(img, jersey("1", "MUSLERA", 380, (70, 70, 80)), cx, 620, t, 0.0)
    pop(img, chip("40 ANOS", 76, INK, AMB), cx, 900, t, wt(3, "quarenta") - 0.2, 0.25, -3)
    tp = wt(3, "três") - 0.2
    for k in range(3): pop(img, check(150, False), 290 + k * 250, 1100, t, tp + k * 0.2)
    pop(img, chip("3 PÊNALTIS DEFENDIDOS NO MARACANÃ", 44, WHITE, INK), cx, 1260, t, tp + 0.7)
def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, (160, 255, 190), 14, 45))
    pop(img, logo("PAL", 160), cx, 380, t, 0.0)
    pop(img, jersey("", "FLACO LÓPEZ", 380, (20, 120, 60)), cx, 650, t, 0.1)
    if t > wt(4, "vinte") - 0.3:
        u = t - wt(4, "vinte") + 0.3
        paste(img, odometer(26, 2, 130, round(min(u, 1.0), 2), 0.8), 330, 1000, 1, back(u / 0.3)); pop(img, chip("GOLS", 56, INK, AMB), 330, 1150, u, 0.3)
    if t > wt(4, "catorze") - 0.3:
        u = t - wt(4, "catorze") + 0.3
        paste(img, odometer(14, 2, 130, round(min(u, 1.0), 2), 0.8), 750, 1000, 1, back(u / 0.3)); pop(img, chip("ASSIST.", 56, INK, WHITE), 750, 1150, u, 0.3)
    pop(img, chip("NA TEMPORADA", 54, INK, WHITE), cx, 1290, t, wt(4, "temporada") - 0.2)
def s5(img, t, T):
    tf = wt(5, "fura") - 0.1
    paste(img, wall(1000, 420, 1.0, clamp((t - tf) / 0.5) if t > tf else 0), cx, 700, 1, 1, shake(t, tf, 3))
    pop(img, EST(170), cx, 700, t, 0.0)
    pop(img, txt("O PALMEIRAS", 100, WHITE), cx, 380, t, 0.0); pop(img, txt("FURA A MURALHA?", 90, AMB), cx, 500, t, tf)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1060, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1060, t, wt(5, "não") - 0.2, 0.25, 4)
    pop(img, chip("COMENTA AÍ • SÁBADO 17H", 54, INK, WHITE), cx, 1260, t, wt(5, "comenta") - 0.1)
S = Short("/home/claude/qui26/mur", MUR, [s0, s1, s2, s3, s4, s5], "FINAL DA LIBERTADORES", ["red", "dark", "night", "dark", "green", "night"], "Interloper", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", 1.2, 0.3), ("apito_curto", S.segs[1][0] + 0.1, 0.15), ("tambor_impacto", S.segs[2][0] + wt(2, "nunca"), 0.3),
                   ("torcida_aww", S.segs[3][0] + wt(3, "três"), 0.15), ("torcida_comemora", S.segs[4][0] + wt(4, "vinte"), 0.15), ("whoosh_boom", S.segs[5][0] + wt(5, "fura"), 0.35)])
