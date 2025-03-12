def generate_fcc82909(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (7, 30))
    w = unifint(diff_lb, diff_ub, (7, 30))
    nobjs = unifint(diff_lb, diff_ub, (1, w // 3))
    opts = interval(0, w, 1)
    tr = 0
    maxtr = 4 * nobjs
    succ = 0
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    while succ < nobjs and tr < maxtr:
        tr += 1
        sopts = sfilter(opts, lambda j: set(interval(j, j + 2, 1)).issubset(opts))
        if len(sopts) == 0:
            break
        numc = unifint(diff_lb, diff_ub, (1, 4))
        jstart = choice(sopts)
        opts = remove(jstart, opts)
        opts = remove(jstart+1, opts)
        options = interval(0, h - 2 - numc + 1, 1)
        if len(options) == 0:
            break
        iloc = choice(options)
        ccols = sample(remcols, numc)
        bd = backdrop(frozenset({(iloc, jstart), (iloc + 1, jstart + 1)}))
        bd = list(bd)
        shuffle(bd)
        obj = {(c, ij) for c, ij in zip(ccols, bd[:numc])} | {(choice(ccols), ij) for ij in bd[numc:]}
        if not mapply(dneighbors, toindices(obj)).issubset(ofcolor(gi, bgc)):
            continue
        gi = paint(gi, obj)
        go = paint(go, obj)
        for k in range(numc):
            go = fill(go, 3, {(iloc+k+2, jstart), (iloc+k+2, jstart+1)})
    return {'input': gi, 'output': go}

