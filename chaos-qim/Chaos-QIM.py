import numpy as np
from SDCVP import SDCVP
import math
import random
from Lattice.Lattice_basis import Lattice_Basis
from Logistic import uniform_transmit
from proposed_Lorenz import improved_lorenz


def chaos_qim_embedding(p: np.array, s: np.array, basic: np.array, a: int,
                        representative: list[np.array], dither: np.array) -> np.array:
    """
     p: carrier signal
     s: secret message
     b: lattice basis
     a: magnification factor
     representative: coset representative
     dither: external dither

    """

    sub_basic = a * basic
    k = np.dot(sub_basic,
               SDCVP(p - dither - np.dot(basic, representative[s]), sub_basic))
    m = k + np.dot(basic, representative[s]) + dither
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


def chaos_qim_extraction(p: np.array, basic: np.array, a: int, representative: list[np.array],
                         dither: np.array) -> int:
    k = SDCVP(p - dither, basic, )
    for i in range(len(representative)):
        if (k % a == representative[i]).all():
            break
    return i

if __name__ == '__main__':
    N = 2
    B_name = 'A2'
    m = Lattice_Basis(B_name, N)

    t_span = (0, 100)
    x_state = [0, 1, 0]
    start = 1

    a = 20
    b = 50
    c = 8
    tau = 1
    dt = 0.01
    steps = 100
    x0, y0, z0 = 0.01, 0.01, 0.02

    n = 100
    d = 2
    miu = 10000

    alpha = 2
    delta = 1
    dither_num = 4500

    x_vals, y_vals, z_vals = improved_lorenz(x0, y0, z0, a, b, c, tau, dt, steps)
    lorenz_proposed_data = np.asarray(x_vals)
    lorenz_proposed_data1 = uniform_transmit(lorenz_proposed_data, miu, d, n)

    edf_dither = lorenz_proposed_data1[start:start + dither_num]
    edf_dither1 = np.asarray(edf_dither)
    edf_dither2 = edf_dither1.tolist()

    num_carrier = 4500

    m = m * delta
    coset_representative = cosets(alpha, N)
    coset_representatives = np.dot(coset_representative, m)
    length = round(math.log(len(coset_representative), alpha))

    np.random.seed(1)
    carrier = np.random.uniform(-15, 15, num_carrier)
    num_secret = pow(alpha, N)
    secret = np.random.randint(0, num_secret, size=math.floor(num_carrier / N))
    edf_dither3 = edf_dither1[:num_carrier]
    num = 0
    chaos_mse = 0
    chaos_sequence = []
    for item in range(0, len(carrier), N):
        carrier_sample = chaos_qim_embedding(carrier[item: item + N], secret[num], m, alpha, coset_representative,
                                             edf_dither3[item:item + N])
        chaos_sequence = np.concatenate([chaos_sequence, carrier_sample])
        chaos_mse += sum(pow(carrier_sample - carrier[item: item + N], 2)) / N
        num += 1

    secret_extration = []
    x = round(len(chaos_sequence) / N)
    for item in range(0, round(len(chaos_sequence)), N):
        coset_index = chaos_qim_extraction(chaos_sequence[item:item + N], m, alpha, coset_representative,
                                           edf_dither3[item:item + N])
        secret_extration.append(coset_index)
    error = 0
    for item in range(len(secret_extration)):
        if secret_extration[item] != secret[item]:
            error += 1
    print("number of error extraction:")
    print(error)

    J = alpha * np.eye(N)
    R = 1 / N * math.log(np.linalg.det(J), 2)
    print("code rate:", R)

    chaos_MSE = np.mean((carrier - chaos_sequence) ** 2)
    print("MSE of chaos-QIM:", chaos_MSE)

    chaos_PSNR = 10 * math.log(1 / chaos_MSE, 10)  # max(carrier) - min(carrier)
    print('PSNR of chaos-QIM:', chaos_PSNR)

    chaos_PRD = np.sqrt(np.sum((carrier - chaos_sequence) ** 2) / np.sum(carrier ** 2)) * 100
    print('PRD of chaos-qim:', chaos_PRD)
