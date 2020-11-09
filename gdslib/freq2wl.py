import numpy as np
from scipy.constants import c


def freq2wl(f):
    return c / np.array(f)


if __name__ == "__main__":
    wl = freq2wl(193e12)
    print(wl * 1e9)
