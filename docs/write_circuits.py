import pathlib
from gdslib.components import circuit_names


p = pathlib.Path("circuits.rst")

with open(p, "w+") as f:
    f.write(
        """
Circuits
=============================
"""
    )

    for name in sorted(circuit_names):
        print(name)
        f.write(
            f"""

{name}
----------------------------------------------------

.. autofunction:: gdslib.c.{name}

"""
        )
