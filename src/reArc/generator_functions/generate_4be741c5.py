def generate_4be741c5(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    numcolors = unifint(diff_lb, diff_ub, (2, w // 3))
    ccols = sample(cols, numcolors)
    go = (tuple(ccols),)
    gi = merge(tuple(repeat(repeat(c, h), 3) for c in ccols))
    while len(gi) < w:
        idx = randint(0, len(gi) - 1)
        gi = gi[:idx] + gi[idx:idx+1] + gi[idx:]
    gi = dmirror(gi)
    ndisturbances = unifint(diff_lb, diff_ub, (0, 3 * h * numcolors))
    for k in range(ndisturbances):
        options = []
        for a in range(h):
            for b in range(w - 3):
                if gi[a][b] == gi[a][b+1] and gi[a][b+2] == gi[a][b+3]:
                    options.append((a, b, gi[a][b], gi[a][b+2]))
        if len(options) == 0:
            break
        a, b, c1, c2 = choice(options)
        if choice((True, False)):
            gi = fill(gi, c2, {(a, b+1)})
        else:
            gi = fill(gi, c1, {(a, b+2)})
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

