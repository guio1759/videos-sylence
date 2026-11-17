"""Voz grátis do Google Cloud TTS (Chirp 3 HD).

Uso:
    python3 gvoz.py <voz> <texto.txt> <saida.wav> [velocidade]
    voz: Charon (vídeos longos) | Fenrir (Shorts) | qualquer pt-BR-Chirp3-HD-*

A chave NUNCA fica no repositório (ele é público). Ela vem de:
    variável GTTS_KEY  ou  arquivo ~/.secrets/gtts_key
Cota grátis: 1 milhão de caracteres/mês (Chirp 3 HD). Uso previsto ~200 mil.
"""
import base64, json, os, re, subprocess, sys, tempfile, urllib.request

URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
MAXB = 4200  # limite da API: 5000 bytes por pedido


def key():
    k = os.environ.get("GTTS_KEY")
    if not k:
        p = os.path.expanduser("~/.secrets/gtts_key")
        if os.path.exists(p):
            k = open(p).read().strip()
    if not k:
        sys.exit("Sem chave do Google TTS: defina GTTS_KEY ou ~/.secrets/gtts_key")
    return k


def chunks(text):
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    out, cur = [], ""
    for s in sents:
        cand = (cur + " " + s).strip()
        if len(cand.encode()) > MAXB and cur:
            out.append(cur)
            cur = s
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


def synth_chunk(text, voice, rate):
    name = voice if voice.startswith("pt-BR") else "pt-BR-Chirp3-HD-" + voice
    body = {
        "input": {"text": text},
        "voice": {"languageCode": "pt-BR", "name": name},
        "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 44100,
                        "speakingRate": rate},
    }
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "x-goog-api-key": key()})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return base64.b64decode(d["audioContent"])


def synth(text, voice="Charon", out="voz.wav", rate=1.0, gap=0.25):
    tmp = tempfile.mkdtemp()
    parts = []
    for i, c in enumerate(chunks(text)):
        p = os.path.join(tmp, f"{i:03d}.wav")
        open(p, "wb").write(synth_chunk(c, voice, rate))
        parts.append(p)
    lst = os.path.join(tmp, "l.txt")
    sil = os.path.join(tmp, "sil.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    "anullsrc=r=44100:cl=mono", "-t", str(gap), sil], check=True)
    with open(lst, "w") as f:
        for j, p in enumerate(parts):
            if j:
                f.write(f"file '{sil}'\n")
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-ar", "44100", "-ac", "1", out], check=True)
    return out


if __name__ == "__main__":
    v, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rate = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    synth(open(src).read(), v, out, rate)
    print(out)
