from simphony.netlist import Subcircuit

from gdslib.autoname import autoname
from gdslib.simphony.components.coupler_ring import coupler_ring
from gdslib.simphony.components.straight import straight


@autoname
def ring_single(
    wg_width=0.5,
    gap=0.2,
    length_x=4,
    bend_radius=5,
    coupler=coupler_ring,
    straight=straight,
):
    r"""Return Single bus ring made of a ring coupler (cb: bottom)

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
    straight = straight(length=length_x) if callable(straight) else straight
    coupler = (
        coupler(length_x=length_x, bend_radius=bend_radius, gap=gap, wg_width=wg_width)
        if callable(coupler)
        else coupler
    )

    # Create the circuit, add all individual instances
    circuit = Subcircuit("ring_double")
    circuit.add([(coupler, "cb"), (straight, "wt")])

    circuit.connect_many([("cb", "N0", "wt", "W0"), ("wt", "E0", "cb", "N1")])
    circuit.elements["cb"].pins["W0"] = "input"
    circuit.elements["cb"].pins["E0"] = "output"
    return circuit


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    from gdslib.simphony import plot_circuit

    c = ring_single()
    plot_circuit(c)
    plt.show()
