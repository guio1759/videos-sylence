"""Dados oficiais grátis: football-data.org (plano free: Brasileirão BSA, Libertadores CLI, Champions CL, Premier PL, Copa WC...).
Chave em ~/.secrets/football_key (o setup.sh grava a partir de FOOTBALL_KEY). Limite: 10 pedidos/min. NUNCA pôr a chave no repo.
Uso:
    python3 futdata.py tabela BSA          # classificação
    python3 futdata.py jogos CLI [STATUS]  # jogos (SCHEDULED, FINISHED...)
    python3 futdata.py artilheiros BSA
Use para CONFERIR placar, tabela e artilharia antes de cada vídeo (a pesquisa na web continua para notícias e contexto).
"""
import json, os, sys, urllib.request
def _get(path):
    k = os.environ.get("FOOTBALL_KEY") or open(os.path.expanduser("~/.secrets/football_key")).read().strip()
    req = urllib.request.Request("https://api.football-data.org/v4/" + path, headers={"X-Auth-Token": k})
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)
def tabela(c="BSA"):
    d = _get(f"competitions/{c}/standings"); return [(r["position"], r["team"]["shortName"], r["points"], r["playedGames"], r["won"], r["draw"], r["lost"], r["goalDifference"], r.get("form")) for r in d["standings"][0]["table"]]
def jogos(c="BSA", status=None):
    d = _get(f"competitions/{c}/matches" + (f"?status={status}" if status else ""))
    return [(m["utcDate"], m["matchday"], m["stage"], (m["homeTeam"] or {}).get("shortName"), (m["awayTeam"] or {}).get("shortName"), m["score"]["fullTime"]["home"], m["score"]["fullTime"]["away"], m["status"]) for m in d["matches"]]
def artilheiros(c="BSA", n=10):
    d = _get(f"competitions/{c}/scorers?limit={n}"); return [(s["player"]["name"], s["team"]["shortName"], s["goals"], s.get("assists")) for s in d["scorers"]]
if __name__ == "__main__":
    cmd, c = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "BSA"
    r = {"tabela": lambda: tabela(c), "jogos": lambda: jogos(c, sys.argv[3] if len(sys.argv) > 3 else None), "artilheiros": lambda: artilheiros(c)}[cmd]()
    for x in r: print(*x, sep=" | ")
