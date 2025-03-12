def generate_1f876c06(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    nlns = unifint(diff_lb, diff_ub, (1, min(min(h, w), 9)))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ccols = sample(remcols, nlns)
    succ = 0
    tr = 0
    maxtr = 10 * nlns
    direcs = ineighbors((0, 0))
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    while succ < nlns and tr < maxtr:
        tr += 1
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        lns = []
        for direc in direcs:
            ln = [loc]
            ofs = 1
            while True:
                nextpix = add(loc, multiply(ofs, direc))
                ofs += 1
                if nextpix not in inds:
                    break
                ln.append(nextpix)
            if len(ln) > 2:
                lns.append(ln)
        if len(lns) > 0:
            succ += 1
            lns = sorted(lns, key=len)
            idx = unifint(diff_lb, diff_ub, (0, len(lns) - 1))
            ln = lns[idx]
            col = ccols[0]
            ccols = ccols[1:]
            gi = fill(gi, col, {ln[0], ln[-1]})
            go = fill(go, col, set(ln))
            inds = inds - set(ln)
    return {'input': gi, 'output': go}

