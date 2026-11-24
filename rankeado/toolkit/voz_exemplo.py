import sys, json, subprocess
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common")
import gvoz
LINES = [
 "Rankeei os dez animais mais perigosos do Brasil... e o número um pode estar no seu quarto agora!",
 "Décimo: a piranha. Dentes afiados como lâmina... e ela nunca anda sozinha!",
 "Nono: a onça-pintada. Ela tem a mordida mais forte de todos os felinos, pro tamanho dela!",
 "Oitavo: a sucuri. Pode passar dos cinco metros... e mata apertando a presa até ela parar de respirar.",
 "Sétimo: o tubarão. Só em Pernambuco, foram oitenta e quatro ataques desde mil novecentos e noventa e dois!",
 "Sexto: a taturana. Parece inofensiva... mas o veneno dela pode causar hemorragia!",
 "Quinto: a aranha-marrom. A picada quase não dói na hora... mas pode necrosar a pele! E segura aí, que o top três você vê quase todo dia.",
 "Quarto: a aranha-armadeira. As aranhas são a segunda maior causa de envenenamento no Brasil: mais de quarenta e três mil picadas em um ano!",
 "Terceiro: a jararaca. É a cobra que mais pica gente no Brasil!",
 "Segundo: o escorpião-amarelo. Foram cerca de duzentos mil acidentes com escorpião em um único ano!",
 "E o número um... o mosquito da dengue! Em dois mil e vinte e quatro, foram quase seis mil mortes no Brasil. O animal mais perigoso do país cabe na ponta do seu dedo!",
 "Qual animal você colocaria nessa lista? Comenta aí, e segue o Rankeado BR!",
]
AF = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
      "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,"
      "highpass=f=80,equalizer=f=3000:t=q:w=1:g=3,equalizer=f=150:t=q:w=1:g=2,"
      "acompressor=ratio=3:threshold=-20dB:attack=5:release=80")
durs = []
for i, t in enumerate(LINES):
    raw = f"raw_{i:02d}.wav"
    open(raw, "wb").write(gvoz.synth_chunk(t, "Sadaltager", 1.12))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", AF, "-ar", "44100", "-ac", "1", f"v_{i:02d}.wav"], check=True)
    durs.append(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"v_{i:02d}.wav"])))
print([round(x,2) for x in durs], round(sum(durs),1))
json.dump(durs, open("vdurs.json", "w"))
