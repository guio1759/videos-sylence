# cada item = uma cena (frase da legenda). CHUNKS = grupos enviados ao TTS (Pedro eleven_v3) com tags.
MUNDO = [
 "Nesse mundo... quando o seu time cai, você perde as cores.",
 "Dá pra ver na rua. Torcedor de time rebaixado anda cinza.",
 "Cinza no ônibus. Cinza no trabalho. Cinza até no casamento.",
 "Os mais velhos dizem que a cor só volta quando o time sobe de novo.",
 "Por isso, tem gente que nem escolhe time. O Caio, de dez anos, nasceu cinza. Pra ele, futebol era coisa de velho.",
 "O velho, no caso, era o avô dele. Seu Antônio. Oitenta anos, o último torcedor colorido do Vila Esperança.",
 "Em sessenta anos, o Vila nunca tinha caído. E o seu Antônio nunca perdeu um jogo no estádio.",
 "Toda vez, ele comprava dois ingressos. E a cadeira do lado... ficava sempre vazia.",
 "Até que chegou a última rodada. O Vila precisava de um empate pra não cair.",
 "Naquele dia, o Caio foi junto. Obrigado. Sentou na cadeira vazia, de braço cruzado.",
 "Zero a zero. Noventa minutos. E aí... gol do adversário.",
 "O estádio foi ficando cinza. Arquibancada por arquibancada.",
 "O seu Antônio olhou pras mãos. O verde tava indo embora.",
 "Foi aí que o Caio fez uma coisa que nunca tinha feito. Segurou a mão do avô... e gritou: Vamos, Vila!",
 "E a cor voltou. Na mão do avô... e, pela primeira vez, na dele.",
 "O Vila caiu naquele dia. Mas ninguém naquelas duas cadeiras ficou cinza.",
 "Porque ninguém perde a cor quando o time cai. Perde quando não tem mais ninguém pra torcer junto.",
 "Naquela noite, o Caio entendeu a cadeira vazia. Era do pai dele. Que um dia parou de ir com o avô... e ficou cinza.",
 "No domingo seguinte, o seu Antônio comprou três ingressos.",
]
CHUNKS = [
 (0, 4, "[mysterious] Nesse mundo... quando o seu time cai, você perde as cores. Dá pra ver na rua. Torcedor de time rebaixado anda cinza. [deadpan] Cinza no ônibus. Cinza no trabalho. Cinza até no casamento. Os mais velhos dizem que a cor só volta quando o time sobe de novo."),
 (4, 8, "Por isso, tem gente que nem escolhe time. O Caio, de dez anos, nasceu cinza. Pra ele, futebol era coisa de velho. [warmly] O velho, no caso, era o avô dele. Seu Antônio. Oitenta anos, o último torcedor colorido do Vila Esperança. Em sessenta anos, o Vila nunca tinha caído. E o seu Antônio nunca perdeu um jogo no estádio. [softly] Toda vez, ele comprava dois ingressos. E a cadeira do lado... ficava sempre vazia."),
 (8, 13, "[tense] Até que chegou a última rodada. O Vila precisava de um empate pra não cair. Naquele dia, o Caio foi junto. Obrigado. Sentou na cadeira vazia, de braço cruzado. Zero a zero. Noventa minutos. E aí... [sad] gol do adversário. O estádio foi ficando cinza. Arquibancada por arquibancada. O seu Antônio olhou pras mãos. O verde tava indo embora."),
 (13, 17, "[emotional] Foi aí que o Caio fez uma coisa que nunca tinha feito. Segurou a mão do avô... e gritou: [shouting] Vamos, Vila! [emotional] E a cor voltou. Na mão do avô... e, pela primeira vez, na dele. O Vila caiu naquele dia. Mas ninguém naquelas duas cadeiras ficou cinza. [softly] Porque ninguém perde a cor quando o time cai. Perde quando não tem mais ninguém pra torcer junto."),
 (17, 19, "[softly] Naquela noite, o Caio entendeu a cadeira vazia. Era do pai dele. Que um dia parou de ir com o avô... e ficou cinza. [warmly] No domingo seguinte, o seu Antônio comprou três ingressos."),
]
