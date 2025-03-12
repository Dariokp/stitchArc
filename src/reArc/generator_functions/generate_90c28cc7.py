def generate_90c28cc7(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(1, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 10))
    w = unifint(diff_lb, diff_ub, (2, 10))
    nc = unifint(diff_lb, diff_ub, (2, 9))
    gi = canvas(-1, (h, w))
    inds = totuple(asindices(gi))
    colss = sample(cols, nc)
    for ij in inds:
        gi = fill(gi, choice(colss), {ij})
    gi = dmirror(dedupe(dmirror(dedupe(gi))))
    go = tuple(e for e in gi)
    h, w = shape(gi)
    fullh = unifint(diff_lb, diff_ub, (h, 30))
    fullw = unifint(diff_lb, diff_ub, (w, 30))
    inh = unifint(diff_lb, diff_ub, (h, fullh))
    inw = unifint(diff_lb, diff_ub, (w, fullw))
    while h < inh or w < inw:
        opts = []
        if h < inh:
            opts.append((h, identity))
        elif w < inw:
            opts.append((w, dmirror))
        dim, mirrf = choice(opts)
        idx = randint(0, dim - 1)
        gi = mirrf(gi)
        gi = gi[:idx+1] + gi[idx:]
        gi = mirrf(gi)
        h, w = shape(gi)
    while h < fullh or w < fullw:
        opts = []
        if h < fullh:
            opts.append(identity)
        elif w < fullw:
            opts.append(dmirror)
        mirrf = choice(opts)
        gi = mirrf(gi)
        gi = merge(tuple(sample((((0,) * width(gi),), gi), 2)))
        gi = mirrf(gi)
        h, w = shape(gi)
    return {'input': gi, 'output': go}

