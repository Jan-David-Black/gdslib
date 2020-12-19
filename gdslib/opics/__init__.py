"""Opics circuit simulator interface."""
from gdslib.opics.bend_circular import bend_circular
from gdslib.opics.coupler_ring import coupler_ring
from gdslib.opics.mmi1x2 import mmi1x2
from gdslib.opics.waveguide import waveguide


name_to_function = dict(
    waveguide=waveguide,
    mmi1x2=mmi1x2,
    coupler_ring=coupler_ring,
    bend_circular=bend_circular,
)


def model_factory(name):
    """Returns the function to build a particular model."""
    if name not in name_to_function:
        print(f"model name `{name}` is not in {list(name_to_function.keys())}")
        return None
    return name_to_function[name]
