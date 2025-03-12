def generate_ae4f1146(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(1, interval(0, 10, 1))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    dh = unifint(diff_lb, diff_ub, (2, h // 3))
    dw = unifint(diff_lb, diff_ub, (2, w // 3))
    num = unifint(diff_lb, diff_ub, (1, (h * w) // (2 * dh * dw)))
    cards = interval(0, dh * dw, 1)
    ccards = sorted(sample(cards, min(num, len(cards))))
    sgs = []
    c1 = canvas(fgc, (dh, dw))
    inds = totuple(asindices(c1))
    for card in ccards:
        x = sample(inds, card)
        x1 = fill(c1, 1, x)
        sgs.append(asobject(x1))
    go = paint(c1, sgs[-1])
    gi = canvas(bgc, (h, w))
    inds2 = asindices(canvas(bgc, (h - dh, w - dw)))
    maxtr = 10
    for sg in sgs[::-1]:
        if len(inds2) == 0:
            break
        loc = choice(totuple(inds2))
        plcd = shift(sg, loc)
        tr = 0    
        while (not toindices(plcd).issubset(inds2)) and tr < maxtr:
            loc = choice(totuple(inds2))
            plcd = shift(sg, loc)
            tr += 1
        if tr < maxtr:
            inds2 = difference(inds2, toindices(plcd) | outbox(plcd))
            gi = paint(gi, plcd)
    return {'input': gi, 'output': go}

