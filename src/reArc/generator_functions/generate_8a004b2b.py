def generate_8a004b2b(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    oh = unifint(diff_lb, diff_ub, (2, h//5))
    ow = unifint(diff_lb, diff_ub, (2, w//5))
    bounds = asindices(canvas(-1, (oh, ow)))
    bgc, cornc, ac1, ac2, objc = sample(cols, 5)
    gi = canvas(bgc, (h, w))
    obj = {choice(totuple(bounds))}
    ncellsd = unifint(diff_lb, diff_ub, (0, (oh * ow) // 2))
    ncells = choice((ncellsd, oh * ow - ncellsd))
    ncells = min(max(3, ncells), oh * ow)
    for k in range(ncells - 1):
        obj.add(choice(totuple((bounds - obj) & mapply(neighbors, obj))))
    obj = normalize(obj)
    oh, ow = shape(obj)
    fp1 = choice(totuple(obj))
    fp2 = choice(remove(fp1, totuple(obj)))
    remobj = obj - {fp1, fp2}
    obj = recolor(objc, remobj) | {(ac1, fp1), (ac2, fp2)}
    maxhscf = (h - oh - 4) // oh
    maxwscf = (w - ow - 4) // ow
    hscf = unifint(diff_lb, diff_ub, (1, maxhscf))
    wscf = unifint(diff_lb, diff_ub, (1, maxwscf))
    loci = randint(0, 2)
    locj = randint(0, 2)
    oplcd = shift(obj, (loci, locj))
    gi = paint(gi, oplcd)
    inh = hscf * oh
    inw = wscf * ow
    sqh = unifint(diff_lb, diff_ub, (inh + 2, h - oh - 2))
    sqw = unifint(diff_lb, diff_ub, (inw + 2, w))
    sqloci = randint(loci+oh, h - sqh)
    sqlocj = randint(0, w - sqw)
    crns = corners(frozenset({(sqloci, sqlocj), (sqloci + sqh - 1, sqlocj + sqw - 1)}))
    gi = fill(gi, cornc, crns)
    gomini = subgrid(oplcd, gi)
    goo = vupscale(hupscale(gomini, wscf), hscf)
    goo = asobject(goo)
    gloci = randint(sqloci+1, sqloci+sqh-1-height(goo))
    glocj = randint(sqlocj+1, sqlocj+sqw-1-width(goo))
    gooplcd = shift(goo, (gloci, glocj))
    go = paint(gi, gooplcd)
    go = subgrid(crns, go)
    indic = sfilter(gooplcd, lambda cij: cij[0] in (ac1, ac2))
    gi = paint(gi, indic)
    if choice((True, False)) and len(obj) > 3:
        idx = choice(totuple(toindices(sfilter(obj, lambda cij: cij[0] == objc))))
        idxi, idxj = idx
        xx = shift(asindices(canvas(-1, (hscf, wscf))), (gloci+idxi*hscf, glocj+idxj*wscf))
        gi = fill(gi, objc, xx)
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

