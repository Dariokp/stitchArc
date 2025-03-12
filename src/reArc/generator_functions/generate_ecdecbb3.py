def generate_ecdecbb3(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc, dotc, linc = sample(cols, 3)
    gi = canvas(bgc, (h, w))
    nl = unifint(diff_lb, diff_ub, (1, h//4))
    inds = interval(0, h, 1)
    locs = []
    for k in range(nl):
        if len(inds) == 0:
            break
        idx = choice(inds)
        locs.append(idx)
        inds = remove(idx, inds)
        inds = remove(idx - 1, inds)
        inds = remove(idx + 1, inds)
        inds = remove(idx - 2, inds)
        inds = remove(idx + 2, inds)
    locs = sorted(locs)
    for ii in locs:
        gi = fill(gi, linc, hfrontier((ii, 0)))
    iopts = difference(difference(difference(interval(0, h, 1), locs), apply(increment, locs)), apply(decrement, locs))
    jopts = interval(0, w, 1)
    ndots = unifint(diff_lb, diff_ub, (1, min(len(iopts), w // 2)))
    dlocs = []
    for k in range(ndots):
        if len(iopts) == 0 or len(jopts) == 0:
            break
        loci = choice(iopts)
        locj = choice(jopts)
        dlocs.append((loci, locj))
        jopts = remove(locj, jopts)
        jopts = remove(locj+1, jopts)
        jopts = remove(locj-1, jopts)
    go = gi
    for d in dlocs:
        loci, locj = d
        if loci < min(locs):
            go = fill(go, dotc, connect(d, (min(locs), locj)))
            go = fill(go, linc, neighbors((min(locs), locj)))
        elif loci > max(locs):
            go = fill(go, dotc, connect(d, (max(locs), locj)))
            go = fill(go, linc, neighbors((max(locs), locj)))
        else:
            sp = [e for e in locs if e < loci][-1]
            ep = [e for e in locs if e > loci][0]
            go = fill(go, dotc, connect((sp, locj), (ep, locj)))
            go = fill(go, linc, neighbors((sp, locj)))
            go = fill(go, linc, neighbors((ep, locj)))
        gi = fill(gi, dotc, {d})
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

