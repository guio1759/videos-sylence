import sys, json, subprocess
sys.path.insert(0, "/home/claude/work/hist")
from align2 import align
TEXTS = [
"O futebol de hoje é quase outro esporte. Olha como as regras foram mudando.",
"Mil oitocentos e sessenta e três. Nascem as regras: a bola, só com os pés.",
"Mil oitocentos e setenta e dois. Bola saiu pela linha de fundo? Escanteio.",
"Mil oitocentos e setenta e cinco. O gol ganha travessão. Antes, era uma fita.",
"Mil oitocentos e noventa e um. Nasce o pênalti: o chute da morte.",
"Mil novecentos e vinte e cinco. Impedimento: agora bastam dois adversários à frente. O ataque ganha espaço.",
"Mil novecentos e setenta. Copa do México: estreiam os cartões amarelo e vermelho.",
"Mil novecentos e noventa e dois. Recuo com o pé? O goleiro não pode mais pegar com a mão.",
"Dois mil e dezoito. O VAR chega na Copa. O lance agora é revisto no vídeo.",
"Dois mil e vinte e cinco. Goleiro segurou mais de oito segundos? Escanteio pro rival.",
"E qual vai ser a próxima? Comenta a regra que você mudaria.",
]
PADS = [0.5, 1.0, 1.4, 1.2, 1.4, 1.0, 1.2, 1.2, 1.4, 1.2, 2.6]
LEAD = 0.2
sc = []; t0 = 0
for k, tx in enumerate(TEXTS):
    p = f"narr/n{k}.wav"
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
    w = align(tx, p)
    dur = round(round((LEAD + d + PADS[k]) * 30) / 30, 4)
    sc.append({"start": round(t0, 4), "dur": dur, "words": [[a, b + LEAD, c + LEAD] for a, b, c in w]}); t0 += dur
json.dump(sc, open("scenes.json", "w"), ensure_ascii=False)
print("total", t0)
for s in sc: print(round(s["start"],2), s["dur"], " ".join(f"{w}@{a:.2f}" for w, a, b in s["words"]))
