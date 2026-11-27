from extra import *
from scripts import PAL
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
EST = lambda h: logo("EST", h)
ESTC = (200, 20, 30); PALC = (20, 120, 60)
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def emo(img, name, x, y, t, t0, sz=180):
    if t < t0: return
    paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))
def pbar(img, lg, pct, col, x, y, t, t0, hmax=560):
    if t < t0: return
    u = ease((t - t0) / 0.9); h = hmax * pct / 100 * u; w = 230; d = ImageDraw.Draw(img)
    d.rounded_rectangle((x - w / 2, y - h, x + w / 2, y), 18, fill=col, outline=INK, width=6)
    paste(img, txt(f"{int(round(pct * u))}%", 96, WHITE, 10), x, y - h - 70, 1)
    paste(img, lg, x, y + 110, 1)
def calendar(w, day, mon, col=RED):
    w = int(w); h = int(w * 1.05); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 26, fill=WHITE, outline=INK, width=7)
    d.rounded_rectangle((0, 0, w, h * 0.28), 26, fill=col, outline=INK, width=7); d.rectangle((7, h * 0.18, w - 7, h * 0.28), fill=col)
    d.text((w / 2, h * 0.14), mon, font=font("blk", int(h * 0.15)), fill=WHITE, anchor="mm")
    d.text((w / 2, h * 0.63), day, font=font("blk", int(h * 0.48)), fill=INK, anchor="mm")
    return im
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 850, T, (150, 255, 170), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, chip("FIZ AS CONTAS", 62, INK, AMB), cx, 430, 1, sc, -3)
    paste(img, logo("PAL", 270), cx - 170 + shake(t, 0.05, 12), 760, 1, sc, -4)
    paste(img, trophy(300), cx + 190, 760, 1, sc, 5)
    paste(img, txt("CAMPEÃO HOJE", 108, WHITE, 14), cx, 1060, 1, sc, -2)
    pop(img, stamp("MAS VAI SOFRER!", 96, RED), cx + shake(t, wt(0, "sofrer"), 12), 1260, t, wt(0, "mas") - 0.15, 0.25, -5)
def s1(img, t, T):
    pop(img, chip("MERCADO DE PREVISÕES", 60, INK, WHITE), cx, 420, t, 0.0)
    emo(img, "olhos", 900, 560, t, 0.1, 160)
    pbar(img, logo("PAL", 150), 71, (30, 160, 80), 330, 1180, t, wt(1, "setenta") - 0.3)
    pbar(img, EST(150), 21, ESTC, 750, 1180, t, wt(1, "vinte") - 0.3)
def s2(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 150, 150), 14, 35))
    tm = wt(2, "muslera") - 0.25
    if t < tm:
        pop(img, chip("ELIMINOU O FLAMENGO", 60, WHITE, RED), cx, 420, t, 0.0)
        pop(img, scorebox(EST(110), logo("FLA", 110), 0, 0, 115), cx, 650, t, wt(2, "dois") - 0.2, 0.25, -2)
        pop(img, scorebox(logo("FLA", 110), EST(110), 0, 0, 115), cx, 900, t, wt(2, "zero") , 0.25, 2)
        emo(img, "congelado", 900, 1120, t, wt(2, "zero") + 0.2, 170)
    else:
        pop(img, jersey(1, "MUSLERA", 380, ESTC), cx, 640, t, tm, 0.25, -3)
        for k in range(3):
            t0 = wt(2, "três") - 0.1 + 0.2 * k
            pop(img, check(130, False), cx - 220 + 220 * k, 950, t, t0, 0.25)
        pop(img, chip("3 PÊNALTIS DEFENDIDOS NO MARACANÃ", 46, INK, AMB), cx, 1130, t, wt(2, "pênaltis") - 0.1, 0.25, -2)
def s3(img, t, T):
    pop(img, EST(170), cx, 420, t, 0.0)
    pop(img, calendar(300, "12", "NOV"), 290, 790, t, wt(3, "dia") - 0.3, 0.25, -5)
    if t > wt(3, "dia"):
        d = ImageDraw.Draw(img); d.line((470, 790, 590, 790), fill=WHITE, width=14); d.polygon([(590, 760), (640, 790), (590, 820)], fill=WHITE)
    pop(img, calendar(300, "28", "NOV", GREEN), 800, 790, t, wt(3, "dia") + 0.2, 0.25, 5)
    td = wt(3, "dezesseis") - 0.3
    if t > td: pop(img, odometer(16, 2, 150, t - td, 0.6), cx - 160, 1130, t, td)
    pop(img, txt("DIAS", 110, AMB), cx + 150, 1130, t, td + 0.2)
    pop(img, chip("DESCANSADO", 60, INK, WHITE), cx, 1300, t, wt(3, "descansado") - 0.2, 0.25, -3)
    emo(img, "sono", 900, 450, t, wt(3, "descansado"), 160)
def s4(img, t, T):
    pop(img, logo("PAL", 200), cx, 420, t, 0.0)
    tp = wt(4, "catorze") - 0.3
    if t > tp: pop(img, odometer(14, 2, 150, t - tp, 0.6), cx - 300, 700, t, tp)
    pop(img, txt("POUPADOS", 100, GREEN), cx + 110, 700, t, tp + 0.2)
    for k in range(14):
        x = 150 + (k % 7) * 130; y = 900 + (k // 7) * 150
        pop(img, jersey("", "", 110, PALC), x, y, t, tp + 0.05 * k, 0.2, (k % 3 - 1) * 4)
    pop(img, chip("CONTRA A CHAPECOENSE", 46, WHITE, INK), cx, 1240, t, wt(4, "chapecoense") - 0.2)
    pop(img, stamp("INTEIRO PRA FINAL", 84, GREEN), cx, 1380, t, wt(4, "inteiro") - 0.2, 0.25, -5)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 230, 120), 14, 45))
    pop(img, chip("MEU PALPITE", 64, INK, AMB), cx, 400, t, 0.0)
    pop(img, scorebox("PAL", EST(140), 1, 0, 140), cx + shake(t, wt(5, "um"), 10), 640, t, wt(5, "um") - 0.25)
    pop(img, chip("GOL DO FLACO LÓPEZ", 60, WHITE, GREEN), cx, 860, t, wt(5, "flaco") - 0.25, 0.25, -3)
    emo(img, "bola", 900, 950, t, wt(5, "flaco"), 150)
    pop(img, txt("E O SEU?", 130, WHITE), cx, 1080, t, wt(5, "seu") - 0.3)
    pop(img, txt("COMENTA O PLACAR!", 92, AMB), cx, 1240, t, wt(5, "comenta") - 0.2)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 125, 0.85)
S = Short("/home/claude/sab28b/pal", PAL, [s0, s1, s2, s3, s4, s5], "FINAL • PALPITE", ["green", "dark", "red", "night", "green", "blue"], "Ouroboros", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "sofrer"), 0.3), ("camera_click", S.segs[1][0] + wt(1, "setenta"), 0.2),
                   ("torcida_aww", S.segs[2][0] + wt(2, "três"), 0.14), ("apito_curto", S.segs[3][0] + wt(3, "dia"), 0.15),
                   ("tambor_impacto", S.segs[5][0] + wt(5, "um"), 0.35), ("torcida_grita_gol", S.segs[5][0] + wt(5, "flaco"), 0.15)])
