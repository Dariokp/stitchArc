def generate_6e19193c(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    dirs = (
    ((0, 0), (-1, -1)),
    ((0, 1), (-1, 1)),
    ((1, 0), (1, -1)),
    ((1, 1), (1, 1))
    )
    base = ((0, 0), (1, 0), (0, 1), (1, 1))
    candsi = [
    set(base) - {dr[0]} for dr in dirs
    ]
    candso = [
    (set(base) | shoot(dr[0], dr[1])) - {dr[0]} for dr in dirs
    ]
    cands = list(zip(candsi, candso))    
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    num = unifint(diff_lb, diff_ub, (1, (h * w) // 8))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    fullinds = asindices(gi)
    inds = asindices(canvas(-1, (h, w)))
    kk, tr = 0, 0
    maxtrials = num * 4
    while kk < num and tr < maxtrials:
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        obji, objo = choice(cands)
        obji = shift(obji, loc)
        objo = shift(objo, loc)
        objo = objo & fullinds
        if objo.issubset(inds) and obji.issubset(objo):
            col = choice(remcols)
            gi = fill(gi, col, obji)
            go = fill(go, col, objo)
            inds = (inds - objo) - mapply(dneighbors, obji)
            kk += 1
        tr += 1
    return {'input': gi, 'output': go}

