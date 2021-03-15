import pathlib
from gdslib.components import circuit_factory


p = pathlib.Path("circuits.rst")

with open(p, "w+") as f:
    f.write(
        """
Circuits
=============================
"""
    )

    for name in sorted(list(circuit_factory.keys())):
        print(name)
        f.write(
            f"""

{name}
----------------------------------------------------

.. autofunction:: gdslib.c.{name}

"""
        )
