def generate_05269061(diff_lb: float, diff_ub: float) -> dict:
    dim_bounds = (2, 30)
    colopts = interval(1, 10, 1)
    d = unifint(diff_lb, diff_ub, dim_bounds)
    go = canvas(0, (d, d))
    gi = canvas(0, (d, d))
    if choice((True, False)):
        period_bounds = (2, min(2*d-2, 9))
        num = unifint(diff_lb, diff_ub, period_bounds)
        cols = tuple(choice(colopts) for k in range(num))
        keeps = [choice(interval(j, 2*d-1, num)) for j in range(num)]
        for k, col in enumerate((cols * 30)[:2*d-1]):
            lin = shoot(toivec(k), UP_RIGHT)
            go = fill(go, col, lin)
            if keeps[k % num] == k:
                gi = fill(gi, col, lin)
    else:
        period_bounds = (2, min(d, 9))
        num = unifint(diff_lb, diff_ub, period_bounds)
        cols = tuple(choice(colopts) for k in range(num))
        keeps = [choice(interval(j, d, num)) for j in range(num)]
        for k, col in enumerate((cols * 30)[:d]):
            lin = hfrontier(toivec(k))
            go = fill(go, col, lin)
            if keeps[k % num] == k:
                gi = fill(gi, col, lin)
    if choice((True, False)):
        gi = vmirror(gi)
        go = vmirror(go)
    return {'input': gi, 'output': go}

