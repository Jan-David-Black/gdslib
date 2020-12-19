from typing import Callable
from typing import Dict
from typing import Union

import numpy as np
import opics as op
import pp
from opics.components import compoundElement
from pp.component import Component

from gdslib.components import component_factory
from gdslib.opics import model_factory


def circuit(
    component: Union[Callable, Component],
    model_factory: Dict[str, Callable] = model_factory,
    recursive: bool = True,
) -> compoundElement:
    """Import netlist from gdsfactory component and returns a Simphony circuit.

    Args:
        component: component factory or instance
        model_factory: dict of component_type
        recursive: get flat netlist
    """
    component = pp.call_if_func(component)
    n = component.get_netlist(recursive=recursive)

    circuit = op.Network(component.name)
    model_names = []

    for i in n.instances.keys():
        component_type = n.instances[i]["component"]
        if component_type is None:
            continue

        if component_type not in model_factory:
            print(
                f"skipping component `{component_type}` as it is not in {list(model_factory.keys())}"
            )
            continue
        component_settings = n.instances[i]["settings"]
        assert (
            component_type in model_factory
        ), f"component_type={component_type} not in {list(model_factory.keys())}"
        model_function = model_factory[component_type]
        model = model_function(**component_settings)
        # assert isinstance(model, compoundElement), f"model {model} is not a opics Model"
        # model_names.append(i)
        # model_name_tuple.append((model, i))
        circuit.add_component(model)

    # circuit.add_component(model_name_tuple)

    for k, v in n.connections["flat"].items():
        model1_name, port1_name = k.split(",")
        model2_name, port2_name = v.split(",")

        if model1_name in model_names and model2_name in model_names:
            circuit.connect(model1_name, port1_name, model2_name, port2_name)

    return circuit


def demo_print_transmission():
    """Needs fix."""
    component = pp.c.mzi(delta_length=100)
    c = circuit(component)
    c.elements["mmi1x2_0_0"].pins["W0"] = "input"
    c.elements["mmi1x2_85_0"].pins["W0"] = "output"
    # r = get_transmission(c, num=3)
    # s = np.round(r["s"], decimals=10)
    # s = s.tolist()
    # print(dict(w=r["wavelength_nm"].tolist(), s=s))


def demo_plot_transmission():
    """Needs fix."""
    import matplotlib.pyplot as plt
    import pp

    c = pp.c.mzi(DL=100)
    m = circuit(c)
    m.elements["mmi1x2_0_0"].pins["W0"] = "input"
    m.elements["mmi1x2_85_0"].pins["W0"] = "output"


if __name__ == "__main__":
    # demo_print_transmission()
    # demo_plot_transmission()

    component = pp.c.mzi(delta_length=100)
    c = circuit(component)
    # c.elements["mmi1x2_0_0"].pins["W0"] = "input"
    # c.elements["mmi1x2_85_0"].pins["W0"] = "output"
    circuit.simulate_network()
    circuit.sim_result.plot_sparameters(
        show_freq=False, scale="abs_sq", ports=[[1, 0], [0, 0]]
    )
