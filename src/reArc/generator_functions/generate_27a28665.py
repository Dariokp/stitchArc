def generate_27a28665(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    mapping = [
    (1, {(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)}),
    (2, {(0, 0), (1, 1), (2, 0), (0, 2), (2, 2)}),
    (3, {(2, 0), (0, 1), (0, 2), (1, 1), (1, 2)}),
    (6, {(1, 1), (0, 1), (1, 0), (1, 2), (2, 1)})
    ]
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    col, obj = choice(mapping)
    bgc, objc = sample(cols, 2)
    fac = unifint(diff_lb, diff_ub, (1, min(h, w) // 3))
    go = canvas(col, (1, 1))
    gi = canvas(bgc, (h, w))
    canv = canvas(bgc, (3, 3))
    canv = fill(canv, objc, obj)
    canv = upscale(canv, fac)
    obj = asobject(canv)
    loci = randint(0, h - 3 * fac)
    locj = randint(0, w - 3 * fac)
    loc = (loci, locj)
    gi = paint(gi, shift(obj, loc))
    return {'input': gi, 'output': go}

