# Biblioteca de voz do Pedro (eleven_v3, Speko) — reutilizar para economizar
- `bordoes/`: frases fixas que se repetem em todo episódio. Use sempre que a frase for igual, sem gerar de novo.
  - time_titular_da_lusa_agora.mp3 — "E esse é o time titular da Lusa agora."
- `epN/raw_k.mp3`: falas originais de cada episódio (texto em carreira/portuguesa/epNb/script.py), para recaps ("no episódio passado...").
- Regra: só gerar no Speko o que é novo (nomes, placares, história). Frases genéricas → bordões. Não emendar palavras soltas de áudios antigos (fica robótico).
