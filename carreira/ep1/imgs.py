import sys, os, concurrent.futures as cf
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common")
import cfimg
SC = "Stylized 3D animated film still, Pixar-like, cinematic lighting, wide shot, no text, no logos, no letters. "
FACE = "Stylized 3D Pixar-like cartoon character portrait, chest-up, facing camera, soft studio lighting, plain dark charcoal background, no text, no logos. "
P = {
 "kitchen": SC + "Year 2000 English terraced house kitchen, an 8-year-old boy with curly dark hair and round glasses dancing joyfully next to an old portable radio on the counter, his mother cheering in the living room behind him in front of a TV, warm nostalgic sepia tones, film grain.",
 "kitman": SC + "1992 old cramped football dressing room, amber and black shirts hanging on pegs, a middle-aged kitman with a moustache sitting on a bench wiping tears, warm dim light, sepia nostalgic.",
 "promise": SC + "Night, rain, a 13-year-old boy with curly hair and glasses standing alone at a fence looking at a small old English football stadium with floodlights off, melancholic blue tones.",
 "injury": SC + "Young footballer in an amber and black kit lying on the grass holding his right knee in pain, physio running, small stadium, overcast evening, dramatic.",
 "bus": SC + "A man in his thirties with curly dark hair, glasses and short stubble driving a yellow city bus, view through the windscreen of an English town street at dusk, his face reflected, thoughtful.",
 "notebook": SC + "Close-up of hands writing names in a worn small notebook under a desk lamp at night, a round black and white soccer ball and a whistle beside it, cozy warm light.",
 "phone": SC + "A man with curly hair and glasses in a bus driver uniform answering a mobile phone in an empty bus depot at night, surprised expression, yellow buses behind.",
 "whiteboard": SC + "Small football dressing room with an empty white whiteboard on the wall, amber and black shirts on pegs, benches, morning light.",
 "banner": SC + "Small English football stadium stand full of fans in amber and black scarves, some holding a large blank white banner, grey sky, angry mood.",
 "bike": SC + "Night, floodlit football training ground, a 15-year-old delivery boy with long dark curly hair on a bicycle holding a pizza box, stopped at the fence, young players training behind.",
 "race": SC + "Night floodlit training pitch, two teenagers sprinting side by side, one in a football kit and one in casual clothes and flip-flops winning, motion blur, players cheering.",
 "gaming": SC + "Teenage boy with copper-blond dyed hair and dark shaved sides wearing a headset, playing video games at a desk with RGB lights in his bedroom at night, focused, monitor glow.",
 "bench": SC + "A sulking 16-year-old footballer with copper-blond hair in an amber training bib sitting on a substitutes bench, arms crossed, cold winter evening stadium.",
 "hug": SC + "A 16-year-old footballer with copper-blond hair in an amber and black kit hugging a young 34-year-old manager with thick dark curly hair, glasses, stubble and a black training jacket with amber trim on the touchline, crowd celebrating behind, floodlights, emotional.",
 "offer": SC + "Night office desk, laptop screen glowing with an open email, an envelope icon, a mug of tea, a club scarf in amber and black, tense atmosphere.",
 "fall": SC + "Away fans in amber and black shirts devastated in a stand, hands on heads, one boy crying, floodlights, rain.",
 "h1912": SC + "Sepia old photograph style, 1912 working-class men in heavy boots playing football on a muddy field in an English town, spectators in flat caps.",
 "h1990": SC + "Early 1990s football celebration at a huge old stadium with twin towers, players in amber and black kits lifting each other, crowd waving scarves, vintage film colors.",
 "h2005": SC + "Small empty English football stadium on a grey day, a FOR SALE board style empty sign at the gate, puddles, melancholic.",
 "abbey": SC + "Small traditional English football stadium at night with floodlights, a compact main stand with amber accents, fans walking in, warm atmosphere.",
 "f_tomas": FACE + "A 33-year-old Portuguese centre-back, olive skin, shaved head, thick dark beard, scar on eyebrow, calm veteran look, wearing a plain black crew-neck t-shirt.",
 "f_theo": FACE + "A 21-year-old English striker of Nigerian descent, dark skin, short twists hairstyle, confident smile, wearing a plain black crew-neck t-shirt.",
 "f_kofi": FACE + "A 16-year-old English defensive midfielder of Ghanaian descent, dark skin, short cropped hair, serious focused eyes, wearing a plain black crew-neck t-shirt.",
 "f_ollie": FACE + "A 15-year-old English striker, pale skin with freckles, messy ginger hair, shy grin, wearing a plain black crew-neck t-shirt.",
}
def go(k):
    out = f"img/{k}.jpg"
    if os.path.exists(out): return k
    for _ in range(3):
        try: cfimg.gen(P[k], out, 6, style=False); return k
        except Exception as e: err = e
    return f"{k} FAIL {err}"
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(go, P): print(r)
