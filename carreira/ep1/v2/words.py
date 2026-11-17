import json, re, unicodedata, numpy as np, wave
from faster_whisper import WhisperModel
from script2 import BLOCKS
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())
w = wave.open("narr.wav"); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
import subprocess
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","narr.wav","-ar","16000","-ac","1","n16.wav"],check=True)
w = wave.open("n16.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language="pt", word_timestamps=True, initial_prompt="Cambridge United, Rick Miguel, Murrey, Gildo, Kaikai, Bauer, Pelly Ruddock Mpanzu, Tomás Ferreira, Theo Okafor, Kofi Mensah-Hart, Ollie Fenwick, Accrington, Colchester, Crewe, Abbey Stadium")
hyp = [(x.word.strip(), x.start, x.end) for s in segs for x in s.words]
# palavras do roteiro (sem tags) com cena
ref = []
for bid, mus, sents in BLOCKS:
    for si, (sc, txt) in enumerate(sents):
        clean = re.sub(r"\[[^\]]*\]", "", txt).split()
        for wd in clean: ref.append({"w": wd, "scene": sc, "block": bid, "music": mus, "sent": txt})
# alinhamento DP simples por similaridade
import difflib
H = [norm(h[0]) for h in hyp]; R = [norm(r["w"]) for r in ref]
sm = difflib.SequenceMatcher(None, R, H, autojunk=False)
times = [None] * len(R)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ("equal", "replace"):
        for k in range(i2 - i1):
            j = j1 + min(k, j2 - j1 - 1) if j2 > j1 else None
            if j is not None: times[i1 + k] = (hyp[j][1], hyp[j][2])
# interpola faltantes
for i in range(len(times)):
    if times[i] is None:
        prev = next((times[k] for k in range(i - 1, -1, -1) if times[k]), (0, 0))
        nxt = next((times[k] for k in range(i + 1, len(times)) if times[k]), (prev[1] + 0.3, prev[1] + 0.6))
        times[i] = (prev[1], (prev[1] + nxt[0]) / 2 if nxt[0] > prev[1] else prev[1] + 0.25)
for r, t in zip(ref, times): r["t0"], r["t1"] = round(t[0], 3), round(t[1], 3)
total = len(a) / 16000
json.dump({"words": ref, "total": round(total + 1.0, 2)}, open("words.json", "w"), ensure_ascii=False)
miss = sum(1 for tag,i1,i2,j1,j2 in sm.get_opcodes() if tag in ("delete",) for _ in range(i2-i1))
print(len(ref), "palavras;", miss, "sem match; total", round(total, 1))
