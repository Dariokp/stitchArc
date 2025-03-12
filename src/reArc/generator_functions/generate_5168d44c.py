def generate_5168d44c(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (7, 30))
    w = unifint(diff_lb, diff_ub, (7, 30))
    doth = unifint(diff_lb, diff_ub, (1, h//3))
    dotw = unifint(diff_lb, diff_ub, (1, w//3))
    borderh = unifint(diff_lb, diff_ub, (1, h//4))
    borderw = unifint(diff_lb, diff_ub, (1, w//4))
    direc = choice((DOWN, RIGHT, UNITY))
    dotloci = randint(0, h - doth - 1 if direc == RIGHT else h - doth - borderh - 1)
    dotlocj = randint(0, w - dotw - 1 if direc == DOWN else w - dotw - borderw - 1)
    dotloc = (dotloci, dotlocj)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    dotcol = choice(remcols)
    remcols = remove(dotcol, remcols)
    boxcol = choice(remcols)
    gi = canvas(bgc, (h, w))
    dotshap = (doth, dotw)
    starterdot = backdrop(frozenset({dotloc, add(dotloc, decrement(dotshap))}))
    bordershap = (borderh, borderw)
    offset = add(multiply(direc, dotshap), multiply(direc, bordershap))
    itv = interval(-15, 16, 1)
    itv = apply(lbind(multiply, offset), itv)
    dots = mapply(lbind(shift, starterdot), itv)
    gi = fill(gi, dotcol, dots)
    protobx = backdrop(frozenset({
        (dotloci - borderh, dotlocj - borderw),
        (dotloci + doth + borderh - 1, dotlocj + dotw + borderw - 1),
    }))
    bx = protobx - starterdot
    bxshifted = shift(bx, offset)
    go = fill(gi, boxcol, bxshifted)
    gi = fill(gi, boxcol, bx)
    return {'input': gi, 'output': go}

