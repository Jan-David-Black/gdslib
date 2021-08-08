from simphony.netlist import Subcircuit

from gdslib.autoname import autoname
from gdslib.simphony.components.coupler_ring import coupler_ring
from gdslib.simphony.components.straight import straight
from gdslib.simphony.plot_circuit import plot_circuit


@autoname
def ring_double(
    wg_width=0.5,
    gap=0.2,
    length_x=4,
    bend_radius=5,
    length_y=2,
    coupler=coupler_ring,
    straight=straight,
):
    r"""Return double bus ring Model made of two couplers (ct: top, cb: bottom)
    connected with two vertical straights (yl: left, wr: right)

    .. code::

         --==ct==--
          |      |
          wl     wr length_y
          |      |
         --==cb==-- gap

          length_x


           ---=========---
        E0    length_x    W0
             /         \
            /           \
           |             |
           N1           N0 ___
                            |
          wl            wr  | length_y
                           _|_
           N0            N1
           |             |
            \           /
             \         /
           ---=========---
        W0    length_x    E0



    .. plot::
      :include-source:

      import gdsfactory as gf

      c = gf.components.ring_double(width=0.5, gap=0.2, length_x=4, radius=5, length_y=2)
      c.plot()


    .. plot::
        :include-source:

        import gdslib.simphony as gs
        import gdslib.simphony.components as gc

        c = gc.ring_double()
        gs.plot_circuit(c)
    """

    straight = straight(length=length_y) if callable(straight) else straight
    coupler = (
        coupler(length_x=length_x, bend_radius=bend_radius, gap=gap, wg_width=wg_width)
        if callable(coupler)
        else coupler
    )

    # Create the circuit, add all individual instances
    circuit = Subcircuit("ring_double")
    circuit.add([(coupler, "ct"), (coupler, "cb"), (straight, "wl"), (straight, "wr")])

    # Circuits can be connected using the elements' string names:
    circuit.connect_many(
        [
            ("cb", "N0", "wl", "E0"),
            ("wl", "W0", "ct", "N1"),
            ("ct", "N0", "wr", "E0"),
            ("wr", "W0", "cb", "N1"),
        ]
    )
    circuit.elements["cb"].pins["W0"] = "input"
    circuit.elements["cb"].pins["E0"] = "output"
    circuit.elements["ct"].pins["E0"] = "drop"
    circuit.elements["ct"].pins["W0"] = "cdrop"
    return circuit


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = ring_double()
    plot_circuit(c)
    plt.show()
