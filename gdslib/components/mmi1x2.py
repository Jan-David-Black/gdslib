import pp

from gdslib.autoname import autoname
from gdslib.model_from_gdsfactory import model_from_gdsfactory
from gdslib.plot_model import plot_model


@autoname
def mmi1x2(**kwargs):
    """Return 1x2 MultiModeInterferometer Sparameter model.

    Args:
        width: input and output waveguide width
        width_taper: interface between input waveguides and mmi region
        length_taper: into the mmi region
        length_mmi: in x direction
        width_mmi: in y direction
        gap_mmi:  gap between tapered wg
        taper: taper function
        layer:
        layers_cladding:
        cladding_offset
        tech: technology

    .. code::

               length_mmi
                <------>
                ________
               |        |
               |         \__
               |          __  E1
            __/          /_ _ _ _
        W0  __          | _ _ _ _| gap_mmi
              \          \__
               |          __  E0
               |         /
               |________|

             <->
        length_taper

    .. plot::
      :include-source:

      import pp
      c = pp.c.mmi1x2(width_mmi=2, length_mmi=2.8)
      c.plot()

    .. plot::
        :include-source:

        import gdslib as gl

        c = gl.c.mmi1x2()
        gl.plot_model(c)
    """
    return model_from_gdsfactory(pp.c.mmi1x2, **kwargs)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    wav = np.linspace(1520, 1570, 1024) * 1e-9
    f = 3e8 / wav
    c = mmi1x2()

    # s = c.s_parameters(freq=f)
    # plt.plot(wav, np.abs(s[:, 1] ** 2))
    # print(c.pins)
    # print(c.settings)

    plot_model(c)
    plt.show()
