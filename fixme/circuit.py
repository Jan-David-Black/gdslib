from typing import Callable, Dict

import gdsfactory as gf
import numpy as np
from gdsfactory.component import Component
from simphony.elements import Model
from simphony.netlist import Subcircuit
from simphony.simulation import SweepSimulation
from simphony.tools import freq2wl

from gdslib.simphony.components import component_factory


def get_transmission(
    circuit: Subcircuit,
    pin_in: str = "input",
    pin_out: str = "output",
    start: float = 1500e-9,
    stop: float = 1600e-9,
    num: int = 2000,
):
    """Return transmission for a circuit.

    Args:
        circuit:
        pin_in: input pin
        pin_out: output pin
        start: start wavelength (m)
        stop: stop wavelength (m)
        num: number of points

    """
    simulation = SweepSimulation(circuit, start, stop, num)
    result = simulation.simulate()

    f, s = result.data(pin_in, pin_out)
    w = freq2wl(f) * 1e9
    return dict(wavelength_nm=w, s=s)


def component_to_circuit(
    component: Component,
    model_factory: Dict[str, Callable] = component_factory,
) -> Subcircuit:
    """Returns Simphony circuit from a gdsfactory component netlist.

    Args:
        component: component factory or instance
        model_factory: dict of component_type
    """
    netlist = component.get_netlist()
    instances = netlist["instances"]
    connections = netlist["connections"]

    circuit = Subcircuit(component.name)
    model_names = []
    model_name_tuple = []

    for name, settings in instances.items():
        component_type = settings["component"]
        if component_type is None:
            continue

        if component_type not in model_factory:
            raise ValueError(
                f"Model for `{component_type}` not found in {list(model_factory.keys())}"
            )
        component_settings = settings["settings"]
        model_function = model_factory[component_type]
        model = model_function(**component_settings)
        assert isinstance(model, Model), f"model {model} is not a simphony Model"
        model_names.append(name)
        model_name_tuple.append((model, name))

    circuit.add(model_name_tuple)

    for k, v in connections.items():
        model1_name, port1_name = k.split(",")
        model2_name, port2_name = v.split(",")

        if model1_name in model_names and model2_name in model_names:
            circuit.connect(model1_name, port1_name, model2_name, port2_name)

    circuit.info = netlist
    return circuit


mmi_name = "mmi1x2"
splitter = f"{mmi_name}_0p0_0p0"
combiner = f"{mmi_name}_65p6_m0p0"


def test_circuit_transmission(data_regression, check: bool = True):
    component = gf.c.mzi(delta_length=100, bend=gf.c.bend_circular)
    circuit = component_to_circuit(component)
    for e in circuit.elements:
        print(e)
    circuit.elements[splitter].pins["W0"] = "input"
    circuit.elements[combiner].pins["W0"] = "output"
    r = get_transmission(circuit, num=3)
    s = np.round(r["s"], decimals=10).tolist()
    if check:
        data_regression.check(dict(w=r["wavelength_nm"].tolist(), s=s))
    return circuit


def demo_print_transmission():
    component = gf.c.mzi(delta_length=100)
    c = component_to_circuit(component)
    c.elements[splitter].pins["W0"] = "input"
    c.elements[combiner].pins["W0"] = "output"
    r = get_transmission(c, num=3)
    s = np.round(r["s"], decimals=10)
    s = s.tolist()
    print(dict(w=r["wavelength_nm"].tolist(), s=s))


def demo_plot_transmission():
    import matplotlib.pyplot as plt

    from gdslib.simphony import plot_circuit

    c = gf.c.mzi(delta_length=100)
    m = component_to_circuit(c)
    m.elements[splitter].pins["W0"] = "input"
    m.elements[combiner].pins["W0"] = "output"

    plot_circuit(m)
    plt.show()


if __name__ == "__main__":
    c = test_circuit_transmission(None, check=False)
    # demo_print_transmission()
    # demo_plot_transmission()

    # c = gf.c.mzi(delta_length=100)
    # c = component_to_circuit(c)
    # c.elements[splitter].pins["W0"] = "input"
    # c.elements[combiner].pins["W0"] = "output"
    # r = get_transmission(c, num=3)
    # print(r)
