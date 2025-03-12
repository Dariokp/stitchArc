def generate_c0f76784(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (6, 7, 8))    
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numcols = unifint(diff_lb, diff_ub, (1, len(remcols)))
    ccols = sample(remcols, numcols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    num = unifint(diff_lb, diff_ub, (1, (h * w) // 20))
    indss = asindices(gi)
    maxtrials = 4 * num
    tr = 0
    succ = 0
    while succ < num and tr <= maxtrials:
        if len(indss) == 0:
            break
        oh = choice((3, 4, 5))
        ow = oh
        subs = totuple(sfilter(indss, lambda ij: ij[0] < h - oh and ij[1] < w - ow))
        if len(subs) == 0:
            tr += 1
            continue
        loci, locj = choice(subs)
        obj = frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)})
        bd = backdrop(obj)
        col = choice(ccols)
        if bd.issubset(indss):
            gi = fill(gi, col, bd)
            go = fill(go, col, bd)
            ccc = oh + 3
            bdx = backdrop(inbox(obj))
            gi = fill(gi, bgc, bdx)
            go = fill(go, ccc, bdx)
            succ += 1
            indss = (indss - bd) - outbox(bd)
        tr += 1
    return {'input': gi, 'output': go}

