def generate_40853293(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    nlines = unifint(diff_lb, diff_ub, (2, min(8, (h*w)//2)))
    nhorilines = randint(1, nlines - 1)
    nvertilines = nlines - nhorilines
    ilocs = interval(0, h, 1)
    ilocs = sample(ilocs, min(nhorilines, len(ilocs)))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for ii in ilocs:
        llen = unifint(diff_lb, diff_ub, (2, w - 1))
        js = randint(0, w - llen)
        je = js + llen - 1
        a = (ii, js)
        b = (ii, je)
        hln = connect(a, b)
        col = choice(remcols)
        remcols = remove(col, remcols)
        gi = fill(gi, col, {a, b})
        go = fill(go, col, hln)
    jlocs = interval(0, w, 1)
    gim = dmirror(gi)
    jlocs = sfilter(jlocs, lambda j: sum(1 for e in gim[j] if e == bgc) > 1)
    nvertilines = min(nvertilines, len(jlocs))
    jlocs = sample(jlocs, nvertilines)
    for jj in jlocs:
        jcands = [idx for idx, e in enumerate(gim[jj]) if e == bgc]
        kk = len(jcands)
        locopts = interval(0, kk, 1)
        llen = unifint(diff_lb, diff_ub, (2, kk))
        sp = randint(0, kk - llen)
        ep = sp + llen - 1
        sp = jcands[sp]
        ep = jcands[ep]
        a = (sp, jj)
        b = (ep, jj)
        vln = connect(a, b)
        col = choice(remcols)
        remcols = remove(col, remcols)
        gi = fill(gi, col, {a, b})
        go = fill(go, col, vln)
    return {'input': gi, 'output': go}

