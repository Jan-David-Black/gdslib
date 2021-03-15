import pathlib
from gdslib.components import component_factory


p = pathlib.Path("components.rst")

with open(p, "w+") as f:
    f.write(
        """
Components
=============================
"""
    )

    for name in sorted(list(component_factory.keys())):
        print(name)
        f.write(
            f"""

{name}
----------------------------------------------------

.. autofunction:: gdslib.c.{name}

"""
        )
