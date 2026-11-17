# PLAYBOOK — canal de futebol (sylence_fc / TikTok "João")

Tudo o que uma sessão nova precisa para criar, renderizar e agendar vídeos sem perguntar nada ao usuário.
O usuário (pt-BR, palmeirense) quer: vídeos que gerem views e comentários, 3 por dia, sem ele salvar ou subir nada.

## 0. Preparar o ambiente
```
cd /home/claude && git clone -b videos https://github.com/guio1759/videos-sylence.git || (cd videos-sylence && git pull)
bash /home/claude/videos-sylence/toolkit/setup.sh
```
- Código: `/home/claude/work/{palp,tat,lib21,pre,bra}` (veja "Modelos de vídeo"). Logos: `/home/claude/work/logos/<COD>.png` (20 clubes da Série A 2026; `badge(code)` em make_palp usa o logo real). SFX: `/home/claude/work/sfx/*.wav` + `sfxlib.py` + `mixsfx.py`.
- Saída do shell para a internet é bloqueada (só github/pypi). Pesquisa = WebSearch/WebFetch.

## 1. Escolher o tema (o que funciona)
- Melhor desempenho até agora: SIMULAÇÃO/provocação (foto "Palmeiras campeão, Corinthians cai" = 119k views, 53% assistiram até o fim). Histórias longas flopam (400–900 views).
- Priorizar: palpites com o porquê, simulação de tabela, pré-jogo/pós-jogo do Palmeiras, rivalidade (Corinthians/Flamengo/São Paulo), zoeira com a Seleção, histórias curtas com gancho atual.
- Sempre pesquisar dados reais e atuais antes (valorfinal.com.br tem tabela, probabilidades, forma, mando; notícias de desfalques). Nunca inventar número, escalação ou placar. Palpites sempre com motivo concreto (desfalque, mando, sequência, o que está em jogo).

## 2. Roteiro (regras de narração — o usuário reclama de voz travada)
- 25–35 s na maioria (60 s só para história forte). 1ª frase = a mais polêmica/curiosa (gancho em 2 s).
- Frases inteiras e afirmativas. PROIBIDO: pergunta seguida de resposta curta ("Sabe quem...? O Grêmio." soa como pergunta), reticências, muitos dois-pontos, fragmentos soltos.
- Números e anos por extenso no texto do TTS ("dois mil e sete", "dezessete"). Placar pode ser "2 a 1".
- Terminar com CTA de comentário e fazer o último frame "emendar" no primeiro (loop).
- Sem palavrão na narração (reduz alcance). Zoeira sim.

## 3. Voz (Speko MCP)
- `mcp__Speko__audio_synthesize` body: `{"text":..., "intent":{"language":"pt-BR","optimizeFor":"accuracy"}, "voice":"ulzsiMeCbfKyTPCNhCD5", "constraints":{"allowedProviders":{"tts":["elevenlabs:eleven_multilingual_v2"]}}}` (voz "Pedro Nassif").
- Tempos por palavra: `mcp__Speko__audio_transcribe(audio_url=<link assinado>, language="pt-BR", word_timestamps=true)`. Corrigir erros do transcritor (Athletico, Gómez, Mayke, Raphael, Z4, Sosa...) e montar o módulo `words_X.py` (W=[(palavra, ms)], END=ms).
- NÃO comprimir pausas. NÃO ativar auto top-up do Speko (o usuário não quer). Custo ≈ US$0,15 por minuto de voz.

## 4. Visual
- 1080x1920, 30 fps, libx264 veryfast crf18; render em 2 processos (`python3 make_X.py i 2`) e concat `-c copy`; áudio `loudnorm=I=-14:TP=-1.5`.
- Estilo equilibrado: chamativo mas sem luz estourada; legenda palavra a palavra (vlib.caption y=1500); escudos reais; chips com o "porquê".
- Campo 3D estilo @joktreinador (eng3d.py) para lances, escalações e táticas — o usuário gosta.
- Antes do render completo, gerar alguns frames de preview e olhar.

## 5. Som (biblioteca CC0 em assets/sfx, ver CREDITOS.md)
- `mixsfx.mix(narr, total, events=[(t,"nome",ganho)], out, bed=("estadio_ambiente",0.06))`.
- Nomes: torcida_reacao_gol, torcida_grita_gol, torcida_comemora, torcida_grito_homens, torcida_aww, estadio_ambiente, san_siro_derby, apito_curto, apito_juiz, chute_bola_1/2, whoosh_1/2/3, whoosh_grave, whoosh_boom, tambor_impacto, camera_click.
- Uso: whoosh nas trocas de cena (0.25), tambor_impacto/whoosh_boom em revelação de placar (0.35), chute + torcida em gol (0.3/0.25), aww em lance perdido, apito no início de pré/pós-jogo. Sem música de fundo.
- Sons novos: só com o Mac do usuário ligado (navegador do app em api.openverse.org, licença cc0). Salvar em assets/sfx.

## 6. Publicar (sem o usuário fazer nada)
1. Copiar o mp4 para `/home/claude/videos-sylence/2026-11/` (ou mês atual), commit e `git -c push.negotiate=true push origin videos`.
   Mensagem de commit termina com:
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` e `Claude-Session: <link da sessão atual>`.
2. `mcp__Metricool_Social_Media_Management__createScheduledPost`, blogId "8152680", date com -03:00, timezone America/Sao_Paulo, media = `https://raw.githubusercontent.com/guio1759/videos-sylence/videos/<pasta>/<arquivo>.mp4`.
   providers tiktok, instagram, youtube, facebook.
   - tiktokData: `{"privacyOption":"PUBLIC_TO_EVERYONE","title":"<obrigatório>","isAigc":true}`
   - instagramData: `{"type":"REEL","showReelOnFeed":true}`
   - youtubeData: `{"title":"... #shorts","type":"short","privacy":"public","category":"SPORTS","madeForKids":false,"tags":[...]}`
   - facebookData: `{"type":"REEL"}`
   - `firstCommentText`: pergunta/enquete curta para puxar comentários (ex.: "Qual seu placar? 👇").
   - `videoCoverMilliseconds`: frame com placar/escudos (não o 1º frame escuro).
   - Legenda curta, gancho + CTA, **3–4 hashtags** específicas.
3. Horários: **09:00, 12:30, 19:30** (America/Sao_Paulo). Conferir com getScheduledPosts quais estão livres. Se der 502, conferir e repetir uma vez.
4. Conteúdo com escalação provável não deve sair perto do anúncio oficial (≈1h antes do jogo).

## 7. IDs
- Metricool blogId 8152680. Windsor: TikTok `_0000zurIXQs1nmr6sSoj_yqirB0OAhZXZI-`, YouTube 97309, Instagram 17841439094316734.
- Repo: guio1759/videos-sylence, branch `videos`.

## 8. Modelos de vídeo (código existente)
- `palp/make_qua.py` + `make_palp.py`: cards de jogo com motivos (`match_card2`), tabela, simulação (`scene_sim2`), história (`scene_hist`). Selecionar pelo env `WORDS=words_X`; adicionar nova cena no dict SCENE.
- `lib21/make_lib.py`: história com lances em 3D (gols, erro, título).
- `pre/make_pre.py`: pré-jogo 3D (escalação aparecendo, ghosts de desfalques, setas táticas, palpite).
- `bra/make_bra.py`: seleção/zoeira 2D (bandeiras, placares, campinho 2D, despertador).
- `tat/eng3d.py`: motor 3D (Cam, draw_pitch, billboards, goals, polyline/poly).
