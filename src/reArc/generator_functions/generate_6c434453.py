def generate_6c434453(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(2, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    nobjs = unifint(diff_lb, diff_ub, (2, (h * w) // 16))
    succ = 0
    tr = 0
    maxtr = 5 * nobjs
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    while succ < nobjs and tr < maxtr:
        tr += 1
        if choice((True, False)):
            oh = choice((3, 5))
            ow = choice((3, 5))
            obji = box(frozenset({(0, 0), (oh - 1, ow - 1)}))
        else:
            oh = randint(1, 5)
            ow = randint(1, 5)
            bounds = asindices(canvas(-1, (oh, ow)))
            ncells = randint(1, oh * ow)
            obji = {choice(totuple(bounds))}
            for k in range(ncells - 1):
                obji.add(choice(totuple((bounds - obji) & mapply(dneighbors, obji))))
            obji = normalize(obji)
        oh, ow = shape(obji)
        flag = obji == box(obji) and set(shape(obji)).issubset({3, 5})
        if flag:
            objo = connect((0, ow//2), (oh - 1, ow//2)) | connect((oh//2, 0), (oh//2, ow - 1))
            tocover = backdrop(obji)
        else:
            objo = obji
            tocover = obji
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        loc = choice(totuple(cands))
        plcdi = shift(obji, loc)
        if plcdi.issubset(inds):
            plcdo = shift(objo, loc)
            succ += 1
            tocoveri = shift(tocover, loc)
            inds = (inds - tocoveri) - mapply(dneighbors, tocoveri)
            col = choice(ccols)
            gi = fill(gi, col, plcdi)
            go = fill(go, 2 if flag else col, plcdo)
    return {'input': gi, 'output': go}

