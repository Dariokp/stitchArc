def generate_963e52fc(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (6, 15))
    p = unifint(diff_lb, diff_ub, (2, w // 2))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numc = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(remcols, numc)
    obj = set()
    for j in range(p):
        ub = unifint(diff_lb, diff_ub, (0, h//2))
        ub = h//2-ub
        lb = unifint(diff_lb, diff_ub, (ub, h-1))
        numcells = unifint(diff_lb, diff_ub, (1, lb-ub+1))
        for ii in sample(interval(ub, lb+1, 1), numcells):
            loc = (ii, j)
            col = choice(ccols)
            cell = (col, loc)
            obj.add(cell)
    go = canvas(bgc, (h, w*2))
    minobj = obj | shift(obj, (0, p))
    addonw = randint(0, p)
    addon = sfilter(obj, lambda cij: cij[1][1] < addonw)
    fullobj = minobj | addon
    leftshift = randint(0, addonw)
    fullobj = shift(fullobj, (0, -leftshift))
    go = paint(go, fullobj)
    for j in range((2*w)//(2*p)+1):
        go = paint(go, shift(fullobj, (0, j * 2 * p)))
    gi = lefthalf(go)
    return {'input': gi, 'output': go}

