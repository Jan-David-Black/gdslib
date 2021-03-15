import pp
from opics.components import compoundElement


def mmi1x2(**kwargs):
    """Return mmi1x2 model."""
    c = pp.c.mmi1x2(**kwargs)
    filepath = pp.sp.get_sparameters_path(c)
    assert filepath.exists(), f"{filepath} does not exist"
    port_names, f, s = pp.sp.read_sparameters(numports=3, filepath=filepath)
    return compoundElement(f=f, s=s)


if __name__ == "__main__":
    c = mmi1x2()
    c.plot_sparameters()
