import pp

from gdslib.autoname import autoname
from gdslib.model_from_gdsfactory import model_from_gdsfactory


@autoname
def coupler2(c=pp.c.coupler, wg_width=0.5, length=20, gap=0.224):
    """ coupler for half a ring based on Lumerical 3D FDTD simulations

    Args:
        wg_width:0.5
        gap: 0.2
        length: 4

    .. code::

       W1 __             __ E1
            \           /
             \         /
              ========= gap
             /          \
           _/            \_
        W0      length    E0


    .. plot::
        :include-source:

        import gdslib as gl

        m = gl.c.coupler_ring()
        gl.plot_model(m)

    """
    if callable(c):
        c = c(wg_width=wg_width, length=length, gap=gap)
    m = model_from_gdsfactory(c)
    return m


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    wav = np.linspace(1520, 1570, 1024) * 1e-9
    f = 3e8 / wav
    c = pp.c.coupler(length=20, gap=0.224)
    m = coupler2(c=c)
    s = m.s_parameters(freq=f)

    plt.plot(wav, np.abs(s[:, 1] ** 2))
    print(m.pins)
    plt.show()
