import pathlib
from gdslib.components import component_names


p = pathlib.Path("circuits.rst")

with open(p, "w+") as f:
    f.write(
        """
Circuits
=============================
"""
    )

    for name in sorted(component_names):
        print(name)
        f.write(
            f"""

{name}
----------------------------------------------------

.. autofunction:: gdslib.c.{name}

"""
        )
