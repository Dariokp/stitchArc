def generate_9dfd6313(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    dh = unifint(diff_lb, diff_ub, (1, 14))
    d = 2 * dh + 1
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    linc = choice(remcols)
    remcols = remove(linc, remcols)
    gi = canvas(bgc, (d, d))
    inds = asindices(gi)
    lni = randint(1, 4)
    if lni == 1:
        ln = connect((dh, 0), (dh, d - 1))
        mirrf = hmirror
        cands = sfilter(inds, lambda ij: ij[0] > dh)
    elif lni == 2:
        ln = connect((0, dh), (d - 1, dh))
        mirrf = vmirror
        cands = sfilter(inds, lambda ij: ij[1] > dh)
    elif lni == 3:
        ln = connect((0, 0), (d - 1, d - 1))
        mirrf = dmirror
        cands = sfilter(inds, lambda ij: ij[0] > ij[1])
    elif lni == 4:
        ln = connect((d - 1, 0), (0, d - 1))
        mirrf = cmirror
        cands = sfilter(inds, lambda ij: (ij[0] + ij[1]) > d)
    gi = fill(gi, linc, ln)
    mp = (d * (d - 1)) // 2
    numcols = unifint(diff_lb, diff_ub, (1, min(7, mp)))
    colsch = sample(remcols, numcols)
    numpix = unifint(diff_lb, diff_ub, (1, len(cands)))
    pixs = sample(totuple(cands), numpix)
    for pix in pixs:
        gi = fill(gi, choice(colsch), {pix})
    go = mirrf(gi)
    if choice((True, False)):
        gi, go = go, gi
    return {'input': gi, 'output': go}

