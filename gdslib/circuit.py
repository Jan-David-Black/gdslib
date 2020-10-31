from typing import Callable

import pp
from simphony.netlist import Subcircuit
from simphony.simulation import SweepSimulation
from simphony.tools import freq2wl

from gdslib.components import component_factory


def get_transmission(
    circuit, iport="input", oport="output", start=1500e-9, stop=1600e-9, num=2000
):
    """ returns transmission for a circuit
    """
    circuit = pp.call_if_func(circuit)

    simulation = SweepSimulation(circuit, start, stop, num)
    result = simulation.simulate()

    f, s = result.data(iport, oport)
    w = freq2wl(f) * 1e9
    return dict(wavelength_nm=w, s=s)


def model_factory(model_name, **settings):
    return component_factory[model_name](**settings)


def circuit(component: Callable, model_factory=model_factory) -> Subcircuit:
    """imports netlist from gdsfactory component and returns a Simphony circuit

    Args:
        component: component factory or instance
    """
    component = pp.call_if_func(component)
    n = component.get_netlist()

    circuit = Subcircuit(component.name)

    model_name_tuple = []

    for i in n.instances.keys():
        component_type = n.instances[i]["component"]
        component_settings = n.instances[i]["settings"]
        model = model_factory(component_type, **component_settings)
        model_name_tuple.append((model, i))

    circuit.add(model_name_tuple)

    for k, v in n.connections.items():
        c1, p1 = k.split(",")
        c2, p2 = v.split(",")
        circuit.connect(c1, p1, c2, p2)

    return circuit


def test_circuit_transmission(data_regression):
    component = pp.c.mzi(DL=50)
    c = circuit(component)
    c.elements["mmi1x2_12_0"].pins["W0"] = "input"
    c.elements["mmi1x2_98_0"].pins["W0"] = "output"
    r = get_transmission(c, num=3)
    data_regression.check(dict(w=r["wavelength_nm"].tolist(), s=r["s"].tolist()))


def demo_print_transmission():
    component = pp.c.mzi(DL=50)
    c = circuit(component)
    c.elements["mmi1x2_12_0"].pins["W0"] = "input"
    c.elements["mmi1x2_98_0"].pins["W0"] = "output"
    r = get_transmission(c, num=3)
    print(dict(w=r["wavelength_nm"].tolist(), s=r["s"].tolist()))


def demo_plot_transmission():
    import matplotlib.pyplot as plt
    from gdslib import plot_circuit
    import pp

    c = pp.c.mzi(DL=50)
    m = circuit(c)
    m.elements["mmi1x2_12_0"].pins["W0"] = "input"
    m.elements["mmi1x2_98_0"].pins["W0"] = "output"

    plot_circuit(m)
    plt.show()


if __name__ == "__main__":
    demo_print_transmission()
