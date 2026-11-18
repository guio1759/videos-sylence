"""Voz Google Sadaltager por frase -> narr.wav + segs.json + words.json"""
import sys, json, subprocess, numpy as np, soundfile as sf, importlib.util
sys.path.insert(0, '/home/claude/videos-sylence/toolkit/common'); import gvoz
SR = 24000
def squeeze(a, maxgap=0.22, keep=0.16, thr=0.012):
    win = int(0.02 * SR); env = np.sqrt(np.convolve(a * a, np.ones(win) / win, "same")); q = env < thr
    nz = np.where(~q)[0]; s0, s1 = max(0, nz[0] - int(0.04 * SR)), nz[-1] + int(0.06 * SR); a, q = a[s0:s1], q[s0:s1]
    out = []; i = 0; n = len(a)
    while i < n:
        j = i
        while j < n and q[j] == q[i]: j += 1
        if q[i] and j - i > maxgap * SR: out += [a[i:i + int(keep * SR / 2)], a[j - int(keep * SR / 2):j]]
        else: out.append(a[i:j])
        i = j
    return np.concatenate(out)
def build(d, sents, tempo=1.1, voice="Sadaltager"):
    parts, segs, t = [], [], 0.0
    for i, (txt, rate, gap) in enumerate(sents):
        open('/tmp/g.wav', 'wb').write(gvoz.synth_chunk(txt, voice, rate))
        subprocess.run(f"ffmpeg -loglevel error -y -i /tmp/g.wav -ac 1 -ar {SR} /tmp/g24.wav", shell=True, check=True)
        a, _ = sf.read('/tmp/g24.wav', dtype='float32'); a = squeeze(a)
        sf.write('/tmp/s.wav', a, SR)
        subprocess.run(f"ffmpeg -loglevel error -y -i /tmp/s.wav -af atempo={tempo} -ar {SR} /tmp/st.wav", shell=True, check=True)
        b, _ = sf.read('/tmp/st.wav', dtype='float32')
        segs.append((round(t, 3), round(t + len(b) / SR, 3))); parts += [b, np.zeros(int(gap * SR), np.float32)]; t += len(b) / SR + gap
    a = np.concatenate(parts); sf.write(f'{d}/raw.wav', a / np.abs(a).max() * 0.9, SR)
    subprocess.run(f"ffmpeg -loglevel error -y -i {d}/raw.wav -af 'highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=3,equalizer=f=150:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3:attack=5:release=80' -ar 44100 {d}/narr.wav", shell=True, check=True)
    subprocess.run(f"ffmpeg -loglevel error -y -i {d}/narr.wav -ar 16000 -ac 1 /tmp/n16.wav", shell=True, check=True)
    from faster_whisper import WhisperModel
    x, _ = sf.read('/tmp/n16.wav', dtype='float32')
    m = WhisperModel('small', device='cpu', compute_type='int8')
    sg, _ = m.transcribe(x, language='pt', word_timestamps=True, initial_prompt=sents[0][0][:200])
    W = [{"w": w.word.strip(), "t0": round(w.start, 3), "t1": round(w.end, 3)} for s in sg for w in s.words]
    json.dump({"words": W, "segs": segs, "total": round(t + 0.6, 2)}, open(f'{d}/words.json', 'w'), ensure_ascii=False)
    print(d, round(t, 2), "s"); print(' '.join(w['w'] for w in W))
