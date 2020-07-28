from SiPANN.scee import HalfRacetrack
from SiPANN.scee_int import SimphonyWrapper

from gdslib.autoname import autoname


@autoname
def coupler_ring(
    bend_radius: float = 5,
    wg_width: float = 0.5,
    thickness: float = 0.22,
    gap: float = 0.22,
    length_x: float = 4.0,
    sw_angle: float = 90.0,
    **kwargs
):
    """coupler for half a ring

    Args:
        bend_radius: 5
        wg_width: float or ndarray Width of the waveguide in um (Valid for 0.4-0.6)
        thickness : float or ndarray Thickness of waveguide in um (Valid for 0.18-0.24)
        gap : float or ndarray Minimum distance between the two waveguides edge in um. (Must be > 0.1)
        length_x: Length of straight portion of ring waveguide in um

    .. code::

           N0            N1
           |             |
            \           /
             \         /
           ---=========---
        W0    length_x    E0

    .. plot::
        :include-source:

        import gdslib as gl

        m = gl.c.coupler_ring()
        gl.plot_model(m)

    """

    width = wg_width * 1e3
    thickness = thickness * 1e3
    gap = gap * 1e3
    length = length_x * 1e3
    radius = bend_radius * 1e3
    # print(f'ignoring {kwargs}')

    s = HalfRacetrack(
        radius=radius,
        width=width,
        thickness=thickness,
        gap=gap,
        length=length,
        sw_angle=sw_angle,
    )
    s2 = SimphonyWrapper(s)
    s2.pins = ("W0", "W1", "E0", "E1")
    return s2


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from gdslib import plot_model

    c = coupler_ring()
    print(c)
    plot_model(c)
    plt.show()
