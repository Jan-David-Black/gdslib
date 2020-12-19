from typing import Optional

import numpy as np
from SiPANN.nn import straightWaveguide_S

from gdslib.autoname import autoname
from gdslib.model_from_sparameters import model_from_sparameters


@autoname
def waveguide2(
    length: float = 10.0,
    width: float = 0.5,
    thickness: float = 0.22,
    sw_angle: float = 90.0,
    wavelength: Optional[np.array] = None,
    **kwargs,
):
    """Return simphony Model for a Straight waveguide."""
    if wavelength is None:
        wavelength = np.linspace(1200, 1600) * 1e-9
    s = straightWaveguide_S(
        wavelength=wavelength,
        width=width,
        thickness=thickness,
        sw_angle=sw_angle,
        length=length,
    )
    return model_from_sparameters(wavelength, s, pins=("E0", "W0"))


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from gdslib import plot_model

    c = waveguide2()
    print(c)
    plot_model(c)
    # plt.show()
