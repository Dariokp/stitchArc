def generate_7f4411dc(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc, fgc = sample(cols, 2)
    nsq = unifint(diff_lb, diff_ub, (1, (h * w) // 15))
    maxtr = 4 * nsq
    tr = 0
    succ = 0
    go = canvas(bgc, (h, w))
    inds = asindices(go)
    while tr < maxtr and succ < nsq:
        oh = randint(2, 6)
        ow = randint(2, 6)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            break
        loc = choice(totuple(cands))
        loci, locj = loc
        obj = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
        obj = shift(obj, loc)
        if obj.issubset(inds):
            go = fill(go, fgc, obj)
            succ += 1
            inds = (inds - obj) - outbox(obj)
        tr += 1
    inds = ofcolor(go, bgc)
    nnoise = unifint(diff_lb, diff_ub, (0, len(inds) // 2 - 1))
    gi = tuple(e for e in go)
    for k in range(nnoise):
        loc = choice(totuple(inds))
        inds = inds - dneighbors(loc)
        gi = fill(gi, fgc, {loc})
    return {'input': gi, 'output': go}

