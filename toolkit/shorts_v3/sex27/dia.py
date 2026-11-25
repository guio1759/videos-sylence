from extra import *
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common")
import talk, emoji
from fonts import F
from scripts import DIA
EST = lambda h: logo("EST", h)
D = "/home/claude/sex27/dia"
J = json.load(open(D + "/words.json")); SPK = J["spk"]; SEGS = J["segs"]
CUES = talk.lipsync(D + "/narr.wav"); EN = talk.energy_env(D + "/narr.wav")
CH = {"Iapetus": talk.Talker(talk.CHARS["reporter"], cutout=True), "Puck": talk.Talker(talk.CHARS["torcedor"], cutout=True)}
NAME = {"Iapetus": ("REPÓRTER", WHITE), "Puck": ("TORCEDOR PALMEIRENSE", GREEN)}
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def char(img, i, t, T):
    v = SPK[i]; s0, s1 = SEGS[i]
    cues = [c for c in CUES if c[0] >= s0 - 0.05 and c[1] <= s1 + 0.1]
    e = float(EN[min(len(EN) - 1, int(T * 30))]) if s0 <= T <= s1 else 0
    im = CH[v].frame(T, cues, e); sz = 980; im = im.resize((sz, sz), Image.LANCZOS)
    u = back(min(1, t / 0.25)); x = W / 2 + (1 - u) * (-260 if v == "Iapetus" else 260)
    paste(img, im, x, 1420, 1, 1.0)
    nm, col = NAME[v]; paste(img, chip(nm, 40, INK, col), x, 960, 1, 0.6 + 0.4 * u, -2)
def emo(img, name, x, y, t, t0, sz=200):
    if t < t0: return
    paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))
def big(s, size, col=WHITE, font="luckiest"):
    return text_el(s, F(font, size), col, 10)
def s0(img, t, T):
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, chip("FALTAM 2 DIAS", 58, INK, AMB), cx, 300, 1, sc, -3)
    paste(img, big("PALPITE", 150, WHITE), cx, 450, 1, sc, -3); paste(img, big("DA FINAL?", 130, AMB), cx, 600, 1, sc, -3)
    pop(img, logo("PAL", 150), 170, 760, t, 0.6); pop(img, EST(150), 910, 760, t, 0.8)
    char(img, 0, t, T)
def s1(img, t, T):
    pop(img, scorebox("PAL", EST(120), 2, 1, 120), cx, 360, t, 0.0, 0.3)
    pop(img, chip("GOL DO FLACO LÓPEZ", 56, INK, AMB), cx, 560, t, wt(1, "flaco") - 0.2, 0.25, -3)
    emo(img, "fogo", 900, 700, t, wt(1, "flaco"), 190)
    char(img, 1, t, T)
def s2(img, t, T):
    pop(img, EST(170), cx, 330, t, 0.0)
    pop(img, big("+300 MIN", 140, AMB), cx, 520, t, wt(2, "trezentos") - 0.3)
    pop(img, chip("SEM TOMAR GOL", 56, WHITE, RED), cx, 660, t, wt(2, "trezentos"), 0.25, 3)
    emo(img, "olhos", 170, 760, t, 0.4, 170)
    char(img, 2, t, T)
def s3(img, t, T):
    pop(img, stamp("A MURALHA CAI!", 100, GREEN), cx + shake(t, wt(3, "muralha"), 10), 470, t, wt(3, "muralha") - 0.2, 0.25, -6)
    emo(img, "explodindo", 900, 700, t, wt(3, "cai") - 0.1, 190)
    char(img, 3, t, T)
def s4(img, t, T):
    pop(img, big("PÊNALTIS?", 140, WHITE), cx, 380, t, 0.0)
    pop(img, chip("MUSLERA: 3 DEFESAS NO MARACANÃ", 44, WHITE, RED), cx, 560, t, wt(4, "muslera") - 0.2, 0.25, -2)
    emo(img, "grito", 170, 720, t, wt(4, "três"), 180)
    char(img, 4, t, T)
def s5(img, t, T):
    pop(img, chip("CARLOS MIGUEL", 64, INK, AMB), cx, 330, t, wt(5, "carlos") - 0.2)
    if t > wt(5, "dois") - 0.2:
        u = t - wt(5, "dois") + 0.2; pop(img, big("2,04 m", 170, GREEN), cx, 520, u, 0.0)
        d = ImageDraw.Draw(img); hh = 360 * ease(u / 0.8); d.line((120, 900, 120, 900 - hh), fill=WHITE, width=10)
        for k in range(0, int(hh), 40): d.line((120, 900 - k, 150, 900 - k), fill=WHITE, width=5)
    emo(img, "coracao_verde", 910, 720, t, wt(5, "goleiro") - 0.2, 180)
    char(img, 5, t, T)
def s6(img, t, T):
    pop(img, trophy(200), cx, 330, t, 0.0)
    pop(img, chip("SÁBADO • 17H • CENTENÁRIO", 50, INK, WHITE), cx, 520, t, 0.2)
    pop(img, big("QUAL O SEU PLACAR?", 96, AMB), cx, 660, t, wt(6, "comenta") - 0.3)
    emo(img, "bola", 900, 800, t, wt(6, "comenta"), 150)
    char(img, 6, t, T)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 110, 0.85)
BGV = "vid:/home/claude/sex27/bg2/pxb_165713.mp4@2@130@7"
S = Short(D, DIA, [s0, s1, s2, s3, s4, s5, s6], "FINAL DA LIBERTADORES", [BGV] * 7, "Volatile_Reaction", 0)
S.CAPY = 0.455
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("torcida_comemora", S.segs[1][0] + wt(1, "flaco"), 0.15), ("tambor_impacto", S.segs[3][0] + wt(3, "muralha"), 0.3),
                   ("torcida_aww", S.segs[4][0] + wt(4, "três"), 0.12), ("torcida_comemora", S.segs[5][0] + wt(5, "dois"), 0.12)])
