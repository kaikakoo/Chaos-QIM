import numpy as np

def Logistic(z, r=3.58, n=100) -> np.array:
    """
    Generate n dimension Logistic sequence
    """
    assert r > 3.57 and r <= 4, 'r is not in (3.57, 4]'
    assert z > 0 and z <= 1, 'z is not in (0,1]'

    Z = np.array([])

    for i in range(n):
        Z = np.append(Z, z)
        z = r * z * (1 - z)
    return Z


def Sampling(Z, d) -> np.array:
    '''
    Sample Z into row vectors
    Z: Logistic sequence
    d: Sampling interval
    '''
    assert (len(Z) >= d and len(Z) % d == 0), 'Z is too small'

    X = np.array([Z[i] for i in range(d)])

    for i in range(1, len(Z) // d):
        x = np.array([])
        for j in range(d):
            x = np.append(x, Z[i * d + j])
        X = np.vstack((X, x))

    return X


def BabaisClosestPlaneAlgorithm(L, w) -> np.ndarray:
    G, _ = L.gram_schmidt()
    t = w
    i = G.nrows() - 1
    while i >= 0:
        w -= round((w * G[i]) / G[i].norm() ** 2) * L[i]
        i -= 1
    return t - w


def MyBabai(T, B=None) -> [np.ndarray]:
    '''
    find the closest piont of t in L(B)
    B: basis
    T: query vecs
    '''
    if B is None:  # Do rounding in [-0.5, 0.5]

        d = len(T[0])

        for i in range(len(T)):
            for j in range(d):
                T[i][j] = T[i][j] - np.round(T[i][j])
        return T + 0.5  # make T in [0,1]

    else:

        d = len(B[0])

        assert (len(T[0]) == d)

        for i in range(len(T)):
            v = BabaisClosestPlaneAlgorithm(B, np.ndarray(T[i]))
            T[i] = T[i] - v

        return T


def uniform_transmit(data, mu, interval, num):
    data = mu * data
    data1 = Sampling(data, interval)
    y1 = MyBabai(data1)
    y_ = np.reshape(y1, [num])
    return y_


if __name__ == '__main__':
    d = 2
    x_vals=Logistic(z=0.2)
    X = Sampling(x_vals, d)
    b = np.array([[pow(3, 1/2)/2, 0],
                      [0.5,           1]])
    Y = MyBabai(X, b)
