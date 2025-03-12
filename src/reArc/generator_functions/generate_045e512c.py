def generate_045e512c(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (11, 30))
    w = unifint(diff_lb, diff_ub, (11, 30))
    while True:
        oh = unifint(diff_lb, diff_ub, (2, min(4, (h - 2) // 3)))
        ow = unifint(diff_lb, diff_ub, (2, min(4, (w - 2) // 3)))
        bounds = asindices(canvas(-1, (oh, ow)))
        c1 = choice(totuple(connect((0, 0), (oh - 1, 0))))
        c2 = choice(totuple(connect((0, 0), (0, ow - 1))))
        c3 = choice(totuple(connect((oh - 1, ow - 1), (oh - 1, 0))))
        c4 = choice(totuple(connect((oh - 1, ow - 1), (0, ow - 1))))
        obj = {c1, c2, c3, c4}
        remcands = totuple(bounds - obj)
        ncells = unifint(diff_lb, diff_ub, (0, len(remcands)))
        for k in range(ncells):
            loc = choice(remcands)
            obj.add(loc)
            remcands = remove(loc, remcands)
        objt = normalize(obj)
        cc = canvas(0, shape(obj))
        cc = fill(cc, 1, objt)
        if len(colorfilter(objects(cc, T, T, F), 1)) == 1:
            break
    loci = randint(oh + 1, h - 2 * oh - 1)
    locj = randint(ow + 1, w - 2 * ow - 1)
    loc = (loci, locj)
    bgc, objc = sample(cols, 2)
    remcols = remove(bgc, remove(objc, cols))
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    obj = shift(recolor(objc, obj), loc)
    gi = paint(gi, obj)
    go = paint(go, obj)
    options = totuple(neighbors((0, 0)))
    ndirs = unifint(diff_lb, diff_ub, (1, 8))
    dirs = sample(options, ndirs)
    dcols = [choice(ccols) for k in range(ndirs)]
    hbars = hfrontier((loci - 2, 0)) | hfrontier((loci+oh+1, 0))
    vbars = vfrontier((0, locj - 2)) | vfrontier((0, locj+ow+1))
    bars = hbars | vbars
    ofs = increment((oh, ow))
    for direc, col in zip(dirs, dcols):
        indicatorobj = shift(obj, multiply(direc, increment((oh, ow))))
        indicatorobj = sfilter(indicatorobj, lambda cij: cij[1] in bars)
        nindsd = unifint(diff_lb, diff_ub, (0, len(indicatorobj) - 1))
        ninds = len(indicatorobj) - nindsd
        indicatorobj = set(sample(totuple(indicatorobj), ninds))
        if len(indicatorobj) > 0 and len(indicatorobj) < len(obj):
            gi = fill(gi, col, indicatorobj)
            for k in range(1, 10):
                go = fill(go, col, shift(obj, multiply(multiply(k, direc), ofs)))
    return {'input': gi, 'output': go}

