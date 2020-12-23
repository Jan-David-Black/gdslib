""" stores configuration variables
"""

__all__ = ["path"]

import pathlib


module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent


class Path:
    module = module_path
    repo = repo_path
    sp = repo_path / "sp"


path = Path()

if __name__ == "__main__":
    print(path.sp)
