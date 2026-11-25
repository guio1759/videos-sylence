"""Fotos REAIS com licença livre (Wikimedia Commons, via busca do Openverse): estádios, jogadores, técnicos, torcidas, troféus.
Só licenças que permitem uso comercial (CC0, CC BY, CC BY-SA). O CRÉDITO é obrigatório e vai PEQUENO NA TELA enquanto a foto aparece
("Foto: <autor> / Wikimedia Commons, CC BY-SA 4.0") — nunca na legenda do post. NUNCA usar foto de agência/clube/TV (Getty, Globo, sites de clubes).

Uso:
    python3 fotos_cc.py "Flaco Lopez Palmeiras" pasta [n]      -> baixa n fotos (1280 px) + pasta/creditos.json
    import fotos_cc; fotos = fotos_cc.buscar("Estadio Centenario Montevideo", "pasta", 3)  # [{"file","title","credit","w","h"}]
Wikimedia exige User-Agent identificado e tamanhos padrão de miniatura (1280); respeite as pausas (erro 429 = esperar).
"""
import json, os, sys, time, urllib.parse, urllib.request

UA = "VideosSylence/1.0 (https://github.com/guio1759/videos-sylence) python-urllib"
LIC = {"cc0": "CC0", "pdm": "Domínio público", "by": "CC BY", "by-sa": "CC BY-SA"}


def _get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and k < tries - 1: time.sleep(15 * (k + 1)); continue
            raise


def _thumb(url, width=1280):
    # https://upload.wikimedia.org/wikipedia/commons/a/ab/Nome.jpg -> .../commons/thumb/a/ab/Nome.jpg/1280px-Nome.jpg
    if "/wikipedia/commons/" not in url or "/thumb/" in url: return url
    pre, rest = url.split("/wikipedia/commons/", 1); name = rest.split("/")[-1]
    return f"{pre}/wikipedia/commons/thumb/{rest}/{width}px-{name}"


def buscar(q, pasta, n=3, min_w=900, retrato=None):
    os.makedirs(pasta, exist_ok=True)
    api = f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(q)}&license_type=commercial&source=wikimedia&page_size=20"
    res = json.loads(_get(api)).get("results", []); out = []
    credf = os.path.join(pasta, "creditos.json"); creds = json.load(open(credf)) if os.path.exists(credf) else {}
    for r in res:
        if len(out) >= n: break
        w, h = r.get("width") or 0, r.get("height") or 0
        if w < min_w and h < min_w: continue
        if retrato is True and h < w: continue
        if retrato is False and w < h: continue
        fn = os.path.join(pasta, "cc_" + r["id"][:8] + ".jpg")
        if not os.path.exists(fn):
            try: data = _get(_thumb(r["url"]) if max(w, h) > 1280 else r["url"])
            except Exception as e: print("falhou", r["title"], e); continue
            open(fn, "wb").write(data); time.sleep(2)
        lic = LIC.get(r["license"], r["license"].upper()) + (" " + r["license_version"] if r.get("license_version") and r["license"] not in ("cc0", "pdm") else "")
        cr = f"Foto: {(r.get('creator') or 'autor desconhecido').strip()[:40]} / Wikimedia Commons, {lic}"
        item = {"file": fn, "title": r["title"], "credit": cr, "page": r.get("foreign_landing_url"), "w": w, "h": h}
        creds[os.path.basename(fn)] = item; out.append(item)
    json.dump(creds, open(credf, "w"), ensure_ascii=False, indent=1)
    return out


def credito(path):
    d = json.load(open(os.path.join(os.path.dirname(path), "creditos.json")))
    return d.get(os.path.basename(path), {}).get("credit", "")


if __name__ == "__main__":
    for it in buscar(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3):
        print(it["file"], "|", it["title"], "|", it["credit"])
