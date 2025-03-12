def generate_72ca375d(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // 25))
    srcobjh = unifint(diff_lb, diff_ub, (2, 8))
    srcobjwh = unifint(diff_lb, diff_ub, (1, 4))
    bnds = asindices(canvas(-1, (srcobjh, srcobjwh)))
    spi = randint(0, srcobjh - 1)
    sp = (spi, srcobjwh - 1)
    srcobj = {sp}
    bnds = remove(sp, bnds)
    ncellsd = unifint(diff_lb, diff_ub, (0, (srcobjh * srcobjwh) // 2))
    ncells1 = choice((ncellsd, srcobjh * srcobjwh - ncellsd))
    ncells2 = unifint(diff_lb, diff_ub, (1, srcobjh * srcobjwh))
    ncells = (ncells1 + ncells2) // 2
    ncells = min(max(1, ncells), srcobjh * srcobjwh, (h * w) // 2 - 1)
    for k in range(ncells - 1):
        srcobj.add(choice(totuple((bnds - srcobj) & mapply(neighbors, srcobj))))
    srcobj = normalize(srcobj)
    srcobj = srcobj | shift(vmirror(srcobj), (0, width(srcobj)))
    srcobjh, srcobjw = shape(srcobj)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    trgc = choice(remcols)
    go = canvas(bgc, (srcobjh, srcobjw))
    go = fill(go, trgc, srcobj)
    loci = randint(0, h - srcobjh)
    locj = randint(0, w - srcobjw)
    locc = (loci, locj)
    gi = canvas(bgc, (h, w))
    shftd = shift(srcobj, locc)
    gi = fill(gi, trgc, shftd)
    indss = asindices(gi)
    indss = (indss - shftd) - mapply(neighbors, shftd)
    maxtrials = 4 * nobjs
    tr = 0
    succ = 0
    remcands = asindices(canvas(-1, (8, 8))) - srcobj
    while succ < nobjs and tr <= maxtrials:
        if len(indss) == 0:
            break
        while True:
            newobj = {e for e in srcobj}
            numperti = unifint(diff_lb, diff_ub, (1, 63))
            numpert = 64 - numperti
            for np in range(numpert):
                isadd = choice((True, False))
                if isadd and len(newobj) < 64:
                    cndds = totuple((remcands - newobj) & mapply(neighbors, newobj))
                    if len(cndds) == 0:
                        break
                    newobj.add(choice(cndds))
                if not isadd and len(newobj) > 2:
                    newobj = remove(choice(totuple(newobj)), newobj)
            newobj = normalize(newobj)
            a, b = shape(newobj)
            cc = canvas(-1, (a+2, b+2))
            cc2 = compress(fill(cc, -2, shift(newobj, (1, 1))))
            newobj = toindices(argmax(colorfilter(objects(cc2, T, T, F), -2), size))
            if newobj != vmirror(newobj):
                break
        col = choice(remcols)
        loccands = sfilter(indss, lambda ij: shift(newobj, ij).issubset(indss))
        if len(loccands) == 0:
            tr += 1
            continue
        locc = choice(totuple(loccands))
        newobj = shift(newobj, locc)
        gi = fill(gi, col, newobj)
        succ += 1
        indss = (indss - newobj) - mapply(neighbors, newobj)
    return {'input': gi, 'output': go}

