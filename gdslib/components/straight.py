from SiPANN.scee import Waveguide
from SiPANN.scee_int import SimphonyWrapper
from gdslib.autoname import autoname


@autoname
def straight(
    length: float = 10.0,
    width: float = 0.5,
    thickness: float = 0.22,
    sw_angle: float = 90.0,
    **kwargs,
):
    """Return simphony Model for a Straight straight.

    Args:
        length: Length of the straight in um.
        width: Width of the straight in um (Valid for 0.4-0.6)
        thickness: Thickness of straight in um (Valid for 180nm-240nm)
        sw_angle: Sidewall angle. Valid for 80-90 degrees.
        kwargs: geometrical args that this model ignores

    """
    width = width * 1e3
    thickness = thickness * 1e3
    length = length * 1e3

    s = Waveguide(width=width, thickness=thickness, sw_angle=sw_angle, length=length)
    s2 = SimphonyWrapper(s)
    s2.pins = ("W0", "E0")
    return s2


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = straight()

    # wav = np.linspace(1520, 1570, 3) * 1e-9
    # f = 3e8 / wav
    # s = c.s_parameters(freq=f)
    # _, rows, cols = np.shape(s)
    # sdict = {
    #     f"S{i+1}{j+1}": np.abs(s[:, i, j]).tolist()
    #     for i in range(rows)
    #     for j in range(cols)
    # }
    # print(sdict)

    # plot_model(c, logscale=False)
    # plt.show()
