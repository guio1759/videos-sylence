from extra import *
from scripts import SPFC
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
D = "/home/claude/sab28e/"
FOTO = Image.open(D + "foto.png").convert("RGBA"); DMI = Image.open(D + "dm.jpg").convert("RGBA")
HANDLE = "@p3dr0._.p3dro"
def wt(i, w, d=0.5, nth=0):
    k = 0
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)):
            if k == nth: return c["t0"] - S.segs[i][0]
            k += 1
    return d
def emo(img, name, x, y, t, t0, sz=170):
    if t >= t0: paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))
def avatar(sz, t=0):
    sz = int(sz); r = 26; im = Image.new("RGBA", (sz + 2 * r, sz + 2 * r), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, c in enumerate(((220, 30, 40), WHITE, (15, 15, 15))):
        a0 = (t * 90 + k * 120) % 360; d.arc((4, 4, sz + 2 * r - 4, sz + 2 * r - 4), a0, a0 + 120, fill=c, width=r - 4)
    im.alpha_composite(FOTO.resize((sz, sz), Image.LANCZOS), (r, r)); return im
def dmshot(w=1000):
    return DMI.resize((w, int(DMI.height * w / DMI.width)), Image.LANCZOS)
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
    img.alpha_composite(rays(W, H, cx, 820, T, (255, 120, 120), 14, 45))
    slide(img, dmshot(), cx, 360, t, 0.0, -900, 0.35)
    pop(img, avatar(430, t), cx, 800, t, 0.35, 0.3, -3)
    pop(img, chip(HANDLE, 60, WHITE, (180, 20, 30)), cx, 1100, t, 0.55, 0.25, 2)
    tl = wt(0, "lei", 1.6) - 0.15
    pop(img, stamp("PEDIDO ATENDIDO!", 96, GREEN), cx + shake(t, tl + 0.05, 12), 1280, t, tl, 0.25, -6)
    ts = wt(0, "paulo", 2.6) - 0.3
    pop(img, logo("SAO", 190), 900, 620, t, ts, 0.3, 8)
    emo(img, "festa", 180, 620, t, tl + 0.2)
def s1(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 120), 14, 45))
    pop(img, logo("SAO", 200), cx, 360, t, 0.0)
    pop(img, chip("TRI DA LIBERTADORES", 58, INK, AMB), cx, 560, t, 0.15, 0.25, -2)
    for k, y in enumerate(("1992", "1993", "2005")):
        x = cx - 300 + 300 * k; t0 = 0.3 + 0.12 * k
        pop(img, trophy(200), x, 740, t, t0); pop(img, txt(y, 50, WHITE, 6), x, 880, t, t0 + 0.1)
    tm = wt(1, "tricampe", 1.8, 1) - 0.25
    pop(img, chip("TRI DO MUNDO", 58, INK, WHITE), cx, 1030, t, tm, 0.25, 2)
    for k, y in enumerate(("1992", "1993", "2005")):
        x = cx - 300 + 300 * k; t0 = tm + 0.12 + 0.12 * k
        pop(img, goldball(170, t), x, 1190, t, t0); pop(img, txt(y, 50, WHITE, 6), x, 1320, t, t0 + 0.1)
def s2(img, t, T):
    tf = wt(2, "faltando", 1.6) - 0.2
    if t < tf:
        pop(img, txt("2026", 260, WHITE, 14), cx, 700, t, 0.0, 0.3, -3)
        pop(img, stamp("A BRIGA É OUTRA", 90, RED), cx, 950, t, wt(2, "briga", 0.9) - 0.2, 0.25, -5)
    else:
        pop(img, chip("FALTA 1 RODADA", 60, INK, AMB), cx, 380, t, tf, 0.25, -2)
        paste(img, table(t - tf - 0.15), cx, 880, 1, 0.9 + 0.1 * back(min(1, (t - tf) / 0.3)))
