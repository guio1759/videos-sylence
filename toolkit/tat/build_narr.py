import json, numpy as np
from scipy.io import wavfile
D = "/tmp/claude-tool-results/b5e2005c-0934-5f8b-951e-f5e00d1575ae/mcp-Speko-blob-"
RAW = ["1794841628043-681ul5-f88989d8", "1794841668009-zjqqcd-06951fd3", "1794841804376-r5t6yj-7805a08a", "1794841639391-zqf7ix-759f16a0",
       "1794841782641-uc3q4i-25dec9e9", "1794841644306-z80m4m-62a7abb4", "1794841646407-am9lqz-1de24f07", "1794841648234-sa7i88-5678685f",
       "1794841650609-oup3mr-426ca4b7", "1794841653186-bkoj1q-bf08905c", "1794841655590-0uc03a-bd1872c5"]
W = [
 [("O",100),("futebol",100),("de",600),("hoje",700),("é",1000),("quase",1100),("outro",1400),("esporte.",1600),("Olha",3200),("como",3400),("as",3600),("regras",3700),("foram",4100),("mudando.",4300)],
 [("1863.",100),("Nascem",4700),("as",5400),("regras.",5600),("A",6300),("bola,",6400),("só",7400),("com",7600),("os",7800),("pés.",8000)],
 [("Ano",100),("de",400),("1872.",500),("Bola",2200),("saiu",2600),("pela",3100),("linha",3400),("de",3600),("fundo?",3700),("Escanteio.",5900)],
 [("1875.",100),("O",2600),("gol",2600),("ganha",3600),("travessão.",3800),("Antes,",5100),("era",5600),("uma",5800),("fita.",5900)],
 [("1891.",100),("Nasce",1800),("o",2100),("pênalti:",2100),("o",2700),("chute",2800),("da",3200),("morte.",3300)],
 [("1925.",100),("Impedimento:",2200),("agora",2800),("bastam",3100),("dois",3600),("adversários",4000),("à",4600),("frente.",4700),("O",5800),("ataque",5900),("ganha",6300),("espaço.",6500)],
 [("1970.",100),("Copa",2900),("do",3200),("México:",3300),("estreiam",4100),("os",4600),("cartões",4700),("amarelo",5200),("e",5600),("vermelho.",5700)],
 [("1992.",100),("Recuo",1700),("com",1900),("o",1950),("pé?",2000),("O",4000),("goleiro",4000),("não",4400),("pode",4450),("mais",4700),("pegar",4900),("com",5200),("a",5300),("mão.",5300)],
 [("2018.",100),("O",1400),("VAR",1500),("chega",1800),("na",2000),("Copa.",2100),("O",3100),("lance",3200),("agora",3600),("é",4600),("revisto",4600),("no",5700),("vídeo.",5900)],
 [("2025.",100),("Goleiro",2400),("segurou",3400),("mais",4000),("de",4300),("oito",4400),("segundos?",4600),("Escanteio",6400),("pro",7100),("rival.",7200)],
 [("E",100),("qual",200),("vai",300),("ser",400),("a",600),("próxima?",600),("Comenta",1100),("a",1500),("regra",1600),("que",1900),("você",2000),("mudaria.",2600)],
]
SR = None; out = []
for k, (r, words) in enumerate(zip(RAW, W)):
    sr, x = wavfile.read(D + r + ".wav"); x = x.astype(np.float32)
    if x.ndim > 1: x = x.mean(1)
    hop = int(sr * 0.01); n = len(x) // hop
    e = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
    thr = e.max() * 0.03; on = e > thr
    first = np.argmax(on); last = n - np.argmax(on[::-1])
    # build keep mask: compress silent runs > 30 frames to 30 frames (0.30 s)
    keep = np.zeros(n, bool); keep[first:last] = True
    i = first
    while i < last:
        if not on[i]:
            j = i
            while j < last and not on[j]: j += 1
            if j - i > 30:
                keep[i + 15:j - 15] = False
            i = j
        else: i += 1
    tmap = np.cumsum(keep) * 0.01   # output time at end of frame i
    y = np.concatenate([x[i * hop:(i + 1) * hop] for i in range(n) if keep[i]])
    wavfile.write(f"narr/n{k}.wav", sr, y.astype(np.int16) if y.dtype != np.int16 else y)
    def m(ms):
        f = min(n - 1, max(0, int(ms / 10))); return float(tmap[f])
    ws = []
    for i, (w, st) in enumerate(words):
        en = words[i + 1][1] if i + 1 < len(words) else last * 10
        a = m(max(st, first * 10)); b = max(a + 0.08, m(en))
        ws.append([w, round(a, 3), round(b, 3)])
    out.append({"dur": len(y) / sr, "words": ws})
json.dump(out, open("narr_words.json", "w"), ensure_ascii=False)
for o in out: print(round(o["dur"], 2), " ".join(f"{w}@{a:.2f}" for w, a, b in o["words"]))
