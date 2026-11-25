from extra import *
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common")
import fotofx as FX, fotos_cc, emoji
from fonts import F
from scripts import TRES
FP = "/home/claude/videos-sylence/assets/fotos_cc/"
PAN = FP + "est/cc_a8e55cb3.jpg"; TOWER = FP + "est/cc_fbfbb3a9.jpg"
FLA = FP + "fl/cc_cdd983df.jpg"; ABEL = FP + "abel/cc_e4571f8d.jpg"; MUS = FP + "mus/cc_30d9a437.jpg"
CR = {p: fotos_cc.credito(p) for p in (PAN, TOWER, FLA, ABEL, MUS)}
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def dur(i): return S.segs[i][1] - S.segs[i][0] + 0.1
def big(s, size, col=WHITE, f="anton", st=10): return text_el(s, F(f, size), col, st)
def num(n, sz=150):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, sz - 4, sz - 4), fill=AMB, outline=INK, width=6); d.text((sz / 2, sz / 2 + 4), str(n), font=F("anton", sz * 0.62), fill=INK, anchor="mm"); return im
def s0(img, t, T):
    img.alpha_composite(FX.pan_wide(FX.load(PAN), t, dur(0) + 0.6, 0.15, 0.55, 1.0))
    sc = 1.0 + 0.04 * math.sin(min(t, 0.4) * 8)
    paste(img, big("3 NOMES", 190, WHITE), cx, 470, 1, sc, -3)
    paste(img, big("DECIDEM A FINAL", 112, AMB), cx, 640, 1, sc, -3)
    for k in range(3): pop(img, num(k + 1, 130), 300 + k * 240, 860, t, 0.5 + k * 0.15)
    if t > wt(0, "terceiro") - 0.2:
        pop(img, stamp("O 3º É O MAIS PERIGOSO", 66, RED), cx, 1060, t, wt(0, "terceiro") - 0.2, 0.25, -5)
    FX.credit(img, CR[PAN])
def s1(img, t, T):
    img.alpha_composite(FX.pop3d(FLA, t, dur(1), (0.5, 0.35), h=1350, y=1230, delay=0.05))
    pop(img, num(1, 120), 150, 330, t, 0.0)
    pop(img, big("FLACO LÓPEZ", 140, WHITE), cx + 40, 330, t, 0.15, 0.3, -2)
    pop(img, logo("PAL", 110), 940, 470, t, 0.35)
    tg = wt(1, "vinte") - 0.25
    if t > tg:
        u = t - tg; paste(img, odometer(26, 2, 120, round(min(u, 1.0), 2), 0.8), 230, 620, 1, back(min(1, u / 0.3)), -4)
        pop(img, chip("GOLS", 50, INK, AMB), 230, 760, u, 0.2, 0.25, -4)
    ta = wt(1, "catorze") - 0.25
    if t > ta:
        u = t - ta; paste(img, odometer(14, 2, 120, round(min(u, 1.0), 2), 0.8), 850, 620, 1, back(min(1, u / 0.3)), 4)
        pop(img, chip("ASSIST.", 50, INK, WHITE), 850, 760, u, 0.2, 0.25, 4)
        paste(img, emoji.get("fogo", 150, u), 850, 470, 1, back(min(1, u / 0.3)))
    FX.credit(img, CR[FLA])
