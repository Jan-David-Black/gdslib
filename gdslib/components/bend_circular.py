import numpy as np
from SiPANN.scee import Waveguide
from SiPANN.scee_int import SimphonyWrapper

from gdslib import plot_model
from gdslib.autoname import autoname


@autoname
def bend_circular(
    radius: float = 10.0,
    width: float = 0.5,
    thickness: float = 0.22,
    angle: int = 90,
    sw_angle: float = 90.0,
    **kwargs,
):
    """Returns simphony Model for a bend using a waveguide
    notice that this is fake bend!

    Args:
        radius: Radius of waveguide in microns.
        width: Width of the waveguides in microns
        thickness: Thickness of the waveguides in microns
        angle: Number of deg of circle that bent waveguide transverses
        sw_angle: Sidewall angle from horizontal in degrees, ie 90 makes a square. Defaults to 90.
        wavelength:  Wavelength points to evaluate

    """
    angle = np.deg2rad(angle)
    width = width * 1e3
    thickness = thickness * 1e3
    length = angle * radius * 1e3

    s = Waveguide(width=width, thickness=thickness, sw_angle=sw_angle, length=length)
    s2 = SimphonyWrapper(s)
    s2.pins = ("W0", "N0")
    return s2


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = bend_circular()
    plot_model(c)
    plt.show()
