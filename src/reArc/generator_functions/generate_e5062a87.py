def generate_e5062a87(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(1, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    eligcol, objc = sample(cols, 2)
    gi = canvas(eligcol, (h, w))
    inds = asindices(gi)
    sp = choice(totuple(inds))
    obj = {sp}
    ncells = unifint(diff_lb, diff_ub, (3, 9))
    for k in range(ncells - 1):
        obj.add(choice(totuple((inds - obj) & mapply(neighbors, obj))))
    obj = normalize(obj)
    nnoise = unifint(diff_lb, diff_ub, (int(0.2*h*w), int(0.5*h*w)))
    locs = sample(totuple(inds), nnoise)
    gi = fill(gi, 0, locs)
    noccs = unifint(diff_lb, diff_ub, (2, max(2, (h * w) // (len(obj) * 3))))
    oh, ow = shape(obj)
    for k in range(noccs):
        loci = randint(0, h - oh)
        locj = randint(0, w - ow)
        loc = (loci, locj)
        gi = fill(gi, objc if k == noccs - 1 else 0, shift(obj, loc))
    occs = occurrences(gi, recolor(0, obj))
    res = mapply(lbind(shift, obj), occs)
    go = fill(gi, objc, res)
    return {'input': gi, 'output': go}

