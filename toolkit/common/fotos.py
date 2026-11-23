"""Busca fotos livres para os vídeos (estádios, torcida, bola, cidades). NUNCA fotos de jogadores/pessoas reais.
Uso: python3 fotos.py "football stadium night" saida_prefixo [n]
Fonte 1: Pixabay (chave em ~/.secrets/pixabay_key ou env PIXABAY_KEY; licença Pixabay, sem crédito obrigatório).
Fonte 2 (sem chave): Openverse (CC; guarda o crédito em <prefixo>_creditos.txt para pôr pequeno na tela)."""
import json, os, sys, urllib.parse, urllib.request
def _key():
    k = os.environ.get("PIXABAY_KEY"); p = os.path.expanduser("~/.secrets/pixabay_key")
    return k or (open(p).read().strip() if os.path.exists(p) else None)
def _get(url, out=None):
    req = urllib.request.Request(url, headers={"User-Agent": "videos-sylence/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if out: open(out, "wb").write(data)
    return data
def buscar(q, prefixo, n=4):
    outs, cred = [], []
    k = _key()
    if k:
        d = json.loads(_get(f"https://pixabay.com/api/?key={k}&q={urllib.parse.quote(q)}&image_type=photo&orientation=vertical&safesearch=true&per_page={max(3, n)}"))
        for i, h in enumerate(d.get("hits", [])[:n]):
            o = f"{prefixo}_{i}.jpg"; _get(h["largeImageURL"], o); outs.append(o); cred.append(f"{o}: Pixabay ({h['pageURL']})")
    if len(outs) < n:
        d = json.loads(_get(f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(q)}&license_type=commercial&page_size={n}"))
        for i, h in enumerate(d.get("results", [])[: n - len(outs)]):
            o = f"{prefixo}_ov{i}.jpg"
            try: _get(h["url"], o); outs.append(o); cred.append(f"{o}: {h.get('title','')} – {h.get('creator','')} – {h.get('license','').upper()} {h.get('license_version','')}")
            except Exception as e: print("falhou", h.get("url"), e)
    open(f"{prefixo}_creditos.txt", "w").write("\n".join(cred))
    return outs
if __name__ == "__main__":
    print(buscar(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 4))
