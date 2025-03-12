def generate_c444b776(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 9))
    w = unifint(diff_lb, diff_ub, (2, 9))
    nh = unifint(diff_lb, diff_ub, (1, 3))
    nw = unifint(diff_lb, diff_ub, (1 if nh > 1 else 2, 3))
    bgclinc = sample(cols, 2)
    bgc, linc = bgclinc
    remcols = difference(cols, bgclinc)
    fullh = h * nh + (nh - 1)
    fullw = w * nw + (nw - 1)
    c = canvas(linc, (fullh, fullw))
    smallc = canvas(bgc, (h, w))
    inds = totuple(asindices(smallc))
    numcol = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, numcol)
    numcels = unifint(diff_lb, diff_ub, (1, (h * w) // 2))
    cels = sample(inds, numcels)
    obj = {(choice(ccols), ij) for ij in cels}
    smallcpainted = paint(smallc, obj)
    llocs = set()
    for a in range(0, fullh, h+1):
        for b in range(0, fullw, w + 1):
            llocs.add((a, b))
    llocs = tuple(llocs)
    srcloc = choice(llocs)
    obj = asobject(smallcpainted)
    gi = paint(c, shift(obj, srcloc))
    remlocs = remove(srcloc, llocs)
    bobj = asobject(smallc)
    for rl in remlocs:
        gi = paint(gi, shift(bobj, rl))
    go = tuple(e for e in gi)
    for rl in remlocs:
        go = paint(go, shift(obj, rl))
    return {'input': gi, 'output': go}

