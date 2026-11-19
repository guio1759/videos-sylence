"""Edição de LANCES REAIS (clipes que o usuário manda) em vídeo vertical 1080x1920.

Uso: python3 clipedit.py spec.json saida.mp4
spec.json:
{
 "topic": "GOLAÇO DO MEIO-CAMPO",            # etiqueta no topo
 "music": "/caminho/musica.mp3" ou null,      # música do usuário (ou Kevin MacLeod); "music_off": segundos
 "narr": "/caminho/narr.wav" ou null,         # narração (voz Google/Pedro); "words": words.json para legenda
 "clips": [                                   # trechos em ordem
   {"src": "lance.mp4", "t0": 3.0, "t1": 7.5, "speed": 1.0, "zoom": 1.0, "cx": 0.5, "cy": 0.5,
    "freeze": [{"at": 5.2, "dur": 1.2, "draw": [
        {"type": "circle", "x": 0.62, "y": 0.48, "r": 0.06, "color": "amber"},
        {"type": "arrow", "from": [0.62, 0.48], "to": [0.85, 0.40], "color": "amber"},
        {"type": "text", "x": 0.5, "y": 0.2, "s": "OLHA O ESPAÇO!", "size": 90}]}],
    "label": "1º TEMPO • 17'"}
 ],
 "scoreboard": {"home": "PAL", "away": "FLA", "score": "1 x 0"}   # opcional (escudos de /home/claude/work/logos)
}
Layout: lance 16:9 em cima de um fundo com o próprio vídeo desfocado (preenche o 9:16); zoom/cx/cy para dar close.
Coordenadas de desenho normalizadas (0–1) em relação ao QUADRO ORIGINAL do clipe. "ar": proporção do recorte (ex.: 1.33 deixa o lance maior na tela; cx/cy escolhem o centro).
"""
import sys, json, subprocess, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, "/home/claude/ep1/v2")
from gfx import font, chip, tag_box, paste, text_el, AMB, WHITE, RED, GREEN, INK, back

W, H, FPS = 1080, 1920, 30
COL = {"amber": AMB, "white": WHITE, "red": RED, "green": GREEN}

def probe(src):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
    return int(o[0]), int(o[1])

def frames(src, t0, t1, w, h):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-to", str(t1), "-i", src, "-r", str(FPS), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield Image.frombuffer("RGB", (w, h), b)

