import json
NW = json.load(open("narr_words.json"))
PADS = [0.5, 1.0, 1.5, 1.3, 1.6, 1.2, 1.3, 1.3, 1.5, 1.3, 2.8]
LEAD = 0.2; sc = []; t0 = 0
for k, o in enumerate(NW):
    dur = round(round((LEAD + o["dur"] + PADS[k]) * 30) / 30, 4)
    sc.append({"start": round(t0, 4), "dur": dur, "words": [[w, a + LEAD, b + LEAD] for w, a, b in o["words"]]}); t0 += dur
json.dump(sc, open("scenes.json", "w"), ensure_ascii=False); print("total", t0)
