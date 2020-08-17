from simphony.library import siepic
from simphony.netlist import Subcircuit

from gdslib import plot_circuit
from gdslib.autoname import autoname
from gdslib.components.coupler_ring import coupler_ring
from gdslib.components.waveguide import waveguide


@autoname
def ring_single(
    wg_width=0.5,
    gap=0.2,
    length_x=4,
    bend_radius=5,
    coupler=coupler_ring,
    waveguide=waveguide,
):
    """single bus ring made of a ring coupler (cb: bottom)
    connected with a waveguide

    FIXME! Sparameters are zero

    .. code::

                wt
           N0            N1
           |             |
            \           /
             \         /
           ---=========---
        W0    length_x    E0


    """
    waveguide = waveguide(length=length_x) if callable(waveguide) else waveguide
    coupler = (
        coupler(length_x=length_x, bend_radius=bend_radius, gap=gap, wg_width=wg_width)
        if callable(coupler)
        else coupler
    )

    # Create the circuit, add all individual instances
    circuit = Subcircuit("ring_double")
    circuit.add([(coupler, "cb"), (waveguide, "wt")])

    circuit.connect_many(
        [("cb", "N0", "wt", "W0"), ("wt", "E0", "cb", "N1"),]
    )
    circuit.elements["cb"].pins["W0"] = "input"
    circuit.elements["cb"].pins["E0"] = "output"
    return circuit


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = ring_single()
    plot_circuit(c)
    plt.show()
