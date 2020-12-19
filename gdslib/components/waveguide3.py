import numpy as np
from scipy.constants import c


def waveguide(wavelengths, length, loss_dB_cm, ne=2.40705, ng=4.17917, nd=0.000143768):
    """Returns the Sparameters for a waveguide based on OPICS."""
    w = wavelengths
    w0 = np.mean(w)
    alpha = loss_dB_cm / (20 * np.log10(np.exp(1)))

    K = (
        2 * np.pi * ne / w0
        + (ng / c) * (w - w0)
        - (nd * w0 ** 2 / (4 * np.pi * c)) * ((w - w0) ** 2)
    )

    s = np.zeros((len(wavelengths), 2, 2), dtype=complex)
    s[:, 0, 1] = s[:, 1, 0] = np.exp(-alpha * length + (K * length * 1j))
    return s


if __name__ == "__main__":
    w = np.linspace(1.50, 1.6, 128) * 1e-6
    s = waveguide(w, length=10e-6, loss_dB_cm=2)
    import matplotlib.pyplot as plt

    s21 = np.abs(s[:, 0, 1]) ** 2
    s21phase = np.angle(s[:, 0, 1])
    plt.plot(w, s21)
    plt.show()
