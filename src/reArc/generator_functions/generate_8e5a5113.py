def generate_8e5a5113(diff_lb: float, diff_ub: float) -> dict:
    colopts = interval(0, 10, 1)
    d = unifint(diff_lb, diff_ub, (2, 9))
    bgc = choice(colopts)
    remcols = remove(bgc, colopts)
    k = 4 if d < 7 else 3
    nbound = (2, k)
    num = unifint(diff_lb, diff_ub, nbound)
    rotfs = (identity, rot90, rot180, rot270)
    barc = choice(remcols)
    remcols = remove(barc, remcols)
    colbnds = (1, 8)
    ncols = unifint(diff_lb, diff_ub, colbnds)
    patcols = sample(remcols, ncols)
    bgcanv = canvas(bgc, (d, d))
    c = canvas(bgc, (d, d))
    inds = totuple(asindices(c))
    ncolbnds = (1, d ** 2 - 1)
    ncells = unifint(diff_lb, diff_ub, ncolbnds)
    indsss = sample(inds, ncells)
    for ij in indsss:
        c = fill(c, choice(patcols), {ij})
    barr = canvas(barc, (d, 1))
    fillinidx = choice(interval(0, num, 1))
    gi = rot90(rot270(c if fillinidx == 0 else bgcanv))
    go = rot90(rot270(c))
    for j in range(num - 1):
        c = rot90(c)
        gi = hconcat(hconcat(gi, barr), c if j + 1 == fillinidx else bgcanv)
        go = hconcat(hconcat(go, barr), c)
    if choice((True, False)):
        gi = rot90(gi)
        go = rot90(go)
    return {'input': gi, 'output': go}

