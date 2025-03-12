def generate_6cdd2623(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (8, 30))
    w = unifint(diff_lb, diff_ub, (8, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    linc = choice(remcols)
    remcols = remove(linc, remcols)
    nnoisecols = unifint(diff_lb, diff_ub, (1, 7))
    noisecols = sample(remcols, nnoisecols)
    c = canvas(bgc, (h, w))
    ininds = totuple(shift(asindices(canvas(-1, (h-2, w-1))), (1, 1)))
    fixinds = sample(ininds, nnoisecols)
    fixobj = {(col, ij) for col, ij in zip(list(noisecols), fixinds)}
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    gi = paint(gi, fixobj)
    nnoise = unifint(diff_lb, diff_ub, (1, (h * w - nnoisecols) // 3))
    noise = sample(totuple(asindices(c) - set(fixinds)), nnoise)
    noise = {(choice(remcols), ij) for ij in noise}
    gi = paint(gi, noise)
    ilocs = interval(1, h - 1, 1)
    jlocs = interval(1, w - 1, 1)
    aa, bb = sample((0, 1), 2)
    nilocs = unifint(diff_lb, diff_ub, (aa, (h - 2) // 2))
    njlocs = unifint(diff_lb, diff_ub, (bb, (w - 2) // 2))
    ilocs = sample(ilocs, nilocs)
    jlocs = sample(jlocs, njlocs)
    for ii in ilocs:
        gi = fill(gi, linc, {(ii, 0)})
        gi = fill(gi, linc, {(ii, w - 1)})
        go = fill(go, linc, connect((ii, 0), (ii, w - 1)))
    for jj in jlocs:
        gi = fill(gi, linc, {(0, jj)})
        gi = fill(gi, linc, {(h - 1, jj)})
        go = fill(go, linc, connect((0, jj), (h - 1, jj)))
    return {'input': gi, 'output': go}

