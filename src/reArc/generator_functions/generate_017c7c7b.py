def generate_017c7c7b(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (0, 2))
    h = unifint(diff_lb, diff_ub, (3, 10))
    w = unifint(diff_lb, diff_ub, (2, 30))
    h += h
    fgc = choice(cols)
    go = canvas(0, (h + h // 2, w))
    oh = unifint(diff_lb, diff_ub, (1, h//3*2))
    ow = unifint(diff_lb, diff_ub, (1, w))
    locj = randint(0, w - ow)
    bounds = asindices(canvas(-1, (oh, ow)))
    ncellsd = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    ncells = choice((ncellsd, oh * ow - ncellsd))
    ncells = min(max(1, ncells), oh * ow)
    obj = sample(totuple(bounds), ncells)
    for k in range((2*h)//oh):
        go = fill(go, 2, shift(obj, (k*oh, 0)))
    gi = replace(go[:h], 2, fgc)
    return {'input': gi, 'output': go}

