from extra import *
from scripts import SPFC
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
SPR = (220, 30, 40)
def wt(i, w, d=0.5, nth=0):
    k = 0
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]) == norm(w):
            if k == nth: return c["t0"] - S.segs[i][0]
            k += 1
    return d
def emo(img, name, x, y, t, t0, sz=170):
    if t >= t0: paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))
def dm(w=900):
    h = 230; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 44, fill=(36, 38, 44, 250), outline=(90, 90, 100), width=3)
    d.ellipse((30, 60, 130, 160), fill=(120, 120, 130)); d.ellipse((62, 78, 98, 114), fill=(200, 200, 205)); d.pieslice((48, 112, 112, 176), 180, 360, fill=(200, 200, 205))
    d.text((160, 45), "MENSAGEM DE UM SEGUIDOR", font=font("bd", 30), fill=(170, 170, 180))
    d.text((160, 95), "faz um video sobre o", font=font("blk", 54), fill=WHITE); d.text((160, 158), "são paulo? por favor", font=font("blk", 54), fill=WHITE)
    return im
ROWS = [(8, "BRAGANTINO", "RBB", 50), (9, "SANTOS", "SAN", 50), (10, "SÃO PAULO", "SAO", 48), (11, "VASCO", "VAS", 47), (12, "CORITIBA", "CFC", 45)]
def table(t, w=940):
    rh = 120; h = 110 + rh * len(ROWS); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 30, fill=(14, 16, 22, 240), outline=WHITE, width=4)
    d.text((40, 55), "BRASILEIRÃO • 37 DE 38 RODADAS", font=font("blk", 38), fill=AMB, anchor="lm"); d.text((w - 40, 55), "PTS", font=font("blk", 38), fill=WHITE, anchor="rm")
    for k, (p, nm, lg, pts) in enumerate(ROWS):
        if t < 0.08 * k: continue
        y = 110 + rh * k
        if lg == "SAO": d.rounded_rectangle((12, y + 6, w - 12, y + rh - 6), 18, fill=(180, 20, 30, 235))
        d.text((70, y + rh / 2), f"{p}º", font=font("blk", 50), fill=WHITE, anchor="mm")
        im.alpha_composite(logo(lg, 84), (130, int(y + rh / 2 - 42)))
        d.text((250, y + rh / 2), nm, font=font("blk", 50), fill=WHITE, anchor="lm"); d.text((w - 40, y + rh / 2), str(pts), font=font("blk", 56), fill=WHITE, anchor="rm")
    return im
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (255, 120, 120), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, dm(), cx, 430, 1, sc)
    paste(img, logo("SAO", 330), cx, 870, 1, sc)
    pop(img, stamp("PEDIDO ATENDIDO!", 100, GREEN), cx, 1240, t, wt(0, "atendeu", 1.0) - 0.15, 0.25, -6)
    emo(img, "festa", 880, 700, t, 0.5)
def s1(img, t, T):
    pop(img, chip("FALTA 1 RODADA", 60, INK, AMB), cx, 380, t, 0.0, 0.25, -2)
    paste(img, table(t - 0.2), cx, 880, 1, 0.9 + 0.1 * back(min(1, t / 0.3)))
def s2(img, t, T):
    img.alpha_composite(Image.new("RGBA", (W, H), (60, 0, 0, 80)))
    pop(img, txt("LIBERTADORES", 120, WHITE), cx, 460, t, 0.0)
    pop(img, trophy(380, (170, 170, 175)), cx, 820, t, 0.2)
    pop(img, check(220, False), cx + 170, 950, t, wt(2, "era", 0.8) - 0.1)
    pop(img, stamp("MATEMATICAMENTE FORA", 62, RED), cx, 1230, t, wt(2, "matematicamente", 1.3) - 0.2, 0.25, -5)
def s3(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (150, 255, 170), 14, 35))
    pop(img, txt("SUL-AMERICANA", 110, GREEN), cx, 400, t, 0.0); pop(img, chip("TÁ VIVA!", 60, INK, AMB), cx, 540, t, 0.3, 0.25, -3)
    pop(img, scorebox("SAO", "REM", 3, 1, 110), cx, 760, t, wt(3, "remo", 1.6) - 0.3)
    pop(img, chip("ÚLTIMA RODADA", 46, WHITE, INK), cx, 1000, t, wt(3, "athletico", 3.0) - 0.3)
    pop(img, scorebox("CAP", "SAO", "", "", 110), cx, 1170, t, wt(3, "athletico", 3.0) - 0.2)
    pop(img, chip("QUA 02/12 • 21H30 • FORA", 46, INK, AMB), cx, 1360, t, wt(3, "quarta", 4.0) - 0.2)
def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (255, 220, 120), 14, 45))
    pop(img, chip("SE VENCER O ATHLETICO", 56, INK, WHITE), cx, 420, t, 0.0)
    tn = wt(4, "noventa", 1.4) - 0.3
    if t > tn: pop(img, odometer(99, 2, 260, t - tn, 0.9), cx - 120, 780, t, tn)
    pop(img, txt("%", 220, GREEN), cx + 200, 780, t, tn + 0.2)
    pop(img, chip("DE CHANCE DE VAGA", 60, WHITE, GREEN), cx, 1050, t, wt(4, "chance", 2.2) - 0.2)
    pop(img, chip("simulação: valorfinal.com.br", 30, WHITE, INK), cx, 1170, t, 1.0)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (255, 120, 120), 14, 40))
    pop(img, logo("SAO", 200), cx, 380, t, 0.0)
    pop(img, txt("VAI DAR?", 140, WHITE), cx, 600, t, 0.2)
    pop(img, chip("SIM", 110, WHITE, GREEN), 320, 830, t, wt(5, "sim", 2.0) - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 760, 830, t, wt(5, "não", 2.3) - 0.2, 0.25, 4)
    pop(img, stamp("PEDE O SEU TIME!", 90, AMB), cx, 1120, t, wt(5, "pede", 3.0) - 0.2, 0.25, -4)
    emo(img, "olhos", 880, 1320, t, wt(5, "pede", 3.0))
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 125, 0.85)
S = Short("/home/claude/sab28d/spfc", SPFC, [s0, s1, s2, s3, s4, s5], "VOCÊ PEDIU • SÃO PAULO", ["red", "dark", "night", "green", "dark", "red"], "Movement_Proposition", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("torcida_comemora", wt(0, "atendeu", 1.0), 0.25), ("torcida_aww", S.segs[2][0] + 0.5, 0.2),
                   ("tambor_impacto", S.segs[4][0] + wt(4, "noventa", 1.4), 0.3)])
