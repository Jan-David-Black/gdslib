from typing import Callable
from typing import Optional

from simphony.library import siepic
from simphony.netlist import Subcircuit

from gdslib import plot_circuit
from gdslib.autoname import autoname
from gdslib.components.mmi1x2 import mmi1x2
from gdslib.components.waveguide import waveguide as waveguide_function


@autoname
def mzi(
    delta_length: float = 10.0,
    length_y: float = 4.0,
    length_x: float = 0.1,
    splitter: Callable = mmi1x2,
    combiner: Optional[Callable] = None,
    wg: Callable = waveguide_function,
):
    """Mzi circuit model

    Args:
        delta_length: bottom arm vertical extra length
        length_y: vertical length for both and top arms
        length_x: horizontal length
        splitter: model function for combiner
        combiner: model function for combiner
        wg: waveguide model function

    Return: mzi circuit model

    .. code::


                   __Lx__
                  |      |
                  Ly     Lyr
                  |      |
         splitter=|      |==combiner
                  |      |
                  Ly     Lyr
                  |      |
                 DL/2   DL/2
                  |      |
                  |__Lx__|



    .. plot::
      :include-source:

      import pp

      c = pp.c.mzi(delta_length=10)
      pp.plotgds(c)


    .. plot::
        :include-source:

        import gdslib as gl

        c = gl.mzi()
        gl.plot_circuit(c)


    """
    combiner = combiner or splitter
    splitter = splitter() if callable(splitter) else splitter
    combiner = combiner() if callable(combiner) else combiner

    wg_long = wg(length=2 * length_y + delta_length + length_x)
    wg_short = wg(length=2 * length_y + length_x)

    # Create the circuit, add all individual instances
    circuit = Subcircuit("mzi")
    circuit.add(
        [
            (splitter, "splitter"),
            (combiner, "recombiner"),
            (wg_long, "wg_long"),
            (wg_short, "wg_short"),
        ]
    )

    # Circuits can be connected using the elements' string names:
    circuit.connect_many(
        [
            ("splitter", "E0", "wg_long", "W0"),
            ("splitter", "E1", "wg_short", "W0"),
            ("recombiner", "E0", "wg_long", "E0"),
            ("recombiner", "E1", "wg_short", "E0"),
        ]
    )
    circuit.elements["splitter"].pins["W0"] = "input"
    circuit.elements["recombiner"].pins["W0"] = "output"
    return circuit


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = mzi()
    plot_circuit(c)
    plt.show()
