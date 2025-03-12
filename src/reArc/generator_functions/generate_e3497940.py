def generate_e3497940(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (3, 14))
    bgc, barc = sample(cols, 2)
    remcols = remove(barc, remove(bgc, cols))
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    nlinesocc = unifint(diff_lb, diff_ub, (1, h))
    lopts = interval(0, h, 1)
    linesocc = sample(lopts, nlinesocc)
    rs = canvas(bgc, (h, w))
    ls = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for idx in linesocc:
        j = unifint(diff_lb, diff_ub, (1, w - 1))
        obj = [(choice(ccols), (idx, jj)) for jj in range(j)]
        go = paint(go, obj)
        slen = randint(1, j)
        obj2 = obj[:slen]
        if choice((True, False)):
            obj, obj2 = obj2, obj
        rs = paint(rs, obj)
        ls = paint(ls, obj2)
    gi = hconcat(hconcat(vmirror(ls), canvas(barc, (h, 1))), rs)
    go = vmirror(go)
    return {'input': gi, 'output': go}

