from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np
from simphony.netlist import Subcircuit
from simphony.simulation import SweepSimulation
from simphony.tools import freq2wl


def plot_circuit(
    circuit: Subcircuit,
    pin_in: str = "input",
    pins_out: Iterable[str] = ("output",),
    start: float = 1500e-9,
    stop: float = 1600e-9,
    num: int = 2000,
    logscale: bool = True,
    fig: Optional[plt.Figure] = None,
    phase=False,
    **kwargs,
):
    """Plot Sparameter circuit transmission over wavelength

    Args:
        circuit:
        pin_in: input port name
        pins_out: iterable of pins out to plot
        start: wavelength (m)
        stop: wavelength (m)
        num: number of sampled points
        logscale: plot in dB scale
        fig: matplotlib figure
    """
    if not isinstance(pins_out, (set, list, tuple)):
        raise ValueError("pins out is not iterable")
    circuit = circuit() if callable(circuit) else circuit

    simulation = SweepSimulation(circuit, start, stop, num)
    result = simulation.simulate()

    fig = fig or plt.subplot()
    ax = fig.axes

    for pin_out in pins_out:
        f, s = result.data(pin_in, pin_out)
        w = freq2wl(f) * 1e9

        if phase:
            y = np.angle(s)
            ylabel = "angle (rad)"
        else:
            y = np.abs(s)
            y = 10 * np.log10(y) if logscale else y
            ylabel = "|S|" if logscale else "|S (dB)|"

        ax.plot(w, y, label=pin_out)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel(ylabel)
    ax.set_title(circuit.name)
    ax.legend()
    return ax


def demo_single_port():
    import gdslib.simphony.components as gc

    c = gc.mzi()
    plot_circuit(c, logscale=False)
    plt.show()


if __name__ == "__main__":
    from gdslib.simphony.components.mzi import mzi

    # import gdslib.simphony.components as gc
    # c = gc.ring_double()
    # plot_circuit(c, pins_out=("cdrop", "drop", "output", "input"))

    c = mzi()
    plot_circuit(c)
    plt.show()
