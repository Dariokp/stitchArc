def generate_00d62c1b(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(4, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc, fgc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    nblocks = unifint(diff_lb, diff_ub, (1, (h * w) // 20))
    succ = 0
    tr = 0
    maxtr = 5 * nblocks
    inds = asindices(gi)
    while succ < nblocks and tr < maxtr:
        tr += 1
        oh = randint(3, 8)
        ow = randint(3, 8)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        loci, locj = loc
        bx = box(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
        bx = bx - set(sample(totuple(corners(bx)), randint(0, 4)))
        if bx.issubset(inds) and len(inds - bx) > (h * w) // 2 + 1:
            gi = fill(gi, fgc, bx)
            succ += 1
            inds = inds - bx
    maxnnoise = max(0, (h * w) // 2 - 1 - colorcount(gi, fgc))
    namt = unifint(diff_lb, diff_ub, (0, maxnnoise))
    noise = sample(totuple(inds), namt)
    gi = fill(gi, fgc, noise)
    objs = objects(gi, T, F, F)
    cands = colorfilter(objs, bgc)
    res = mfilter(cands, compose(flip, rbind(bordering, gi)))
    go = fill(gi, 4, res)
    return {'input': gi, 'output': go}

