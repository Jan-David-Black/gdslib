"""Circuit models for gdsfactory
"""
from .bend_circular import bend_circular
from .coupler import coupler
from .coupler_ring import coupler_ring
from .gc import gc1550te
from .mmi1x2 import mmi1x2
from .mmi2x2 import mmi2x2
from .mzi import mzi
from .ring_double import ring_double
from .ring_single import ring_single
from .waveguide import waveguide


component_factory = dict(
    bend_circular=bend_circular,
    coupler_ring=coupler_ring,
    coupler=coupler,
    mmi1x2=mmi1x2,
    mmi2x2=mmi2x2,
    waveguide=waveguide,
    gc1550te=gc1550te,
)

circuit_factory = dict(mzi=mzi, ring_double=ring_double, ring_single=ring_single)


components = list(component_factory.keys())
circuits = list(circuit_factory.keys())

_circuits = set(circuits) - set(["ring_single"])
_components = set(components)

__all__ = components + circuits
