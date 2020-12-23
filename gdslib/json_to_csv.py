import pathlib
import json
import pandas as pd
from gdslib.config import path


def json_to_csv(dirpathin, dirpathout=None):
    """Converts all the JSON files into CSV

    Args:
        dirpathin: path to read files from
        dirpathout: path to save files into
    """
    dirpathin = pathlib.Path(dirpathin)
    dirpathout = dirpathout or dirpathin / "csv"
    dirpathout = pathlib.Path(dirpathout)

    for f in dirpathin.glob("*.json"):
        filename = f.stem
        results = json.loads(open(f).read())
        df = pd.DataFrame(results)
        df.to_csv(dirpathout / f"{filename}.csv")


if __name__ == "__main__":
    json_to_csv(path.sp)
