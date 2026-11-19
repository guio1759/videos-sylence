# PLAYBOOK — canal de futebol (sylence_fc / TikTok "João")

Tudo o que uma sessão nova precisa para criar, renderizar e agendar vídeos sem perguntar nada ao usuário.
O usuário (pt-BR, palmeirense) quer: vídeos que gerem views e comentários, 3 por dia, sem ele salvar ou subir nada.

## 0. Preparar o ambiente
```
cd /home/claude && git clone -b videos https://github.com/guio1759/videos-sylence.git || (cd videos-sylence && git pull)
bash /home/claude/videos-sylence/toolkit/setup.sh
```
- Código: `/home/claude/work/{palp,tat,lib21,pre,bra}` (veja "Modelos de vídeo"). Logos: `/home/claude/work/logos/<COD>.png` (20 clubes da Série A 2026; `badge(code)` em make_palp usa o logo real). SFX: `/home/claude/work/sfx/*.wav` + `sfxlib.py` + `mixsfx.py`.
- Saída do shell para a internet: só github, pypi, texttospeech.googleapis.com e speech.platform.bing.com (voz grátis Microsoft "Antonio" via `edge-tts --proxy "$HTTPS_PROXY"`, reserva). Pesquisa = WebSearch/WebFetch.

## 0.5 PADRÃO SHORTS v2 (OBRIGATÓRIO desde 17/11/2026 — os Shorts estavam flopando)
Dados TikTok 10–17/11: vídeos de 52–122 s com média assistida de 7–19 s e só 1–8% vendo até o fim (≈500–800 views). O único hit (121k views) teve 52% até o fim. Diagnóstico do usuário: início feio, não chama a pessoa, lento.
1. **DURAÇÃO: 20–30 s. Nunca passar de 35 s.** Um assunto por vídeo; corte tudo que não é o gancho, o porquê e o CTA.
2. **SEGUNDO 0 já é o gancho**: a 1ª imagem e a 1ª frase são a conclusão mais polêmica/curiosa ("O Corinthians cai em 15 dias", "Fiz as contas: o Palmeiras é campeão"). Nada de logo, título, data ou "fala galera" no começo. Texto gigante na tela + voz já falando no frame 1.
3. **Chamar a pessoa**: falar com o espectador ("olha isso", "presta atenção", "você não vai acreditar") nos primeiros 3 s e de novo no meio.
4. **VOZ PADRÃO DOS SHORTS DE FUTEBOL desde 18/11/2026 = Google Chirp 3 HD Sadaltager (grátis)** — decisão do usuário para economizar; se ele achar ruim, volta para o Pedro. Receita no item "Quando acabar o crédito" abaixo e em toolkit/s15. O Modo Carreira continua com o Pedro eleven_v3. **Voz rápida e com emoção** (antes / Modo Carreira): Pedro no Speko com **elevenlabs:eleven_v3** (voice ulzsiMeCbfKyTPCNhCD5) e tags [excited] [tense] [laughs] [shouting]; depois acelerar 1.1x e cortar silêncios > 0,22 s (carreira/ep1/v2/voice.py: squeeze + atempo). Alvo ~210 palavras/min, nenhuma pausa > 0,4 s. **Quando acabar o crédito do Speko/ElevenLabs** (decisão do usuário, 17/11): usar a voz GRÁTIS do Google Chirp 3 HD **Sadaltager** (a mais expressiva entre as 16 masculinas), uma chamada por frase com speakingRate 1.05–1.12 e muita pontuação (!, ...), depois squeeze + atempo 1.1 + highpass 80, EQ +3 dB em 3 kHz e +2 dB em 150 Hz, acompressor 3:1 (exemplo: toolkit/s15). NÃO usar OmniVoice (modelo CC-BY-NC, proíbe monetização) nem clone Chatterbox (o usuário achou sem emoção). Tempos por palavra com faster-whisper local (carreira/ep1/v2/words.py), sem custo.
5. **Visual muda a cada 1–2 s** (zoom, carta entrando, número rolando, tremida no impacto); **legenda 1 palavra por vez** grande no balão (pular palavras curtas); **etiqueta de assunto** no topo; efeito sonoro em todo corte. Use os elementos de carreira/ep1/v2/gfx.py (chip, tag_box, odometer, newspaper, stamp, card, rays, confetti, speedlines) e o campo 3D.
6. **Final em loop**: a última frase emenda na primeira, CTA de comentário com pergunta simples (A ou B, placar, sim/não).
7. **Trilha de fundo SEMPRE** (o usuário acha que a falta dela derrubou views): faixa conhecida e não genérica do Kevin MacLeod (CC BY, não muta no TikTok/Reels/YT), ex.: Hitman a partir de 50,95 s para tensão/conta, Volatile Reaction para hype, Interloper para drama. Bem baixa: ~-14 dB abaixo da voz quando ela fala (ducking), ~-9 dB nas pausas, fade de 0,6 s no fim. **NUNCA escrever "Música: ..." na legenda/descrição dos posts (o usuário não quer, 19/11).** O crédito exigido pela licença CC BY vai PEQUENO NA TELA nos últimos 2,5 s do vídeo (engine.py de toolkit/shorts_v3 já faz isso sozinho; nos episódios longos, na tela final). Exemplo pronto: toolkit/s15/mix.py.
8. Antes de entregar, assista a 3 frames do primeiro segundo: se não der vontade de parar o scroll, refaça o gancho.

