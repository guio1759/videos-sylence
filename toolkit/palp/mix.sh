set -e
m=$1; narr=$2; out=$3
read cuts pops < <(WORDS=$m python3 -c "
import make_qua as M
T=M.T
if '$m'=='words_qua3':
    cuts=[T('cruzeiro')-0.3,T('flamengo')-0.35,T('corinthians')-0.35,T('grêmio')-0.35,T('coritiba')-0.25,T('se')-0.3,T('comenta')-0.25]
elif '$m'=='words_hist':
    cuts=[T('e')-0.2,T('em',1)-0.15,T('na',1)-0.2,T('na',2)-0.1,T('corinthians',2)-0.2,T('agora')-0.2,T('e',2)-0.1,T('a',4)-0.1]
elif '$m'=='words_qua2':
    cuts=[T('cruzeiro')-0.3,T('flamengo')-0.35,T('corinthians')-0.35,T('grêmio')-0.35,T('coritiba')-0.25,T('agora')-0.25,T('comenta')-0.25]
elif '$m'=='words_qui2':
    cuts=[T('são')-0.3,T('vasco')-0.35,T('vitória')-0.35,T('comenta')-0.25]
else:
    cuts=[T('rodada',i)-0.2 for i in range(3)]+[T('na')-0.2,T('campeão')-0.3,T('lá')-0.3,T('palmeiras',4)-0.2,T('comenta')-0.25]
from PIL import Image
pops=M.SCENE[M.WMOD.__name__](Image.new('RGBA',(M.W,M.H)),0)
print(','.join('%.2f'%c for c in cuts), ','.join('%.2f'%p for p in pops))")
WORDS=$m python3 aud.py $narr "$cuts" "$pops" trilha_$m.wav
ls chunks_$m/c0*.mp4 | sed "s/^/file '/;s/$/'/" > l_$m.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i l_$m.txt -i trilha_$m.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-1.5 -c:a aac -b:a 192k -shortest $out
ffprobe -v error -show_entries format=duration -of csv=p=0 $out
