def generate_272f95fa(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2, 3, 4, 6))    
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc, linc = sample(cols, 2)
    c = canvas(bgc, (5, 5))
    l1 = connect((1, 0), (1, 4))
    l2 = connect((3, 0), (3, 4))
    lns = l1 | l2
    gi = fill(dmirror(fill(c, linc, lns)), linc, lns)
    hdist = [0, 0, 0]
    wdist = [0, 0, 0]
    idx = 0
    for k in range(h - 2):
        hdist[idx] += 1
        idx = (idx + 1) % 3
    for k in range(w - 2):
        wdist[idx] += 1
        idx = (idx + 1) % 3
    shuffle(hdist)
    shuffle(wdist)
    hdelt1 = unifint(diff_lb, diff_ub, (0, hdist[0] - 1))
    hdist[0] -= hdelt1
    hdist[1] += hdelt1
    hdelt2 = unifint(diff_lb, diff_ub, (0, min(hdist[1], hdist[2]) - 1))
    hdelt2 = choice((+hdelt2, -hdelt2))
    hdist[1] += hdelt2
    hdist[2] -= hdelt2
    wdelt1 = unifint(diff_lb, diff_ub, (0, wdist[0] - 1))
    wdist[0] -= wdelt1
    wdist[1] += wdelt1
    wdelt2 = unifint(diff_lb, diff_ub, (0, min(wdist[1], wdist[2]) - 1))
    wdelt2 = choice((+wdelt2, -wdelt2))
    wdist[1] += wdelt2
    wdist[2] -= wdelt2
    gi = gi[:1] * hdist[0] + gi[1:2] + gi[2:3] * hdist[1] + gi[3:4] + gi[4:5] * hdist[2]
    gi = dmirror(gi)
    gi = gi[:1] * wdist[0] + gi[1:2] + gi[2:3] * wdist[1] + gi[3:4] + gi[4:5] * wdist[2]
    gi = dmirror(gi)
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
    objs = objects(gi, T, T, F)
    bgobjs = colorfilter(objs, bgc)
    cnrs = corners(asindices(gi))
    bgobjs = sfilter(bgobjs, lambda o: len(toindices(o) & cnrs) == 0)
    pinkobj = extract(bgobjs, lambda o: not bordering(o, gi))
    yellobj = argmin(bgobjs, leftmost)
    greenobj = argmax(bgobjs, rightmost)
    redobj = argmin(bgobjs, uppermost)
    blueobj = argmax(bgobjs, lowermost)
    go = fill(gi, 6, pinkobj)
    go = fill(go, 4, yellobj)
    go = fill(go, 3, greenobj)
    go = fill(go, 2, redobj)
    go = fill(go, 1, blueobj)
    return {'input': gi, 'output': go}

