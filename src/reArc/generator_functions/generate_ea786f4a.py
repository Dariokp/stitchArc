def generate_ea786f4a(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (1, 14))
    w = unifint(diff_lb, diff_ub, (1, 14))
    mp = (h, w)
    h = 2 * h + 1
    w = 2 * w + 1
    linc = choice(cols)
    remcols = remove(linc, cols)
    gi = canvas(linc, (h, w))
    inds = remove(mp, asindices(gi))
    ncols = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(remcols, ncols)
    obj = {(choice(ccols), ij) for ij in inds}
    gi = paint(gi, obj)
    ln1 = shoot(mp, (-1, -1))
    ln2 = shoot(mp, (1, 1))
    ln3 = shoot(mp, (-1, 1))
    ln4 = shoot(mp, (1, -1))
    go = fill(gi, linc, ln1 | ln2 | ln3 | ln4)
    return {'input': gi, 'output': go}

