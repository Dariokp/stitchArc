def generate_f25fbde4(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    ncd = unifint(diff_lb, diff_ub, (1, max(1, (min(15, h-1) * min(15, w-1)) // 2)))
    nc = choice((ncd, (h-1) * (w-1) - ncd))
    nc = min(max(1, ncd), (h-1) * (w-1) - 1)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    c = canvas(bgc, (h, w))
    bounds = asindices(canvas(-1, (min(15, h - 1), min(15, w - 1))))
    ch = choice(totuple(bounds))
    shp = {ch}
    bounds = remove(ch, bounds)
    for j in range(nc):
        shp.add(choice(totuple((bounds - shp) & mapply(neighbors, shp))))
    shp = normalize(shp)
    oh, ow = shape(shp)
    loci = randint(0, h - oh)
    locj = randint(0, w - ow)
    loc = (loci, locj)
    plcd = shift(shp, loc)
    gi = fill(c, fgc, plcd)
    go = compress(gi)
    go = upscale(go, 2)
    return {'input': gi, 'output': go}

