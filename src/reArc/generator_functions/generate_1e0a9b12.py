def generate_1e0a9b12(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    ff = chain(dmirror, lbind(apply, rbind(order, identity)), dmirror)
    while True:
        h = unifint(diff_lb, diff_ub, (3, 30))
        w = unifint(diff_lb, diff_ub, (3, 30))
        nc = unifint(diff_lb, diff_ub, (1, w))
        bgc = choice(cols)
        gi = canvas(bgc, (h, w))
        remcols = remove(bgc, cols)
        scols = [choice(remcols) for j in range(nc)]
        slocs = sample(interval(0, w, 1), nc)
        inds = totuple(connect(ORIGIN, (h - 1, 0)))
        for c, l in zip(scols, slocs):
            nc2 = randint(1, h - 1)
            sel = sample(inds, nc2)
            gi = fill(gi, c, shift(sel, tojvec(l)))
        go = replace(ff(replace(gi, bgc, -1)), -1, bgc)
        if colorcount(gi, bgc) > argmax(remove(bgc, palette(gi)), lbind(colorcount, gi)):
            break
    return {'input': gi, 'output': go}

