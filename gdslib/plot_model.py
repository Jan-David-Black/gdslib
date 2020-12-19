import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import speed_of_light


def get_sparameters(c, wavelengths=None):
    if wavelengths is None:
        wavelengths = c.wavelengths
    f = speed_of_light / wavelengths
    return c.s_parameters(freq=f)


def plot_model(
    model, pin_in: str = "W0", pins=None, wavelengths=None, logscale=True, fig=None,
):
    """Plot simphony Sparameters for a model

    Args:
        model: simphony model
        pin_in: input pin name
        pins: list of pins
        wavelengths (m):
        logscale:
        fig: figure

    .. plot::
        :include-source:

        import gdslib as gl
        import gdslib.components as gc

        c = gc.mmi1x2()
        gl.plot_model(c)
    """
    m = model() if callable(model) else model

    if wavelengths is None:
        if hasattr(m, "wavelengths"):
            wavelengths = m.wavelengths
        else:
            wavelengths = np.linspace(1520e-9, 1580e-9, 2000)
    f = speed_of_light / wavelengths
    s = m.s_parameters(freq=f)

    pins = pins or m.pins
    if not isinstance(pins, (tuple, set, list)):
        raise ValueError(f"pins {pins} need to be a tuple, set or list")
    for pin in pins:
        if pin not in m.pins:
            raise ValueError(f"{pin} not in {m.pins}")

    if pin_in not in m.pins:
        raise ValueError(f"pin_in = `{pin_in}` not in {m.pins}")

    pin_in_index = m.pins.index(pin_in)

    fig = fig or plt.subplot()
    ax = fig.axes

    for pin_out in pins:
        pin_out_index = m.pins.index(pin_out)
        y = np.abs(s[:, pin_out_index, pin_in_index]) ** 2
        y = 10 * np.log10(y) if logscale else y
        ax.plot(wavelengths * 1e9, y, label=pin_out)
    ax.set_xlabel("wavelength (nm)")
    if logscale:
        ax.set_ylabel("S (dB)")
    else:
        ax.set_ylabel("S (%)")
    plt.legend()
    return ax


if __name__ == "__main__":
    from simphony.library import siepic
    import gdslib as gl

    w = np.linspace(1520, 1570, 1024) * 1e-9
    coupler = siepic.ebeam_dc_halfring_straight(
        gap=200e-9, radius=10e-6, width=500e-9, thickness=220e-9, couple_length=0.0
    )
    # m = gl.c.waveguide()
    # plot_model(m)

    plot_model(coupler, pin_in="n1")

    # plt.legend()
    # plt.show()
