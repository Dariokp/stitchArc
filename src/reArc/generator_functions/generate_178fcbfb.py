def generate_178fcbfb(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2, 3))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = totuple(asindices(gi))
    iforb = set()
    jforb = set()
    mp = (h * w) // 3
    for col in (2, 1, 3):
        bnd = unifint(diff_lb, diff_ub, (1, w if col == 2 else h // 2))
        for ndots in range(bnd):
            if col == 2:
                ij = choice(sfilter(inds, lambda ij: last(ij) not in jforb))
                jforb.add(last(ij))
            if col == 1 or col == 3:
                ij = choice(sfilter(inds, lambda ij: first(ij) not in iforb))
                iforb.add(first(ij))
            gi = fill(gi, col, initset(ij))
            go = fill(go, col, (vfrontier if col == 2 else hfrontier)(ij))
            inds = remove(ij, inds)
    return {'input': gi, 'output': go}

