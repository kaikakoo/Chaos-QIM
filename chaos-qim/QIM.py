import numpy as np
from SDCVP import SDCVP
import math
import random


def standard_qim_embedding(p: np.array, s: np.array, basic: np.array, a: int,
                           representative: list[np.array]) -> np.array:
    """
         p: carrier signal
         s: secret message
         b: lattice basis
         a: magnification factor
         representative: coset representative

    """

    sub_basic = a * basic
    k = np.dot(sub_basic, SDCVP(p - np.dot(basic, representative[s]), sub_basic))
    m = k + np.dot(basic, representative[s])
    return m


def cosets(a: int, n: int) -> list[np.array]:
    vector = []
    for i in range(a):
        vector.append(i)
        pass
    representatives = [vector] * n
    representative = []
    from itertools import product
    for item in list(product(*representatives)):
        representative.append(np.asarray(item))
    return representative


def standard_qim_extraction(p: np.array, basic: np.array, a: int, representative: list[np.array]) -> int:
    k = SDCVP(p, basic, )
    for i in range(len(representative)):
        if (k % a == representative[i]).all():
            break
    return i


if __name__ == '__main__':
    # b = np.array([[1]])
    b = np.array([[pow(3, 1 / 2) / 2, 0],
                  [0.5, 1]])
    # b = np.array([[2, 1, 1, 1],
    #              [0, 1, 0, 0],
    #              [0, 0, 1, 0],
    #              [0, 0, 0, 1]])
    # b = np.array([[2, -1, 0, 0, 0, 0, 0, 0.5],
    #              [0, 1, -1, 0, 0, 0, 0, 0.5],
    #              [0, 0, 1, -1, 0, 0, 0, 0.5],
    #              [0, 0, 0, 1, -1, 0, 0, 0.5],
    #              [0, 0, 0, 0, 1, -1, 0, 0.5],
    #              [0, 0, 0, 0, 0, 1, -1, 0.5],
    #              [0, 0, 0, 0, 0, 0, 1, 0.5],
    #              [0, 0, 0, 0, 0, 0, 0, 0.5]])
    N = b.shape[0]
    num_carrier = 4500
    alpha = 2
    delta = 1
    b = b * delta
    coset_representative = cosets(alpha, N)
    coset_representatives = np.dot(coset_representative, b)
    length = round(math.log(len(coset_representative), alpha))
    num_secret = pow(alpha, N)
    np.random.seed(1)
    secret = np.random.randint(0, num_secret, size=math.floor(num_carrier / N))

    carrier = np.random.uniform(-1, 1, num_carrier)
    qim_sequence = []
    num = 0
    carrier_embedding = []
    for item in range(0, len(carrier), N):
        carrier_sample = standard_qim_embedding(carrier[item: item + N], secret[num], b, alpha,
                                                coset_representative)
        carrier_embedding = np.concatenate([carrier_embedding, carrier_sample])
        num += 1
    qim_sequence = np.concatenate([qim_sequence, carrier_embedding])

    secret_extration = []
    x = round(len(carrier_embedding) / N)
    for item in range(0, round(len(carrier_embedding)), N):
        coset_index = standard_qim_extraction(carrier_embedding[item:item + N], b, alpha, coset_representative)
        secret_extration.append(coset_index)
    error = 0
    for item in range(len(secret_extration)):
        if secret_extration[item] != secret[item]:
            error += 1
    print(error)
