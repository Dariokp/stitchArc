def generate_d06dbe63(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(5, interval(0, 10, 1))
    obj1 = mapply(lbind(shift, frozenset({(-1, 0), (-2, 0), (-2, 1), (-2, 2)})), {(-k * 2, 2 * k) for k in range(15)})
    obj2 = mapply(lbind(shift, frozenset({(1, 0), (2, 0), (2, -1), (2, -2)})), {(2 * k, -k * 2) for k in range(15)})
    obj = obj1 | obj2
    objf = lambda ij: shift(obj, ij)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    ndots = unifint(diff_lb, diff_ub, (1, min(h, w)))
    succ = 0
    tr = 0
    maxtr = 4 * ndots
    bgc, dotc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    fullinds = asindices(gi)
    while tr < maxtr and succ < ndots:
        tr += 1
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        objx = objf(loc)
        if (objx & fullinds).issubset(inds):
            succ += 1
            inds = (inds - objx) - {loc}
            gi = fill(gi, dotc, {loc})
            go = fill(go, dotc, {loc})
            go = fill(go, 5, objx)
    return {'input': gi, 'output': go}

