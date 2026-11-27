from extra import *
from scripts import PAL3
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
EST = lambda h: logo("EST", h)
ESTC = (200, 20, 30); PALC = (20, 120, 60)
def wt(i, w, dflt=0.5):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return dflt
def emo(img, name, x, y, t, t0, sz=180):
    if t < t0: return
    paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))
def pbar(img, lg, pct, col, x, y, t, t0, hmax=560):
    if t < t0: return
    u = ease((t - t0) / 0.9); h = hmax * pct / 100 * u; w = 230; d = ImageDraw.Draw(img)
    d.rounded_rectangle((x - w / 2, y - h, x + w / 2, y), 18, fill=col, outline=INK, width=6)
    paste(img, txt(f"{int(round(pct * u))}%", 96, WHITE, 10), x, y - h - 70, 1)
    paste(img, lg, x, y + 110, 1)
def clock(sz, minute, t, t0):
    sz = int(sz); im = Image.new("RGBA", (sz * 2, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, sz * 2, sz), 26, fill=(15, 18, 26, 240), outline=WHITE, width=6)
    m = int(round(minute * ease((t - t0) / 0.7))) if t > t0 else 0
    d.text((sz, sz / 2), f"{m}'", font=font("blk", int(sz * 0.62)), fill=AMB, anchor="mm")
    return im
def goal(img, t, T, i, minute, name, score, kw_min, kw_name, kw_score):
    img.alpha_composite(rays(W, H, cx, 820, T, (150, 255, 170), 14, 40))
    pop(img, clock(150, minute, t, 0.0), cx, 400, t, 0.0, 0.25, -3)
    tn = wt(i, kw_name, 1.0) - 0.25
    pop(img, jersey("", name, 380, PALC), cx, 760, t, tn, 0.25, -3)
    pop(img, chip(f"⚽ {name}", 60, INK, AMB) if False else chip(name, 66, INK, AMB), cx, 1010, t, tn + 0.15, 0.25, 3)
    ts = wt(i, kw_score, 2.2) - 0.25
    if t > ts:
        pop(img, scorebox("PAL", EST(120), score, 0, 120), cx + shake(t, ts + 0.1, 12), 1250, t, ts)
        u = t - ts
        if u < 1.2: img.alpha_composite(confetti(W, H, u, seed=i))
    emo(img, "fogo", 900, 560, t, tn + 0.2, 160)
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 850, T, (150, 255, 170), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, chip("PALPITE CRAVADO", 64, INK, AMB), cx, 440, 1, sc, -3)
    paste(img, scorebox("PAL", EST(150), 3, 0, 150), cx + shake(t, 0.05, 14), 760, 1, sc, -2)
    paste(img, txt("ATROPELO", 150, WHITE, 14), cx, 1040, 1, sc, 2)
    pop(img, chip("HOJE • 17H • CENTENÁRIO", 52, WHITE, INK), cx, 1230, t, 0.6, 0.25, -2)
    emo(img, "explodindo", 900, 560, t, 1.3, 170)
def s1(img, t, T):
    pop(img, chip("MERCADO DE PREVISÕES", 60, INK, WHITE), cx, 420, t, 0.0)
    emo(img, "olhos", 900, 560, t, 0.1, 160)
    pbar(img, logo("PAL", 150), 71, (30, 160, 80), 330, 1180, t, wt(1, "setenta") - 0.3)
    pbar(img, EST(150), 21, ESTC, 750, 1180, t, wt(1, "vinte") - 0.3)
def s2(img, t, T): goal(img, t, T, 2, 33, "GUSTAVO GÓMEZ", 1, "trinta", "gustavo", "um")
def s3(img, t, T): goal(img, t, T, 3, 61, "FLACO LÓPEZ", 2, "sessenta", "flaco", "dois")
def s4(img, t, T):
    goal(img, t, T, 4, 80, "RAMÓN SOSA", 3, "oitenta", "ramón", "três")
    tt = wt(4, "tetra", 3.4) - 0.2
    if t > tt:
        pop(img, stamp("TETRA!", 150, GREEN), cx, 1030, t, tt, 0.25, -6)
        paste(img, emoji.get("trofeu", 190, t - tt), 160, 820, 1)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 230, 120), 14, 45))
    pop(img, chip("MEU PALPITE", 64, INK, AMB), cx, 400, t, 0.0)
    pop(img, scorebox("PAL", EST(140), 3, 0, 140), cx, 620, t, 0.05)
    for k, s in enumerate(("33' GUSTAVO GÓMEZ", "61' FLACO LÓPEZ", "80' RAMÓN SOSA")):
        pop(img, chip(s, 46, WHITE, GREEN), cx, 800 + 85 * k, t, 0.2 + 0.12 * k, 0.25, (-2, 2, -2)[k])
    pop(img, txt("E O SEU?", 120, WHITE), cx, 1130, t, wt(5, "seu", 1.0) - 0.3)
    pop(img, txt("COMENTA O PLACAR!", 92, AMB), cx, 1280, t, wt(5, "comenta", 1.4) - 0.2)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 125, 0.85)
S = Short("/home/claude/sab28b/pal3", PAL3, [s0, s1, s2, s3, s4, s5], "FINAL • PALPITE", ["green", "dark", "green", "night", "green", "blue"], "Rising_Game", 0)
if __name__ == "__main__":
    ev = [("tambor_impacto", 0.0, 0.45), ("camera_click", S.segs[1][0] + wt(1, "setenta"), 0.2)]
    for i, kw in ((2, "um"), (3, "dois"), (4, "três")):
        ts = S.segs[i][0] + wt(i, kw, 2.2) - 0.2
        ev += [("chute_bola_1", ts - 0.3, 0.3), ("torcida_grita_gol", ts, 0.2)]
    ev += [("tambor_impacto", S.segs[4][0] + wt(4, "tetra", 3.4), 0.35)]
    main(S, extra=ev)
