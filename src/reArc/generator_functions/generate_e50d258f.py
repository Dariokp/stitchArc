def generate_e50d258f(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(2, interval(0, 10, 1))    
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    padcol = choice(remcols)
    remcols = remove(padcol, remcols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    num = unifint(diff_lb, diff_ub, (1, 10))
    indss = asindices(gi)
    maxtrials = 4 * num
    tr = 0
    succ = 0
    bound = None
    go = None
    while succ < num and tr <= maxtrials:
        if len(remcols) == 0 or len(indss) == 0:
            break
        oh = randint(3, 8)
        ow = randint(3, 8)
        subs = totuple(sfilter(indss, lambda ij: ij[0] < h - oh and ij[1] < w - ow))
        if len(subs) == 0:
            tr += 1
            continue
        loci, locj = choice(subs)
        obj = frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)})
        bd = backdrop(obj)
        if bd.issubset(indss):
            numcc = unifint(diff_lb, diff_ub, (1, 7))
            ccols = sample(remcols, numcc)
            if succ == 0:
                numred = unifint(diff_lb, diff_ub, (1, oh * ow))
                bound = numred
            else:
                numred = unifint(diff_lb, diff_ub, (0, min(oh * ow, bound - 1)))
            cc = canvas(choice(ccols), (oh, ow))
            cci = asindices(cc)
            subs = sample(totuple(cci), numred)
            obj1 = {(choice(ccols), ij) for ij in cci - set(subs)}
            obj2 = {(2, ij) for ij in subs}
            obj = obj1 | obj2
            gi = paint(gi, shift(obj, (loci, locj)))
            if go is None:
                go = paint(cc, obj)
            succ += 1
            indss = (indss - bd) - outbox(bd)
        tr += 1
    return {'input': gi, 'output': go}

