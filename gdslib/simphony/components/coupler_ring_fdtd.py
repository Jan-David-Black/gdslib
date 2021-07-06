import pp

from gdslib.autoname import autoname
from gdslib.simphony.model_from_gdsfactory import model_from_gdsfactory


@autoname
def coupler_ring_fdtd(
    factory=pp.c.coupler_ring, width=0.5, length_x=4.0, gap=0.2, radius=5
):
    r"""Return half ring model based on Lumerical 3D FDTD simulations.

    Args:
        c: gdsfactory component
        width:0.5
        gap: 0.2
        length_x: 4
        radius: 5

    .. code::

           N0            N1
           |             |
            \           /
             \         /
           ---=========---
        W0    length_x    E0


    """
    coupler = (
        factory(width=width, length_x=length_x, gap=gap, radius=radius)
        if callable(factory)
        else factory
    )
    return model_from_gdsfactory(coupler)


if __name__ == "__main__":
    import gdslib.simphony as gs
    import matplotlib.pyplot as plt
    import numpy as np

    wav = np.linspace(1520, 1570, 1024) * 1e-9
    c = coupler_ring_fdtd()
    wavelengths = np.linspace(1.5, 1.6) * 1e-6
    gs.plot_model(c, wavelengths=wavelengths)
    plt.show()

    # f = 3e8 / wav
    # s = c.s_parameters(freq=f)
    # plt.plot(wav, np.abs(s[:, 1] ** 2))
    # print(c.pins)
    # plt.show()