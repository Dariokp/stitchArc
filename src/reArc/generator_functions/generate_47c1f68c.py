def generate_47c1f68c(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(1, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 14))
    w = unifint(diff_lb, diff_ub, (2, 14))
    bgc, linc = sample(cols, 2)
    remcols = difference(cols, (bgc, linc))
    objc = choice(remcols)
    canv = canvas(bgc, (h, w))
    nc = unifint(diff_lb, diff_ub, (1, h * w - 1))
    bx = asindices(canv)
    obj = {choice(totuple(bx))}
    for kk in range(nc - 1):
        dns = mapply(neighbors, obj)
        ch = choice(totuple(bx & dns))
        obj.add(ch)
        bx = bx - {ch}
    obj = recolor(objc, obj)
    gi = paint(canv, obj)
    gi1 = hconcat(hconcat(gi, canvas(linc, (h, 1))), canv)
    gi2 = hconcat(hconcat(canv, canvas(linc, (h, 1))), canv)
    gi = vconcat(vconcat(gi1, canvas(linc, (1, 2*w+1))), gi2)
    go = paint(canv, obj)
    go = hconcat(go, vmirror(go))
    go = vconcat(go, hmirror(go))
    go = replace(go, objc, linc)
    scf = choice((identity, hmirror, vmirror, compose(hmirror, vmirror)))
    gi = scf(gi)
    go = scf(go)
    return {'input': gi, 'output': go}

