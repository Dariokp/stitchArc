def generate_539a4f51(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(1, 10, 1)
    d = unifint(diff_lb, diff_ub, (2, 15))
    h, w = d, d
    gi = canvas(0, (h, w))
    numc = unifint(diff_lb, diff_ub, (2, 9))
    ccols = sample(cols, numc)
    numocc = unifint(diff_lb, diff_ub, (1, d))
    arr = [choice(ccols) for k in range(numocc)]
    while len(set(arr)) == 1:
        arr = [choice(ccols) for k in range(d)]
    for j, col in enumerate(arr):
        gi = fill(gi, col, connect((j, 0), (j, j)) | connect((0, j), (j, j)))
    go = canvas(0, (2*d, 2*d))
    for j in range(2*d):
        col = arr[j % len(arr)]
        go = fill(go, col, connect((j, 0), (j, j)) | connect((0, j), (j, j)))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