## 1. Escolher o tema (o que funciona)
- Melhor desempenho até agora: SIMULAÇÃO/provocação (foto "Palmeiras campeão, Corinthians cai" = 119k views, 53% assistiram até o fim). Histórias longas flopam (400–900 views).
- Priorizar: palpites com o porquê, simulação de tabela, pré-jogo/pós-jogo do Palmeiras, rivalidade (Corinthians/Flamengo/São Paulo), zoeira com a Seleção, histórias curtas com gancho atual.
- Sempre pesquisar dados reais e atuais antes (valorfinal.com.br tem tabela, probabilidades, forma, mando; notícias de desfalques). Nunca inventar número, escalação ou placar. Palpites sempre com motivo concreto (desfalque, mando, sequência, o que está em jogo).

## 2. Roteiro (regras de narração — o usuário reclama de voz travada)
- 20–30 s (ver 0.5). 1ª frase = a mais polêmica/curiosa, já no frame 1.
- Frases inteiras e afirmativas. PROIBIDO: pergunta seguida de resposta curta ("Sabe quem...? O Grêmio." soa como pergunta), reticências, muitos dois-pontos, fragmentos soltos.
- Números e anos por extenso no texto do TTS ("dois mil e sete", "dezessete"). Placar pode ser "2 a 1".
- Terminar com CTA de comentário e fazer o último frame "emendar" no primeiro (loop).
- Sem palavrão na narração (reduz alcance). Zoeira sim.

## 3. Voz
### 3a. Google Chirp 3 HD (GRÁTIS — padrão desde 17/11/2026)
- Google é só RESERVA (o usuário achou a Charon lenta e sem emoção). Use Fenrir 1.15 + voice.py apenas se o Speko falhar ou o saldo acabar. Padrão de voz: seção 0.5.
- `GTTS_KEY=<chave do prompt da tarefa> bash toolkit/setup.sh` grava a chave em ~/.secrets/gtts_key. Depois: `python3 /home/claude/work/common/gvoz.py Charon roteiro.txt voz.wav 1.0`. A chave NUNCA vai para o repo (público) nem para mensagens.
- O shell precisa do domínio texttospeech.googleapis.com liberado (já está). Cota grátis 1M caracteres/mês; uso previsto ~200k.
- Tempos por palavra: subir o wav para o repo (branch videos, pasta audio/) e usar o raw URL em `mcp__Speko__audio_transcribe` (custa centavos), como abaixo.
- Se o Google falhar (erro de cota/chave), usar o Pedro (3b) e avisar o usuário.

