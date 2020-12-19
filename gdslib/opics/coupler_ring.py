import opics as op
import pp
from opics.components import compoundElement


def coupler_ring(**kwargs):
    """Return Halfcoupler ring model."""
    c = pp.c.coupler_ring(**kwargs)
    filepath = pp.sp.get_sparameters_path(c)
    assert filepath.exists(), f"{filepath} does not exist"
    port_names, f, s = pp.sp.read_sparameters(numports=4, filepath=filepath)
    return compoundElement(f=f, s=s)


if __name__ == "__main__":
    c = coupler_ring()
    c.plot_sparameters()
