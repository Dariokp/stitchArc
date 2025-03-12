def generate_0ca9ddb6(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2, 4, 6, 7, 8))
    xi = {(8, (0, 0))}
    xo = {(8, (0, 0))}
    ai = {(6, (0, 0))}
    ao = {(6, (0, 0))}
    bi = {(2, (1, 1))}
    bo = {(2, (1, 1))} | recolor(4, ineighbors((1, 1)))
    ci = {(1, (1, 1))}
    co = {(1, (1, 1))} | recolor(7, dneighbors((1, 1)))
    arr = ((ai, ao), (bi, bo), (ci, co), (xi, xo))    
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // 4))
    maxtr = 5 * nobjs
    tr = 0
    succ = 0
    bgc = choice(cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    while succ < nobjs and tr < maxtr:
        ino, outo = choice(arr)
        loc = choice(totuple(inds))
        oplcd = shift(outo, loc)
        oplcdi = toindices(oplcd)
        if oplcdi.issubset(inds):
            succ += 1
            gi = paint(gi, shift(ino, loc))
            go = paint(go, oplcd)
            inds = inds - oplcdi
        tr += 1
    return {'input': gi, 'output': go}

