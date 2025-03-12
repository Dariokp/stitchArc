def generate_23b5c85d(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc = choice(cols)
    colopts = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    oh = unifint(diff_lb, diff_ub, (2, h - 1))
    ow = unifint(diff_lb, diff_ub, (2, w - 1))
    num = unifint(diff_lb, diff_ub, (1, 8))
    cnt = 0
    while cnt < num:
        loci = randint(0, h - oh)
        locj = randint(0, w - ow)
        col = choice(colopts)
        colopts = remove(col, colopts)
        obj = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
        gi2 = fill(gi, col, obj)
        if color(argmin(sfilter(partition(gi2), fork(equality, size, fork(multiply, height, width))), fork(multiply, height, width))) != col:
            break
        else:
            gi = gi2
            go = canvas(col, shape(obj))
        oh = unifint(diff_lb, diff_ub, (max(0, oh - 4), oh - 1))
        ow = unifint(diff_lb, diff_ub, (max(0, ow - 4), ow - 1))
        if oh < 1 or ow < 1:
            break
        cnt += 1
    return {'input': gi, 'output': go}

