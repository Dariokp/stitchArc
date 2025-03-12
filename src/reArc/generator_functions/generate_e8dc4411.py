def generate_e8dc4411(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)  
    h = unifint(diff_lb, diff_ub, (9, 30))
    w = unifint(diff_lb, diff_ub, (9, 30))
    d = unifint(diff_lb, diff_ub, (3, min(h, w)//2-1))
    bgc, objc, remc = sample(cols, 3)
    c = canvas(bgc, (d, d))
    inds = sfilter(asindices(c), lambda ij: ij[0]>=d//2 and ij[1]>=d//2)
    ncd = unifint(diff_lb, diff_ub, (1, len(inds)//2))
    nc = choice((ncd, len(inds)-ncd))
    nc = min(max(2, nc), len(inds) - 1)
    cells = sample(totuple(inds), nc)
    cells = set(cells) | {choice(((d//2, d//2), (d//2, d//2-1)))}
    cells = cells | {(jj, ii) for ii, jj in cells}
    for k in range(4):
        c = fill(c, objc, cells)
        c = rot90(c)
    while palette(toobject(box(asindices(c)), c)) == frozenset({bgc}) and height(c) > 3:
        c = trim(c)
    obj = ofcolor(c, objc)
    od = height(obj)
    loci = randint(1, h - 2*od)
    locj = randint(1, w - 2*od)
    obj = shift(obj, (loci, locj))
    bd = backdrop(obj)
    p = 0
    while len(shift(obj, (p, p)) & bd) > 0:
        p += 1
    obj2 = shift(obj, (p, p))
    nbhs = mapply(neighbors, obj)
    while len(obj2 & nbhs) == 0:
        nbhs = mapply(neighbors, nbhs)
    indic = obj2 & nbhs
    gi = canvas(bgc, (h, w))
    gi = fill(gi, objc, obj)
    gi = fill(gi, remc, indic)
    go = tuple(e for e in gi)
    for k in range(30):
        newg = fill(go, remc, shift(obj, (p*(k+1), p*(k+1))))
        if newg == go:
            break
        go = newg
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

