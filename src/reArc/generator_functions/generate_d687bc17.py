def generate_d687bc17(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc, c1, c2, c3, c4 = sample(cols, 5)
    gi = canvas(bgc, (h, w))
    gi = fill(gi, c1, connect((0, 0), (0, w - 1)))
    gi = fill(gi, c2, connect((0, 0), (h - 1, 0)))
    gi = fill(gi, c3, connect((h - 1, w - 1), (0, w - 1)))
    gi = fill(gi, c4, connect((h - 1, w - 1), (h - 1, 0)))
    inds = asindices(gi)
    gi = fill(gi, bgc, corners(inds))
    go = tuple(e for e in gi)
    cands = backdrop(inbox(inbox(inds)))
    ndots = unifint(diff_lb, diff_ub, (1, min(len(cands), h + h + w + w)))
    dots = sample(totuple(cands), ndots)
    dots = {(choice((c1, c2, c3, c4)), ij) for ij in dots}
    n1 = toindices(sfilter(dots, lambda cij: cij[0] == c1))
    n1coverage = apply(last, n1)
    if len(n1coverage) == w - 4 and w > 5:
        n1coverage = remove(choice(totuple(n1coverage)), n1coverage)
    for jj in n1coverage:
        loci = choice([ij[0] for ij in sfilter(n1, lambda ij: ij[1] == jj)])
        gi = fill(gi, c1, {(loci, jj)})
        go = fill(go, c1, {(1, jj)})
    n2 = toindices(sfilter(dots, lambda cij: cij[0] == c2))
    n2coverage = apply(first, n2)
    if len(n2coverage) == h - 4 and h > 5:
        n2coverage = remove(choice(totuple(n2coverage)), n2coverage)
    for ii in n2coverage:
        locj = choice([ij[1] for ij in sfilter(n2, lambda ij: ij[0] == ii)])
        gi = fill(gi, c2, {(ii, locj)})
        go = fill(go, c2, {(ii, 1)})
    n3 = toindices(sfilter(dots, lambda cij: cij[0] == c4))
    n3coverage = apply(last, n3)
    if len(n3coverage) == w - 4 and w > 5:
        n3coverage = remove(choice(totuple(n3coverage)), n3coverage)
    for jj in n3coverage:
        loci = choice([ij[0] for ij in sfilter(n3, lambda ij: ij[1] == jj)])
        gi = fill(gi, c4, {(loci, jj)})
        go = fill(go, c4, {(h - 2, jj)})
    n4 = toindices(sfilter(dots, lambda cij: cij[0] == c3))
    n4coverage = apply(first, n4)
    if len(n4coverage) == h - 4 and h > 5:
        n4coverage = remove(choice(totuple(n4coverage)), n4coverage)
    for ii in n4coverage:
        locj = choice([ij[1] for ij in sfilter(n4, lambda ij: ij[0] == ii)])
        gi = fill(gi, c3, {(ii, locj)})
        go = fill(go, c3, {(ii, w - 2)})
    noisecands = ofcolor(gi, bgc)
    noisecols = difference(cols, (bgc, c1, c2, c3, c4))
    nnoise = unifint(diff_lb, diff_ub, (0, len(noisecands)))
    ub = ((h * w) - 2 * h - 2 * (w - 2)) // 2 - ndots - 1
    nnoise = unifint(diff_lb, diff_ub, (0, max(0, ub)))
    noise = sample(totuple(noisecands), nnoise)
    noiseobj = {(choice(noisecols), ij) for ij in noise}
    gi = paint(gi, noiseobj)
    return {'input': gi, 'output': go}

