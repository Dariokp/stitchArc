# from dsl import *
# from utils import *

# def just_a_test(x, y):
#     # do some operations using functions with multiple arguments
#     z = choice([x+10, x+20, x+30])
#     h = unifint(x, z, y)
#     k = x + y
#     return (h, k)

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
    return dict([("input", gi), ("output", go)])


# def generate_b9b7f026(diff_lb: float, diff_ub: float) -> dict:
#     cols = interval(0, 10, 1)    
#     h = unifint(diff_lb, diff_ub, (10, 30))
#     w = unifint(diff_lb, diff_ub, (10, 30))
#     bgc = choice(cols)
#     remcols = remove(bgc, cols)
#     gi = canvas(bgc, (h, w))
#     num = unifint(diff_lb, diff_ub, (1, 9))
#     indss = asindices(gi)
#     maxtrials = 4 * num
#     succ = 0
#     tr = 0
#     outcol = None
#     while succ < num and tr <= maxtrials:
#         if len(remcols) == 0 or len(indss) == 0:
#             break
#         oh = randint(3, 7)
#         ow = randint(3, 7)
#         subs = totuple(sfilter(indss, lambda ij: ij[0] < h - oh and ij[1] < w - ow))
#         if len(subs) == 0:
#             tr += 1
#             continue
#         loci, locj = choice(subs)
#         obj = frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)})
#         bd = backdrop(obj)
#         col = choice(remcols)
#         if bd.issubset(indss):
#             remcols = remove(col, remcols)
#             gi = fill(gi, col, bd)
#             succ += 1
#             indss = indss - bd
#             if outcol is None:
#                 outcol = col
#                 cands = totuple(backdrop(inbox(bd)))
#                 bd2 = backdrop(
#                     frozenset(sample(cands, 2)) if len(cands) > 2 else frozenset(cands)
#                 )
#                 gi = fill(gi, bgc, bd2)
#         tr += 1
#     go = canvas(outcol, (1, 1))
#     return {'input': gi, 'output': go}

# def generate_1a07d186(diff_lb: float, diff_ub: float) -> dict:
#     cols = interval(0, 10, 1)
#     h = unifint(diff_lb, diff_ub, (8, 30))
#     w = unifint(diff_lb, diff_ub, (8, 30))
#     bgc = choice(cols)
#     remcols = remove(bgc, cols)
#     nlines = unifint(diff_lb, diff_ub, (1, w // 5))
#     linecols = sample(remcols, nlines)
#     remcols = difference(remcols, linecols)
#     nnoisecols = unifint(diff_lb, diff_ub, (0, len(remcols)))
#     noisecols = sample(remcols, nnoisecols)
#     locopts = interval(0, w, 1)
#     locs = []
#     for k in range(nlines):
#         if len(locopts) == 0:
#             break
#         loc = choice(locopts)
#         locopts = difference(locopts, interval(loc - 2, loc + 3, 1))
#         locs.append(loc)
#     locs = sorted(locs)
#     nlines = len(locs)
#     linecols = linecols[:nlines]
#     gi = canvas(bgc, (h, w))
#     for loc, col in zip(locs, linecols):
#         gi = fill(gi, col, connect((0, loc), (h - 1, loc)))
#     go = tuple(e for e in gi)
#     nilocs = unifint(diff_lb, diff_ub, (1, h))
#     ilocs = sample(interval(0, h, 1), nilocs)
#     dotlocopts = difference(interval(0, w, 1), locs)
#     for ii in ilocs:
#         ndots = unifint(diff_lb, diff_ub, (1, min(nlines + nnoisecols, (w - nlines) // 2 - 1)))
#         dotlocs = sample(dotlocopts, ndots)
#         dotcols = sample(totuple(set(linecols) | set(noisecols)), ndots)
#         for dotlocj, col in zip(dotlocs, dotcols):
#             gi = fill(gi, col, {(ii, dotlocj)})
#             if col in linecols:
#                 idx = linecols.index(col)
#                 linelocj = locs[idx]
#                 if dotlocj > linelocj:
#                     go = fill(go, col, {(ii, linelocj + 1)})
#                 else:
#                     go = fill(go, col, {(ii, linelocj - 1)})
#     if choice((True, False)):
#         gi = dmirror(gi)
#         go = dmirror(go)
#     return {'input': gi, 'output': go}
