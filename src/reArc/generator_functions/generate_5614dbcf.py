def generate_5614dbcf(diff_lb: float, diff_ub: float) -> dict:
    dim_bounds = (2, 10)
    col_card_bounds = (1, 8)
    noise_card_bounds = (0, 8)
    colopts = remove(5, interval(1, 10, 1))
    noisedindscands = totuple(asindices(canvas(0, (3, 3))))
    d = unifint(diff_lb, diff_ub, dim_bounds)
    cells_card_bounds = (1, d * d)
    go = canvas(0, (d, d))
    inds = totuple(asindices(go))
    numocc = unifint(diff_lb, diff_ub, cells_card_bounds)
    numcol = unifint(diff_lb, diff_ub, col_card_bounds)
    occs = sample(inds, numocc)
    colset = sample(colopts, numcol)
    gi = upscale(go, THREE)
    for occ in inds:
        offset = multiply(3, occ)
        numnoise = unifint(diff_lb, diff_ub, noise_card_bounds)
        noise = sample(noisedindscands, numnoise)
        if occ in occs:
            col = choice(colset)
            go = fill(go, col, initset(occ))
            gi = fill(gi, col, shift(noisedindscands, offset))
        gi = fill(gi, 5, shift(noise, offset))
    return {'input': gi, 'output': go}

