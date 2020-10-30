""" parameterized circuit models for https://github.com/gdsfactory/gdsfactory components
"""
from .bend_circular import bend_circular
from .coupler import coupler
from .coupler_ring import coupler_ring
from .mmi1x2 import mmi1x2
from .mmi2x2 import mmi2x2
from .mzi import mzi
from .ring_double import ring_double
from .waveguide import waveguide


component_factory = dict(
    bend_circular=bend_circular,
    coupler_ring=coupler_ring,
    coupler=coupler,
    mmi1x2=mmi1x2,
    mmi2x2=mmi2x2,
    mzi=mzi,
    ring_double=ring_double,
    waveguide=waveguide,
)


_elements = [
    "bend_circular",
    "coupler",
    "coupler_ring",
    "mmi1x2",
    "mmi2x2",
    "waveguide",
]
_circuits = ["mzi", "ring_double"]

__all__ = _elements + _circuits