def s3(img, t, T):
    img.alpha_composite(Image.new("RGBA", (W, H), (60, 0, 0, 80)))
    pop(img, txt("LIBERTADORES", 120, WHITE), cx, 460, t, 0.0)
    pop(img, trophy(380, (170, 170, 175)), cx, 820, t, 0.2)
    pop(img, check(220, False), cx + 170, 950, t, wt(3, "era", 0.8) - 0.1)
    pop(img, stamp("MATEMATICAMENTE FORA", 62, RED), cx, 1230, t, wt(3, "matematicamente", 1.3) - 0.2, 0.25, -5)
    emo(img, "chorando", 200, 640, t, wt(3, "mais", 2.0), 160) if hasattr(emoji, "get") else None
def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (150, 255, 170), 14, 35))
    pop(img, txt("SUL-AMERICANA", 110, GREEN), cx, 400, t, 0.0); pop(img, chip("TÁ VIVA!", 60, INK, AMB), cx, 540, t, 0.3, 0.25, -3)
    tr = wt(4, "remo", 1.6) - 0.3
    pop(img, scorebox("SAO", "REM", 3, 1, 110), cx + shake(t, tr + 0.3, 10), 760, t, tr)
    ta = wt(4, "athl", 3.0) - 0.3
    pop(img, chip("ÚLTIMA RODADA", 46, WHITE, INK), cx, 1000, t, ta)
    pop(img, scorebox("CAP", "SAO", "", "", 110), cx, 1170, t, ta + 0.1)
    pop(img, chip("QUA 02/12 • 21H30 • FORA", 46, INK, AMB), cx, 1360, t, wt(4, "quarta", 4.0) - 0.2)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (255, 220, 120), 14, 45))
    pop(img, chip("SE VENCER O ATHLETICO", 56, INK, WHITE), cx, 420, t, 0.0)
    tn = wt(5, "99", 1.4) - 0.3
    if t > tn: pop(img, odometer(99, 2, 260, t - tn, 0.9), cx - 120, 780, t, tn)
    pop(img, txt("%", 220, GREEN), cx + 200, 780, t, tn + 0.2)
    pop(img, chip("DE CHANCE DE VAGA", 60, WHITE, GREEN), cx, 1050, t, wt(5, "chance", 2.2) - 0.2)
    pop(img, chip("simulação: valorfinal.com.br", 30, WHITE, INK), cx, 1170, t, 1.0)
    emo(img, "fogo", 880, 560, t, tn + 0.5, 150)
def s6(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, (255, 120, 120), 14, 40))
    pop(img, avatar(250, t), cx, 370, t, 0.0, 0.3, -4)
    pop(img, chip(HANDLE, 46, WHITE, (180, 20, 30)), cx, 590, t, 0.1, 0.25, -2)
    emo(img, "olhos", 860, 330, t, 0.3, 130)
    pop(img, txt("VAI DAR?", 130, WHITE), cx, 760, t, wt(6, "vai", 0.8) - 0.2, 0.25, 3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 320, 950, t, wt(6, "sim", 2.0, 0) - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 760, 950, t, wt(6, "não", 2.3) - 0.2, 0.25, 4)
    tp = wt(6, "pede", 3.0) - 0.2
    pop(img, stamp("PEDE O SEU TIME!", 90, AMB), cx, 1150, t, tp, 0.25, -4)
    pop(img, chip("O PRÓXIMO PODE SER VOCÊ", 52, INK, WHITE), cx, 1320, t, wt(6, "próximo", 4.0) - 0.2, 0.25, 2)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 170, 0.85)
S = Short(D + "spfc", SPFC, [s0, s1, s2, s3, s4, s5, s6], "VOCÊ PEDIU • SÃO PAULO", ["red", "dark", "night", "night", "green", "dark", "red"], "Movement_Proposition", 0)
if __name__ == "__main__":
    main(S, extra=[("whoosh_boom", 0.0, 0.35), ("tambor_impacto", wt(0, "lei", 1.6), 0.4), ("torcida_comemora", wt(0, "paulo", 2.6), 0.22),
                   ("tambor_impacto", S.segs[1][0] + 0.3, 0.3), ("torcida_aww", S.segs[3][0] + 0.5, 0.2),
                   ("torcida_grita_gol", S.segs[4][0] + wt(4, "remo", 1.6), 0.15), ("tambor_impacto", S.segs[5][0] + wt(5, "99", 1.4), 0.3)])
