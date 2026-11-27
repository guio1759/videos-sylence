import json, urllib.parse, urllib.request, time, sys
UA = "VideosSylence/1.0 (https://github.com/guio1759/videos-sylence) python-urllib"
def get(url):
    for k in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(15 * (k + 1)); continue
            raise
def search(q, n=8):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": n})
    return [r["title"] for r in json.loads(get(u))["query"]["search"]]
def info(title, w=600):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": w})
    p = list(json.loads(get(u))["query"]["pages"].values())[0]["imageinfo"][0]; m = p["extmetadata"]
    return p.get("thumburl") or p["url"], m.get("LicenseShortName", {}).get("value", ""), m.get("Artist", {}).get("value", "")[:80]
if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("==", q)
        for t in search(q): print("  ", t)
        time.sleep(1)
