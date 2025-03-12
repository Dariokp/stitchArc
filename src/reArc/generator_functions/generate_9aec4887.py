def generate_9aec4887(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (12, 30))
    w = unifint(diff_lb, diff_ub, (12, 30))
    oh = unifint(diff_lb, diff_ub, (4, h//2-2))
    ow = unifint(diff_lb, diff_ub, (4, w//2-2))
    bgc, pc, c1, c2, c3, c4 = sample(cols, 6)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (oh, ow))
    ln1 = connect((1, 0), (oh - 2, 0))
    ln2 = connect((1, ow - 1), (oh - 2, ow - 1))
    ln3 = connect((0, 1), (0, ow - 2))
    ln4 = connect((oh - 1, 1), (oh - 1, ow - 2))
    go = fill(go, c1, ln1)
    go = fill(go, c2, ln2)
    go = fill(go, c3, ln3)
    go = fill(go, c4, ln4)
    objB = asobject(go)
    bounds = asindices(canvas(-1, (oh - 2, ow - 2)))
    objA = {choice(totuple(bounds))}
    ncells = unifint(diff_lb, diff_ub, (1, ((oh - 2) * (ow - 2)) // 2))
    for k in range(ncells - 1):
        objA.add(choice(totuple((bounds - objA) & mapply(neighbors, objA))))
    while shape(objA) != (oh - 2, ow - 2):
        objA.add(choice(totuple((bounds - objA) & mapply(neighbors, objA))))
    fullinds = asindices(gi)
    loci = randint(0, h - 2 * oh + 2)
    locj = randint(0, w - ow)
    plcdB = shift(objB, (loci, locj))
    plcdi = toindices(plcdB)
    rems = sfilter(fullinds - plcdi, lambda ij: loci + oh <= ij[0] <= h - oh + 2 and ij[1] <= w - ow + 2)
    loc = choice(totuple(rems))
    plcdA = shift(objA, loc)
    gi = paint(gi, plcdB)
    gi = fill(gi, pc, plcdA)
    objA = shift(objA, (1, 1))
    objs = objects(go, T, F, T)
    for ij in objA:
        manhs = {obj: manhattan(obj, {ij}) for obj in objs}
        manhsl = list(manhs.values())
        mmh = min(manhsl)
        if manhsl.count(mmh) == 1:
            col = color([o for o, mnh in manhs.items() if mmh == mnh][0])
        else:
            col = pc
        go = fill(go, col, {ij})
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

