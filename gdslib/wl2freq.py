import numpy as np
from scipy.constants import c


def wl2freq(wl):
    return c / np.array(wl)


if __name__ == "__main__":
    f = wl2freq(1550e-9)
    print(f / 1e12)
