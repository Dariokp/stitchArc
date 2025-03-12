def generate_2bee17df(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (7, 30))
    w = unifint(diff_lb, diff_ub, (7, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    c = canvas(bgc, (h, w))
    indord1 = apply(tojvec, interval(0, w, 1))
    indord2 = apply(rbind(astuple, w - 1), interval(1, h - 1, 1))
    indord3 = apply(lbind(astuple, h - 1), interval(w - 1, 0, -1))
    indord4 = apply(toivec, interval(h - 1, 0, -1))
    indord = indord1 + indord2 + indord3 + indord4
    k = len(indord)
    sp = randint(0, k)
    arr = indord[sp:] + indord[:sp]
    ep = randint(k // 2 - 3, k // 2 + 1)
    a = arr[:ep]
    b = arr[ep:]
    cola = choice(remcols)
    remcols = remove(cola, remcols)
    colb = choice(remcols)
    gi = fill(c, cola, a)
    gi = fill(gi, colb, b)
    nr = unifint(diff_lb, diff_ub, (1, min(4, min(h, w) // 2)))
    for kk in range(nr):
        ring = box(frozenset({(1 + kk, 1 + kk), (h - 1 - kk, w - 1 - kk)}))
        for br in (cola, colb):
            blacks = ofcolor(gi, br)
            bcands = totuple(ring & ofcolor(gi, bgc) & mapply(dneighbors, ofcolor(gi, br)))
            jj = len(bcands)
            jj2 = randint(max(0, jj // 2 - 2), min(jj, jj // 2 + 1))
            ss = sample(bcands, jj2)
            gi = fill(gi, br, ss)
    res = shift(merge(frontiers(trim(gi))), (1, 1))
    go = fill(gi, 3, res)
    return {'input': gi, 'output': go}

