def generate_6f8cd79b(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(8, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    ncells = unifint(diff_lb, diff_ub, (0, h * w))
    inds = asindices(gi)
    cells = sample(totuple(inds), ncells)
    obj = {(choice(ccols), ij) for ij in cells}
    gi = paint(gi, obj)
    brd = box(inds)
    go = fill(gi, 8, brd)
    return {'input': gi, 'output': go}

