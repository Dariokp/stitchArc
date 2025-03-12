def generate_e26a3af2(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    nr = unifint(diff_lb, diff_ub, (1, 10))
    w = unifint(diff_lb, diff_ub, (4, 30))
    scols = sample(cols, nr)
    sgs = [canvas(col, (2, w)) for col in scols]
    numexp = unifint(diff_lb, diff_ub, (0, 30 - nr))
    for k in range(numexp):
        idx = randint(0, nr - 1)
        sgs[idx] = sgs[idx] + sgs[idx][-1:]
    sgs2 = []
    for idx, col in enumerate(scols):
        sg = sgs[idx]
        a, b = shape(sg)
        ub = (a * b) // 2 - 1
        nnoise = unifint(diff_lb, diff_ub, (0, ub))
        inds = totuple(asindices(sg))
        noise = sample(inds, nnoise)
        oc = remove(col, cols)
        noise = frozenset({(choice(oc), ij) for ij in noise})
        sg2 = paint(sg, noise)
        for idxx in [0, -1]:
            while sum([e == col for e in sg2[idxx]]) < w // 2:
                locs = [j for j, e in enumerate(sg2[idxx]) if e != col]
                ch = choice(locs)
                if idxx == 0:
                    sg2 = (sg2[0][:ch] + (col,) + sg2[0][ch+1:],) + sg2[1:]
                else:
                    sg2 = sg2[:-1] + (sg2[-1][:ch] + (col,) + sg2[-1][ch+1:],)
        sgs2.append(sg2)
    gi = tuple(row for sg in sgs2 for row in sg)
    go = tuple(row for sg in sgs for row in sg)
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

