def generate_6455b5f5(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 8))
    while True:
        h = unifint(diff_lb, diff_ub, (6, 30))
        w = unifint(diff_lb, diff_ub, (6, 30))
        bgc = choice(cols)
        fgc = choice(remove(bgc, cols))
        gi = canvas(bgc, (h, w))
        ub = int((h * w) ** 0.5 * 1.5)
        num = unifint(diff_lb, diff_ub, (1, ub))
        for k in range(num):
            objs = colorfilter(objects(gi, T, T, F), bgc)
            eligobjs = sfilter(objs, lambda o: height(o) > 2 or width(o) > 2)
            if len(eligobjs) == 0:
                break
            if choice((True, False)):
                ro = argmax(eligobjs, size)
            else:
                ro = choice(totuple(eligobjs))
            if choice((True, False)):
                vfr = height(ro) < width(ro)
            else:
                vfr = choice((True, False))
            if vfr and width(ro) < 3:
                vfr = False
            if (not vfr) and height(ro) < 3:
                vfr = True
            if vfr:
                j = randint(leftmost(ro)+1, rightmost(ro)-1)
                ln = connect((uppermost(ro), j), (lowermost(ro), j))
            else:
                j = randint(uppermost(ro)+1, lowermost(ro)-1)
                ln = connect((j, leftmost(ro)), (j, rightmost(ro)))
            gi = fill(gi, fgc, ln)
        objs = colorfilter(objects(gi, T, T, F), bgc)
        if valmin(objs, size) != valmax(objs, size):
            break
    lblues = mfilter(objs, matcher(size, valmin(objs, size)))
    dblues = mfilter(objs, matcher(size, valmax(objs, size)))
    go = fill(gi, 8, lblues)
    go = fill(go, 1, dblues)
    return {'input': gi, 'output': go}

