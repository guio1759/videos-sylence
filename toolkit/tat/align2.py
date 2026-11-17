import re, itertools, sys
sys.path.insert(0, "/home/claude/work/hist")
from timing import segments
def align(text, path):
    segs = segments(path)
    phrases = [p for p in re.split(r"(?<=[.,:;!?])\s+", text) if p]
    a, b = segs[0][0], segs[-1][1]; tot = b - a
    cl = [len(p) for p in phrases]; ct = sum(cl)
    n = len(phrases); gaps = list(range(len(segs) - 1))
    best = None
    if len(segs) >= n:
        for comb in itertools.combinations(gaps, n - 1):
            bounds = [a] + [x for g in comb for x in (segs[g][1], segs[g + 1][0])] + [b]
            spans = [(bounds[2 * i], bounds[2 * i + 1]) for i in range(n)]
            err = sum(((s1 - s0) / tot - c / ct) ** 2 for (s0, s1), c in zip(spans, cl))
            gap = sum(segs[g + 1][0] - segs[g][1] for g in comb)
            score = gap - 25 * err
            if best is None or score > best[0]: best = (score, spans)
        spans = best[1]
    else:
        t = a; spans = []
        for c in cl: d = tot * c / ct; spans.append((t, t + d)); t += d
    out = []
    for p, (s0, s1) in zip(phrases, spans):
        ws = p.split(); wl = [len(w) + 2 for w in ws]; T = sum(wl); t = s0
        for w, k in zip(ws, wl):
            d = (s1 - s0) * k / T; out.append([w, round(t, 3), round(t + d, 3)]); t += d
    return out
