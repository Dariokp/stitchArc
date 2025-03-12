def generate_a5f85a15(diff_lb: float, diff_ub: float) -> dict:
    colopts = remove(4, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    startlocs = apply(toivec, interval(h - 1, 0, -1)) + apply(tojvec, interval(0, w, 1))
    cands = interval(0, h + w - 1, 1)
    num = unifint(diff_lb, diff_ub, (1, (h + w - 1) // 3))
    locs = []
    for k in range(num):
        if len(cands) == 0:
            break
        loc = choice(cands)
        locs.append(loc)
        cands = remove(loc, cands)
        cands = remove(loc - 1, cands)
        cands = remove(loc + 1, cands)
    locs = set([startlocs[loc] for loc in locs])
    bgc, fgc = sample(colopts, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for loc in locs:
        ln = order(shoot(loc, (1, 1)), first)
        gi = fill(gi, fgc, ln)
        go = fill(go, fgc, ln)
        go = fill(go, 4, ln[1::2])
    return {'input': gi, 'output': go}

