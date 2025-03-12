def generate_c3f564a4(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (7, 30))
    w = unifint(diff_lb, diff_ub, (7, 30))
    p = unifint(diff_lb, diff_ub, (2, min(9, min(h//3, w//3))))
    fixc = choice(cols)
    remcols = remove(fixc, cols)
    ccols = list(sample(remcols, p))
    shuffle(ccols)
    c = canvas(-1, (h, w))
    baseobj = {(cc, (0, jj)) for cc, jj in zip(ccols, range(p))}
    obj = {c for c in baseobj}
    while rightmost(obj) < 2 * max(w, h):
        obj = obj | shift(obj, (0, p))
    if choice((True, False)):
        obj = mapply(lbind(shift, obj), {(jj, 0) for jj in interval(0, h, 1)})
    else:
        obj = mapply(lbind(shift, obj), {(jj, -jj) for jj in interval(0, h, 1)})
    go = paint(c, obj)
    gi = tuple(e for e in go)
    nsq = unifint(diff_lb, diff_ub, (1, max(1, (h * w) // 25)))
    maxtr = 4 * nsq
    tr = 0
    succ = 0
    while succ < nsq and tr < maxtr:
        oh = unifint(diff_lb, diff_ub, (2, 5))
        ow = unifint(diff_lb, diff_ub, (2, 5))
        loci = randint(0, h - oh)
        locj = randint(0, w - ow)
        tmpg = fill(gi, fixc, backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)})))
        if len(occurrences(tmpg, baseobj)) > 1 and len([r for r in tmpg if fixc not in r]) > 0 and len([r for r in dmirror(tmpg) if fixc not in r]) > 0:
            gi = tmpg
            succ += 1
        tr += 1
    if choice((True, False)):
        gi = rot90(gi)
        go = rot90(go)
    return {'input': gi, 'output': go}

