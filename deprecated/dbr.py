""" Bragg simulator using transfer matrix method (TMM) approach
adapted from https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


# set the wavelength span for the simulation
wavelength_start = 1500e-9
wavelength_stop = 1600e-9
resolution = 0.1
wavelengths = np.linspace(
    wavelength_start,
    wavelength_stop,
    round((wavelength_stop - wavelength_start) * 1e9 / resolution),
)

# Grating straight compact model (cavity)
# these are polynomial fit constants from a straight width of 500 nm
n1_wg = 4.077182700600432
n2_wg = -0.982556173493906
n3_wg = -0.046366956781710

# Cavity straight compact model (cavity)
# these are polynomial fit constants from a straight width of 500 nm
n1_c = 4.077182700600432
n2_c = -0.982556173493906
n3_c = -0.046366956781710

# grating parameters
period = 317e-9
dn = 0.0  # effective index perturbation
lambda_Bragg = 1550e-9
dw = 20e-9
kappa = -1.53519e19 * dw ** 2 + 2.2751e12 * dw
dn = kappa * lambda_Bragg / 2
n_periods = 200  # number of periods (left of cavity)

# Cavity Parameters
alpha_dBcm = 7  # dB per cm
alpha = np.log(10) * alpha_dBcm / 10 * 100.0  # per meter
L = period / 2  # length of cavity


def tmatrix_straight(wavelength, neff, length):
    """straight

    Args:
        wavelength (same units as length)
        neff: effective index
        length (same units as wavelength)
    """
    beta = 2 * np.pi * neff / wavelength - 1j * alpha / 2
    v = [np.exp(1j * beta * length), np.exp(-1j * beta * length)]
    T_hw = np.diag(v)
    return T_hw


def tmatrix_boundary(neff1, neff2):
    a = (neff1 + neff2) / (2 * np.sqrt(neff1 * neff2))
    b = (neff1 - neff2) / (2 * np.sqrt(neff1 * neff2))

    T_is = [[a, b], [b, a]]
    return T_is


def tmatrix_dbr(wavelength, n1, n2, period, n_periods=n_periods):
    """ DBR Tmatrix """
    length = period / 2
    T_hw1 = tmatrix_straight(wavelength, n1, length)
    T_is12 = tmatrix_boundary(n1, n2)
    T_hw2 = tmatrix_straight(wavelength, n2, length)
    T_is21 = tmatrix_boundary(n2, n1)
    Tp1 = np.matmul(T_hw1, T_is12)
    Tp2 = np.matmul(T_hw2, T_is21)
    Tp = np.matmul(Tp1, Tp2)
    return np.linalg.matrix_power(Tp, n_periods)


def tmatrix_dbr_cavity(
    wavelength, n1, n2, period, length=0.01, n_periods_left=600, n_periods_right=600,
):
    """ 2 DBR with a straight cavity of length in the middle"""
    T_hw1 = tmatrix_straight(wavelength, n1, period / 2)
    T_is12 = tmatrix_boundary(n1, n2)
    T_hw2 = tmatrix_straight(wavelength, n2, period / 2)
    T_is21 = tmatrix_boundary(n2, n1)

    Tp1 = np.matmul(T_hw1, T_is12)
    Tp2 = np.matmul(T_hw2, T_is21)
    Tp_Left = np.matmul(Tp1, Tp2)

    T_cavity = tmatrix_straight(wavelength, n1, length)

    Tp1 = np.matmul(T_hw1, T_is12)
    Tp2 = np.matmul(T_hw2, T_is21)
    Tp_Right = np.matmul(Tp1, Tp2)

    return np.matmul(
        np.matmul(np.linalg.matrix_power(Tp_Left, n_periods_left), T_cavity),
        np.linalg.matrix_power(Tp_Right, n_periods_right),
    )


def tmatrix_t_r(M):
    """returns Tmatrix Transmission and Reflection coefficients"""
    T = np.abs(1 / M[0][0]) ** 2
    R = np.abs(M[1][0] / M[0][0]) ** 2.0  # or M[0][1]?
    return [T, R]


def smatrix(tmatrix):
    m = tmatrix
    t11 = m[0][0]
    t12 = m[0][1]
    t21 = m[1][0]
    t22 = m[1][1]

    s11 = t21 / t11
    s12 = t22 - t12 * t21 / t11
    s21 = 1 / t11
    s22 = -t12 / t11
    return np.array([[s11, s12], [s21, s22]])


def dbr_r(wavelengths, dn, period=period, tmax_dB=0):
    """ DBR reflection """
    wavelengths = wavelengths
    neff0 = n1_wg + n2_wg * (wavelengths * 1e6) + n3_wg * (wavelengths * 1e6) ** 2
    n1 = neff0 - dn / 2
    n2 = neff0 + dn / 2

    R = []
    T = []
    for wavelength, n1i, n2i in zip(wavelengths, n1, n2):
        m = tmatrix_dbr(
            wavelength=wavelength, n1=n1i, n2=n2i, period=period, n_periods=n_periods
        )
        [t, r] = tmatrix_t_r(m)
        R.append(r)
        T.append(t)

    return tmax_dB + 10 * np.log10(R)


def plot_tmatrix_dbr(dn=dn, period=period, n_periods=600, title="DBR TMM spectrum"):
    wavelengths = np.linspace(
        wavelength_start,
        wavelength_stop,
        round((wavelength_stop - wavelength_start) * 1e9 / resolution),
    )
    neff0 = n1_wg + n2_wg * (wavelengths * 1e6) + n3_wg * (wavelengths * 1e6) ** 2

    n1 = neff0 - dn / 2
    n2 = neff0 + dn / 2

    R = []
    T = []
    for wavelength, n1i, n2i in zip(wavelengths, n1, n2):
        m = tmatrix_dbr(
            wavelength=wavelength, n1=n1i, n2=n2i, period=period, n_periods=n_periods
        )
        [t, r] = tmatrix_t_r(m)
        R.append(r)
        T.append(t)

        # s = smatrix(m)
        # R.append(np.abs(s[0][0]))
        # T.append(np.abs(s[0][1]))

    f, ax = plt.subplots()
    plt.plot(wavelengths * 1e9, 10 * np.log10(T), label="Transmission", color="blue")
    plt.plot(wavelengths * 1e9, 10 * np.log10(R), label="Reflection", color="red")
    plt.legend(loc=0)
    plt.ylabel("Response (dB)", color="black")
    plt.xlabel("Wavelength (nm)", color="black")
    plt.xlim(round(min(wavelengths * 1e9)), round(max(wavelengths * 1e9)))
    plt.title(title)
    plt.show()
    return f, ax


def plot_smatrix_dbr_cavity(dn=dn, title="DBR cavity", length=20e-6, n_periods=600):
    wavelengths = np.linspace(
        wavelength_start,
        wavelength_stop,
        round((wavelength_stop - wavelength_start) * 1e9 / resolution),
    )
    neff0 = n1_wg + n2_wg * (wavelengths * 1e6) + n3_wg * (wavelengths * 1e6) ** 2

    n1 = neff0 - dn / 2
    n2 = neff0 + dn / 2

    R = []
    T = []
    for wavelength, n1i, n2i in zip(wavelengths, n1, n2):
        m = tmatrix_dbr_cavity(
            wavelength=wavelength, n1=n1i, n2=n2i, period=period, length=length
        )
        s = smatrix(m)
        R.append(np.abs(s[0][0]))
        T.append(np.abs(s[0][1]))

    f, ax = plt.subplots()
    plt.plot(wavelengths * 1e9, 10 * np.log10(T), label="Transmission", color="blue")
    plt.plot(wavelengths * 1e9, 10 * np.log10(R), label="Reflection", color="red")
    plt.legend(loc=0)
    plt.ylabel("Response (dB)", color="black")
    plt.xlabel("Wavelength (nm)", color="black")
    plt.xlim(round(min(wavelengths * 1e9)), round(max(wavelengths * 1e9)))
    plt.title(title)
    plt.show()
    return f, ax


if __name__ == "__main__":
    # plot_smatrix_dbr_cavity()
    # plot_tmatrix_dbr(dn=0.15, period=period)

    r = dbr_r(wavelengths=wavelengths, dn=0.05, tmax_dB=-5)
    plt.plot(wavelengths, r)
    plt.show()
