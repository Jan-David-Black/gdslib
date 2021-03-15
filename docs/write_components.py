import pathlib
from gdslib.components import circuit_names


p = pathlib.Path("components.rst")

with open(p, "w+") as f:
    f.write(
        """
Components
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
