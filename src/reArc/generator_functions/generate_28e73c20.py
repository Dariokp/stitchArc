def generate_28e73c20(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (3,))
    direcmapper = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1)}
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    sp = (0, w - 1)
    direc = (1, 0)
    ncols = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(cols, ncols)
    gi = canvas(-1, (h, w))
    inds = asindices(gi)
    obj = {(choice(ccols), ij) for ij in inds}
    gi = paint(gi, obj)
    go = fill(gi, 3, connect((0, 0), sp))
    lw = w
    lh = h
    ld = h
    isverti = False
    while ld > 0:
        lw -= 1
        lh -= 1
        ep = add(sp, multiply(direc, ld - 1))
        ln = connect(sp, ep)
        go = fill(go, 3, ln)
        direc = direcmapper[direc]
        if isverti:
            ld = lh
        else:
            ld = lw
        isverti = not isverti
        sp = ep
    gi = dmirror(dmirror(gi)[1:])
    go = dmirror(dmirror(go)[1:])
    return {'input': gi, 'output': go}

