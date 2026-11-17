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

## 6. Publicar (custo zero)
Metricool é plano GRÁTIS: só 20 publicações/mês e CADA REDE CONTA (1 vídeo em 4 redes = 4). Por isso:
- **TikTok, Instagram e YouTube → vidIQ** (grátis, sem limite).
- **Facebook → Metricool**, só Facebook, no máximo 20/mês (conte as publicações do mês com getScheduledPosts antes; se o limite estiver perto, pule o Facebook e diga isso no resumo).

0. Acesso de escrita no GitHub: se `git push` falhar por permissão, chame `mcp__claude-code-remote__add_repo(owner="guio1759", repo="videos-sylence", access="push")`, siga o clone que ele devolver (`--depth 1 -b videos`), copie o mp4 e faça o push.
1. Copiar o mp4 para `/home/claude/videos-sylence/<AAAA-MM>/`, commit e `git -c push.negotiate=true push origin videos`. Mensagem de commit termina com
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` e `Claude-Session: <link da sessão atual>`.
   URL pública: `https://raw.githubusercontent.com/guio1759/videos-sylence/videos/<AAAA-MM>/<arquivo>.mp4`.
2. vidIQ: `vidiq_video_upload(url=<URL pública>, title=...)` → uploadId. Depois `vidiq_social_post_draft_create` com media `[{"type":"video","id":uploadId}]`, `publishAt` ISO com -03:00, legenda curta (gancho + CTA + 3–4 hashtags) e destinations:
   - TIKTOK `_000bWFGJM_1fUSMtLuMnSVpkxo60lkuvBOj` (conta "João"): `privacyLevel:"PUBLIC_TO_EVERYONE", allowComment:true, musicUsageConfirmed:true, isAiGenerated:true` (escolhas já feitas pelo usuário em 16/11/2026).
   - INSTAGRAM `29280546794919548` (sylence_fc). NUNCA usar outra conta de Instagram.
   - YOUTUBE `UC2yQMzFVDLJ7EYf_ryzOOXA`: `title` com "#shorts", `privacyStatus:"public"`, `categoryId:17`, tags.
   **Publicar exige aprovação do usuário**: crie os rascunhos, NÃO chame vidiq_social_post_publish sozinho. Termine a sessão mostrando a lista (horário, vídeo, título) e pedindo "aprovado". Quando o usuário responder "aprovado" na mesma sessão, chame `vidiq_social_post_publish(postId, revision)` para cada rascunho. Se pedir verificação do YouTube, mostre o link e espere. Posts agendados no vidIQ não podem ser cancelados.
3. Metricool (só Facebook): `createScheduledPost` blogId "8152680", providers `[{"network":"facebook"}]`, `facebookData:{"type":"REEL"}`, media = URL pública, mesmo horário. Esse pode ser agendado direto (sem aprovação).
4. Horários: **09:00, 12:30, 19:30** (America/Sao_Paulo). Verifique os ocupados com `vidiq_social_post_list` e getScheduledPosts. Escalação provável não deve sair perto do anúncio oficial (≈1h antes do jogo).

## 7. IDs
- Metricool blogId 8152680 (plano grátis, só Facebook). Windsor: TikTok `_0000zurIXQs1nmr6sSoj_yqirB0OAhZXZI-`, YouTube 97309, Instagram 17841439094316734.
- Repo: guio1759/videos-sylence, branch `videos`.
- vidIQ (conector) disponível: use `vidiq_trending_videos` / `vidiq_outliers` para achar temas de futebol em alta antes de escolher o tema.

## 8. Modelos de vídeo (código existente)
- `palp/make_qua.py` + `make_palp.py`: cards de jogo com motivos (`match_card2`), tabela, simulação (`scene_sim2`), história (`scene_hist`). Selecionar pelo env `WORDS=words_X`; adicionar nova cena no dict SCENE.
- `lib21/make_lib.py`: história com lances em 3D (gols, erro, título).
- `pre/make_pre.py`: pré-jogo 3D (escalação aparecendo, ghosts de desfalques, setas táticas, palpite).
- `bra/make_bra.py`: seleção/zoeira 2D (bandeiras, placares, campinho 2D, despertador).
- `tat/eng3d.py`: motor 3D (Cam, draw_pitch, billboards, goals, polyline/poly).
