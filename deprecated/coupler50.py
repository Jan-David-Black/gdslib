import ctypes
from numba import njit
from numba.extending import get_cython_function_address
import numpy as np
from SiPANN import scee

from simphony.elements import Model
from simphony.tools import freq2wl, interpolate

from gdslib.config import PATH


class coupler50(Model):
    """Regression Based form of a 50/50 directional coupler at lambda=1550nm"""

    # pins = ("n1", "n2", "n3", "n4")  #: The default pin names of the device
    pins = ("W0", "W1", "E0", "E1")  #: The default pin names of the device
    loaded = np.load(PATH.sp / "sipann" / "sipann_scee_fifty_s.npz")
    s_params = (loaded["f"], loaded["s"])
    freq_range = (
        s_params[0][0],
        s_params[0][-1],
    )  #: The valid frequency range for this model.

    def s_parameters(self, freq):
        return interpolate(freq, self.s_params[0], self.s_params[1])

    def s_parameters2(self, freq: np.ndarray) -> np.ndarray:
        """Return s-parameters of a parameterized 50/50 directional coupler.

        Args:
            freq: A frequency array to calculate s-parameters over (in Hz).

        Returns:
            s: Returns the calculated s-parameter matrix.
        """
        loaded = np.load(PATH.sp / "sipann" / "sipann_fifty.npz")
        x = loaded["GAP"]
        b = loaded["LENGTH"]

        # load scipy.special.binom as a C-compiled function
        addr = get_cython_function_address("scipy.special.cython_special", "binom")
        functype = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)
        binom_fn = functype(addr)

        # load all seperate functions that we'll need
        n = len(x) - 1

        @njit
        def binom_in_njit(x, y):
            return binom_fn(x, y)

        @njit
        def bernstein(n, j, t):
            return binom_in_njit(n, j) * t ** j * (1 - t) ** (n - j)

        @njit
        def bez(t):
            n = len(x) - 1
            return np.sum(
                np.array([(x[j]) * bernstein(n, j, t / b) for j in range(len(x))]),
                axis=0,
            )

        @njit
        def dbez(t):
            return (
                np.sum(
                    np.array(
                        [
                            n
                            * (x[j])
                            * (
                                bernstein(n - 1, j - 1, t / b)
                                - bernstein(n - 1, j, t / b)
                            )
                            for j in range(len(x))
                        ]
                    ),
                    axis=0,
                )
                / b
            )

        # resize everything to nms
        width = 500
        thickness = 220

        # switch to wavelength
        wl = freq2wl(freq) * 1e9

        item = scee.GapFuncSymmetric(width, thickness, bez, dbez, 0, b)
        return item.sparams(wl)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from gdslib.simphony.plot_model import plot_model

    # loaded = np.load(PATH.sp / 'sipann'/ "sipann_scee_fifty.npz")

    c = coupler50()
    plot_model(c)
    plt.show()
