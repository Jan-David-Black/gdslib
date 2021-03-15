from gdslib.autoname import autoname
from gdslib.config import path
from gdslib.model_from_sparameters import model_from_filepath


@autoname
def gc1550te(filepath=path.sp / "gc2dte" / "gc1550.dat", numports=2):
    """Returns Sparameter model for 1550nm TE grating_coupler.

    .. plot::
        :include-source:

        import gdslib as gl

        c = gl.c.gc1550te()
        gl.plot_model(c)
    """
    return model_from_filepath(filepath=filepath, numports=numports)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    wav = np.linspace(1520, 1570, 1024) * 1e-9
    f = 3e8 / wav
    c = gc1550te()
    s = c.s_parameters(freq=f)

    plt.plot(wav, np.abs(s[:, 1] ** 2))
    print(c.pins)
    plt.show()