def s2(img, t, T):
    bgk = FX.kb(FX.load(TOWER), t, dur(2), (1.2, 1.3), (0.6, 0.5), (0.55, 0.45)).filter(ImageFilter.GaussianBlur(10))
    bgk.alpha_composite(Image.new("RGBA", (W, H), (10, 40, 20, 140))); img.alpha_composite(bgk)
    u = ease(t / 0.45); pc = FX.polaroid(ABEL, 700, -4 + 3 * math.sin(t * 0.8))
    paste(img, pc, cx + (1 - u) * 700, 900, 1, 0.95 + 0.05 * ease(t / dur(2)))
    pop(img, num(2, 120), 170, 330, t, 0.0); pop(img, big("ABEL FERREIRA", 130, WHITE), cx + 50, 330, t, 0.15, 0.3, -2)
    pop(img, chip("4ª FINAL DE LIBERTADORES", 54, INK, WHITE), cx, 470, t, wt(2, "quarta") - 0.2, 0.25, 2)
    if t > wt(2, "tricampeão") - 0.25:
        pop(img, stamp("TRI?", 150, GREEN), 820, 1230, t, wt(2, "tricampeão") - 0.25, 0.25, -10)
        for k, y in enumerate(("2020", "2021")): pop(img, chip(y, 46, INK, AMB), 230 + k * 170, 1600, t, wt(2, "tricampeão") + 0.1 * k)
    FX.credit(img, CR[ABEL], y=H - 120)
def s3(img, t, T):
    img.alpha_composite(FX.pop3d(MUS, t, dur(3), (0.45, 0.3), h=1250, y=1250, delay=0.05, dim=130))
    if t < 0.5: img.alpha_composite(Image.new("RGBA", (W, H), (200, 20, 20, int(110 * (1 - t / 0.5)))))
    pop(img, num(3, 120), 150, 330, t, 0.0); pop(img, big("MULSERA", 1, WHITE) if False else big("MUSLERA", 160, WHITE), cx + 40, 330, t, 0.15, 0.3, -2)
    pop(img, logo("EST", 120), 940, 480, t, 0.35)
    pop(img, chip("40 ANOS", 64, INK, AMB), 230, 520, t, wt(3, "quarenta") - 0.2, 0.25, -4)
    tp = wt(3, "três") - 0.2
    for k in range(3): pop(img, check(110, False), 190 + k * 140, 680, t, tp + k * 0.18)
    pop(img, chip("3 PÊNALTIS NO MARACANÃ", 46, WHITE, RED), 330, 810, t, tp + 0.6, 0.25, -2)
    if t > tp: paste(img, emoji.get("grito", 140, t - tp), 920, 700, 1, back(min(1, (t - tp) / 0.3)))
    FX.credit(img, CR[MUS])
def s4(img, t, T):
    img.alpha_composite(FX.kb(FX.load(TOWER), t, dur(4) + 0.6, (1.0, 1.12), (0.5, 0.55), (0.62, 0.45), vig=160))
    pop(img, chip("SÁBADO • 17H • CENTENÁRIO", 54, INK, WHITE), cx, 330, t, 0.0)
    pop(img, big("QUEM DECIDE?", 150, AMB), cx, 500, t, wt(4, "quem") - 0.2, 0.3, -3)
    for k, (p, nm) in enumerate(((FLA, "FLACO"), (ABEL, "ABEL"), (MUS, "MUSLERA"))):
        x = 200 + k * 340; tt = wt(4, "comenta") - 0.3 + k * 0.15
        if t > tt:
            st = FX.sticker(p, 430, 8); sc = back(min(1, (t - tt) / 0.3))
            paste(img, st, x, 1000, 1, sc * 0.9, (-5, 0, 5)[k]); pop(img, chip(nm, 50, INK, AMB if k < 2 else RED), x, 1270, t, tt + 0.1)
    FX.credit(img, CR[TOWER])
S = Short("/home/claude/sex27b/tres", TRES, [s0, s1, s2, s3, s4], "FINAL DA LIBERTADORES", "dark", "Five_Armies", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "terceiro") - 0.2, 0.3), ("torcida_comemora", S.segs[1][0] + wt(1, "vinte"), 0.15),
                   ("tambor_impacto", S.segs[2][0] + wt(2, "tricampeão"), 0.3), ("tambor_impacto", S.segs[3][0], 0.35), ("torcida_aww", S.segs[3][0] + wt(3, "três"), 0.12)])
