import sys, json, numpy as np, subprocess
sys.path.insert(0, "/home/claude/videos-sylence/assets/sfx"); import sfxlib
from scipy.io import wavfile
SR = 44100
d = json.load(open("durs.json")); starts = np.concatenate([[0], np.cumsum(d)[:-1]])
N = int(sum(d) * SR)
voz = np.zeros(N, np.float32)
for i, s in enumerate(starts):
    _, v = wavfile.read(f"v_{i:02d}.wav"); v = v.astype(np.float32) / 32768
    a = int((s + (0.05 if i == 0 else 0.12)) * SR); e = min(N, a + len(v)); voz[a:e] += v[:e - a]
voz *= 0.9 / (np.abs(voz).max() + 1e-9)
subprocess.run(f"ffmpeg -loglevel error -y -ss 50.95 -i /tmp/hitman.mp3 -ac 1 -ar {SR} /tmp/hm.wav", shell=True, check=True)
_, m = wavfile.read("/tmp/hm.wav"); m = m.astype(np.float32) / 32768
m = np.tile(m, 2)[:N]; m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.06
env = np.sqrt(np.convolve(voz ** 2, np.ones(4410) / 4410, "same"))
duck = np.convolve(np.where(env > 0.02, 0.5, 1.0).astype(np.float32), np.ones(4410) / 4410, "same")
m *= duck; fl = int(0.6 * SR); m[-fl:] *= np.linspace(1, 0, fl)
fx = np.zeros(N, np.float32)
def add(name, t, g):
    s = sfxlib.load(name) * g; i = int(max(0, t) * SR); e = min(N, i + len(s)); fx[i:e] += s[:e - i]
add("whoosh_boom", 0.0, 0.25)
for k in range(1, 12):
    c = starts[k]
    add("whoosh_grave", c - 0.23, 0.5)          # passagem: sobe e explode no corte
    add("whoosh_2", c - 0.05, 0.32)             # swish curto no corte
    if 1 <= k <= 10: add("tambor_impacto", c + 0.16, 0.55 if k == 10 else 0.22)  # batida do #numero
W_=json.load(open("words.json"))
tn=next(w["t0"] for w in W_[10] if w["w"].strip(".,") == "6")
add("whoosh_boom", starts[10]+0.12+tn-0.05, 0.5)
for j in range(1,10): add("whoosh_1", j*0.34-0.05, 0.08)
mix = voz + m + fx
mix /= max(1.0, np.abs(mix).max() / 0.98)
wavfile.write("mix.wav", SR, (mix * 32767).astype(np.int16))
