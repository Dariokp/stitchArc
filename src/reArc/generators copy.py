from dsl import *
from utils import *



def generate_dbc1a6ce(diff_lb: float, diff_ub: float) -> dict:
    dim_bounds = (3, 30)
    colopts = remove(8, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, dim_bounds)
    w = unifint(diff_lb, diff_ub, dim_bounds)
    bgc = choice(colopts)
    c = canvas(bgc, (h, w))
    inds = totuple(asindices(c))
    card_bounds = (0, max(1, (h * w) // 4))
    num = unifint(diff_lb, diff_ub, card_bounds)
    s = sample(inds, num)
    fgcol = choice(remove(bgc, colopts))
    gi = fill(c, fgcol, s)
    resh = frozenset()
    for x, r in enumerate(gi):
        if r.count(fgcol) > 1:
            resh = combine(resh, connect((x, r.index(fgcol)), (x, -1 + w - r[::-1].index(fgcol))))
    go = fill(c, 8, resh)
    resv = frozenset()
    for x, r in enumerate(dmirror(gi)):
        if r.count(fgcol) > 1:
            resv = combine(resv, connect((x, r.index(fgcol)), (x, -1 + h - r[::-1].index(fgcol))))
    go = dmirror(fill(dmirror(go), 8, resv))
    go = fill(go, fgcol, s)
    return {'input': gi, 'output': go}


def generate_2281f1f4(diff_lb: float, diff_ub: float) -> dict:
    dim_bounds = (3, 30)
    colopts = remove(2, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, dim_bounds)
    w = unifint(diff_lb, diff_ub, dim_bounds)
    card_h_bounds = (1, h // 2 + 1)
    card_w_bounds = (1, w // 2 + 1)
    numtop = unifint(diff_lb, diff_ub, card_w_bounds)
    numright = unifint(diff_lb, diff_ub, card_h_bounds)
    if numtop == numright == 1:
        numtop, numright = sample([1, 2], 2)
    tp = sample(interval(0, w - 1, 1), numtop)
    rp = sample(interval(1, h, 1), numright)
    res = combine(apply(lbind(astuple, 0), tp), apply(rbind(astuple, w - 1), rp))
    bgc = choice(colopts)
    dc = choice(remove(bgc, colopts))
    gi = fill(canvas(bgc, (h, w)), dc, res)
    go = fill(gi, 2, product(rp, tp))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}


def generate_c1d99e64(diff_lb: float, diff_ub: float) -> dict:
    dim_bounds = (4, 30)
    colopts = remove(2, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, dim_bounds)
    w = unifint(diff_lb, diff_ub, dim_bounds)
    nofrontcol = choice(colopts)
    noisefrontcol = choice(remove(nofrontcol, colopts))
    gi = canvas(nofrontcol, (h, w))
    cands = totuple(asindices(gi))
    horifront_bounds = (1, h//4)
    vertifront_bounds = (1, w//4)
    nhf = unifint(diff_lb, diff_ub, horifront_bounds)
    nvf = unifint(diff_lb, diff_ub, vertifront_bounds)
    vfs = mapply(compose(vfrontier, tojvec), sample(interval(0, w, 1), nvf))
    hfs = mapply(compose(hfrontier, toivec), sample(interval(0, h, 1), nhf))
    gi = fill(gi, noisefrontcol, combine(vfs, hfs))
    cands = totuple(ofcolor(gi, nofrontcol))
    kk = size(cands)
    midp = (h * w) // 2
    noise_bounds = (0, max(0, kk - midp - 1))
    num_noise = unifint(diff_lb, diff_ub, noise_bounds)
    noise = sample(cands, num_noise)
    gi = fill(gi, noisefrontcol, noise)
    go = fill(gi, 2, merge(colorfilter(frontiers(gi), noisefrontcol)))
    return {'input': gi, 'output': go}
