def generate_234bbc79(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    while True:
        h = unifint(diff_lb, diff_ub, (5, 30))
        w = unifint(diff_lb, diff_ub, (6, 20))
        bgc, dotc = sample(cols, 2)
        remcols = difference(cols, (bgc, dotc))
        go = canvas(bgc, (h, 30))
        ncols = unifint(diff_lb, diff_ub, (1, 8))
        ccols = sample(remcols, ncols)
        spi = randint(0, h - 1)
        snek = [(spi, 0)]
        gi = fill(go, dotc, {(spi, 0)})
        while True:
            previ, prevj = snek[-1]
            if prevj == w - 1:
                if choice((True, False, False)):
                    break
            options = []
            if previ < h - 1:
                if go[previ+1][prevj] == bgc:
                    options.append((previ+1, prevj))
            if previ > 0:
                if go[previ-1][prevj] == bgc:
                    options.append((previ-1, prevj))
            if prevj < w - 1:
                options.append((previ, prevj+1))
            if len(options) == 0:
                break
            loc = choice(options)
            snek.append(loc)
            go = fill(go, dotc, {loc})
        objs = []
        cobj = []
        for idx, cel in enumerate(snek):
            if len(cobj) > 2 and width(frozenset(cobj)) > 1 and snek[idx-1] == add(cel, (0, -1)):
                objs.append(cobj)
                cobj = [cel]
            else:
                cobj.append(cel)
        objs[-1] += cobj
        nobjs = len(objs)
        if nobjs < 2:
            continue
        ntokeep = unifint(diff_lb, diff_ub, (2, nobjs))
        ntorem = nobjs - ntokeep
        for k in range(ntorem):
            idx = randint(0, len(objs) - 2)
            objs = objs[:idx] + [objs[idx] + objs[idx+1]] + objs[idx+2:]
        inobjs = []
        for idx, obj in enumerate(objs):
            col = choice(ccols)
            go = fill(go, col, set(obj))
            centerpart = recolor(col, set(obj[1:-1]))
            leftpart = {(dotc if idx > 0 else col, obj[0])}
            rightpart = {(dotc if idx < len(objs) - 1 else col, obj[-1])}
            inobj = centerpart | leftpart | rightpart
            inobjs.append(inobj)
        spacings = [1 for idx in range(len(inobjs) - 1)]
        fullw = unifint(diff_lb, diff_ub, (w, 30))
        for k in range(fullw - w - len(inobjs) - 1):
            idx = randint(0, len(spacings) - 1)
            spacings[idx] += 1
        lspacings = [0] + spacings
        gi = canvas(bgc, (h, fullw))
        ofs = 0
        for i, (lsp, obj) in enumerate(zip(lspacings, inobjs)):
            obj = set(obj)
            if i == 0:
                ulc = ulcorner(obj)
            else:
                ulci = randint(0, h - height(obj))
                ulcj = ofs + lsp
                ulc = (ulci, ulcj)
            ofs += width(obj) + lsp
            plcd = shift(normalize(obj), ulc)
            gi = paint(gi, plcd)
        break
    ins = size(merge(fgpartition(gi)))
    while True:
        go2 = dmirror(dmirror(go)[:-1])
        if size(sfilter(asobject(go2), lambda cij: cij[0] != bgc)) < ins:
            break
        else:
            go = go2
    return {'input': gi, 'output': go}

