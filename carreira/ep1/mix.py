import sys, json
sys.path.insert(0, "/home/claude/work/sfx")
from mixsfx import mix
sys.argv = ["x", "preview"]
import make_ep1 as M
ev = []
for i, s in enumerate(M.SHOTS):
    sc, t0, t1 = s["scene"], s["t0"], s["t1"]
    if i > 0: ev.append((t0, ["whoosh_1", "whoosh_2", "whoosh_3"][i % 3], 0.18))
    if sc in ("crewe", "boxing", "boxing_sub"):
        k = t0
        while k < t1 - 1: ev.append((k, "estadio_ambiente", 0.10)); k += 11.5
    if sc == "crewe": ev.append((t0 + 0.2, "torcida_grito_homens", 0.12))
    if sc == "crewe_goal":
        tg = min(4.2, (t1 - t0) * 0.55)
        ev += [(t0, "estadio_ambiente", 0.10), (t0 + tg - 1.6, "chute_bola_1", 0.3), (t0 + tg - 0.15, "chute_bola_2", 0.3), (t0 + tg + 0.35, "whoosh_boom", 0.3), (t0 + tg + 0.5, "torcida_aww", 0.35)]
    if sc == "fall": ev.append((t0 + 0.3, "torcida_aww", 0.25))
    if sc in ("title", "offer", "ab"): ev.append((t0 + (2.0 if sc == "offer" else 0.2), "tambor_impacto", 0.35))
    if sc in ("tr_tomas", "tr_theo", "murrey_card", "gildo_card", "kofi", "ollie", "rickcard"): ev.append((t0 + 0.1, "camera_click", 0.3)); ev.append((t0 + 0.7, "whoosh_grave", 0.2))
    if sc == "murrey_assist" and s["cues"][0]["i"] == 45:
        a = s["cues"][1]["t0"] - 0.4; tl = min(2.2, (t1 - t0) * 0.3) + 1.3 + 1.1
        ev += [(t0, "estadio_ambiente", 0.08), (a + tl - 1.1, "chute_bola_1", 0.3), (a + tl, "chute_bola_2", 0.35), (a + tl + 0.4, "torcida_reacao_gol", 0.3)]
    if sc == "murrey_goal":
        tsh = min(1.6, (t1 - t0) * 0.25) + 1.2 + 0.6
        ev += [(t0, "estadio_ambiente", 0.10), (t0 + tsh, "chute_bola_2", 0.4), (t0 + tsh + 0.5, "torcida_grita_gol", 0.4), (t0 + tsh + 0.8, "torcida_comemora", 0.3)]
    if sc == "hug": ev.append((t0, "torcida_comemora", 0.18))
    if sc == "boxing_sub": ev.append((t0 + 0.3, "apito_curto", 0.3))
    if sc == "crewe": ev.append((t0 + 0.1, "apito_curto", 0.0))
    if sc == "table_up": ev.append((t0 + 0.8, "torcida_comemora", 0.15))
    if sc == "banner": ev.append((t0, "torcida_grito_homens", 0.2))
mix("narr.wav", M.TOTAL, ev, "trilha.wav", lead=0.0)
print(len(ev), "eventos")
