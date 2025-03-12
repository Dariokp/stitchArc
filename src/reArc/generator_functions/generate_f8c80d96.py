def generate_f8c80d96(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(5, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (8, 30))
    w = unifint(diff_lb, diff_ub, (8, 30))
    ow = randint(1, 3 if h > 10 else 2)
    oh = randint(1, 3 if w > 10 else 2)
    loci = randint(-oh+1, h-1)
    locj = randint(-ow+1, w-1)
    obj = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
    bgc, linc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(5, (h, w))
    ln1 = outbox(obj)
    ulci, ulcj = decrement(ulcorner(obj))
    lrci, lrcj = increment(lrcorner(obj))
    hoffs = randint(2, 4 if h > 12 else 3)
    woffs = randint(2, 4 if w > 12 else 3)
    lns = []
    for k in range(max(h, w) // min(hoffs, woffs) + 1):
        lnx = box(frozenset({(ulci - hoffs * k, ulcj - woffs * k), (lrci + hoffs * k, lrcj + woffs * k)}))
        lns.append(lnx)
    inds = asindices(gi)
    lns = sfilter(lns, lambda ln: len(ln & inds) > 0)
    nlns = len(lns)
    nmissing = unifint(diff_lb, diff_ub, (0, nlns - 2))
    npresent = nlns - nmissing
    for k in range(npresent):
        gi = fill(gi, linc, lns[k])
    for ln in lns:
        go = fill(go, linc, ln)
    return {'input': gi, 'output': go}

