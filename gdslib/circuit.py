from typing import Callable
from typing import Dict
from typing import Union

import numpy as np
import pp
from pp.component import Component
from simphony.elements import Model
from simphony.netlist import Subcircuit
from simphony.simulation import SweepSimulation
from simphony.tools import freq2wl

from gdslib.components import component_factory


def get_transmission(
    circuit,
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
    circuit = pp.call_if_func(circuit)

    simulation = SweepSimulation(circuit, start, stop, num)
    result = simulation.simulate()

    f, s = result.data(pin_in, pin_out)
    w = freq2wl(f) * 1e9
    return dict(wavelength_nm=w, s=s)


def component_to_circuit(
    component: Union[Callable, Component],
    model_factory: Dict[str, Callable] = component_factory,
) -> Subcircuit:
    """Returns Simphony circuit from a gdsfactory component netlist.

    Args:
        component: component factory or instance
        model_factory: dict of component_type
    """
    component = pp.call_if_func(component)
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

    return circuit


splitter = "mmi1x2_0.0_0.0"
combiner = "mmi1x2_65.596_-0.0"


def test_circuit_transmission(data_regression, check: bool = True):
    component = pp.c.mzi(delta_length=100)
    c = component_to_circuit(component)
    c.elements[splitter].pins["W0"] = "input"
    c.elements[combiner].pins["W0"] = "output"
    r = get_transmission(c, num=3)
    s = np.round(r["s"], decimals=10).tolist()
    if check:
        data_regression.check(dict(w=r["wavelength_nm"].tolist(), s=s))
    return s


def demo_print_transmission():
    component = pp.c.mzi(delta_length=100)
    c = component_to_circuit(component)
    c.elements[splitter].pins["W0"] = "input"
    c.elements[combiner].pins["W0"] = "output"
    r = get_transmission(c, num=3)
    s = np.round(r["s"], decimals=10)
    s = s.tolist()
    print(dict(w=r["wavelength_nm"].tolist(), s=s))


def demo_plot_transmission():
    import matplotlib.pyplot as plt
    from gdslib import plot_circuit
    import pp

    c = pp.c.mzi(delta_length=100)
    m = component_to_circuit(c)
    m.elements[splitter].pins["W0"] = "input"
    m.elements[combiner].pins["W0"] = "output"

    plot_circuit(m)
    plt.show()


if __name__ == "__main__":
    # s = test_circuit_transmission(None, check=False)
    # demo_print_transmission()
    demo_plot_transmission()

    # component = pp.c.mzi(delta_length=100)
    # c = component_to_circuit(component)
    # c.elements[splitter].pins["W0"] = "input"
    # c.elements[combiner].pins["W0"] = "output"
    # r = get_transmission(c, num=3)
    # print(r)
