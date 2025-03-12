def generate_ac0a08a4(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 5))
    w = unifint(diff_lb, diff_ub, (2, 5))
    num = unifint(diff_lb, diff_ub, (1, min(min(9, h * w - 2), min(30//h, 30//w))))
    bgc = choice(cols)
    c = canvas(bgc, (h, w))
    inds = asindices(c)
    locs = sample(totuple(inds), num)
    remcols = remove(bgc, cols)
    obj = {(col, loc) for col, loc in zip(sample(remcols, num), locs)}
    gi = paint(c, obj)
    go = upscale(gi, num)
    return {'input': gi, 'output': go}

