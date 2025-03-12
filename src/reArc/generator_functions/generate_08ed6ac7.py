def generate_08ed6ac7(diff_lb: float, diff_ub: float) -> dict:
    colopts = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc = choice(difference(colopts, (1, 2, 3, 4)))
    remcols = remove(bgc, colopts)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    barrange = (4, w)
    locopts = interval(0, w, 1)
    nbars = unifint(diff_lb, diff_ub, barrange)
    barlocs = sample(locopts, nbars)
    barhopts = interval(0, h, 1)
    barhs = sample(barhopts, 4)
    barcols = [choice(remcols) for j in range(nbars)]
    barhsfx = [choice(barhs) for j in range(nbars - 4)] + list(barhs)
    shuffle(barhsfx)
    ordered = sorted(barhs)
    colord = interval(1, 5, 1)
    for col, (loci, locj) in zip(barcols, list(zip(barhsfx, barlocs))):
        bar = connect((loci, locj), (h - 1, locj))
        gi = fill(gi, col, bar)
        go = fill(go, colord[ordered.index(loci)], bar)
    return {'input': gi, 'output': go}

