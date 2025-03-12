def generate_28bf18c6(diff_lb: float, diff_ub: float) -> dict:
    colopts = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(colopts)
    fgc = choice(remove(bgc, colopts))
    gi = canvas(bgc, (h, w))
    hb = unifint(diff_lb, diff_ub, (1, min(14, h - 1)))
    wb = unifint(diff_lb, diff_ub, (1, min(14, w - 1)))
    bounds = asindices(canvas(0, (hb, wb)))
    shp = {choice(totuple(corners(bounds)))}
    mp = (hb * wb) // 2
    dev = unifint(diff_lb, diff_ub, (0, mp))
    nc = choice((dev, hb * wb - dev))
    nc = max(0, min(hb * wb - 1, nc))
    for j in range(nc):
        shp.add(choice(totuple((bounds - shp) & mapply(neighbors, shp))))
    shp = normalize(shp)
    di = randint(0, h - height(shp))
    dj = randint(0, w - width(shp))
    shpp = shift(shp, (di, dj))
    gi = fill(gi, fgc, shpp)
    go = fill(canvas(bgc, shape(shp)), fgc, shp)
    go = hconcat(go, go)
    return {'input': gi, 'output': go}

