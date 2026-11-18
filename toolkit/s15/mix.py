import sys, numpy as np, subprocess
sys.path.insert(0, "/home/claude/work/sfx"); import sfxlib
from scipy.io import wavfile
SR = 44100
sr, v = wavfile.read("narr.wav"); v = v.astype(np.float32) / 32768
if v.ndim > 1: v = v.mean(1)
N = int((len(v) / SR + 0.5) * SR); out_v = np.zeros(N, np.float32); out_v[:len(v)] = v
subprocess.run("ffmpeg -loglevel error -y -ss 50.95 -t 30 -i /home/claude/ep1/music/Hitman.mp3 -ac 1 -ar 44100 /tmp/hm.wav", shell=True)
_, m = wavfile.read("/tmp/hm.wav"); m = m.astype(np.float32)[:N] / 32768
m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.05          # bed baixo
# ducking: envelope da voz
blk = 441; env = np.sqrt(np.convolve(out_v ** 2, np.ones(blk * 10) / (blk * 10), "same"))
duck = np.where(env > 0.02, 0.55, 1.0).astype(np.float32)
duck = np.convolve(duck, np.ones(4410) / 4410, "same")
m *= duck
fade = np.ones(N, np.float32); fl = int(0.6 * SR); fade[-fl:] = np.linspace(1, 0, fl); m *= fade
fx = np.zeros(N, np.float32)
def add(name, t, g):
    s = sfxlib.load(name) * g; i = int(t * SR); e = min(N, i + len(s)); fx[i:e] += s[:e - i]
add("tambor_impacto", 0.0, 0.5)
for t in (5.18, 6.76, 11.48, 16.04, 18.62, 20.66, 22.94): add("whoosh_1" if t < 15 else "whoosh_2", max(0, t - 0.15), 0.18)
for t in (11.82, 12.26, 12.4, 12.55): add("chute_bola_1", t, 0.25)
add("tambor_impacto", 15.02, 0.4)
add("torcida_comemora", 20.3, 0.12)
mix = out_v + m + fx
mix /= max(1.0, np.abs(mix).max() / 0.98)
wavfile.write("mix.wav", SR, (mix * 32767).astype(np.int16))
