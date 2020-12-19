"""Opics circuit simulator interface."""
from gdslib.opics.bend_circular import bend_circular
from gdslib.opics.coupler_ring import coupler_ring
from gdslib.opics.mmi1x2 import mmi1x2
from gdslib.opics.waveguide import waveguide


model_factory = dict(
    waveguide=waveguide,
    mmi1x2=mmi1x2,
    coupler_ring=coupler_ring,
    bend_circular=bend_circular,
)
