def generate_2dd70a9a(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (2, 3))
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc, fgc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    if choice((True, False)):
        oh = unifint(diff_lb, diff_ub, (5, h - 2))
        ow = unifint(diff_lb, diff_ub, (3, w - 2))
        loci = randint(1, h - oh - 1)
        locj = randint(1, w - ow - 1)
        hli = randint(loci+2, loci+oh-3)
        sp = {(loci+oh-1, locj), (loci+oh-2, locj)}
        ep = {(loci, locj+ow-1), (loci+1, locj+ow-1)}
        bp1 = (hli-1, locj)
        bp2 = (hli, locj+ow)
        ln1 = connect((loci+oh-1, locj), (hli, locj))
        ln2 = connect((hli, locj), (hli, locj+ow-1))
        ln3 = connect((hli, locj+ow-1), (loci+2, locj+ow-1))
    else:
        oh = unifint(diff_lb, diff_ub, (3, h-2))
        ow = unifint(diff_lb, diff_ub, (3, w-2))
        loci = randint(1, h - oh - 1)
        locj = randint(1, w - ow - 1)
        if choice((True, False)):
            sp1j = randint(locj, locj+ow-3)
            ep1j = locj
        else:
            ep1j = randint(locj, locj+ow-3)
            sp1j = locj
        sp = {(loci, sp1j), (loci, sp1j+1)}
        ep = {(loci+oh-1, ep1j), (loci+oh-1, ep1j+1)}
        bp1 = (loci, locj+ow)
        bp2 = (loci+oh, locj+ow-1)
        ln1 = connect((loci, sp1j+2), (loci, locj+ow-1))
        ln2 = connect((loci, locj+ow-1), (loci+oh-1, locj+ow-1))
        ln3 = connect((loci+oh-1, ep1j+2), (loci+oh-1, locj+ow-1))
    gi = fill(gi, 3, sp)
    gi = fill(gi, 2, ep)
    go = fill(go, 3, sp)
    go = fill(go, 2, ep)
    lns = ln1 | ln2 | ln3
    bps = {bp1, bp2}
    gi = fill(gi, fgc, bps)
    go = fill(go, fgc, bps)
    go = fill(go, 3, lns)
    inds = ofcolor(go, bgc)
    namt = unifint(diff_lb, diff_ub, (0, len(inds) // 2))
    noise = sample(totuple(inds), namt)
    gi = fill(gi, fgc, noise)
    go = fill(go, fgc, noise)
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

