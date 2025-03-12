def generate_48d8fb45(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    nobjs = unifint(diff_lb, diff_ub, (2, (h * w) // 15))
    tr = 0
    maxtr = 4 * nobjs
    done = False
    succ = 0
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    inds = asindices(gi)
    while tr < maxtr and succ < nobjs:
        oh = randint(2, 6)
        ow = randint(2, 6)
        bx = asindices(canvas(-1, (oh, ow)))
        nc = randint(3, oh * ow)
        sp = choice(totuple(bx))
        bx = remove(sp, bx)
        obj = {sp}
        for k in range(nc - 1):
            obj.add(choice(totuple((bx - obj) & mapply(neighbors, obj))))
        if not done:
            done = True
            idx = choice(totuple(obj))
            coll = choice(remcols)
            obj2 = {(coll, idx)}
            obj3 = recolor(choice(remove(coll, remcols)), remove(idx, obj))
            obj = obj2 | obj3
            go = paint(canvas(bgc, shape(obj3)), normalize(obj3))
        else:
            obj = recolor(choice(remcols), obj)
        locopts = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        tr += 1
        if len(locopts) == 0:
            continue
        loc = choice(totuple(locopts))
        plcd = shift(obj, loc)
        plcdi = toindices(plcd)
        if plcdi.issubset(inds):
            gi = paint(gi, plcd)
            succ += 1
            inds = (inds - plcdi) - mapply(neighbors, plcdi)
    return {'input': gi, 'output': go}

