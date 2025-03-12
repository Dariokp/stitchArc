def generate_beb8660c(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(8, interval(0, 10, 1))
    w = unifint(diff_lb, diff_ub, (3, 30))
    h = unifint(diff_lb, diff_ub, (w, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    k = min(8, w - 1)
    k = unifint(diff_lb, diff_ub, (1, k))
    co = sample(remcols, k)
    wds = sorted(sample(interval(1, w, 1), k))
    for j, (c, l) in enumerate(zip(co, wds)):
        j = h - k - 1 + j
        gi = fill(gi, c, connect((j, 0), (j, l - 1)))
    gi = fill(gi, 8, connect((h - 1, 0), (h - 1, w - 1)))
    go = vmirror(gi)
    gi = list(list(r) for r in gi[:-1])
    shuffle(gi)
    gi = tuple(tuple(r) for r in gi)
    gi = gi + go[-1:]
    gif = tuple()
    for r in gi:
        nbc = r.count(bgc)
        ofs = randint(0, nbc)
        gif = gif + (r[-ofs:] + r[:-ofs],)
    gi = vmirror(gif)
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

