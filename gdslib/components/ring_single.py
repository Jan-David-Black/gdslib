from simphony.library import siepic
from simphony.netlist import Subcircuit

from gdslib import plot_circuit
from gdslib.autoname import autoname
from gdslib.components.bend_circular import bend_circular
from gdslib.components.coupler_ring import coupler_ring
from gdslib.components.waveguide import waveguide


@autoname
def ring_single(
    wg_width=0.5,
    gap=0.2,
    length_x=4,
    bend_radius=5,
    length_y=2,
    coupler=coupler_ring,
    waveguide=waveguide,
    bend=bend_circular,
):
    """single bus ring made of a ring coupler (cb: bottom)
    connected with:
    - 2 vertical waveguides (wl: left, wr: right)
    - 2 bend90 waveguides (bl: left, br: right)
    - 1 waveguide at the top (wt)

    FIXME! it has some issues

    .. code::

              wt (top)
              length_x
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

      import pp

      c = pp.c.ring_single(wg_width=0.5, gap=0.2, length_x=4, bend_radius=5, length_y=2)
      pp.plotgds(c)


    .. plot::
        :include-source:

        import gdslib as gl

        c = gl.c.ring_single()
        gl.plot_circuit(c)
    """

    waveguide = waveguide(length=length_y) if callable(waveguide) else waveguide
    bend = bend(width=wg_width, radius=bend_radius) if callable(bend) else bend
    coupler = (
        coupler(length_x=length_x, bend_radius=bend_radius, gap=gap, wg_width=wg_width)
        if callable(coupler)
        else coupler
    )

    # Create the circuit, add all individual instances
    circuit = Subcircuit("ring_double")
    circuit.add(
        [
            (bend, "bl"),
            (bend, "br"),
            (coupler, "cb"),
            (waveguide, "wl"),
            (waveguide, "wr"),
            (waveguide, "wt"),
        ]
    )

    # Circuits can be connected using the elements' string names:
    circuit.connect_many(
        [
            ("cb", "N0", "wl", "E0"),
            ("wl", "W0", "bl", "N0"),
            ("bl", "W0", "wt", "W0"),
            ("wt", "E0", "br", "W0"),
            ("br", "N0", "wr", "E0"),
            ("wr", "W0", "cb", "N1"),
        ]
    )
    circuit.elements["cb"].pins["W0"] = "input"
    circuit.elements["cb"].pins["E0"] = "output"
    return circuit


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = ring_single()
    plot_circuit(c)
    plt.show()
