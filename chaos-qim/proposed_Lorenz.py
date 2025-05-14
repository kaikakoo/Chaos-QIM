import numpy as np


def lorenz_system(x, y, z, a, b, c, dt):
    x_dot = a * (y - x)
    y_dot = x * (b - z) - y
    z_dot = x * y - c * z
    x = x + x_dot * dt
    y = y + y_dot * dt
    z = z + z_dot * dt
    return x, y, z


def improved_lorenz(x, y, z, a, b, c, tau, dt, steps):
    x_vals, y_vals, z_vals = [], [], []
    x_hist, y_hist, z_hist = [x], [y], [z]
    for i in range(steps):
        if i > tau:
            x_mod = (x + x_hist[i - tau] + np.sin(i * dt)) % 1
            y_mod = (y + y_hist[i - tau] + np.sin(i * dt)) % 1
            z_mod = (z + z_hist[i - tau] + np.sin(i * dt)) % 1
        else:
            x_mod, y_mod, z_mod = x, y, z
        x, y, z = lorenz_system(x_mod, y_mod, z_mod, a, b, c, dt)
        x_hist.append(x)
        y_hist.append(y)
        z_hist.append(z)
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)
    return x_vals, y_vals, z_vals


if __name__ == '__main__':
    a = 20
    b = 50
    c = 8
    tau = 1
    dt = 0.1
    steps = 500
    x0, y0, z0 = 0.01, 0.02, 0.01

    x_vals, y_vals, z_vals = improved_lorenz(x0, y0, z0, a, b, c, tau, dt, steps)
