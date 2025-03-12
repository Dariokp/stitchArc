def generate_760b3cac(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    objL = frozenset({(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)})
    objR = vmirror(objL)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (3, 14))
    w = 2 * w + 1
    bgc, objc, indc = sample(cols, 3)
    objh = unifint(diff_lb, diff_ub, (1, h - 3))
    objw = unifint(diff_lb, diff_ub, (1, w // 6))
    objw = 2 * objw + 1
    c = canvas(-1, (objh, objw))
    gi = canvas(bgc, (h, w))
    if choice((True, False)):
        obj = objL
        sgn = -1
    else:
        obj = objR
        sgn = 1
    gi = fill(gi, indc, shift(obj, (h - 3, w//2 - 1)))
    inds = asindices(c)
    sp = choice(totuple(inds))
    objx = {sp}
    numcd = unifint(diff_lb, diff_ub, (0, (objh * objw) // 2))
    numc = choice((numcd, objh * objw - numcd))
    numc = min(max(1, numc), objh * objw)
    for k in range(numc - 1):
        objx.add(choice(totuple((inds - objx) & mapply(neighbors, objx))))
    while width(objx) != objw:
        objx.add(choice(totuple((inds - objx) & mapply(neighbors, objx))))
    objx = normalize(objx)
    objh, objw = shape(objx)
    loci = randint(0, h - 3 - objh)
    locj = w//2 - objw//2
    loc = (loci, locj)
    plcd = shift(objx, loc)
    gi = fill(gi, objc, plcd)
    objx2 = vmirror(plcd)
    plcd2 = shift(objx2, (0, objw * sgn))
    go = fill(gi, objc, plcd2)
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

