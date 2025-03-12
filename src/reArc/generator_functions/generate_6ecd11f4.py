def generate_6ecd11f4(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 7))
    w = unifint(diff_lb, diff_ub, (2, 7))
    bgc, fgc = sample(cols, 2)
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (2, 9))
    ccols = sample(remcols, ncols)
    inds = asindices(canvas(bgc, (h, w)))
    nlocsd = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    nlocs = choice((nlocsd, h * w - nlocsd))
    nlocs = min(max(3, nlocs), h * w - 1)
    sp = choice(totuple(inds))
    inds = remove(sp, inds)
    shp = {sp}
    for j in range(nlocs):
        ij = choice(totuple((inds - shp) & mapply(neighbors, shp)))
        shp.add(ij)
    shp = normalize(shp)
    h, w = shape(shp)
    canv = canvas(bgc, (h, w))
    objbase = fill(canv, fgc, shp)
    maxhscf = (2*h+h+1) // h
    maxwscf = (2*w+w+1) // w
    hscf = unifint(diff_lb, diff_ub, (2, maxhscf))
    wscf = unifint(diff_lb, diff_ub, (2, maxwscf))
    obj = asobject(hupscale(vupscale(objbase, hscf), wscf))
    oh, ow = shape(obj)
    inds = asindices(canv)
    objx = {(choice(ccols), ij) for ij in inds}
    if len(palette(objx)) == 1:
        objxodo = first(objx)
        objx = insert((choice(remove(objxodo[0], ccols)), objxodo[1]), remove(objxodo, objx))
    fullh = unifint(diff_lb, diff_ub, (hscf*h+h+1, 30))
    fullw = unifint(diff_lb, diff_ub, (wscf*w+w+1, 30))
    gi = canvas(bgc, (fullh, fullw))
    fullinds = asindices(gi)
    while True:
        loci = randint(0, fullh - oh)
        locj = randint(0, fullw - ow)
        loc = (loci, locj)
        gix = paint(gi, shift(obj, loc))
        ofc = ofcolor(gix, fgc)
        delt = (fullinds - ofc)
        delt2 = delt - mapply(neighbors, ofc)
        scands = sfilter(
            delt2,
            lambda ij: ij[0] <= fullh - oh and ij[1] <= fullw - ow
        )
        if len(scands) == 0:
            continue
        locc = choice(totuple(scands))
        shftd = shift(objx, locc)
        if toindices(shftd).issubset(delt2):
            gi = paint(gix, shftd)
            break
    go = paint(canv, objx)
    go = fill(go, bgc, ofcolor(objbase, bgc))
    return {'input': gi, 'output': go}

