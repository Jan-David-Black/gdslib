"""Store configuration variables."""

__all__ = ["PATH"]

import pathlib

module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent


class Path:
    module = module_path
    repo = repo_path
    sp = repo_path / "sp"


PATH = Path()

if __name__ == "__main__":
    print(PATH.sp)
