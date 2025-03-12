def generate_b27ca6d3(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc, dotc = sample(cols, 2)
    c = canvas(bgc, (h, w))
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    ndots = unifint(diff_lb, diff_ub, (0, (h * w) // 5))
    nbars = unifint(diff_lb, diff_ub, (0, (h * w) // 12))
    dot = frozenset({(dotc, (1, 1))}) | recolor(bgc, dneighbors((1, 1)))
    bar1 = fill(canvas(bgc, (4, 3)), dotc, {(1, 1), (2, 1)})
    bar2 = dmirror(bar1)
    bar1 = asobject(bar1)
    bar2 = asobject(bar2)
    opts = [dot] * ndots + [choice((bar1, bar2)) for k in range(nbars)]
    shuffle(opts)
    inds = shift(asindices(canvas(-1, (h+2, w+2))), (-1, -1))
    for elem in opts:
        loc = (-1, -1)
        tr = 0
        while not toindices(shift(elem, loc)).issubset(inds) and tr < 5:
            loc = choice(totuple(inds))
            tr += 1
        xx = shift(elem, loc)
        if toindices(xx).issubset(inds):
            gi = paint(gi, xx)
            if len(elem) == 12:
                go = paint(go, {cel if cel[0] != bgc else (3, cel[1]) for cel in xx})
            else:
                go = paint(go, xx)
            inds = inds - toindices(xx)
    return {'input': gi, 'output': go}

