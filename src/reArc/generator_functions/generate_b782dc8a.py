def generate_b782dc8a(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    dlt = [('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]
    walls = {'N': True, 'S': True, 'E': True, 'W': True}
    fullsucc = False
    while True:
        h = unifint(diff_lb, diff_ub, (3, 15))
        w = unifint(diff_lb, diff_ub, (3, 15))
        maze = [[{'x': x, 'y': y, 'walls': {**walls}} for y in range(h)] for x in range(w)]
        kk = h * w
        stck = []
        cc = maze[0][0]
        nv = 1
        while nv < kk:
            nbhs = []
            for direc, (dx, dy) in dlt:
                x2, y2 = cc['x'] + dx, cc['y'] + dy
                if 0 <= x2 < w and 0 <= y2 < h:
                    neighbour = maze[x2][y2]
                    if all(neighbour['walls'].values()):
                        nbhs.append((direc, neighbour))
            if not nbhs:
                cc = stck.pop()
                continue
            direc, next_cell = choice(nbhs)
            cc['walls'][direc] = False
            next_cell['walls'][wall_pairs[direc]] = False
            stck.append(cc)
            cc = next_cell
            nv += 1
        pathcol, wallcol, dotcol, ncol = sample(cols, 4)
        grid = [[pathcol for x in range(w * 2)]]
        for y in range(h):
            row = [pathcol]
            for x in range(w):
                row.append(wallcol)
                row.append(pathcol if maze[x][y]['walls']['E'] else wallcol)
            grid.append(row)
            row = [pathcol]
            for x in range(w):
                row.append(pathcol if maze[x][y]['walls']['S'] else wallcol)
                row.append(pathcol)
            grid.append(row)
        gi = tuple(tuple(r[1:-1]) for r in grid[1:-1])
        objs = objects(gi, T, F, F)
        objs = colorfilter(objs, pathcol)
        objs = sfilter(objs, lambda obj: size(obj) > 4)
        if len(objs) == 0:
            continue
        objs = order(objs, size)
        nobjs = len(objs)
        idx = unifint(diff_lb, diff_ub, (0, nobjs - 1))
        obj = toindices(objs[idx])
        cell = choice(totuple(obj))
        gi = fill(gi, dotcol, {cell})
        nbhs = dneighbors(cell) & ofcolor(gi, pathcol)
        gi = fill(gi, ncol, nbhs)
        obj1 = sfilter(obj, lambda ij: even(manhattan({ij}, {cell})))
        obj2 = obj - obj1
        go = fill(gi, dotcol, obj1)
        go = fill(go, ncol, obj2)
        break
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

