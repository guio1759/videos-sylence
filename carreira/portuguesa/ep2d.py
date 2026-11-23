"""Lusa Ep.2 v2 — no modelo do Cambridge (telas de jogo, HUD, lances 3D com nomes)."""
import sys, functools, re; sys.path.insert(0, "/home/claude/por"); sys.path.insert(0, "/home/claude/sex20"); sys.path.insert(0, "/home/claude/carreira")
from com import *
import card as C
import lances2 as L
from face import face
sys.path.insert(0, "/home/claude/por/ep2b"); from script import S as RAW
TXT = [re.sub(r"\[[a-z ]+\] ?", "", s) for s in RAW]
D = "/home/claude/por/ep2b"; IM = "/home/claude/por/img/"
GOLD = (255, 205, 60); cy = H / 2

@functools.lru_cache(32)
def cut(k, h): im = Image.open(IM + k + "_cut.png").convert("RGBA"); h = int(h); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
@functools.lru_cache(64)
def pcard(key, name, ovr, pos, w=380, prom=False):
    return C.make_card(face(key), name, ovr, pos, list(STATS.get(key, (65, 55, 58, 60, 40, 50))), w=w, promessa=prom, crest="POR.png")
STATS = {"davi": (66, 52, 62, 64, 28, 42), "levi3d": (72, 60, 64, 70, 30, 50), "cauari3d": (78, 60, 58, 66, 30, 55), "benny": (62, 38, 50, 52, 48, 46), "romarinho3d": (62, 68, 66, 70, 30, 55)}
def gray(key, h):
    im = cut(key, h); g = im.convert("LA").convert("RGBA"); g.putalpha(im.getchannel("A")); return g

import inspect, gfx as _G
_src = inspect.getsource(_G.newspaper).replace('"CAMBRIDGE DAILY"', '"DIÁRIO DA LUSA"')
exec(_src, _G.__dict__); newspaper = _G.newspaper
def wt(i, word, n=1):
    i -= 1; s0 = SH.segs[i][0]; c = 0
    for w in SH.caps:
        if SH.segs[i][0] - 0.01 <= w["t0"] <= SH.segs[i][1] + 0.01 and norm(w["w"]).startswith(norm(word)):
            c += 1
            if c == n: return w["t0"] - s0
    return 0.0
def B(img, key, T): img.alpha_composite(bg(W, H, key, T))
def flashw(img, t, t0, dur=0.22):
    u = t - t0
    if 0 <= u < dur: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(200 * (1 - u / dur)))))
def poptext(img, s, x, y, t, t0, size=120, col=WHITE, rot=0):
    if t < t0: return
    paste(img, text_el(s, font("blk", size), col, 10), x, y, 1, 0.3 + 0.7 * back((t - t0) / 0.3), rot)
