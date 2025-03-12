def generate_db93a21d(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 3))
    h = unifint(diff_lb, diff_ub, (12, 31))
    w = unifint(diff_lb, diff_ub, (12, 32))
    num = unifint(diff_lb, diff_ub, (1, (h * w) // 25))
    bgc, fgc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    indss = asindices(gi)
    maxtrials = 4 * num
    tr = 0
    succ = 0
    while succ < num and tr <= maxtrials:
        if len(indss) == 0:
            break
        oh = randint(1, h // 4)
        ow = oh
        fullh = 4 * oh
        fullw = 4 * ow
        subs = totuple(sfilter(indss, lambda ij: ij[0] < h - fullh and ij[1] < w - fullw))
        if len(subs) == 0:
            tr += 1
            continue
        loci, locj = choice(subs)
        bigobj = backdrop(frozenset({(loci, locj), (loci + fullh - 1, locj + fullw - 1)}))
        smallobj = backdrop(frozenset({(loci+oh, locj+ow), (loci + fullh - 1 - oh, locj + fullw - 1 - ow)}))
        if bigobj.issubset(indss | ofcolor(go, 3)):
            gi = fill(gi, fgc, smallobj)
            go = fill(go, 3, bigobj)
            go = fill(go, fgc, smallobj)
            strp = mapply(rbind(shoot, (1, 0)), connect(lrcorner(smallobj), llcorner(smallobj)))
            go = fill(go, 1, ofcolor(go, bgc) & strp)
            succ += 1
            indss = indss - bigobj
        tr += 1
    gi = gi[1:]
    go = go[1:]
    gi = tuple(r[1:-1] for r in gi)
    go = tuple(r[1:-1] for r in go)
    return {'input': gi, 'output': go}

