import numpy as np, wave, subprocess, json, re, unicodedata
SR=24000
exec(open('/home/claude/ep1/v2/voice.py').read().split('parts = []')[0].split('from script2')[0])
def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
import importlib.util, sys
src=open('/home/claude/ep1/v2/voice.py').read()
ns={}; exec(src.split('parts = []')[0].replace('from script2 import BLOCKS',''), ns)
a = ns['squeeze'](load('raw.wav'))
w = wave.open('slow.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes()); w.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','slow.wav','-af','atempo=1.1','-ar','44100','narr.wav'],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','narr.wav','-ar','16000','-ac','1','n16.wav'],check=True)
from faster_whisper import WhisperModel
w=wave.open('n16.wav'); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
m=WhisperModel('small',device='cpu',compute_type='int8')
segs,_=m.transcribe(x,language='pt',word_timestamps=True,initial_prompt='Palmeiras, Flamengo, Cruzeiro, Verdão')
W=[{"w":wd.word.strip(),"t0":round(wd.start,3),"t1":round(wd.end,3)} for s in segs for wd in s.words]
json.dump({"words":W,"total":round(len(x)/16000+0.3,2)},open('words.json','w'),ensure_ascii=False)
print(len(x)/16000); print(' '.join(f"{w['w']}@{w['t0']}" for w in W))
