def generate_694f12f3(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2))
    h = unifint(diff_lb, diff_ub, (9, 30))
    w = unifint(diff_lb, diff_ub, (9, 30))
    seploc = randint(4, h - 5)
    bigh = unifint(diff_lb, diff_ub, (4, seploc))
    bigw = unifint(diff_lb, diff_ub, (3, w - 1))
    bigloci = randint(0, seploc - bigh)
    biglocj = randint(0, w - bigw)
    smallmaxh = h - seploc - 1
    smallmaxw = w - 1
    cands = []
    bigsize = bigh * bigw
    for a in range(3, smallmaxh+1):
        for b in range(3, smallmaxw+1):
            if a * b < bigsize:
                cands.append((a, b))
    cands = sorted(cands, key=lambda ab: ab[0]*ab[1])
    num = len(cands)
    idx = unifint(diff_lb, diff_ub, (0, num - 1))
    smallh, smallw = cands[idx]
    smallloci = randint(seploc+1, h - smallh)
    smalllocj = randint(0, w - smallw)
    bgc, sqc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    bigsq = backdrop(frozenset({(bigloci, biglocj), (bigloci + bigh - 1, biglocj + bigw - 1)}))
    smallsq = backdrop(frozenset({(smallloci, smalllocj), (smallloci + smallh - 1, smalllocj + smallw - 1)}))
    gi = fill(gi, sqc, bigsq | smallsq)
    go = fill(gi, 2, backdrop(inbox(bigsq)))
    go = fill(go, 1, backdrop(inbox(smallsq)))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

