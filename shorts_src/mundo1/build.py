import sys, json, subprocess, numpy as np, soundfile as sf, difflib
sys.path.insert(0,'/home/claude/mundo'); from voz import squeeze, SR
from scripts import MUNDO
from engine import norm
d='/home/claude/mundo/m'; parts=[]
for i in range(5):
    subprocess.run(f"ffmpeg -loglevel error -y -i wav/c{i}.wav -ac 1 -ar {SR} /tmp/c.wav", shell=True, check=True)
    a,_=sf.read('/tmp/c.wav',dtype='float32'); a=squeeze(a,maxgap=0.55,keep=0.42); parts+=[a,np.zeros(int(0.35*SR),np.float32)]
a=np.concatenate(parts); sf.write('/tmp/s.wav',a,SR)
subprocess.run(f"ffmpeg -loglevel error -y -i /tmp/s.wav -af atempo=1.06 -ar {SR} {d}/raw.wav", shell=True, check=True)
subprocess.run(f"ffmpeg -loglevel error -y -i {d}/raw.wav -af 'highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-18dB:ratio=3:attack=5:release=80' -ar 44100 {d}/narr.wav", shell=True, check=True)
subprocess.run(f"ffmpeg -loglevel error -y -i {d}/narr.wav -ar 16000 -ac 1 /tmp/n16.wav", shell=True, check=True)
from faster_whisper import WhisperModel
x,_=sf.read('/tmp/n16.wav',dtype='float32'); tot=len(x)/16000
m=WhisperModel('small',device='cpu',compute_type='int8')
sg,_=m.transcribe(x,language='pt',word_timestamps=True,initial_prompt=MUNDO[0])
Wd=[{"w":w.word.strip(),"t0":round(w.start,3),"t1":round(w.end,3)} for s in sg for w in s.words]
sw=[]; own=[]
for i,s in enumerate(MUNDO):
    for w in s.split(): sw.append(norm(w)); own.append(i)
b=[norm(w['w']) for w in Wd]; tm={}
for bl in difflib.SequenceMatcher(None,sw,b,autojunk=False).get_matching_blocks():
    for k in range(bl.size): tm[bl.a+k]=Wd[bl.b+k]
segs=[]
for i in range(len(MUNDO)):
    ks=[k for k in range(len(sw)) if own[k]==i and k in tm]
    segs.append([tm[ks[0]]['t0'] if ks else None, tm[ks[-1]]['t1'] if ks else None])
for i in range(len(segs)):
    if segs[i][0] is None: segs[i][0]=segs[i-1][1]+0.05
    if segs[i][1] is None: segs[i][1]=segs[i+1][0]-0.05 if i+1<len(segs) and segs[i+1][0] else segs[i][0]+2
segs[0][0]=0.0
json.dump({"words":Wd,"segs":segs,"total":round(tot+0.8,2)},open(f'{d}/words.json','w'),ensure_ascii=False)
print(round(tot,2)); print(segs); print(' '.join(w['w'] for w in Wd))
