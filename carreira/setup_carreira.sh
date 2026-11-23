#!/bin/bash
# Recria os caminhos que make2.py/gfx.py esperam (rodar depois de toolkit/setup.sh)
R=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p /home/claude/carreira/assets /home/claude/ep1/img /home/claude/ep1/music
cp "$R"/carreira/card.py /home/claude/carreira/
cp "$R"/carreira/assets/* /home/claude/carreira/assets/
cp "$R"/carreira/img/* /home/claude/ep1/img/
cp "$R"/carreira/ep1/lances.py /home/claude/ep1/
pip install --break-system-packages -q faster-whisper "rembg[cpu]" 2>/dev/null
cd /home/claude/ep1/music && for n in "Five Armies" "Interloper" "Dreamer" "Heartbreaking" "Lasting Hope" "Rising Game" "Volatile Reaction" "Wholesome" "Crossing the Chasm" "Hitman" "Killers" "Ouroboros" "Movement Proposition" "Take a Chance" "Exhilarate" "Malicious" "Clash Defiant" "Impact Prelude" "Night of Chaos" "Rynos Theme" "Galactic Rap"; do
  f=$(echo "$n" | tr ' ' '_'); [ -f "$f.mp3" ] || curl -s -o "$f.mp3" "https://incompetech.com/music/royalty-free/mp3-royaltyfree/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$n").mp3"
done
echo "carreira pronta"