def keyed(c, key, lt, default):
    ks = c.get(key + "_keys")
    if not ks: return c.get(key, default)
    if lt <= ks[0][0]: return ks[0][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if lt <= t1: u = (lt - t0) / max(1e-6, t1 - t0); u = u * u * (3 - 2 * u); return v0 + (v1 - v0) * u
    return ks[-1][1]

def compose(fr, c, draw=None, u=1.0, lt=0.0):
    # FULL (padrão do canal): "ar": 0.5625 → o lance ocupa a tela inteira 9:16; cx_keys/zoom_keys seguem a bola
    z = keyed(c, "zoom", lt, 1.0); cx, cy = keyed(c, "cx", lt, 0.5), c.get("cy", 0.5)
    fw, fh = fr.size; ch = fh / z; cw = min(fw / z, ch * c["ar"]) if c.get("ar") else fw / z
    x0 = min(max(0, cx * fw - cw / 2), fw - cw); y0 = min(max(0, cy * fh - ch / 2), fh - ch)
    crop = fr.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    main_h = min(H, int(W * ch / cw))
    main = crop.resize((W, main_h), Image.LANCZOS)
    bgi = fr.resize((int(H * fw / fh), H)).crop((0, 0, W, H)) if fw / fh > W / H else fr.resize((W, int(W * fh / fw)))
    bgi = bgi.resize((W, H)).filter(ImageFilter.GaussianBlur(28))
    img = bgi.convert("RGBA"); img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
    top = (H - main_h) // 2 - 80
    if main_h >= H - 10: main = crop.resize((W, H), Image.LANCZOS); main_h = H; top = 0
    img.alpha_composite(main.convert("RGBA"), (0, top))
    if draw:
        d = ImageDraw.Draw(img)
        for it in draw:
            col = COL.get(it.get("color", "amber"), AMB)
            P = lambda x, y: ((x * fw - x0) / cw * W, top + (y * fh - y0) / ch * main_h)  # coords do QUADRO ORIGINAL (0–1)
            if it["type"] == "circle":
                x, y = P(it["x"], it["y"]); r = it.get("r", 0.05) * W * (0.6 + 0.4 * back(min(1, u * 3)))
                d.ellipse((x - r, y - r * 0.6, x + r, y + r * 0.6), outline=col, width=10)
            elif it["type"] == "arrow":
                (a, b), (e, f) = P(*it["from"]), P(*it["to"]); k = min(1, u * 2.5); e, f = a + (e - a) * k, b + (f - b) * k
                d.line((a, b, e, f), fill=col, width=14); ang = math.atan2(f - b, e - a)
                d.polygon([(e + 34 * math.cos(ang), f + 34 * math.sin(ang)), (e + 26 * math.cos(ang + 2.3), f + 26 * math.sin(ang + 2.3)), (e + 26 * math.cos(ang - 2.3), f + 26 * math.sin(ang - 2.3))], fill=col)
            elif it["type"] == "line":
                (a, b), (e, f) = P(*it["from"]), P(*it["to"]); d.line((a, b, e, f), fill=col, width=8)
            elif it["type"] == "text":
                paste(img, text_el(it["s"], font("blk", it.get("size", 80)), col if it.get("color") else WHITE, 8), W / 2, it["y"] * H if it.get("abs") else top - 70 if it["y"] < 0.5 else top + main_h + 80, 1, 0.8 + 0.2 * back(min(1, u * 3)))
    return img, top, main_h

def main(spec, out):
    S = json.load(open(spec)); tmp = out + ".v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    T = 0.0; cuts = []
    logos = {}
    def logo(k):
        if k not in logos:
            im = Image.open(f"/home/claude/work/logos/{k}.png").convert("RGBA"); im = im.crop(im.getchannel("A").getbbox()); im.thumbnail((110, 110)); logos[k] = im
        return logos[k]
    def hud(img, c, lt):
        paste(img, tag_box(S.get("topic", ""), 44, WHITE, INK), W / 2, 150, 1)
        sb = S.get("scoreboard")
        if sb:
            paste(img, logo(sb["home"]), W / 2 - 170, 250, 1); paste(img, text_el(sb["score"], font("blk", 70), WHITE, 6), W / 2, 290, 1); paste(img, logo(sb["away"]), W / 2 + 170, 290, 1)
        if c.get("label"): paste(img, chip(c["label"], 40, INK, AMB), W / 2, H - 420, 1)
        for tx in c.get("texts", []):
            if tx["at"] <= lt <= tx.get("to", 1e9):
                u = min(1, (lt - tx["at"]) / 0.2)
                el = chip(tx["s"], tx.get("size", 70), INK, COL.get(tx.get("color", "amber"), AMB)) if tx.get("chip") else text_el(tx["s"], font("blk", tx.get("size", 90)), COL.get(tx.get("color", "white"), WHITE), 9)
                paste(img, el, W / 2, tx.get("y", 0.25) * H, 1, 0.7 + 0.3 * back(u), tx.get("rot", 0))
    WORDS = json.load(open(S["words"]))["words"] if S.get("words") else []
    SKIP = {"o", "a", "e", "de", "da", "do", "no", "na", "os", "as", "em", "se", "um", "uma", "que", "pra", "com"}
    def cap(img, TT):
        cur = None
        for wd in WORDS:
            if wd["t0"] - 0.03 <= TT < wd["t1"] + 0.12 and wd["w"].lower().strip(".,!?") not in SKIP: cur = wd
        if cur:
            s_ = cur["w"].upper().strip(".,!?…")
            if s_: paste(img, chip(s_, 88, INK, AMB if (len(s_) > 7 or any(ch.isdigit() for ch in s_)) else WHITE, "blk", 0.5, 0.25), W / 2, H * 0.80, 1, 0.8 + 0.2 * back(min(1, (TT - cur["t0"]) / 0.15)))
    for c in S["clips"]:
        w, h = probe(c["src"]); sp = c.get("speed", 1.0); cuts.append(T)
        fz = sorted(c.get("freeze", []), key=lambda f: f["at"])
        t = c["t0"]; step = sp / FPS; acc = 0.0
        for fr in frames(c["src"], c["t0"], c["t1"], w, h):
            # câmera lenta: repete quadros
            acc += 1 / sp
            while acc >= 1:
                acc -= 1
                img, _, _ = compose(fr, c, lt=t); hud(img, c, t); cap(img, T); enc.stdin.write(img.convert("RGB").tobytes()); T += 1 / FPS
            for f in list(fz):
                if t >= f["at"]:
                    n = int(f.get("dur", 1.0) * FPS); cuts.append(T)
                    for k in range(n):
                        img, _, _ = compose(fr, c, f.get("draw"), k / max(1, n - 1), lt=t)
                        if k < 4: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 120 - 30 * k)))
                        hud(img, c, t); cap(img, T); enc.stdin.write(img.convert("RGB").tobytes()); T += 1 / FPS
                    fz.remove(f)
            t += 1 / FPS
    enc.stdin.close(); enc.wait()
    # áudio: narração + música (ducking) + whoosh nos cortes
    dur = T; a = [f"-f lavfi -t {dur} -i anullsrc=r=44100:cl=stereo"]; filt = []; mix = ["[1:a]"]
    idx = 2
    if S.get("music"):
        a.append(f"-ss {S.get('music_off', 0)} -t {dur} -i '{S['music']}'"); filt.append(f"[{idx}:a]volume={S.get('music_vol', 0.35 if S.get('narr') else 0.9)},afade=t=out:st={max(0, dur - 0.8)}:d=0.8[m]"); mix.append("[m]"); idx += 1
    if S.get("narr"):
        a.append(f"-i '{S['narr']}'"); filt.append(f"[{idx}:a]volume=1.0[n]"); mix.append("[n]"); idx += 1
    if S.get("narr") and S.get("music"):
        filt.append("[m][n]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md]"); mix = ["[1:a]", "[md]", "[n]"]
        filt[-1] = filt[-1]; 
    for k, (name, at, g) in enumerate(S.get("sfx", [])):
        a.append(f"-i /home/claude/work/sfx/{name}.wav"); filt.append(f"[{idx}:a]volume={g},adelay={int(at*1000)}|{int(at*1000)}[s{k}]"); mix.append(f"[s{k}]"); idx += 1
    filt.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
    cmd = f"ffmpeg -y -loglevel error -i {tmp} {' '.join(a)} -filter_complex \"{';'.join(filt)}\" -map 0:v -map [a] -c:v copy -c:a aac -b:a 192k -shortest {out}"
    if S.get("narr") and S.get("music"):
        cmd = cmd.replace("[n]sidechain", "[nsc]sidechain").replace("volume=1.0[n]", "volume=1.0,asplit=2[n][nsc]")
    subprocess.run(cmd, shell=True, check=True); os.remove(tmp)
    print(out, round(dur, 2), "s")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
