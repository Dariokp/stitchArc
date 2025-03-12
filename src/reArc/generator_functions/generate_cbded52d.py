def generate_cbded52d(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    oh = unifint(diff_lb, diff_ub, (1, 4))
    ow = unifint(diff_lb, diff_ub, (1, 4))
    numh = unifint(diff_lb, diff_ub, (3, 31 // (oh + 1)))
    numw = unifint(diff_lb, diff_ub, (3, 31 // (ow + 1)))
    bgc, linc = sample(cols, 2)
    remcols = difference(cols, (bgc, linc))
    ncols = unifint(diff_lb, diff_ub, (1, min(8, (numh * numh) // 3)))
    ccols = sample(remcols, ncols)
    fullh = numh * oh + numh - 1
    fullw = numw * ow + numw - 1
    gi = canvas(linc, (fullh, fullw))
    sgi = asindices(canvas(bgc, (oh, ow)))
    for a in range(numh):
        for b in range(numw):
            gi = fill(gi, bgc, shift(sgi, (a * (oh + 1), b * (ow + 1))))
    go = tuple(e for e in gi)
    for col in ccols:
        inds = ofcolor(go, bgc)
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        narms = randint(1, 4)
        armdirs = sample(totuple(dneighbors((0, 0))), narms)
        succ = 0
        for armdir in armdirs:
            x, y = armdir
            arm = []
            for k in range(1, max(numh, numw)):
                nextloc = add(loc, (k * x * (oh + 1), k * y * (ow + 1)))
                if nextloc not in inds:
                    break
                arm.append(nextloc)
            if len(arm) < 2:
                continue
            aidx = unifint(diff_lb, diff_ub, (1, len(arm) - 1))
            endp = arm[aidx]
            gi = fill(gi, col, {endp})
            go = fill(go, col, set(arm[:aidx+1]))
            succ += 1
        if succ > 0:
            gi = fill(gi, col, {loc})
            go = fill(go, col, {loc})
    return {'input': gi, 'output': go}

