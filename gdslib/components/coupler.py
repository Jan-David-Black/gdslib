from SiPANN.scee import Standard
from SiPANN.scee_int import SimphonyWrapper

from gdslib.autoname import autoname
from gdslib.plot_model import plot_model


@autoname
def coupler(
    width: float = 0.5,
    thickness: float = 0.22,
    gap: float = 0.22,
    length: float = 10.0,
    sw_angle: float = 90.0,
    H: float = 1.5,
    V: float = 0.0,
    **kwargs,
):
    r"""Return simphony Directional coupler model.

    Args:
        width: Width of the waveguide in um (Valid for 0.4-0.6)
        thickness: Thickness of waveguide in um (Valid for 0.18-0.24)
        gap: Minimum distance between the two waveguides edge in um. (Must be > 0.1)
        length: float or ndarray Length of the straight portion of both waveguides in um.
        H: Horizontal distance between end of coupler until straight portion in nm.
        V: Vertical distance between end of coupler until straight portion in um.
        sw_angle: Sidewall angle from horizontal in degrees

    This is what most people think of when they think directional coupler. Ports are numbered as

    .. code::
                           <--H-->
            W1 2---\      /-------- 4 E1
                    ------        |
                                  | V
                    ------        |
            W0 1---/      \-------- 3 E0

    .. plot::
        :include-source:

        import gdslib as gl

        c = gl.c.coupler()
        gl.plot_model(c)

    """

    width = width * 1e3
    thickness = thickness * 1e3
    gap = gap * 1e3
    length = length * 1e3
    H = H * 1e3
    V = V * 1e3

    s = Standard(
        width=width,
        thickness=thickness,
        gap=gap,
        length=length,
        H=H,
        V=V,
        sw_angle=sw_angle,
    )
    s2 = SimphonyWrapper(s)
    s2.pins = ("W0", "W1", "E0", "E1")
    return s2


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = coupler()
    print(c)
    plot_model(c)
    plt.show()
