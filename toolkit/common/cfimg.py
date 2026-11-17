"""Imagens grátis via Cloudflare Workers AI (FLUX schnell, ~170 imagens/dia na cota grátis).

Uso: python3 cfimg.py "prompt" saida.jpg [steps]
Chaves NUNCA no repo: CF_ACCOUNT / CF_TOKEN no ambiente ou ~/.secrets/cf_account e ~/.secrets/cf_token.
Estilo padrão dos personagens da série Modo Carreira: veja STYLE.
"""
import base64, json, os, sys, urllib.request

STYLE = ("Stylized 3D Pixar-like cartoon character portrait, chest-up, facing camera, adult proportions, "
         "soft studio lighting, plain dark charcoal background, no text, no logos. ")


def _get(env, f):
    v = os.environ.get(env)
    if not v and os.path.exists(os.path.expanduser(f)):
        v = open(os.path.expanduser(f)).read().strip()
    if not v:
        sys.exit(f"falta {env}")
    return v


def gen(prompt, out, steps=6, style=True):
    acc = _get("CF_ACCOUNT", "~/.secrets/cf_account")
    tok = _get("CF_TOKEN", "~/.secrets/cf_token")
    url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    body = json.dumps({"prompt": (STYLE if style else "") + prompt, "steps": steps}).encode()
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {tok}",
                                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    open(out, "wb").write(base64.b64decode(d["result"]["image"]))
    return out


if __name__ == "__main__":
    gen(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6)
    print(sys.argv[2])
