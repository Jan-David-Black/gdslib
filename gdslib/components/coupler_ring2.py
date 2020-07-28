import pp

from gdslib.autoname import autoname
from gdslib.model_from_gdsfactory import model_from_gdsfactory


@autoname
def coupler_ring2(
    c=pp.c.coupler_ring, wg_width=0.5, length_x=4.0, gap=0.2, bend_radius=5
):
    """ coupler for half a ring based on Lumerical 3D FDTD simulations

    Args:
        wg_width:0.5
        gap: 0.2
        length_x: 4
        bend_radius: 5

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
    if callable(c):
        c = c(wg_width=wg_width, length_x=length_x, gap=gap, bend_radius=bend_radius)
    m = model_from_gdsfactory(c)
    return m


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    wav = np.linspace(1520, 1570, 1024) * 1e-9
    f = 3e8 / wav
    c = coupler_ring2()
    s = c.s_parameters(freq=f)

    plt.plot(wav, np.abs(s[:, 1] ** 2))
    print(c.pins)
    plt.show()