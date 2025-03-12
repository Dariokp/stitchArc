def generate_44d8ac46(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(2, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    num = unifint(diff_lb, diff_ub, (1, 10))
    indss = asindices(gi)
    maxtrials = 4 * num
    tr = 0
    succ = 0
    while succ < num and tr <= maxtrials:
        tr += 1
        if len(remcols) == 0 or len(indss) == 0:
            break
        oh = randint(5, 7)
        ow = randint(5, 7)
        subs = totuple(sfilter(indss, lambda ij: ij[0] < h - oh and ij[1] < w - ow))
        if len(subs) == 0:
            continue
        loci, locj = choice(subs)
        obj = frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)})
        bd = backdrop(obj)
        col = choice(remcols)
        if bd.issubset(indss):
            ensuresq = choice((True, False))
            if ensuresq:
                dim = randint(1, min(oh, ow) - 2)
                iloci = randint(1, oh - dim - 1)
                ilocj = randint(1, ow - dim - 1)
                inpart = backdrop({(loci + iloci, locj + ilocj), (loci + iloci + dim - 1, locj + ilocj + dim - 1)})
            else:
                cnds = backdrop(inbox(bd))
                ch = choice(totuple(cnds))
                inpart = {ch}
                kk = unifint(diff_lb, diff_ub, (1, len(cnds)))
                for k in range(kk - 1):
                    inpart.add(choice(totuple((cnds - inpart) & mapply(dneighbors, inpart))))
            inpart = frozenset(inpart)
            hi, wi = shape(inpart)
            if hi == wi and len(inpart) == hi * wi:
                incol = 2
            else:
                incol = bgc
            gi = fill(gi, col, bd)
            go = fill(go, col, bd)
            gi = fill(gi, bgc, inpart)
            go = fill(go, incol, inpart)
            succ += 1
            indss = (indss - bd) - outbox(bd)
    return {'input': gi, 'output': go}

