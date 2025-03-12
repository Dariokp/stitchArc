def generate_b190f7f5(diff_lb: float, diff_ub: float) -> dict:
    fullcols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 5))
    w = unifint(diff_lb, diff_ub, (2, 5))
    bgc = choice(fullcols)
    cols = remove(bgc, fullcols)
    c = canvas(bgc, (h, w))
    numcd = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    numc = choice((numcd, h * w - numcd))
    numc = min(max(1, numc), h * w - 1)
    numcd2 = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    numc2 = choice((numcd2, h * w - numcd2))
    numc2 = min(max(2, numc2), h * w - 1)
    inds = totuple(asindices(c))
    srclocs = sample(inds, numc)
    srccol = choice(cols)
    remcols = remove(srccol, cols)
    numcols = unifint(diff_lb, diff_ub, (2, 8))
    trglocs = sample(inds, numc2)
    ccols = sample(remcols, numcols)
    fixc1 = choice(ccols)
    trgobj = [(fixc1, trglocs[0]), (choice(remove(fixc1, ccols)), trglocs[1])] + [(choice(ccols), ij) for ij in trglocs[2:]]
    trgobj = frozenset(trgobj)
    gisrc = fill(c, srccol, srclocs)
    gitrg = paint(c, trgobj)
    catf = choice((hconcat, vconcat))
    ordd = choice(([gisrc, gitrg], [gitrg, gisrc]))
    gi = catf(*ordd)
    go = canvas(bgc, (h**2, w**2))
    for loc in trglocs:
        a, b = loc
        go = fill(go, gitrg[a][b], shift(srclocs, multiply(loc, (h, w))))
    return {'input': gi, 'output': go}

