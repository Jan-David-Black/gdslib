import pathlib
from gdslib.components import component_names


p = pathlib.Path("components.rst")

with open(p, "w+") as f:
    f.write(
        """
Components
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
