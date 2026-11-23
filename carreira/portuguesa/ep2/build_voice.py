import sys, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0,'/home/claude/sex20'); from voz import squeeze, SR
from script import S
import re
S=[re.sub(r'\[[a-z ]+\] ?','',x) for x in S]
parts, segs, t = [], [], 0.0
for k in range(len(S)):
    subprocess.run(f"ffmpeg -loglevel error -y -i raw_{k}.wav -ac 1 -ar {SR} /tmp/r.wav", shell=True, check=True)
    a,_ = sf.read('/tmp/r.wav', dtype='float32'); a = squeeze(a, maxgap=0.22, keep=0.16)
    sf.write('/tmp/s.wav', a, SR)
    subprocess.run(f"ffmpeg -loglevel error -y -i /tmp/s.wav -af atempo=1.1 -ar {SR} /tmp/st.wav", shell=True, check=True)
    b,_ = sf.read('/tmp/st.wav', dtype='float32'); gap = 0.15
    segs.append((round(t,3), round(t+len(b)/SR,3))); parts += [b, np.zeros(int(gap*SR),np.float32)]; t += len(b)/SR + gap
a = np.concatenate(parts); sf.write('raw.wav', a/np.abs(a).max()*0.9, SR)
subprocess.run("ffmpeg -loglevel error -y -i raw.wav -af 'highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80' -ar 44100 narr.wav", shell=True, check=True)
subprocess.run("ffmpeg -loglevel error -y -i narr.wav -ar 16000 -ac 1 /tmp/n16.wav", shell=True, check=True)
from faster_whisper import WhisperModel
x,_ = sf.read('/tmp/n16.wav', dtype='float32')
m = WhisperModel('small', device='cpu', compute_type='int8')
sg,_ = m.transcribe(x, language='pt', word_timestamps=True, initial_prompt="Portuguesa, Série D, Libertadores, Thiago Tee, Canindé, Jonas Toró, Cadorini, Romarinho, Levi Santos, SAF, Benny, Cauari, Davi, Diadema, Paulistão")
W = [{"w": w.word.strip(), "t0": round(w.start,3), "t1": round(w.end,3)} for s in sg for w in s.words]
json.dump({"words": W, "segs": segs, "total": round(t+0.8,2)}, open('words.json','w'), ensure_ascii=False)
print(round(t,2)); print(segs); print(' '.join(w['w'] for w in W))
