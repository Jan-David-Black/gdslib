from SiPANN.scee import Waveguide
from SiPANN.scee_int import SimphonyWrapper

from gdslib import plot_model
from gdslib.autoname import autoname


@autoname
def waveguide(
    length: float = 10.0,
    width: float = 0.5,
    thickness: float = 0.22,
    sw_angle: float = 90.0,
    **kwargs,
):
    """Returns simphony Model for a Straight waveguide

    Args:
        length : float or ndarray Length of the waveguide in um.
        width : float or ndarray Width of the waveguide in um (Valid for 0.4-0.6)
        thickness : float or ndarray Thickness of waveguide in um (Valid for 180nm-240nm)
        sw_angle : float or ndarray, optional Sidewall angle of waveguide from horizontal in degrees (Valid for 80-90 degrees). Defaults to 90.

    """
    width = width * 1e3
    thickness = thickness * 1e3
    length = length * 1e3

    s = Waveguide(width=width, thickness=thickness, sw_angle=sw_angle, length=length,)
    s2 = SimphonyWrapper(s)
    s2.pins = ("W0", "E0")
    return s2


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = waveguide()
    print(c)
    plot_model(c)
    plt.show()
