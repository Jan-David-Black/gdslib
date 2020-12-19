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


def circuit(
    component: Union[Callable, Component],
    model_factory: Dict[str, Callable] = component_factory,
    recursive: bool = True,
) -> Subcircuit:
    """imports netlist from gdsfactory component and returns a Simphony circuit

    Args:
        component: component factory or instance
        model_factory: dict of component_type
        recursive: get flat netlist
    """
    component = pp.call_if_func(component)
    n = component.get_netlist(recursive=recursive)

    circuit = Subcircuit(component.name)
    model_names = []
    model_name_tuple = []

    for i in n.instances.keys():
        component_type = n.instances[i]["component"]
        if component_type is None:
            continue

        if component_type not in model_factory:
            print(
                f"skipping component `{component_type}` as it is not in {list(model_factory.keys())}"
            )
            continue
        component_settings = n.instances[i]["settings"]["settings"]
        assert (
            component_type in model_factory
        ), f"component_type={component_type} not in {list(model_factory.keys())}"
        model_function = model_factory[component_type]
        model = model_function(**component_settings)
        assert isinstance(model, Model), f"model {model} is not a simphony Model"
        model_names.append(i)
        model_name_tuple.append((model, i))

    circuit.add(model_name_tuple)

    for k, v in n.connections["flat"].items():
        model1_name, port1_name = k.split(",")
        model2_name, port2_name = v.split(",")

        if model1_name in model_names and model2_name in model_names:
            circuit.connect(model1_name, port1_name, model2_name, port2_name)

    return circuit


def test_circuit_transmission(data_regression):
    component = pp.c.mzi(delta_length=100)
    c = circuit(component)
    c.elements["mmi1x2_0_0"].pins["W0"] = "input"
    c.elements["mmi1x2_65_0"].pins["W0"] = "output"
    r = get_transmission(c, num=3)
    data_regression.check(dict(w=r["wavelength_nm"].tolist(), s=r["s"].tolist()))


def demo_print_transmission():
    component = pp.c.mzi(delta_length=100)
    c = circuit(component)
    c.elements["mmi1x2_0_0"].pins["W0"] = "input"
    c.elements["mmi1x2_65_0"].pins["W0"] = "output"
    r = get_transmission(c, num=3)
    s = np.round(r["s"], decimals=10)
    s = s.tolist()
    print(dict(w=r["wavelength_nm"].tolist(), s=s))


def demo_plot_transmission():
    import matplotlib.pyplot as plt
    from gdslib import plot_circuit
    import pp

    c = pp.c.mzi(delta_length=100)
    m = circuit(c)
    m.elements["mmi1x2_0_0"].pins["W0"] = "input"
    m.elements["mmi1x2_65_0"].pins["W0"] = "output"

    plot_circuit(m)
    plt.show()


if __name__ == "__main__":
    # demo_print_transmission()
    # demo_plot_transmission()

    component = pp.c.mzi(delta_length=100)
    c = circuit(component)
    c.elements["mmi1x2_0_0"].pins["W0"] = "input"
    c.elements["mmi1x2_65_0"].pins["W0"] = "output"
    r = get_transmission(c, num=3)
