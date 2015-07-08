def calc_rmsd(x, y):
    delta = x - y
    N = len(delta)
    np.multiply(delta, delta, delta)
    return np.sqrt((delta.sum() / N))
