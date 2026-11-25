import sys; sys.path.insert(0, "/home/claude/sex27"); sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common")
from engine import *
from fonts import F
import bgvideo
BG = bgvideo.BG("/home/claude/sex27/bg2/pxb_165713.mp4", 2, 1, 150, 9)
def base(tag):
    im = BG.frame(0.5); paste(im, tag_box(tag, 44, WHITE, INK), W / 2, 150, 1); return im
def T(s, size, col=WHITE, f="luckiest"): return text_el(s, F(f, size), col, 10)
def sb(a, b, ga, gb, sub=None, sz=110):
    w = int(sz * 7.4); h = int(sz * 1.5); im = Image.new("RGBA", (w, h + (60 if sub else 0)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 28, fill=(15, 18, 26, 235), outline=WHITE, width=4)
    la, lb = logo(a, sz), logo(b, sz); im.alpha_composite(la, (int(sz * 0.8 - la.width / 2), int(h / 2 - la.height / 2))); im.alpha_composite(lb, (int(w - sz * 0.8 - lb.width / 2), int(h / 2 - lb.height / 2)))
    d.text((w / 2, h / 2), f"{ga} x {gb}", font=font("blk", sz * 0.7), fill=WHITE, anchor="mm")
    if sub: d.text((w / 2, h + 32), sub, font=font("bd", 36), fill=AMB, anchor="mm")
    return im
out = []
# 1 capa
im = base("FINAL DA LIBERTADORES • SÁB 28/11 • 17H")
paste(im, logo("PAL", 300), 280, 620, 1); paste(im, logo("EST", 300), 800, 620, 1); paste(im, T("X", 140), W / 2, 620, 1)
paste(im, T("QUEM LEVA", 150), W / 2, 1000, 1, 1, -3); paste(im, T("A AMÉRICA?", 150, AMB), W / 2, 1170, 1, 1, -3)
paste(im, chip("ARRASTA PRO LADO  →", 54, INK, WHITE), W / 2, 1500, 1); out.append(im)
# 2 caminho Palmeiras
im = base("O CAMINHO DO PALMEIRAS"); paste(im, logo("PAL", 200), W / 2, 380, 1)
for k, (lab, a, b, ga, gb, sub) in enumerate([("OITAVAS", "PAL", "CER", 2, 1, "1x1 e 1x0"), ("QUARTAS", "PAL", "LDU", 3, 3, "4x3 NOS PÊNALTIS"), ("SEMIFINAL", "PAL", "FLU", 2, 2, "5x3 NOS PÊNALTIS")]):
    y = 680 + k * 330; paste(im, chip(lab, 44, INK, AMB), W / 2, y - 105, 1)
    box = Image.new("RGBA", (10, 10)); 
    w = 820; h = 160; p = Image.new("RGBA", (w, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, w, h), 28, fill=(15, 18, 26, 235), outline=WHITE, width=4)
    p.alpha_composite(logo("PAL", 110), (40, 25))
    d.text((w / 2, h / 2), f"{ga} x {gb}", font=font("blk", 80), fill=WHITE, anchor="mm")
    d.text((w - 100, h / 2), {"CER": "CERRO", "LDU": "LDU", "FLU": None}[b] or "", font=font("blk", 40), fill=WHITE, anchor="mm")
    if b == "FLU": p.alpha_composite(logo("FLU", 110), (w - 150, 25))
    d.text((w / 2, h + 32), sub, font=font("bd", 38), fill=AMB, anchor="mm"); paste(im, p, W / 2, y + 30, 1)
paste(im, chip("2 DISPUTAS DE PÊNALTI • 9 DE 10 CONVERTIDOS", 40, WHITE, GREEN), W / 2, 1720, 1); out.append(im)
# 3 caminho Estudiantes
im = base("O CAMINHO DO ESTUDIANTES"); paste(im, logo("EST", 200), W / 2, 380, 1)
for k, (lab, b, ga, gb, sub) in enumerate([("OITAVAS", "U. CATÓLICA", 4, 1, "1x1 e 3x0"), ("QUARTAS", "COR", 2, 1, "1x1 e 1x0"), ("SEMIFINAL", "FLA", 0, 0, "3x2 NOS PÊNALTIS • NO MARACANÃ")]):
    y = 680 + k * 330; paste(im, chip(lab, 44, INK, AMB), W / 2, y - 105, 1)
    w = 820; h = 160; p = Image.new("RGBA", (w, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, w, h), 28, fill=(15, 18, 26, 235), outline=WHITE, width=4)
    p.alpha_composite(logo("EST", 110), (40, 25)); d.text((w / 2, h / 2), f"{ga} x {gb}", font=font("blk", 80), fill=WHITE, anchor="mm")
    if b in ("COR", "FLA"): p.alpha_composite(logo(b, 110), (w - 150, 25))
    else: d.text((w - 130, h / 2), "U. CATÓLICA", font=font("blk", 30), fill=WHITE, anchor="mm")
    d.text((w / 2, h + 32), sub, font=font("bd", 34), fill=AMB, anchor="mm"); paste(im, p, W / 2, y + 30, 1)
paste(im, chip("ELIMINOU 2 BRASILEIROS", 50, WHITE, RED), W / 2, 1720, 1); out.append(im)
# 4 goleiros
im = base("SE FOR PROS PÊNALTIS...")
paste(im, T("DUELO DE", 120), W / 2, 380, 1, 1, -3); paste(im, T("GOLEIROS", 140, AMB), W / 2, 520, 1, 1, -3)
paste(im, jersey("", "CARLOS MIGUEL", 340, (20, 120, 60)), 290, 900, 1); paste(im, jersey("1", "MUSLERA", 340, (70, 70, 80)), 790, 900, 1)
for x, ls in ((290, ["2,04 m", "PEGOU NAS 2", "DISPUTAS"]), (790, ["40 ANOS", "3 DEFESAS NO", "MARACANÃ"])):
    for j, l in enumerate(ls): paste(im, chip(l, 46 if j else 60, INK, AMB if j == 0 else WHITE), x, 1170 + j * 100, 1)
paste(im, T("QUEM PEGA MAIS?", 90), W / 2, 1620, 1); out.append(im)
# 5 títulos
im = base("TÍTULOS DA LIBERTADORES")
paste(im, logo("EST", 220), 290, 520, 1); paste(im, logo("PAL", 220), 790, 520, 1)
paste(im, T("4", 260, AMB), 290, 830, 1); paste(im, T("3", 260, GREEN), 790, 830, 1)
paste(im, chip("68 • 69 • 70 • 2009", 44, INK, WHITE), 290, 1010, 1); paste(im, chip("99 • 2020 • 2021", 44, INK, WHITE), 790, 1010, 1)
paste(im, chip("EM 1968 O ESTUDIANTES GANHOU DO PALMEIRAS", 38, WHITE, RED), W / 2, 1220, 1)
paste(im, chip("NO JOGO EXTRA, NO CENTENÁRIO", 38, WHITE, RED), W / 2, 1300, 1)
paste(im, T("58 ANOS DEPOIS:", 90), W / 2, 1500, 1); paste(im, T("REVANCHE?", 120, AMB), W / 2, 1630, 1); out.append(im)
# 6 CTA
im = base("FINAL • SÁB 28/11 • 17H • CENTENÁRIO")
paste(im, trophy(380), W / 2, 600, 1)
paste(im, T("QUAL O SEU", 130), W / 2, 950, 1, 1, -3); paste(im, T("PLACAR?", 170, AMB), W / 2, 1120, 1, 1, -3)
paste(im, chip("COMENTA AÍ", 70, INK, WHITE), W / 2, 1380, 1)
for i, s in enumerate(["PALMEIRAS CAMPEÃO", "ESTUDIANTES CAMPEÃO"]): paste(im, chip(s, 46, WHITE, GREEN if i == 0 else RED), W / 2, 1520 + i * 100, 1)
out.append(im)
for k, im in enumerate(out): im.convert("RGB").save(f"/home/claude/carr/final_{k + 1}.jpg", quality=93)
c = Image.new("RGB", (6 * 270, 480))
for k, im in enumerate(out): c.paste(im.convert("RGB").resize((270, 480)), (k * 270, 0))
c.save("/tmp/carr.jpg")
