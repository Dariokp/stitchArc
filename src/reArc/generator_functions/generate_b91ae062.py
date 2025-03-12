def generate_b91ae062(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 5))
    w = unifint(diff_lb, diff_ub, (2, 5))
    numc = unifint(diff_lb, diff_ub, (3, min(h * w, min(10, 30 // max(h, w)))))
    ccols = sample(cols, numc)
    c = canvas(-1, (h, w))
    inds = totuple(asindices(c))
    fixinds = sample(inds, numc)
    obj = {(cc, ij) for cc, ij in zip(ccols, fixinds)}
    for ij in difference(inds, fixinds):
        obj.add((choice(ccols), ij))
    gi = paint(c, obj)
    go = upscale(gi, numc - 1)
    return {'input': gi, 'output': go}

