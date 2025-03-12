def generate_60b61512(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(7, interval(0, 10, 1))    
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numcols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, numcols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    num = unifint(diff_lb, diff_ub, (1, (h * w) // 20))
    indss = asindices(gi)
    maxtrials = 4 * num
    tr = 0
    succ = 0
    while succ < num and tr <= maxtrials:
        if len(indss) == 0:
            break
        oh = randint(2, 7)
        ow = randint(2, 7)
        subs = totuple(sfilter(indss, lambda ij: ij[0] < h - oh and ij[1] < w - ow))
        if len(subs) == 0:
            tr += 1
            continue
        loci, locj = choice(subs)
        indsss = asindices(canvas(-1, (oh, ow)))
        chch = choice(totuple(indsss))
        obj = {chch}
        indsss = remove(chch, indsss)
        numcd = unifint(diff_lb, diff_ub, (0, (oh * ow) // 2))
        numc = choice((numcd, oh * ow - numcd))
        numc = min(max(2, numc), oh * ow - 1)
        for k in range(numc):
            obj.add(choice(totuple(indsss & mapply(neighbors, obj))))
            indsss = indsss - obj
        oh, ow = shape(obj)
        obj = shift(obj, (loci, locj))
        bd = backdrop(obj)
        col = choice(ccols)
        if bd.issubset(indss):
            gi = fill(gi, col, obj)
            go = fill(go, 7, bd)
            go = fill(go, col, obj)
            succ += 1
            indss = (indss - bd) - outbox(bd)
        tr += 1
    return {'input': gi, 'output': go}

