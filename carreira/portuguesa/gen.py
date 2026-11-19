import sys, os, concurrent.futures as cf
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import cfimg
SC = "Stylized 3D animated film still, Pixar-like, cinematic lighting, vertical composition, no text, no logos, no letters. "
FACE = "Stylized 3D Pixar-like cartoon character portrait, chest-up, facing camera, soft studio lighting, plain dark charcoal background, no text, no logos. "
TEE = "a very overweight 42-year-old Brazilian football coach, completely bald shiny head, chubby round face, big round belly, double chin, black moustache, wearing a tight red polo shirt with green collar and green sleeve trim"
P = {
 "tee": FACE + TEE + ", warm cheeky smile, holding a dark green clipboard",
 "tee_press": SC + TEE + ", sitting alone at a press conference table with microphones, nervous sweat, camera flashes, journalists laughing in the foreground blurred",
 "tee_shout": SC + TEE + ", shouting passionately on the touchline of a small stadium at night, arms raised, floodlights, rain",
 "davi": FACE + "a 16-year-old Brazilian boy footballer, brown skin, short curly black hair, big hopeful eyes, shy smile, wearing a plain red t-shirt",
 "davi_stadium": SC + "a 16-year-old Brazilian boy with curly black hair sleeping on a blanket in the empty concrete stands of an old red and green football stadium at dawn, a worn football beside him, city skyline behind, golden light",
 "kaua": FACE + "a 17-year-old Brazilian boy, dark skin, buzz cut with a bleached blond top, skinny, confident grin, wearing a plain green t-shirt",
 "pedro": FACE + "a 17-year-old Brazilian boy of Portuguese descent, fair skin, dark wavy hair, serious leader look, strong jaw, wearing a plain red t-shirt",
 "gui": FACE + "a 16-year-old short Brazilian boy goalkeeper, light brown skin, messy hair, determined eyes, wearing a plain black goalkeeper jersey with green gloves",
 "fan": FACE + "a Brazilian football fan in his 20s, wearing a red and green striped scarf, face paint red and green, screaming happily",
 "rival": FACE + "a smug Brazilian football coach in his 50s with slicked-back grey hair and sunglasses on head, black suit, arms crossed",
 "vice96": SC + "1996 vintage film photo style, Brazilian football players in red and green kits celebrating in a packed stadium, flares, confetti, nostalgic grain",
 "tapetao": SC + "dark court room with a judge's gavel slamming on a desk, a red and green football shirt lying on the table, dramatic red light",
 "obras": SC + "old red and green Brazilian football stadium under demolition and construction, cranes, fences with warning tape, dusty, grey sky, melancholic",
 "cofre": SC + "a nearly empty metal safe with a few coins inside, a red and green football scarf hanging on it, dark boardroom, dramatic light",
 "libertadores": SC + "a giant silver South American football trophy glowing on a pedestal in a dark stadium tunnel, red and green light beams, epic, smoke",
}
def go(k):
    out = f"{k}.jpg"
    if os.path.exists(out): return k
    err = None
    for _ in range(3):
        try: cfimg.gen(P[k], out, 8, style=False); return k
        except Exception as e: err = e
    return f"{k} FAIL {err}"
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(go, P): print(r)
