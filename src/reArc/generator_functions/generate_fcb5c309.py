def generate_fcb5c309(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc, dotc, sqc = sample(cols, 3)
    numsq = unifint(diff_lb, diff_ub, (1, (h * w) // 25))
    gi = canvas(bgc, (h, w))
    inds = asindices(gi)
    maxtr = 4 * numsq
    tr = 0
    succ = 0
    numcells = None
    take = False
    while tr < maxtr and succ < numsq:
        oh = randint(3, 7)
        ow = randint(3, 7)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            break
        loc = choice(totuple(cands))
        loci, locj = loc
        sq = box(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
        bd = backdrop(sq)
        if bd.issubset(inds):
            gi = fill(gi, sqc, sq)
            ib = backdrop(inbox(sq))
            if numcells is None:
                numcells = unifint(diff_lb, diff_ub, (1, len(ib)))
                cells = sample(totuple(ib), numcells)
                take = True
            else:
                nc = unifint(diff_lb, diff_ub, (0, min(max(0, numcells - 1), len(ib))))
                cells = sample(totuple(ib), nc)
            gi = fill(gi, dotc, cells)
            if take:
                go = replace(subgrid(sq, gi), sqc, dotc)
                take = False
            inds = (inds - bd) - outbox(bd)
            succ += 1
        tr += 1
    nnoise = unifint(diff_lb, diff_ub, (0, max(0, len(inds) // 2 - 1)))
    noise = sample(totuple(inds), nnoise)
    gi = fill(gi, dotc, noise)
    return {'input': gi, 'output': go}

