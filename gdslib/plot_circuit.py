import matplotlib.pyplot as plt
import numpy as np
import pp
from simphony.simulation import SweepSimulation
from simphony.tools import freq2wl


def plot_circuit(
    circuit,
    pin_in="input",
    pins_out=("output",),
    start=1500e-9,
    stop=1600e-9,
    num=2000,
    logscale=True,
    fig=None,
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
    circuit = pp.call_if_func(circuit)

    simulation = SweepSimulation(circuit, start, stop, num)
    result = simulation.simulate()

    fig = fig or plt.subplot()
    ax = fig.axes

    for pin_out in pins_out:
        f, s = result.data(pin_in, pin_out)
        w = freq2wl(f) * 1e9

        if logscale:
            s = 10 * np.log10(abs(s))
            ylabel = "|S| (dB)"
        else:
            ylabel = "|S|"

        ax.plot(w, s, label=pin_out)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel(ylabel)
    ax.set_title(circuit.name)
    ax.legend()
    return ax


def demo_single_port():
    c = gdslib.c.mzi()
    plot_circuit(c, logscale=False)
    plt.show()


if __name__ == "__main__":
    import gdslib

    # c = gdslib.c.ring_double()
    # plot_circuit(c, pins_out=("cdrop", "drop", "output", "input"))

    c = gdslib.c.mzi()
    plot_circuit(c)
    plt.show()