### 3b. Speko / ElevenLabs "Pedro" (pago)
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
- **TikTok Shop (aprovado pelo usuário em 19/11/2026)**: 1 vídeo de venda a cada 2 dias, SÓ no TikTok (conta "João", já afiliada; vitrine ainda vazia em 19/11). Produtos de FUTEBOL (chuteira, bola, camisa, caneleira, meião, acessórios de torcedor) escolhidos pelo usuário no Mercado de Afiliados do app. Formato "futebol + produto": short no nosso estilo (gancho de futebol, dado curioso real) que puxa o produto no fim; 20–35 s. Regras: só afirmações que estão no anúncio do produto (preço, material, avaliação); NUNCA depoimento inventado nem "comprei e amei" de pessoa fictícia; marcar como conteúdo comercial. A marcação do produto é feita no app pelo usuário (pela API não dá): entregar o vídeo como rascunho/caixa de entrada do TikTok e lembrar o usuário de adicionar o link do produto. Horário: 20:30 em dias alternados (não bate com 09:00, 12:30, 19:30, 18:00 Lusa, nem 18:00/21:30 Cambridge).
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

## 9. Série longa: Modo Carreira Cambridge United (YouTube, 1 episódio a cada 2 dias + 4 Shorts)
- **DESDE 19/11/2026 (decisão do usuário): os 4 Shorts por episódio FLOPARAM (ficavam perdidos, sem conexão). A partir do Ep.2: episódio grande no YouTube + UM vídeo curto vertical de ATÉ 3 MINUTOS, bem rápido, só com as informações mais importantes do episódio (resumo com começo-meio-fim e o dilema A/B no final), postado no TikTok/Instagram/Shorts.** As regras de 4 Shorts abaixo valem só para o Ep.1.
- **ORDEM DOS SHORTS = ORDEM DA HISTÓRIA** (o usuário reclamou no Ep.1, quando o dilema saiu antes do Gildo e do Murrey): agende os 4 Shorts na ordem em que as cenas aparecem no episódio, e o Short do DILEMA A/B sempre por ÚLTIMO, pelo menos 24 h antes da contagem de votos.
- Bíblia da série (doc): https://claude.ai/artifact/BBKWmiy47PX4KMMFBHbCBk — premissa, história real do clube, Rick Miguel, elenco, formato.
- Nossa versão: Cambridge ficou na League Two 2026/27 (na vida real subiu). Elenco real + técnico Rick Miguel (34, ex-motorista de ônibus, caderninho) + base inventada.
- Estado após Ep.1 (jul–dez 2026): 7º lugar, orçamento £180K, Rick efetivado. Reforços: Tomás Ferreira (ZAG 68, POR, grátis), Theo Okafor (ATA 63, empréstimo). Base: Murrey (MEI 16a, 57 OVR, pot 91), Gildo (PE 15a, 48, pot 89, entregador de pizza, RIT 98), Kofi Mensah-Hart (VOL 16a, 50, pot 79), Ollie Fenwick (ATA 15a, 46, pot 77). Dilema do Ep.1: proposta de £1,2 mi da Premier League pelo Murrey (A vender / B segurar).
- REGRA DA BASE: 2 revelações importantes por TEMPORADA (cada temporada = 2 episódios). 2026/27: Murrey e Gildo (Kofi e Ollie são secundários). 2027/28 (Ep.3–4): Victor (GOL, trauma de pênalti, 47→86) e Matic (ZAG, família sérvia, 54→85). Secundários novos só se o roteiro pedir.
- FLUXO DE CADA EPISÓDIO: votação A/B → roteiro enviado ao usuário para revisão → ajustes → "roteiro aprovado" → voz, vídeo e Shorts → rascunhos → "aprovado". Episódio com NO MÍNIMO 8 minutos (~1.700 palavras). Nunca usar fotos reais; avatares estilo bonequinho 3D (carreira/assets/*_ai.png; novos rostos com cfimg.py, camiseta preta lisa, sem logo, recorte com rembg).
- O que o usuário aprovou (Ep.1 v2): voz Pedro no **elevenlabs:eleven_v3** (Speko, voice ulzsiMeCbfKyTPCNhCD5) com tags [excited] [tense] [sad] [laughs] [whispers]; ~210 palavras/min (voice.py acelera 1.1x e corta pausas > 0.22 s); legenda 1 palavra por vez; etiqueta de assunto no topo; HUD fixo (posição, orçamento, rumo à Champions); troca de cena a cada 1–3 s; telas de jogo animadas (jornal girando, elenco, mercado, cartas abrindo tipo pacote FIFA, tabela, celular, e-mail, A/B); trilha Kevin MacLeod por bloco (CC BY: crédito pequeno na tela final do vídeo, NUNCA na descrição); efeitos em todo corte. Odiou: voz lenta/monótona, imagens de IA paradas, cenas longas.
- Código: carreira/ep1/v2/ (script2.py roteiro em blocos com cenas; voice.py; words.py com faster-whisper; make2.py cenas 16:9 e 9:16; mix2.py trilha; shorts2.py Shorts nativos verticais com final próprio). Para o Ep.N: copiar a pasta, reescrever script2.py e as cenas novas em make2.py, manter gfx.py.
- Shorts: SEMPRE nativos na vertical (make2 renderiza 1080x1920) e SEMPRE com final (fala curta + tela com escudo, CTA e INSCREVA-SE). Um dos 4 Shorts é o dilema A/B.
- Episódio começa com "Vocês escolheram: …" mostrando o comentário vencedor (estilo série interativa).
- Música: /home/claude/ep1/music não existe em sessão nova: baixar de https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Nome>.mp3 (Five Armies, Interloper, Dreamer, Heartbreaking, Lasting Hope, Rising Game, Volatile Reaction, Wholesome, Crossing the Chasm, Hitman).

## 10. Série vertical: Modo Carreira PORTUGUESA (TikTok, Instagram, Shorts) — aprovada em 19/11/2026
- Premissa: Portuguesa (SP) na Série D (na vida real foi eliminada na Série D 2026 e a SAF quer a Série A em 2029). Objetivo da série: sair da Série D e ganhar a LIBERTADORES.
- Formato: vertical nativo, **60–90 s por episódio, 3 por semana**. Cada episódio = um bloco (jogos, mercado ou base) + **decisão A/B no final** (votação aberta ~48 h).
- **Base forte**: muitos garotos da base com arcos próprios (como Gildo/Murrey no Cambridge).
- **Contratações espertas e realistas**: jogadores REAIS, promessas de clubes pequenos e "achados", com salário/valor compatível com Série D. Sempre pesquisar antes (clube atual, idade, posição, números reais). Nunca fotos reais: avatares bonequinho 3D.
- **Comentário mais curtido entra na série e FICA**: a cada episódio, o comentário com mais likes vira personagem fixo, com o @ e o comentário na tela. O PAPEL é decidido pela história (torcedor com faixa, garoto da base, técnico rival, olheiro, jornalista, presidente de clube rival...). Manter uma lista dos personagens-comentário e trazê-los de volta.
- Voz: **Pedro eleven_v3 (Speko)** com tags de emoção, igual ao Modo Carreira do Cambridge (NUNCA ativar auto top-up).
- Fluxo: igual ao do Cambridge (roteiro para revisão → "roteiro aprovado" → vídeo → rascunhos → "aprovado").
- **Tom e mecânica (pedido do usuário 19/11)**: MUITO drama e emoção (viradas, lesões, propostas, briga com diretoria, garoto que quase desiste, gol no último minuto) e foco forte em EVOLUÇÃO estilo FIFA: cada jogador tem carta com OVR e POTENCIAL; mostrar o OVR subindo na tela (+2, +3 com animação de carta melhorando: bronze → prata → ouro → especial), atributos (RIT, FIN, PAS, DRI, DEF, FÍS) crescendo, e um "placar de evolução" recorrente dos garotos da base. Toda evolução precisa de motivo na história (jogou bem, treino extra, mentor). Usar card()/odometer de gfx.py e as cartas tipo pacote FIFA do Ep.1 do Cambridge.
- **Bíblia da série (doc)**: https://claude.ai/artifact/1oz8ymCJPjRRxHN1dfu53A — elenco real, base inventada (Davi "Canindé", Kauã Bala, Pedro Lusitano, Gui Muralha), alvos reais de mercado, mecânicas e roteiro do Ep.1.
- Técnico: **Thiago Teh** — careca e gordinho (pedido do usuário), ex-técnico de várzea, ninguém acredita nele.
- Escudo real: carreira/portuguesa/assets/POR.png (também assets/logos/POR.png). Foto do Canindé: carreira/portuguesa/assets/caninde.jpg (referência; na versão da série a Lusa começa 2027 sem casa, jogando em Diadema, e volta ao Canindé como marco).
- **Início de TODO Ep.1/trailer**: bem chamativo e explicando claramente como a série funciona (meta Série D → Libertadores, você decide A/B, comentário mais curtido vira personagem, evolução estilo FIFA) nos primeiros ~15 s, para o público entender e ficar.
- **AGENDA DA SÉRIE LUSA (decisão do usuário 19/11/2026): Segunda, Quarta e Sexta às 18:00 (America/Sao_Paulo).** Ep.1 estreia sexta 20/11 às 18:00. A tarefa diária dos Shorts (09:00, 12:30, 19:30) não usa esse horário. Votação A/B de cada episódio fica aberta até o próximo (48 h).

## 11. Foco do momento
- Até 28/11/2026: FINAL DA LIBERTADORES (Palmeiras x Estudiantes, 28/11, 17h, Centenário). Para o usuário, o jogo contra o Flamengo "não importa". Pelo menos 2 de 3 shorts por dia sobre a final. Zoeira com o Flamengo permitida (eliminado pelo Vitória na Copa do Brasil e pelo Estudiantes na Libertadores; Brasileirão era obrigação), sempre sem palavrão e sem ofender torcedores, e intercalada com vídeos normais.

## 12. Edits com LANCES REAIS (aprovado pelo usuário em 19/11/2026)
- O usuário autoriza usar lances de transmissão (Globo, Premiere, CazéTV etc.). Cuidados: trechos curtos (3–8 s por lance, base Lei Pelé: flagrantes até 3% do jogo, fim jornalístico/esportivo), SEMPRE com comentário/análise por cima (freeze, setas, câmera lenta, narração) e NUNCA em vídeo de venda/TikTok Shop. Se o YouTube der claim, contestar ou trocar o trecho.
- Daqui não dá para baixar vídeo de TV/YouTube: o USUÁRIO manda os clipes (gravação de tela ou arquivo). Fluxo: depois de cada rodada/jogo importante, listar 2–4 lances que dão edit/análise (golaço, lance polêmico, erro, jogada tática) e pedir os clipes ao usuário; quando chegarem, editar.
- **ESTILO PADRÃO DOS EDITS (pedido do usuário 19/11): igual aos nossos shorts — lance em TELA CHEIA 9:16 (sem faixas vazias em cima e embaixo: "ar": 0.5625 + "cx_keys" seguindo a bola), narração da voz dos shorts comentando, legenda 1 palavra ("words": words.json do voz.py), etiqueta, placar, freeze com setas/círculos, música. Pedir ao usuário os clipes na MAIOR qualidade possível (o WhatsApp comprime e o recorte vertical amplia ~4x). Postagem: com a música do usuário em TODAS as redes (decisão dele).**
- Ferramenta: toolkit/clips/clipedit.py (spec JSON: trechos com velocidade/zoom/close, freeze-frame com círculo/seta/linha/texto, placar com escudos, etiqueta, música do usuário ou Kevin MacLeod com ducking sob a narração, loudnorm). Narração: mesma voz dos shorts (Google Sadaltager) com legenda 1 palavra.
- Músicas virais que o usuário mandar: cortar no ritmo (cortes no beat). No TikTok, preferir que o usuário escolha o som viral no app ao postar (não muta); no YouTube usar a versão com trilha Kevin MacLeod.
