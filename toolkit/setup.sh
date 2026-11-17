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
echo "ok: /home/claude/work pronto"
