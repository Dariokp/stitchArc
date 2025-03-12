def generate_0a938d79(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (4, 29))
    w = unifint(diff_lb, diff_ub, (h+1, 30))
    bgc, cola, colb = sample(cols, 3)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    locja = unifint(diff_lb, diff_ub, (3, w - 2))
    locjb = unifint(diff_lb, diff_ub, (1, locja - 2))
    locia = choice((0, h-1))
    locib = choice((0, h-1))
    gi = fill(gi, cola, {(locia, locja)})
    gi = fill(gi, colb, {(locib, locjb)})
    ofs = -2 * (locja-locjb)
    for aa in range(locja, -1, ofs):
        go = fill(go, cola, connect((0, aa), (h-1, aa)))
    for bb in range(locjb, -1, ofs):    
        go = fill(go, colb, connect((0, bb), (h-1, bb)))
    rotf = choice((rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

