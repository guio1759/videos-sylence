import sys, os, time; sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import cfimg
SC = "Stylized 3D animated film still, Pixar-like, cinematic lighting, vertical composition, no text, no logos, no letters. "
TEE = "a very overweight 42-year-old Brazilian football coach, completely bald shiny head, chubby round face, big round belly, double chin, black moustache, wearing a tight red polo shirt with green collar and green sleeve trim"
P = {
 "penalti": SC + "a Brazilian football player in a red shirt with green trim, seen from behind, holding the ball at the penalty spot at night, packed stadium, floodlights, smoke, extreme tension, goalkeeper in the distance",
 "faixa": SC + "angry Brazilian football fans in red and green behind a fence at night holding up a long blank white banner, rain, floodlights, dramatic, frustrated faces",
 "diadema": SC + "an old red bus arriving at a small modest municipal football stadium in a working-class Brazilian city at dusk, red and green flags, a few fans waiting",
 "festa": SC + "Brazilian football players in red shirts with green trim celebrating wildly at night, piling on each other near the corner flag, fans climbing the fence, flares, confetti, pure joy",
 "tee_cry": SC + TEE + ", crying tears of joy on the touchline at night, hands on his bald head, floodlights, rain",
 "romarinho_banco": SC + "a 35-year-old Brazilian veteran footballer with short dark hair and a trimmed beard, red training bib, sitting on the substitutes bench with arms crossed, annoyed serious face, night stadium",
}
for k, p in P.items():
    if os.path.exists(k + ".jpg"): continue
    for _ in range(5):
        try: cfimg.gen(p, k + ".jpg", 8, style=False); print(k, "ok"); break
        except Exception as e: print(k, e); time.sleep(6)
