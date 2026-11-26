import sys, json, numpy as np, subprocess
sys.path.insert(0, "/home/claude/videos-sylence/assets/sfx"); import sfxlib
from scipy.io import wavfile
SR = 44100
def build(d, music, mgain=0.06, events=None):
    du = json.load(open(f"{d}/durs.json")); starts = np.concatenate([[0], np.cumsum(du)[:-1]])
    N = int(sum(du) * SR); voz = np.zeros(N, np.float32)
    for i, s in enumerate(starts):
        _, v = wavfile.read(f"{d}/v_{i:02d}.wav"); v = v.astype(np.float32) / 32768
        a = int((s + 0.12) * SR); e = min(N, a + len(v)); voz[a:e] += v[:e - a]
    voz *= 0.9 / (np.abs(voz).max() + 1e-9)
    subprocess.run(f"ffmpeg -loglevel error -y -i {music} -ac 1 -ar {SR} /tmp/_m.wav", shell=True, check=True)
    _, m = wavfile.read("/tmp/_m.wav"); m = m.astype(np.float32) / 32768
    m = np.tile(m, 3)[:N]; m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * mgain
    env = np.sqrt(np.convolve(voz ** 2, np.ones(4410) / 4410, "same"))
    duck = np.convolve(np.where(env > 0.02, 0.5, 1.0).astype(np.float32), np.ones(4410) / 4410, "same")
    m *= duck; fl = int(1.0 * SR); m[-fl:] *= np.linspace(1, 0, fl)
    fx = np.zeros(N, np.float32)
    def add(name, t, g, maxlen=None):
        s = sfxlib.load(name) * g
        if maxlen: s = s[:int(maxlen * SR)].copy(); f = min(len(s), int(0.4 * SR)); s[-f:] *= np.linspace(1, 0, f)
        i = int(max(0, t) * SR); e = min(N, i + len(s)); fx[i:e] += s[:e - i]
    for k in range(1, len(du)):
        add("whoosh_grave", starts[k] - 0.23, 0.45); add("whoosh_2", starts[k] - 0.05, 0.3)
    if events: events(add, starts)
    mix = voz + m + fx; mix /= max(1.0, np.abs(mix).max() / 0.98)
    wavfile.write(f"{d}/mix.wav", SR, (mix * 32767).astype(np.int16))
    subprocess.run(f"ffmpeg -loglevel error -y -i {d}/mix.wav -af loudnorm=I=-14:TP=-1.5 -ar 44100 {d}/mixn.wav", shell=True, check=True)
def final(d, prefix, n, out):
    open(f"{d}/list.txt", "w").write("".join(f"file '{prefix}_{k:02d}.mp4'\n" for k in range(n)))
    subprocess.run(f"cd {d} && ffmpeg -loglevel error -y -f concat -safe 0 -i list.txt -c copy video.mp4 && ffmpeg -loglevel error -y -i video.mp4 -i mixn.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest {out}", shell=True, check=True)
