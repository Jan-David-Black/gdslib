"""Parameterized circuit models for circuit simulations."""

from simphony.tools import freq2wl
from simphony.tools import wl2freq

import gdslib.components as components
from gdslib.add_gc import add_gc
from gdslib.autoname import autoname
from gdslib.circuit import component_to_circuit
from gdslib.circuit import get_transmission
from gdslib.components import component_factory
from gdslib.model_from_gdsfactory import model_from_gdsfactory
from gdslib.model_from_sparameters import model_from_filepath
from gdslib.model_from_sparameters import model_from_sparameters
from gdslib.plot_circuit import plot_circuit
from gdslib.plot_circuit_montecarlo import plot_circuit_montecarlo
from gdslib.plot_model import plot_model

c = components

__all__ = [
    "add_gc",
    "autoname",
    "c",
    "component_to_circuit",
    "components",
    "component_factory",
    "model_from_gdsfactory",
    "model_from_sparameters",
    "model_from_filepath",
    "plot_model",
    "get_transmission",
    "plot_circuit",
    "plot_circuit_montecarlo",
    "freq2wl",
    "wl2freq",
]
__version__ = "0.1.5"
