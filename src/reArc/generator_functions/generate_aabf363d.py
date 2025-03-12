def generate_aabf363d(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 28))
    w = unifint(diff_lb, diff_ub, (3, 28))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    cola = choice(remcols)
    remcols = remove(cola, remcols)
    colb = choice(remcols)
    c = canvas(bgc, (h, w))
    bounds = asindices(c)
    sp = choice(totuple(bounds))
    ub = min(h * w - 1, max(1, (2/3) * h * w))
    ncells = unifint(diff_lb, diff_ub, (1, ub))
    shp = {sp}
    for k in range(ncells):
        ij = choice(totuple((bounds - shp) & mapply(neighbors, shp)))
        shp.add(ij)
    shp = shift(shp, (1, 1))
    c2 = canvas(bgc, (h+2, w+2))
    gi = fill(c2, cola, shp)
    go = fill(c2, colb, shp)
    gi = fill(gi, colb, {choice(totuple(ofcolor(gi, bgc)))})
    return {'input': gi, 'output': go}

