def generate_a740d043(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(0, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    ncd = unifint(diff_lb, diff_ub, (1, max(1, ((h-1) * (w-1)) // 2)))
    nc = choice((ncd, (h-1) * (w-1) - ncd))
    nc = min(max(1, ncd), (h-1) * (w-1) - 1)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numc = unifint(diff_lb, diff_ub, (1, len(remcols)))
    remcols = sample(remcols, numc)
    c = canvas(bgc, (h, w))
    bounds = asindices(canvas(-1, (h - 1, w - 1)))
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
    obj = {(choice(remcols), ij) for ij in plcd}
    gi = paint(c, obj)
    go = compress(gi)
    go = replace(go, bgc, 0)
    return {'input': gi, 'output': go}

