def generate_0962bcdd(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (3, 4))    
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numc = unifint(diff_lb, diff_ub, (2, 7))
    ccols = sample(remcols, numc)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    num = unifint(diff_lb, diff_ub, (1, (h * w) // 25))
    indss = asindices(gi)
    maxtrials = 4 * num
    tr = 0
    succ = 0
    oh, ow = 5, 5
    subs = totuple(sfilter(indss, lambda ij: ij[0] < h - oh and ij[1] < w - ow))
    while succ < num and tr <= maxtrials:
        if len(indss) == 0:
            break
        if len(subs) == 0:
            tr += 1
            continue
        loci, locj = choice(subs)
        obj = frozenset({(loci, locj), (loci + 4, locj + 4)})
        bd = backdrop(obj)
        col = choice(ccols)
        if bd.issubset(indss):
            ca, cb = sample(ccols, 2)
            cp = (loci + 2, locj + 2)
            lins1 = connect((loci, locj), (loci + 4, locj + 4))
            lins2 = connect((loci + 4, locj), (loci, locj + 4))
            lins12 = lins1 | lins2
            lins3 = connect((loci + 2, locj), (loci + 2, locj + 4))
            lins4 = connect((loci, locj + 2), (loci + 4, locj + 2))
            lins34 = lins3 | lins4
            go = fill(go, cb, lins34)
            go = fill(go, ca, lins12)
            gi = fill(gi, ca, {cp})
            gi = fill(gi, cb, dneighbors(cp))
            succ += 1
            indss = indss - bd
        tr += 1
    return {'input': gi, 'output': go}

