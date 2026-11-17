import sys, os, json, subprocess, concurrent.futures as cf
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common")
import gvoz
from script import S
os.makedirs("s", exist_ok=True)
def one(i):
    p = f"s/{i:03d}.wav"
    if not os.path.exists(p):
        open(p, "wb").write(gvoz.synth_chunk(S[i][1], "Charon", 1.0))
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
    return d
with cf.ThreadPoolExecutor(6) as ex: durs = list(ex.map(one, range(len(S))))
# gaps: maior pausa entre cenas
t = 0.8; cues = []
HOLD = {'crewe_goal':2.5,'title':2.5,'fall':0.8,'h2005':1.0,'injury':1.2,'rickcard':1.5,'whiteboard':1.5,'murrey_card':2.0,'murrey_assist':2.0,'table_up':2.0,'race':1.5,'gildo_card':1.5,'ollie':1.0,'boxing_sub':1.0,'murrey_goal':3.5,'hug':1.5,'contract':1.5,'offer':1.0,'ab':0.5}
for i, (sc, txt) in enumerate(S):
    cues.append({"i": i, "scene": sc, "text": txt, "t0": round(t, 3), "t1": round(t + durs[i], 3)})
    same = i + 1 < len(S) and S[i + 1][0] == sc
    gap = 0.4 if same else 1.0
    if not same: gap += HOLD.get(sc, 0)
    t += durs[i] + gap
json.dump({"cues": cues, "total": round(t + 1.5, 3)}, open("cues.json", "w"), ensure_ascii=False, indent=0)
# monta narração
import numpy as np, wave
sr = 44100; out = np.zeros(int((t + 1.5) * sr), np.int16)
for c in cues:
    w = wave.open(f"s/{c['i']:03d}.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    if w.getframerate() != sr: raise SystemExit("sr")
    s0 = int(c["t0"] * sr); out[s0:s0 + len(a)] = a[: len(out) - s0]
w = wave.open("narr.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(out.tobytes()); w.close()
print("total", round(t + 1.5, 1), "s")
