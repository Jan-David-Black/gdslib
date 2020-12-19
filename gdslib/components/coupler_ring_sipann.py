from SiPANN.scee import HalfRacetrack


def coupler_ring_sipann(
    bend_radius: float = 5,
    wg_width: float = 0.5,
    thickness: float = 0.22,
    gap: float = 0.22,
    length_x: float = 4.0,
    sw_angle: float = 90.0,
):
    r"""Returns coupler for half a ring

    Args:
        bend_radius: 5
        wg_width: float or ndarray Width of the waveguide in um (Valid for 0.4-0.6)
        thickness : float or ndarray Thickness of waveguide in um (Valid for 0.18-0.24)
        gap : float or ndarray Minimum distance between the two waveguides edge in um. (Must be > 0.1)
        length_x: Length of straight portion of ring waveguide in um
        sw_angle: waveguide Sidewall angle


    .. code::

            2 \           / 4
               \         /
                ---------
            1---------------3
    """

    width = wg_width * 1e3
    thickness = thickness * 1e3
    gap = gap * 1e3
    length = length_x * 1e3
    radius = bend_radius * 1e3
    # print(f'ignoring {kwargs}')

    return HalfRacetrack(
        radius=radius,
        width=width,
        thickness=thickness,
        gap=gap,
        length=length,
        sw_angle=sw_angle,
    )


if __name__ == "__main__":
    hr = coupler_ring_sipann()
    hr.gds(view=True, extra=0, units="microns")
