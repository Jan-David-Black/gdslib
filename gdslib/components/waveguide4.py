"""SIPANN based model for waveguide."""
from itertools import combinations_with_replacement as comb_w_r
import numpy as np

from simphony.elements import Model
from gdslib.config import PATH


def waveguide(
    length,
    width=0.5,
    thickness=0.22,
    radius=5.0,
    sigma_length=0.0,
    sigma_width=5e-3,
    sigma_thickness=2e-3,
    sw_angle=90,
    loss_dB_per_m=700,
):
    """Return Waveguide Model.

    Args:
        length:
        width:
        thickness:
        radius:
        sigma_length:
        sigma_width:
        sigma_thickness:
        sw_angle: sidewall angle
        loss_dB_per_m: loss

    """
    return Waveguide(
        length=length,
        width=width,
        thickness=thickness,
        radius=radius,
        sigma_length=sigma_length,
        sigma_width=sigma_width,
        sigma_thickness=sigma_thickness,
        sw_angle=sw_angle,
        loss_dB_per_m=loss_dB_per_m,
    )


class Waveguide(Model):
    """Neural-net trained model of a waveguide.

    A waveguide easily connects other components within the circuit.
    The SiP-ANN waveguide is different from the EBeam package since its
    values are calculated based on a regression fit to simulation data.

    Args:
        length: length of the waveguide in microns.
        width: width of the waveguide in microns.
        thickness: The thickness of the waveguide in microns.
        radius: radius of the waveguide bends in microns.
        sigma_length: standard deviation
        sigma_width: width standard deviation (um)
        sigma_thickness: thickness standard deviation (um)
        sw_angle: sidewall angle
        loss_dB_per_m: loss (dB/m)
    """

    pins = ("W0", "E0")  #: The default pin names of the device
    # pins = ("n1", "n2")  #: The default pin names of the device
    freq_range = (
        187370000000000.0,
        199862000000000.0,
    )  #: The valid frequency range for this model.

    def __init__(
        self,
        length: float,
        width: float = 0.5,
        thickness: float = 0.22,
        radius: float = 5.0,
        sigma_length: float = 0.0,
        sigma_width: float = 5e-3,
        sigma_thickness: float = 2e-3,
        sw_angle: float = 90.0,
        loss_dB_per_m: float = 700.0,
    ):
        self.length = length
        self.width = width
        self.thickness = thickness
        self.radius = radius
        self.sigma_length = sigma_length
        self.sigma_width = sigma_width
        self.sigma_thickness = sigma_thickness
        self.regenerate_monte_carlo_parameters()
        self.sw_angle = sw_angle
        self.loss_dB_per_m = loss_dB_per_m

    def s_parameters(self, freq):
        s = self.ann_s_params(freq, self.length, self.width, self.thickness)
        return s

    def monte_carlo_s_parameters(self, freq, *args, **kwargs):
        return self.ann_s_params(
            freq, self.rand_length, self.rand_width, self.rand_thickness
        )

    def regenerate_monte_carlo_parameters(self):
        self.rand_width = np.random.normal(self.width, self.sigma_width)
        self.rand_thickness = np.random.normal(self.thickness, self.sigma_thickness)
        self.rand_length = np.random.normal(self.length, self.sigma_length)

    @staticmethod
    def cartesian_product(arrays):
        la = len(arrays)
        dtype = np.find_common_type([a.dtype for a in arrays], [])
        arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
        for i, a in enumerate(np.ix_(*arrays)):
            arr[..., i] = a
        return arr.reshape(-1, la)

    @staticmethod
    def straightWaveguide(wavelength, width, thickness, angle):
        # Sanitize the input
        if type(wavelength) is np.ndarray:
            wavelength = np.squeeze(wavelength)
        else:
            wavelength = np.array([wavelength])
        if type(width) is np.ndarray:
            width = np.squeeze(width)
        else:
            width = np.array([width])
        if type(thickness) is np.ndarray:
            thickness = np.squeeze(thickness)
        else:
            thickness = np.array([thickness])
        if type(angle) is np.ndarray:
            angle = np.squeeze(angle)
        else:
            angle = np.array([angle])

        INPUT = Waveguide.cartesian_product([wavelength, width, thickness, angle])

        # Get all possible combinations to use
        degree = 4
        features = 4
        combos = []
        for i in range(degree + 1):
            combos += [k for k in comb_w_r(range(features), i)]

        # make matrix of all combinations
        n = len(INPUT)
        polyCombos = np.ones((n, len(combos)))
        for j, c in enumerate(combos):
            if c == ():
                polyCombos[:, j] = 1
            else:
                for k in c:
                    polyCombos[:, j] *= INPUT[:, k]

        # get coefficients and return
        coeffs = np.load(
            PATH.sp / "sipann" / "ebeam_wg_integral_1550" / "straightCoeffs.npy"
        )
        return polyCombos @ coeffs

    def ann_s_params(self, frequency, length, width, thickness):
        """
        Function that calculates the s-parameters for a waveguide using the ANN model

        Parameters
        ----------
        frequency : np.array
        length : float
        width : float
        thickness : float

        Returns
        -------
        s : np.ndarray
            Returns a tuple containing the frequency array, `frequency`,
            corresponding to the calculated s-parameter matrix, `s`.
        """

        mat = np.zeros((len(frequency), 2, 2), dtype=complex)
        c0 = 299792458  # m/s
        # mode = 0  # TE

        TE_loss = self.loss_dB_per_m / 1e6  # dB/um for width 500nm
        alpha = TE_loss / (20 * np.log10(np.exp(1)))  # assuming lossless waveguide
        waveguideLength = length

        # calculate wavelength
        wl = np.true_divide(c0, frequency)

        # effective index is calculated by the ANN
        neff = self.straightWaveguide(np.transpose(wl), width, thickness, self.sw_angle)

        # K is calculated from the effective index and wavelength
        K = 2 * np.pi * np.true_divide(neff, wl)

        # the s-matrix is built from alpha, K, and the waveguide length
        for x in range(0, len(neff)):
            mat[x, 0, 1] = mat[x, 1, 0] = np.exp(
                -alpha * waveguideLength + (K[x] * waveguideLength * 1j)
            )
        s = mat

        return s


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from gdslib.plot_model import plot_model

    c = waveguide(length=1e6)
    plot_model(c)
    plt.show()
