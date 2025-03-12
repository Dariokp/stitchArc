def generate_8efcae92(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc, sqc, dotc = sample(cols, 3)
    num = unifint(diff_lb, diff_ub, (1, (h * w) // 25))
    succ = 0
    maxtr = 4 * num
    tr = 0
    gi = canvas(bgc, (h, w))
    go = None
    inds = asindices(gi)
    oho, owo = None, None
    while succ < num and tr < maxtr:
        if oho is None and owo is None:
            oh = randint(2, h - 1)
            ow = randint(2, w - 1)
            oho = oh
            owo = ow
        else:
            ohd = unifint(diff_lb, diff_ub, (0, min(oho, h - 1 - oho)))
            owd = unifint(diff_lb, diff_ub, (0, min(owo, w - 1 - owo)))
            ohd = min(oho, h - 1 - oho) - ohd
            owd = min(owo, w - 1 - owo) - owd
            oh = choice((oho - ohd, oho + ohd))
            ow = choice((owo - owd, owo + owd))
            oh = min(max(2, oh), h - 1)
            ow = min(max(2, ow), w - 1)
        minig = canvas(sqc, (oh, ow))
        mini = asindices(minig)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        tr += 1
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        if not shift(mini, loc).issubset(inds):
            continue
        succ += 1
        if go is None:
            numdots = unifint(diff_lb, diff_ub, (1, (oh * ow) // 2 - 1))
            nd = numdots
        else:
            nd = unifint(diff_lb, diff_ub, (0, min((oh * ow) // 2 - 1, numdots - 1)))
        locs = sample(totuple(mini), nd)
        minig = fill(minig, dotc, locs)
        if go is None:
            go = minig
        obj = asobject(minig)
        plcd = shift(obj, loc)
        gi = paint(gi, plcd)
        inds = (inds - toindices(plcd)) - mapply(dneighbors, toindices(plcd))
    return {'input': gi, 'output': go}

