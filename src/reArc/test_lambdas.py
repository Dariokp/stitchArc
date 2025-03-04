"""
    A quick way to visualize if the translated lambdas correctly model the same logic as the original function.
"""

from dsl import *
from utils import *

# The resulting lambda expression
lambdaExp = (lambda _Y: lambda diff_lb, diff_ub: (lambda cols: (lambda h: (lambda w: (lambda bgc: (lambda remcols: (lambda nlines: (lambda linecols: (lambda remcols: (lambda nnoisecols: (lambda noisecols: (lambda locopts: (lambda locs: (lambda _term4, _items4: (lambda _targ4: (lambda _targ4, k, loc, locopts: (lambda _loop4: _loop4(_targ4, k, loc, locopts))(_Y(lambda _loop4: (lambda _targ4, k, loc, locopts: ((lambda k: ((lambda locs: (lambda nlines: (lambda linecols: (lambda gi: (lambda _term3, _items3: (lambda _targ3: (lambda _targ3, col, gi, loc: (lambda _loop3: _loop3(_targ3, col, gi, loc))(_Y(lambda _loop3: (lambda _targ3, col, gi, loc: ([(lambda gi: (lambda _targ3: _loop3(_targ3, col, gi, loc))(next(_items3, _term3)))(fill(gi, col, connect((0, loc), ((h - 1), loc)))) for (loc, col) in [_targ3]][0]) if (_targ3 is not _term3) else (lambda go: (lambda nilocs: (lambda ilocs: (lambda dotlocopts: (lambda _term1, _items1: (lambda _targ1: (lambda _targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots: (lambda _loop1: _loop1(_targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots))(_Y(lambda _loop1: (lambda _targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots: ((lambda ii: (lambda ndots: (lambda dotlocs: (lambda dotcols: (lambda _term2, _items2: (lambda _targ2: (lambda _targ2, col, dotlocj, gi, go, idx, linelocj: (lambda _loop2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(_Y(lambda _loop2: (lambda _targ2, col, dotlocj, gi, go, idx, linelocj: ([(lambda gi: ((lambda idx: (lambda linelocj: ((lambda go: (lambda _targ2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(next(_items2, _term2)))(fill(go, col, {(ii, (linelocj + 1))})) if (dotlocj > linelocj) else (lambda go: (lambda _targ2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(next(_items2, _term2)))(fill(go, col, {(ii, (linelocj - 1))}))))(locs[idx]))(linecols.index(col)) if (col in linecols) else (lambda _targ2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(next(_items2, _term2))))(fill(gi, col, {(ii, dotlocj)})) for (dotlocj, col) in [_targ2]][0]) if (_targ2 is not _term2) else (lambda _targ1: _loop1(_targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots))(next(_items1, _term1))))))(_targ2 if "_targ2" in dir() else None, col if "col" in dir() else None, dotlocj if "dotlocj" in dir() else None, gi if "gi" in dir() else None, go if "go" in dir() else None, idx if "idx" in dir() else None, linelocj if "linelocj" in dir() else None))(next(_items2, _term2)))([], iter(zip(dotlocs, dotcols))))(sample(totuple((set(linecols) | set(noisecols))), ndots)))(sample(dotlocopts, ndots)))(unifint(diff_lb, diff_ub, (1, min((nlines + nnoisecols), (((w - nlines) // 2) - 1))))))(_targ1)) if (_targ1 is not _term1) else ((lambda gi: (lambda go: {'input': gi, 'output': go})(dmirror(go)))(dmirror(gi)) if choice((True, False)) else {'input': gi, 'output': go})))))(_targ1 if "_targ1" in dir() else None, dotcols if "dotcols" in dir() else None, dotlocs if "dotlocs" in dir() else None, gi if "gi" in dir() else None, go if "go" in dir() else None, idx if "idx" in dir() else None, ii if "ii" in dir() else None, linelocj if "linelocj" in dir() else None, ndots if "ndots" in dir() else None))(next(_items1, _term1)))([], iter(ilocs)))(difference(interval(0, w, 1), locs)))(sample(interval(0, h, 1), nilocs)))(unifint(diff_lb, diff_ub, (1, h))))(tuple((e for e in gi)))))))(_targ3 if "_targ3" in dir() else None, col if "col" in dir() else None, gi if "gi" in dir() else None, loc if "loc" in dir() else None))(next(_items3, _term3)))([], iter(zip(locs, linecols))))(canvas(bgc, (h, w))))(linecols[:nlines:]))(len(locs)))(sorted(locs)) if (len(locopts) == 0) else (lambda loc: (lambda locopts: [locs.append(loc), (lambda _targ4: _loop4(_targ4, k, loc, locopts))(next(_items4, _term4))][-1])(difference(locopts, interval((loc - 2), (loc + 3), 1))))(choice(locopts))))(_targ4)) if (_targ4 is not _term4) else (lambda locs: (lambda nlines: (lambda linecols: (lambda gi: (lambda _term3, _items3: (lambda _targ3: (lambda _targ3, col, gi, loc: (lambda _loop3: _loop3(_targ3, col, gi, loc))(_Y(lambda _loop3: (lambda _targ3, col, gi, loc: ([(lambda gi: (lambda _targ3: _loop3(_targ3, col, gi, loc))(next(_items3, _term3)))(fill(gi, col, connect((0, loc), ((h - 1), loc)))) for (loc, col) in [_targ3]][0]) if (_targ3 is not _term3) else (lambda go: (lambda nilocs: (lambda ilocs: (lambda dotlocopts: (lambda _term1, _items1: (lambda _targ1: (lambda _targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots: (lambda _loop1: _loop1(_targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots))(_Y(lambda _loop1: (lambda _targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots: ((lambda ii: (lambda ndots: (lambda dotlocs: (lambda dotcols: (lambda _term2, _items2: (lambda _targ2: (lambda _targ2, col, dotlocj, gi, go, idx, linelocj: (lambda _loop2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(_Y(lambda _loop2: (lambda _targ2, col, dotlocj, gi, go, idx, linelocj: ([(lambda gi: ((lambda idx: (lambda linelocj: ((lambda go: (lambda _targ2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(next(_items2, _term2)))(fill(go, col, {(ii, (linelocj + 1))})) if (dotlocj > linelocj) else (lambda go: (lambda _targ2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(next(_items2, _term2)))(fill(go, col, {(ii, (linelocj - 1))}))))(locs[idx]))(linecols.index(col)) if (col in linecols) else (lambda _targ2: _loop2(_targ2, col, dotlocj, gi, go, idx, linelocj))(next(_items2, _term2))))(fill(gi, col, {(ii, dotlocj)})) for (dotlocj, col) in [_targ2]][0]) if (_targ2 is not _term2) else (lambda _targ1: _loop1(_targ1, dotcols, dotlocs, gi, go, idx, ii, linelocj, ndots))(next(_items1, _term1))))))(_targ2 if "_targ2" in dir() else None, col if "col" in dir() else None, dotlocj if "dotlocj" in dir() else None, gi if "gi" in dir() else None, go if "go" in dir() else None, idx if "idx" in dir() else None, linelocj if "linelocj" in dir() else None))(next(_items2, _term2)))([], iter(zip(dotlocs, dotcols))))(sample(totuple((set(linecols) | set(noisecols))), ndots)))(sample(dotlocopts, ndots)))(unifint(diff_lb, diff_ub, (1, min((nlines + nnoisecols), (((w - nlines) // 2) - 1))))))(_targ1)) if (_targ1 is not _term1) else ((lambda gi: (lambda go: {'input': gi, 'output': go})(dmirror(go)))(dmirror(gi)) if choice((True, False)) else {'input': gi, 'output': go})))))(_targ1 if "_targ1" in dir() else None, dotcols if "dotcols" in dir() else None, dotlocs if "dotlocs" in dir() else None, gi if "gi" in dir() else None, go if "go" in dir() else None, idx if "idx" in dir() else None, ii if "ii" in dir() else None, linelocj if "linelocj" in dir() else None, ndots if "ndots" in dir() else None))(next(_items1, _term1)))([], iter(ilocs)))(difference(interval(0, w, 1), locs)))(sample(interval(0, h, 1), nilocs)))(unifint(diff_lb, diff_ub, (1, h))))(tuple((e for e in gi)))))))(_targ3 if "_targ3" in dir() else None, col if "col" in dir() else None, gi if "gi" in dir() else None, loc if "loc" in dir() else None))(next(_items3, _term3)))([], iter(zip(locs, linecols))))(canvas(bgc, (h, w))))(linecols[:nlines:]))(len(locs)))(sorted(locs))))))(_targ4 if "_targ4" in dir() else None, k if "k" in dir() else None, loc if "loc" in dir() else None, locopts if "locopts" in dir() else None))(next(_items4, _term4)))([], iter(range(nlines))))([]))(interval(0, w, 1)))(sample(remcols, nnoisecols)))(unifint(diff_lb, diff_ub, (0, len(remcols)))))(difference(remcols, linecols)))(sample(remcols, nlines)))(unifint(diff_lb, diff_ub, (1, (w // 5)))))(remove(bgc, cols)))(choice(cols)))(unifint(diff_lb, diff_ub, (8, 30))))(unifint(diff_lb, diff_ub, (8, 30))))(interval(0, 10, 1)))((lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))))

# It's corresponding generator function
def generate_1a07d186(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (8, 30))
    w = unifint(diff_lb, diff_ub, (8, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    nlines = unifint(diff_lb, diff_ub, (1, w // 5))
    linecols = sample(remcols, nlines)
    remcols = difference(remcols, linecols)
    nnoisecols = unifint(diff_lb, diff_ub, (0, len(remcols)))
    noisecols = sample(remcols, nnoisecols)
    locopts = interval(0, w, 1)
    locs = []
    for k in range(nlines):
        if len(locopts) == 0:
            break
        loc = choice(locopts)
        locopts = difference(locopts, interval(loc - 2, loc + 3, 1))
        locs.append(loc)
    locs = sorted(locs)
    nlines = len(locs)
    linecols = linecols[:nlines]
    gi = canvas(bgc, (h, w))
    for loc, col in zip(locs, linecols):
        gi = fill(gi, col, connect((0, loc), (h - 1, loc)))
    go = tuple(e for e in gi)
    nilocs = unifint(diff_lb, diff_ub, (1, h))
    ilocs = sample(interval(0, h, 1), nilocs)
    dotlocopts = difference(interval(0, w, 1), locs)
    for ii in ilocs:
        ndots = unifint(diff_lb, diff_ub, (1, min(nlines + nnoisecols, (w - nlines) // 2 - 1)))
        dotlocs = sample(dotlocopts, ndots)
        dotcols = sample(totuple(set(linecols) | set(noisecols)), ndots)
        for dotlocj, col in zip(dotlocs, dotcols):
            gi = fill(gi, col, {(ii, dotlocj)})
            if col in linecols:
                idx = linecols.index(col)
                linelocj = locs[idx]
                if dotlocj > linelocj:
                    go = fill(go, col, {(ii, linelocj + 1)})
                else:
                    go = fill(go, col, {(ii, linelocj - 1)})
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}


# Creates a figure using both of the functions
plot_task([generate_1a07d186(0, 1), lambdaExp(0, 1)])("Orignal function (top)\nLambda expression (bottom)")