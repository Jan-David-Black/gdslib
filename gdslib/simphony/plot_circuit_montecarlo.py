import numpy as np
import matplotlib.pyplot as plt
from simphony.simulation import MonteCarloSweepSimulation
from simphony.netlist import Subcircuit
from simphony.tools import freq2wl


def plot_circuit_montecarlo(
    circuit: Subcircuit,
    pin_in: str = "input",
    pin_out: str = "output",
    start: float = 1500e-9,
    stop: float = 1600e-9,
    num: int = 2000,
    logscale: bool = True,
    runs=10,
):
    """Plot MonterCarlo simulations variation.

    Args:
        circuit:
        pin_in: input port name
        pins_out: iterable of pins out to plot
        start: wavelength (m)
        stop: wavelength (m)
        num: number of sampled points
        logscale: plot in dB scale

    """
    circuit = circuit() if callable(circuit) else circuit
    simulation = MonteCarloSweepSimulation(circuit, start=start, stop=stop, num=num)
    result = simulation.simulate(runs=runs)

    for i in range(1, runs + 1):
        f, s = result.data(pin_in, pin_out, i)
        wl = freq2wl(f)
        s = 10 * np.log10(abs(s)) if logscale else abs(s)
        plt.plot(wl, s)

    # The data located at the 0 position is the ideal values.
    f, s = result.data(pin_in, pin_out, 0)
    wl = freq2wl(f)
    plt.plot(wl, s, "k")
    plt.title("MZI Monte Carlo")
    ylabel = "|S| (dB)" if logscale else "|S|"
    plt.xlabel("wavelength (m)")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    from gdslib.components.mzi import mzi

    plot_circuit_montecarlo(mzi)
    plt.show()
