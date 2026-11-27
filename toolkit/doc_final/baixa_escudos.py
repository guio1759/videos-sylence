import json, time, sys, io
from escudos import info, get, search
from PIL import Image
L = [("PEN", "File:Escudo Peñarol 1962.png"), ("BOC", "File:Escudo del Club Atlético Boca Juniors 2012.svg"), ("CAL", "File:Escudo del Deportivo Cali.svg"),
     ("CER", "File:Escudo Club Cerro Porteño 2023-Actual.svg"), ("LDU", "File:Liga Deportiva Universitaria de Quito.png"),
     ("TACA", "File:TaçaLibertadores2024.jpg"), ("TACA2", "File:Troféu Copa Libertadores de 2019 CR Flamengo.jpg"), ("CENT30", "File:Estadio Centenario 1930.jpg")]
cred = {}
try: cred = json.load(open("escudos/creditos.json"))
except Exception: pass
for k, t in L:
    if k in cred: continue
    try:
        url, lic, art = info(t, 700); data = get(url)
        im = Image.open(io.BytesIO(data)); ext = "png" if k not in ("TACA", "TACA2", "CENT30") else "jpg"
        (im.convert("RGBA") if ext == "png" else im.convert("RGB")).save(f"escudos/{k}.{ext}")
        cred[k] = {"file": t, "lic": lic, "artist": art}; print(k, lic, im.size)
    except Exception as e: print("falhou", k, e)
    json.dump(cred, open("escudos/creditos.json", "w"), ensure_ascii=False, indent=1); time.sleep(6)
for q in ["Club Deportivo Universidad Católica", "Escudo Peñarol"]:
    try: print(q, search(q, 10))
    except Exception as e: print("busca falhou", q, e)
    time.sleep(6)
