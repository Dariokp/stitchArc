def generate_1f642eb9(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    ih = unifint(diff_lb, diff_ub, (2, min(h - 4, 2 * (h // 3))))
    iw = unifint(diff_lb, diff_ub, (2, min(w - 4, 2 * (w // 3))))
    loci = randint(2, h - ih - 2)
    locj = randint(2, w - iw - 2)
    bgc, sqc = sample(cols, 2)
    remcols = difference(cols, (bgc, sqc))
    numcells = unifint(diff_lb, diff_ub, (1, 2 * ih + 2 * iw - 4))
    outs = []
    ins = []
    c1 = choice((True, False))
    c2 = choice((True, False))
    c3 = choice((True, False))
    c4 = choice((True, False))
    for a in range(loci + (not c1), loci + ih - (not c2)):
        outs.append((a, 0))
        ins.append((a, locj))
    for a in range(loci + (not c3), loci + ih - (not c4)):
        outs.append((a, w - 1))
        ins.append((a, locj + iw - 1))
    for b in range(locj + c1, locj + iw - (c3)):
        outs.append((0, b))
        ins.append((loci, b))
    for b in range(locj + (c2), locj + iw - (c4)):
        outs.append((h - 1, b))
        ins.append((loci + ih - 1, b))
    inds = interval(0, 2 * ih + 2 * iw - 4, 1)
    locs = sample(inds, numcells)
    numc = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, numc)
    outs = [e for j, e in enumerate(outs) if j in locs]
    ins = [e for j, e in enumerate(ins) if j in locs]
    c = canvas(bgc, (h, w))
    bd = backdrop(frozenset({(loci, locj), (loci + ih - 1, locj + iw - 1)}))
    gi = fill(c, sqc, bd)
    seq = [choice(ccols) for k in range(numcells)]
    for c, loc in zip(seq, outs):
        gi = fill(gi, c, {loc})
    go = tuple(e for e in gi)
    for c, loc in zip(seq, ins):
        go = fill(go, c, {loc})
    return {'input': gi, 'output': go}