def comment(user, text, likes, w=960):
    h = 250; p = panel(w, h, (250, 250, 252, 255), 30, (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.ellipse((30, 40, 120, 130), fill=(160, 80, 190)); d.text((75, 85), user[1].upper(), font=font("blk", 54), fill=WHITE, anchor="mm")
    d.text((145, 50), user, font=font("bd", 40 if len(user) < 22 else 33), fill=(110, 110, 120), anchor="lm")
    d.text((145, 140), text, font=font("blk", 64), fill=INK, anchor="lm")
    d.text((w - 70, 95), "♥", font=font("blk", 70), fill=RED, anchor="mm"); d.text((w - 70, 175), likes, font=font("bd", 40), fill=(90, 90, 100), anchor="mm")
    return p
def result_row(r, s, w=930):
    col = {"V": GREEN, "E": (150, 150, 160), "D": RED}[r]
    p = panel(w, 100, (14, 14, 18, 240), 18); pd = ImageDraw.Draw(p)
    pd.rounded_rectangle((14, 14, 86, 86), 14, fill=col); pd.text((50, 50), r, font=font("blk", 48), fill=WHITE, anchor="mm")
    pd.text((112, 50), s, font=font("bd", 40), fill=WHITE, anchor="lm"); return p
def mailp(frm, subj, w=960):
    p = panel(w, 420, (250, 250, 252, 255), 22, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
    pd.text((40, 40), "Caixa de entrada • 1 nova", font=font("bd", 32), fill=(110, 110, 120))
    pd.text((40, 120), "De: " + frm, font=font("sb", 38), fill=(60, 60, 70)); pd.text((40, 190), "Assunto:", font=font("bd", 36), fill=(90, 90, 100))
    pd.text((40, 270), subj, font=font("blk", 70), fill=RED); return p
def lance(img, fn, t, bug=None, clock=None):
    im, labs = L.render(fn, t, W, H)
    for s, pr, a, b, col in labs:
        if pr and a < t < b:
            v = ease((t - a) / 0.25) * (1 - ease((t - b + 0.25) / 0.25))
            paste(im, chip(s, 34, INK, col), pr[0], pr[1] + 34, v)
    if bug:
        p = panel(860, 88, (12, 12, 16, 235), 40); ImageDraw.Draw(p).text((430, 44), bug, font=font("blk", 40), fill=WHITE, anchor="mm")
        paste(im, p, W / 2, 380)
    if clock: paste(im, chip(clock, 46, WHITE, RED), W / 2, 480, 1, 1 + 0.05 * math.sin(t * 8))
    img.alpha_composite(im)

TOP = {0: "ÚLTIMA RODADA", 1: "EP.2 • A VOTAÇÃO", 2: "O NOVO DA BASE", 3: "1ª RODADA", 4: "1ª RODADA", 5: "FEVEREIRO", 6: "MARÇO • ÚLTIMA RODADA",
       7: "MARÇO • ÚLTIMA RODADA", 8: "EVOLUÇÃO DO TRIMESTRE", 9: "O TIME", 10: "VOCÊ DECIDE"}
POSI = {0: 15, 1: None, 2: None, 3: None, 4: 8, 5: 15, 6: 15, 7: 12, 8: 12, 9: 12, 10: 12}
def hud(img, i):
    y, h = 60, 86; p = panel(W - 60, h, (12, 12, 16, 225), 24); img.alpha_composite(p, (30, y))
    paste(img, logo("POR", 66), 82, y + h / 2); d = ImageDraw.Draw(img)
    d.text((128, y + h / 2), "PORTUGUESA", font=font("blk", 32), fill=WHITE, anchor="lm")
    paste(img, chip("PAULISTÃO", 28, WHITE, (60, 60, 70)), 545, y + h / 2)
    ps = POSI.get(i); paste(img, chip(f"{ps}º" if ps else "PRÉ", 30, INK if ps and ps < 13 else WHITE, GOLD if ps and ps < 13 else (RED if ps else (90, 90, 100))), 700, y + h / 2)
    paste(img, chip("RUMO À LIBERTADORES", 24, INK, (200, 200, 205)), 900, y + h / 2)

def s0(img, t, T):
    tp = wt(0, "pênalti")
    lance(img, lambda u: L.penalty(u, False), t, "PORTUGUESA 1 x 1 SÃO PAULO", "93:00")
    pop(img, chip("SE PERDER, A LUSA CAI", 58, WHITE, RED), cx, 640, t, wt(0, "perder") - 0.2, 0.25, -3)
    if t > tp: flashw(img, t, tp); poptext(img, "PÊNALTI!", cx, cy + 60, t, tp, 170, GOLD, -4)

def s1(img, t, T):
    B(img, "purple", T); img.alpha_composite(speedlines(W, H, T))
    paste(img, text_el("VOCÊS DECIDIRAM!", font("blk", 92), GOLD, 10), cx, 420, 1, 1 + 0.05 * math.sin(min(t, 0.4) * 8), -3)
    tb = 0.15; tl = wt(1, "levi") - 0.2
    if t > tb: paste(img, comment("@beniciorufinodini2186", "Letra b", "1"), cx, 640, 1, 0.85 + 0.15 * back((t - tb) / 0.3))
    pop(img, chip("VOCÊS ESCOLHERAM: B", 60, WHITE, GREEN), cx, 830, t, tb + 0.3, 0.25, -2)
    if t > tl:
        u = (t - tl) / 0.45; paste(img, pcard("levi3d", "LEVI SANTOS", 60, "MEI", 400), cx, 1160, ease(u), 0.5 + 0.5 * back(u), (1 - ease(u)) * 25)
        pop(img, stamp("CONTRATADO", 90, GREEN), cx, 1460, t, wt(1, "joia"), 0.25, -6)

def s2(img, t, T):
    tth, tpe, tpa = wt(2, "thiago") - 0.2, wt(2, "peneira") - 0.4, wt(2, "passou") - 0.2
    if t < tth:
        B(img, "teal", T)
        pop(img, chip("COMENTÁRIO MAIS CURTIDO", 60, INK, GOLD), cx, 420, t, 0.0, 0.25, -2)
        if t > 0.4: paste(img, comment("@BennyDouekPikelaizen", "Bota eu no time", "3", 1000), cx, 660, 1, 0.85 + 0.15 * back((t - 0.4) / 0.3))
        pop(img, cut("benny", 560), cx, 1120, t, 1.0, 0.3)
        pop(img, chip("VIROU PERSONAGEM!", 60, WHITE, RED), cx, 1440, t, 1.6, 0.25, 3)
    elif t < tpe:
        u = t - tth; B(img, "amber", T); img.alpha_composite(rays(W, H, cx, 1000, T, WHITE, 14, 60))
        paste(img, cut("tee", 980), cx, 1220, 1, 0.85 + 0.15 * back(u / 0.35))
        poptext(img, "E O THIAGO", cx, 420, u, 0.0, 110, WHITE); poptext(img, "BOTOU!", cx, 570, u, 0.3, 160, INK, -4)
    else:
        u = t - tpe; B(img, "dark", T)
        p = panel(960, 640, (245, 242, 232, 255), 18, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((40, 40), "PENEIRA DA LUSA", font=font("blk", 60), fill=INK)
        rows = [("Lucas M.", False), ("Rian S.", False), ("Benny", True), ("Gabriel P.", False)]
        for k, (n, ok) in enumerate(rows):
            yy = 150 + k * 112; pd.text((40, yy + 40), n, font=font("blk" if ok else "bd", 54), fill=INK if ok else (120, 120, 120), anchor="lm")
            if ok: pd.text((560, yy + 40), "de chinelo", font=font("sb", 40), fill=(150, 90, 40), anchor="lm")
            if t > tpa or not ok:
                pd.rounded_rectangle((850, yy + 6, 918, yy + 74), 14, fill=GREEN if ok else RED)
                pd.text((884, yy + 40), "✓" if ok else "x", font=font("blk", 50), fill=WHITE, anchor="mm")
        paste(img, p, cx, 820, 1, back(u / 0.35), -2)
        if t > tpa:
            v = (t - tpa) / 0.45; paste(img, pcard("benny", "BENNY", 47, "VOL", 340, True), 780, 1430, ease(v), 0.5 + 0.5 * back(v), (1 - ease(v)) * 25)
            pop(img, stamp("APROVADO", 100, GREEN), 330, 1440, t, tpa + 0.2, 0.25, -8)

def s3(img, t, T):
    B(img, "night", T)
    paste(img, newspaper(W * 0.88, "JANEIRO 2027", "LUSA ESTREIA LONGE DE CASA", "Canindé em obras: jogo em Diadema"), cx, 820, 1, back(t / 0.4), (1 - ease(t / 0.4)) * 300)
    tc = wt(3, "corinthians") - 0.2
    if t > tc: paste(img, scorebox("COR", "POR", "", "", 120), cx, 1340, 1, 0.7 + 0.3 * back((t - tc) / 0.3))
    pop(img, chip("1ª RODADA • EM DIADEMA", 50, INK, GOLD), cx, 1520, t, tc + 0.3)

def s4(img, t, T):
    tg = wt(4, "gol"); tb = wt(4, "primeiro") - 0.3
    t0 = tg - L.TS - 0.35
    if t < tb:
        lt = max(0.0, t - t0) if t > t0 else 0.0
        lance(img, L.davi_goal, lt, "CORINTHIANS 1 x 0 PORTUGUESA" if t < tg else "CORINTHIANS 1 x 1 PORTUGUESA", "88:00")
        if t > tg: flashw(img, t, tg); poptext(img, "GOL DO DAVI!", cx, cy - 40, t, tg, 130, GOLD, -4); img.alpha_composite(confetti(W, H, t - tg))
    else:
        u = t - tb; B(img, "amber", T); img.alpha_composite(confetti(W, H, u + 2))
        b, dv = cut("benny", 760), cut("davi", 720)
        paste(img, b, cx - 200, H - b.height / 2 - 200); paste(img, dv, cx + 200, H - dv.height / 2 - 200)
        poptext(img, "O 1º A ABRAÇAR:", cx, 420, u, 0.0, 80, WHITE); poptext(img, "BENNY!", cx, 540, u, 0.3, 140, INK, -3)
        paste(img, chip("CORINTHIANS 1 x 1 PORTUGUESA", 46, WHITE, INK), cx, 700, 1, back((u - 0.5) / 0.3) if u > 0.5 else 0)

LOSS = [("D", "Portuguesa 0-2 Santos"), ("D", "Palmeiras 3-0 Portuguesa"), ("D", "Portuguesa 1-2 Bragantino")]
def s5(img, t, T):
    tf = wt(5, "torcida") - 0.2; ts = wt(5, "saf") - 0.3
    if t < tf:
        B(img, "red", T); poptext(img, "O PESADELO", cx, 420, t, 0.0, 120, WHITE)
        for k, (r, s) in enumerate(LOSS):
            t0 = wt(5, "três") - 0.2 + k * 0.45
            if t > t0: paste(img, result_row(r, s), cx, 680 + k * 130, 1, back((t - t0) / 0.25))
        tz = wt(5, "três") + 1.4
        if t > tz: paste(img, chip("15º • ZONA DE REBAIXAMENTO", 56, WHITE, RED), cx, 1150, 1, back((t - tz) / 0.3), -4)
    elif t < ts:
        u = t - tf; B(img, "night", T)
        b = panel(980, 190, (250, 250, 250, 255), 6, (0, 0, 0, 0)); ImageDraw.Draw(b).text((490, 95), "FORA, THIAGO", font=font("blk", 100), fill=RED, anchor="mm")
        paste(img, b, cx, 560, 1, back(u / 0.35), -4 + 2 * math.sin(u * 3))
        g = gray("tee", 900); paste(img, g, cx, H - g.height / 2 - 200)
        pop(img, chip("A TORCIDA NA GRADE", 50, INK, WHITE), cx, 780, u, 0.4)
    else:
        u = t - ts; B(img, "night", T)
        paste(img, mailp("SAF Portuguesa", "REUNIÃO URGENTE"), cx, 860, 1, back(u / 0.35))
        pop(img, stamp("O EMPREGO EM RISCO", 80, RED), cx, 1250, u, 0.6, 0.25, -6)

TAB = [("12º", "Mirassol", 12), ("13º", "Novorizontino", 11), ("14º", "Água Santa", 10), ("15º", "PORTUGUESA", 10), ("16º", "Velo Clube", 8)]
def s6(img, t, T):
    tl = wt(6, "um", 1) - 0.2; tm = wt(6, "mesmo") - 0.2; tc = wt(6, "cauari") - 0.3
    if t < tl:
        B(img, "dark", T); poptext(img, "ÚLTIMA RODADA", cx, 420, t, 0.0, 110, WHITE)
        p = panel(940, 560, (12, 14, 18, 240)); pd = ImageDraw.Draw(p)
        for k, (pos, n, pts) in enumerate(TAB):
            yy = 40 + k * 100; me = n == "PORTUGUESA"
            if me: pd.rounded_rectangle((16, yy - 10, 924, yy + 74), 16, fill=RED)
            pd.text((40, yy + 32), pos, font=font("bd", 40), fill=WHITE, anchor="lm"); pd.text((160, yy + 32), n, font=font("blk" if me else "bd", 44), fill=WHITE, anchor="lm")
            pd.text((880, yy + 32), str(pts), font=font("blk", 44), fill=WHITE, anchor="rm")
        paste(img, p, cx, 900, 1, back(t / 0.3)); pop(img, chip("vs SÃO PAULO: PERDEU, CAIU", 52, INK, GOLD), cx, 1270, t, 0.8)
    elif t < tm:
        u = t - tl; lance(img, lambda x: L.penalty(x, False), u + 2, "PORTUGUESA 1 x 1 SÃO PAULO", "93:00")
        pop(img, chip("PÊNALTI PRA LUSA", 60, INK, GOLD), cx, 620, t, wt(6, "pênalti") - 0.2, 0.25, -3)
        if t > tc: paste(img, pcard("cauari3d", "CAUARI", 58, "PE", 300), 840, 1450, 1, 0.8 + 0.2 * back((t - tc) / 0.3))
    else:
        u = t - tm; B(img, "sepia", T)
        paste(img, newspaper(W * 0.88, "PAULISTÃO 2026", "CAUARI PERDE O PÊNALTI", "Corinthians passa nas cobranças", sepia=True), cx, 820, 1, back(u / 0.4), (1 - ease(u / 0.4)) * 200)
        pop(img, chip("ANO PASSADO", 60, WHITE, INK), cx, 1260, u, 0.4)

def s7(img, t, T):
    tg = wt(7, "gol"); t0 = tg - L.TK - 0.4
    lt = max(0.0, t - t0) * (0.6 if t < tg else 1.0) if t > t0 else 0.0
    if t < tg + 0.8:
        lance(img, L.penalty, lt, "PORTUGUESA 1 x 1 SÃO PAULO" if t < tg else "PORTUGUESA 2 x 1 SÃO PAULO", "93:00")
        if t < tg: poptext(img, "ELE FECHA O OLHO...", cx, 660, t, 0.0, 90, WHITE)
        else: flashw(img, t, tg); poptext(img, "GOOOL!", cx, cy - 60, t, tg, 200, GOLD, -4)
    else:
        u = t - tg - 0.8; B(img, "green", T); img.alpha_composite(rays(W, H, cx, cy, T, WHITE, 16, 80)); img.alpha_composite(confetti(W, H, u))
        poptext(img, "A LUSA", cx, 620, u, 0.0, 150, WHITE); poptext(img, "FICA NA ELITE!", cx, 790, u, 0.2, 120, GOLD, -3)
        paste(img, chip("PORTUGUESA 2 x 1 SÃO PAULO", 50, WHITE, INK), cx, 980, 1, back(u / 0.3))
        c = cut("cauari3d", 620); paste(img, c, cx, H - c.height / 2 - 190)

EVO = [("davi", "DAVI", "MEI", 52, 58, True), ("levi3d", "LEVI SANTOS", "MEI", 60, 63, False), ("cauari3d", "CAUARI", "PE", 58, 61, False), ("benny", "BENNY", "VOL", 47, 47, True)]
WD = ["davi", "levi", "cauari", "benny"]
def s8(img, t, T):
    B(img, "purple", T); img.alpha_composite(rays(W, H, cx, cy, T, GOLD, 12, 45))
    for k, (key, nm, pos, a, b, prom) in enumerate(EVO):
        t0 = wt(8, WD[k]) - 0.25
        if t < t0: continue
        x, y = (290 if k % 2 == 0 else 790), (640 if k < 2 else 1160); u = t - t0
        o = int(a + (b - a) * ease(max(0, u - 0.6) / 0.9))
        paste(img, pcard(key, nm, o, pos, 330, prom), x, y, ease(u / 0.4), 0.5 + 0.5 * back(u / 0.4))
        if u > 0.9: paste(img, chip(f"{a} → {b}" if b > a else "ESTREOU", 48, INK, GREEN if b > a else WHITE), x, y + 285, 1, back((u - 0.9) / 0.25))

XI = [("BERTINATO", 60, 0.50, 0.90), ("JOÃO VITOR", 58, 0.86, 0.72), ("BOTTEGHIN", 61, 0.64, 0.76), ("G. HENRIQUE", 58, 0.36, 0.76), ("HIPÓLITO", 57, 0.14, 0.72),
      ("HUDSON", 58, 0.50, 0.57), ("LEVI", 63, 0.76, 0.48), ("DAVI", 58, 0.24, 0.48), ("TORÓ", 65, 0.84, 0.25), ("CADORINI", 63, 0.50, 0.19), ("CAUARI", 61, 0.16, 0.25)]
def s9(img, t, T):
    img.alpha_composite(Image.new("RGBA", (W, H), (24, 92, 52, 255))); dd = ImageDraw.Draw(img)
    for i in range(0, H, 160): dd.rectangle((0, i, W, i + 80), fill=(28, 100, 58))
    X0, Y0, PW, PH = 60, 420, 960, 1160; L_ = (235, 245, 235)
    dd.rectangle((X0, Y0, X0 + PW, Y0 + PH), outline=L_, width=5); dd.line((X0, Y0 + PH / 2, X0 + PW, Y0 + PH / 2), fill=L_, width=4)
    dd.ellipse((cx - 110, Y0 + PH / 2 - 110, cx + 110, Y0 + PH / 2 + 110), outline=L_, width=4)
    dd.rectangle((cx - 240, Y0 + PH - 190, cx + 240, Y0 + PH), outline=L_, width=4); dd.rectangle((cx - 240, Y0, cx + 240, Y0 + 190), outline=L_, width=4)
    poptext(img, "TIME TITULAR", cx, 300, t, 0.0, 90, WHITE)
    for k, (nm, o, fx, fy) in enumerate(XI):
        t0 = 0.2 + k * 0.12
        if t < t0: continue
        x, y = X0 + fx * PW, Y0 + fy * PH; u = back(min(1, (t - t0) / 0.25)); r = 44 * u
        dd.ellipse((x - r, y - r, x + r, y + r), fill=GOLD if nm in ("DAVI", "LEVI", "CAUARI") else WHITE, outline=INK, width=5)
        paste(img, text_el(str(o), font("blk", 42), INK, 0, shadow=False), x, y, u)
        paste(img, chip(nm, 32, WHITE, INK), x, y + 72, u)
    pop(img, chip("4-3-3  •  MÉDIA 60", 56, INK, GOLD), cx, 1660, t, 1.8)
    pop(img, chip("BANCO: ROMARINHO 64 • BENNY 47", 38, WHITE, INK), cx, 1760, t, 2.1)

def s10(img, t, T):
    ta = wt(10, "a", 1); tA = wt(10, "romarinho", 2) - 0.5; tB = wt(10, "continua") - 0.9
    if t < tA:
        B(img, "dark", T); g = gray("romarinho3d", 1050); paste(img, g, cx, H - g.height / 2 - 150)
        pop(img, chip("ROMARINHO • ÍDOLO", 64, INK, WHITE), cx, 420, t, 0.0)
        pop(img, chip("NO BANCO", 100, WHITE, RED), cx, 600, t, wt(10, "perdeu") - 0.1, 0.25, -5)
        pop(img, chip("E NÃO GOSTOU...", 60, WHITE, INK), cx, 760, t, wt(10, "gostou") - 0.2, 0.25, 3)
        return
    dd = ImageDraw.Draw(img); dd.rectangle((0, 0, W, H / 2), fill=(150, 30, 30)); dd.rectangle((0, H / 2, W, H), fill=(26, 110, 60))
    for (y, L_, s1, s2, key, nm, o, t0) in ((H * 0.24, "A", "ROMARINHO VOLTA", "experiência no time", "romarinho3d", "ROMARINHO", 64, tA), (H * 0.58, "B", "TIME COMO ESTÁ", "Davi segue titular", "davi", "DAVI", 58, tB)):
        if t < t0: continue
        u = t - t0
        paste(img, text_el(L_, font("blk", 220), WHITE, 10), 230, y, 1, (0.6 + 0.4 * back(u / 0.3)) * (1 + 0.04 * math.sin(t * 4)))
        paste(img, text_el(s1, font("blk", 66), WHITE, 6), 640, y - 40, ease(u / 0.3)); paste(img, text_el(s2, font("bd", 42), (240, 240, 240), 4), 640, y + 40, ease(u / 0.3))
        paste(img, pcard(key, nm, o, "ATA" if key != "davi" else "MEI", 210, key == "davi"), 640, y + 230, ease(u / 0.3), 0.6 + 0.4 * back(u / 0.3))
    tc = wt(10, "comenta") - 0.2
    pop(img, chip("COMENTA A OU B", 70, INK, WHITE), cx, H / 2, t, tc, 0.25, -2)
    pop(img, chip("EP.3 • QUARTA 18H", 48, WHITE, INK), cx, H - 80, t, tc + 0.8)

class Lusa(Short):
    def frame(self, T):
        i, t = self.seg_at(T)
        img = Image.new("RGBA", (W, H), (10, 10, 12, 255))
        self.scenes[i](img, t, T)
        s0 = self.segs[i][0]
        if i and 0 <= T - s0 < 0.12: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(140 * (1 - (T - s0) / 0.12)))))
        hud(img, i + 1)
        paste(img, tag_box(TOP[i + 1], 46, WHITE, INK), W / 2, 230, 1, 1, -2)
        self.caption(img, T)
        if T > self.total - 2.5:
            paste(img, text_el("Música: Impact Prelude – Kevin MacLeod (incompetech.com) CC BY 4.0", font("sb", 26), (235, 235, 235), 3), W / 2, H - 40, 0.85)
        return img.convert("RGB")

SH = Lusa(D, [(s,) for s in TXT], [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10], "", ["dark"] * 10, "Impact_Prelude", 0)
S = SH
if __name__ == "__main__":
    g = [None] + SH.segs
    ev = [("tambor_impacto", 0.0, 0.5), ("whoosh_boom", g[1][0] + wt(1, "levi"), 0.3),
          ("chute_bola_1", g[4][0] + wt(4, "gol") - 0.4, 0.4), ("torcida_reacao_gol", g[4][0] + wt(4, "gol"), 0.45), ("torcida_aww", g[5][0] + 0.8, 0.2),
          ("tambor_impacto", g[5][0] + wt(5, "saf"), 0.3), ("apito_curto", g[6][0] + wt(6, "pênalti"), 0.3), ("chute_bola_1", g[7][0] + wt(7, "gol") - 0.4, 0.4),
          ("torcida_reacao_gol", g[7][0] + wt(7, "gol"), 0.5), ("tambor_impacto", g[9][0], 0.3), ("tambor_impacto", g[10][0] + wt(10, "perdeu"), 0.3)]
    main(SH, extra=ev)
