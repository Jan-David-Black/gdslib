import opics as op
import pp
from opics.components import compoundElement


def bend_circular(**kwargs):
    """Return radial bend circular Opics model."""
    c = pp.c.bend_circular(**kwargs)
    filepath = pp.sp.get_sparameters_path(c)
    assert filepath.exists(), f"{filepath} does not exist"
    port_names, f, s = pp.sp.read_sparameters(numports=2, filepath=filepath)
    return compoundElement(f=f, s=s)


if __name__ == "__main__":
    c = bend_circular()
    c.plot_sparameters()
