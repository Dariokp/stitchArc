def generate_90f3ed37(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(1, interval(0, 10, 1))
    while True:
        h = unifint(diff_lb, diff_ub, (8, 30))
        w = unifint(diff_lb, diff_ub, (8, 30))
        pathh = unifint(diff_lb, diff_ub, (1, max(1, h//4)))
        pathh = unifint(diff_lb, diff_ub, (pathh, max(1, h//4)))
        Lpatper = unifint(diff_lb, diff_ub, (1, w//7))
        Rpatper = unifint(diff_lb, diff_ub, (1, w//7))
        hh = randint(1, pathh)
        Linds = asindices(canvas(-1, (hh, Lpatper)))
        Rinds = asindices(canvas(-1, (hh, Rpatper)))
        lpatsd = unifint(diff_lb, diff_ub, (0, (hh * Lpatper) // 2))
        rpatsd = unifint(diff_lb, diff_ub, (0, (hh * Rpatper) // 2))
        lpats = choice((lpatsd, hh * Lpatper - lpatsd))
        rpats = choice((rpatsd, hh * Rpatper - rpatsd))
        lpats = min(max(Lpatper, lpats), hh * Lpatper)
        rpats = min(max(Rpatper, rpats), hh * Rpatper)
        lpat = set(sample(totuple(Linds), lpats))
        rpat = set(sample(totuple(Rinds), rpats))
        midpatw = randint(0, w-2*Lpatper-2*Rpatper)
        if midpatw == 0 or Lpatper == hh == 1:
            midpat = set()
            midpatw = 0
        else:
            midpat = set(sample(totuple(asindices(canvas(-1, (hh, midpatw)))), randint(midpatw, (hh * midpatw))))
        if shift(midpat, (0, 2*Lpatper-midpatw)).issubset(lpat):
            midpat = set()
            midpatw = 0
        loci = randint(0, h - pathh)
        lplac = shift(lpat, (loci, 0)) | shift(lpat, (loci, Lpatper))
        mplac = shift(midpat, (loci, 2*Lpatper))
        rplac = shift(rpat, (loci, 2*Lpatper+midpatw)) | shift(rpat, (loci, 2*Lpatper+midpatw+Rpatper))
        sp = 2*Lpatper+midpatw+Rpatper
        for k in range(w//Lpatper+1):
            lplac |= shift(lpat, (loci, -k*Lpatper))
        for k in range(w//Rpatper+1):
            rplac |= shift(rpat, (loci, sp+k*Rpatper))
        pat = lplac | mplac | rplac
        patn = shift(pat, (-loci, 0))
        bgc, fgc = sample(cols, 2)
        gi = canvas(bgc, (h, w))
        gi = fill(gi, fgc, pat)
        options = interval(0, h - pathh + 1, 1)
        options = difference(options, interval(loci-pathh-1, loci+2*pathh, 1))
        nplacements = unifint(diff_lb, diff_ub, (1, max(1, len(options) // pathh)))
        go = tuple(e for e in gi)
        for k in range(nplacements):
            if len(options) == 0:
                break
            locii = choice(options)
            options = difference(options, interval(locii-pathh-1, locii+2*pathh, 1))
            hoffs = randint(0, max(Rpatper, w-sp-2))
            cutoffopts = interval(2*Lpatper+midpatw, 2*Lpatper+midpatw+hoffs+1, 1)
            cutoffopts = cutoffopts[::-1]
            idx = unifint(diff_lb, diff_ub, (0, len(cutoffopts) - 1))
            cutoff = cutoffopts[idx]
            patnc = sfilter(patn, lambda ij: ij[1] <= cutoff)
            go = fill(go, 1, shift(patn, (locii, hoffs)))
            gi = fill(gi, fgc, shift(patnc, (locii, hoffs)))
            go = fill(go, fgc, shift(patnc, (locii, hoffs)))
        if 1 in palette(go):
            break
    return {'input': gi, 'output': go}

