#!/bin/bash
# Restaura o ambiente de trabalho numa sessao nova. Rodar de dentro do clone do repo (branch videos).
R=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p /home/claude/work/logos /home/claude/work/sfx
cp -r "$R"/toolkit/* /home/claude/work/
cp "$R"/assets/logos/*.png "$R"/assets/logos/*.webp /home/claude/work/logos/ 2>/dev/null
cp "$R"/assets/sfx/* /home/claude/work/sfx/
cp /home/claude/work/common/mixsfx.py /home/claude/work/sfx/
# Chave do Google TTS: vem do prompt da tarefa (GTTS_KEY), nunca do repo publico
if [ -n "$GTTS_KEY" ]; then mkdir -p ~/.secrets; umask 077; printf '%s' "$GTTS_KEY" > ~/.secrets/gtts_key; fi
if [ -n "$PIXABAY_KEY" ]; then mkdir -p ~/.secrets; umask 077; printf "%s" "$PIXABAY_KEY" > ~/.secrets/pixabay_key; fi
if [ -n "$CF_ACCOUNT" ]; then mkdir -p ~/.secrets; umask 077; printf '%s' "$CF_ACCOUNT" > ~/.secrets/cf_account; printf '%s' "$CF_TOKEN" > ~/.secrets/cf_token; fi
# Rhubarb Lip Sync (MIT) para os bonecos falarem (talk.py)
if [ ! -x /home/claude/tools/Rhubarb-Lip-Sync-1.13.0-Linux/rhubarb ]; then mkdir -p /home/claude/tools && cd /home/claude/tools && curl -sL -m 120 -o rh.zip https://github.com/DanielSWolf/rhubarb-lip-sync/releases/download/v1.13.0/Rhubarb-Lip-Sync-1.13.0-Linux.zip && unzip -qo rh.zip && chmod +x Rhubarb-Lip-Sync-1.13.0-Linux/rhubarb && rm -f rh.zip; cd - >/dev/null; fi
python3 -c "import soundfile" 2>/dev/null || pip install -q soundfile --break-system-packages
# Chaves grátis opcionais: Pexels (vídeos de fundo) e football-data.org (dados)
if [ -n "$PEXELS_KEY" ]; then mkdir -p ~/.secrets; umask 077; printf '%s' "$PEXELS_KEY" > ~/.secrets/pexels_key; fi
if [ -n "$FOOTBALL_KEY" ]; then mkdir -p ~/.secrets; umask 077; printf '%s' "$FOOTBALL_KEY" > ~/.secrets/football_key; fi
echo "ok: /home/claude/work pronto"
