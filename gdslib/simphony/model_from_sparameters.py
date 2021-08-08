from pathlib import PosixPath
from typing import Tuple

import gdsfactory as gf
import gdsfactory.sp as sp
import numpy as np
from scipy.constants import speed_of_light
from simphony.elements import Model
from simphony.tools import freq2wl, interpolate, wl2freq


def model_from_filepath(filepath: PosixPath, numports: int, name: str = "model"):
    """Returns a Simphony Model.

    Args:
        filepath: path to Sparameters in Lumerical interconnect format
        numports: numer of ports
        name: model name

    """
    pins, f, s = sp.read_sparameters_lumerical(filepath=filepath, numports=numports)
    wavelengths = freq2wl(f)
    return model_from_sparameters(
        wavelengths=wavelengths, sparameters=s, pins=pins, name=name
    )


def model_from_sparameters(
    wavelengths, sparameters, pins: Tuple[str, ...] = ("E0", "W0"), name: str = "model"
):
    """Returns simphony model from wavelengths and Sparameters."""

    f = wl2freq(wavelengths)
    s = sparameters

    def interpolate_sp(freq):
        return interpolate(freq, f, s)

    m = Model()
    m.pins = pins
    m.s_params = (f, s)
    m.s_parameters = interpolate_sp
    m.freq_range = (min(f), max(f))
    m.wavelength_range = (min(wavelengths), max(wavelengths))
    m.wavelengths = speed_of_light / np.array(f)
    m.s = s
    m.name = name
    m.__name__ = name
    return m


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    from gdslib.plot_model import plot_model

    filepath = gf.CONFIG["sp"] / "mmi1x2" / "mmi1x2_S220.dat"
    numports = 3
    c = model_from_filepath(filepath=filepath, numports=numports)
    plot_model(c)
    plt.show()

    # wav = np.linspace(1520, 1570, 1024) * 1e-9
    # f = speed_of_light / wav
    # s = c.s_parameters(freq=f)
    # wav = c.wavelengths
    # s = c.s
    # plt.plot(wav * 1e9, np.abs(s[:, 1] ** 2))
