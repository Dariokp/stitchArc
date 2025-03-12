def generate_5daaa586(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (7, 30))
    w = unifint(diff_lb, diff_ub, (7, 30))
    loci1 = randint(1, h - 4)
    locj1 = randint(1, w - 4)
    loci1dev = unifint(diff_lb, diff_ub, (0, loci1 - 1))
    locj1dev = unifint(diff_lb, diff_ub, (0, locj1 - 1))
    loci1 -= loci1dev
    locj1 -= locj1dev
    loci2 = unifint(diff_lb, diff_ub, (loci1 + 2, h - 2))
    locj2 = unifint(diff_lb, diff_ub, (locj1 + 2, w - 2))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    c1, c2, c3, c4 = sample(remcols, 4)
    f1 = recolor(c1, hfrontier(toivec(loci1)))
    f2 = recolor(c2, hfrontier(toivec(loci2)))
    f3 = recolor(c3, vfrontier(tojvec(locj1)))
    f4 = recolor(c4, vfrontier(tojvec(locj2)))
    gi = canvas(bgc, (h, w))
    fronts = [f1, f2, f3, f4]
    shuffle(fronts)
    for fr in fronts:
        gi = paint(gi, fr)
    cands = totuple(ofcolor(gi, bgc))
    nn = len(cands)
    nnoise = unifint(diff_lb, diff_ub, (1, max(1, nn // 3)))
    noise = sample(cands, nnoise)
    gi = fill(gi, c1, noise)
    while len(frontiers(gi)) > 4:
        gi = fill(gi, bgc, noise)
        nnoise = unifint(diff_lb, diff_ub, (1, max(1, nn // 3)))
        noise = sample(cands, nnoise)
        if len(set(noise) & ofcolor(gi, c1)) >= len(ofcolor(gi, bgc)):
            break
        gi = fill(gi, c1, noise)
    go = crop(gi, (loci1, locj1), (loci2 - loci1 + 1, locj2 - locj1 + 1))
    ns = ofcolor(go, c1)
    go = fill(go, c1, mapply(rbind(shoot, (-1, 0)), ns))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

