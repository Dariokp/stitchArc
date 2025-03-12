def generate_d6ad076f(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(8, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    inh = unifint(diff_lb, diff_ub, (3, h))
    inw = unifint(diff_lb, diff_ub, (3, w))
    bgc, c1, c2 = sample(cols, 3)
    itv = interval(0, inh, 1)
    loci2i = unifint(diff_lb, diff_ub, (2, inh - 1))
    loci2 = itv[loci2i]
    itv = itv[:loci2i-1][::-1]
    loci1i = unifint(diff_lb, diff_ub, (0, len(itv) - 1))
    loci1 = itv[loci1i]
    cp = randint(1, inw - 2)
    ajs = randint(0, cp - 1)
    aje = randint(cp + 1, inw - 1)
    bjs = randint(0, cp - 1)
    bje = randint(cp + 1, inw - 1)
    obja = backdrop(frozenset({(0, ajs), (loci1, aje)}))
    objb = backdrop(frozenset({(loci2, bjs), (inh - 1, bje)}))
    c = canvas(bgc, (inh, inw))
    c = fill(c, c1, obja)
    c = fill(c, c2, objb)
    obj = asobject(c)
    loci = randint(0, h - inh)
    locj = randint(0, w - inw)
    loc = (loci, locj)
    obj = shift(obj, loc)
    gi = canvas(bgc, (h, w))
    gi = paint(gi, obj)
    midobj = backdrop(frozenset({(loci1 + 1, max(ajs, bjs) + 1), (loci2 - 1, min(aje, bje) - 1)}))
    go = fill(gi, 8, shift(midobj, loc))
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

