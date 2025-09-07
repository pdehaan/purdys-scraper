import difflib
import json
from operator import itemgetter
from typing import Dict


def differ(file1: str, file2: str, n=3):
    """
    Creates a unified diff of two specified files.
    """

    def readjson(file: str) -> Dict[str, str | int]:
        """
        Reads specified JSON file and sorts by `url` property for consistent diffing.
        """
        with open(file, "r") as f:
            data = json.loads(f.read())
            data.sort(key=itemgetter("url"))
            return data

    def dumpjson(file: str) -> str:
        """
        Reads specified JSON file and formats it as an indented string.
        """
        return json.dumps(readjson(file), indent=2)

    diff = difflib.unified_diff(
        dumpjson(file1).splitlines(keepends=True),
        dumpjson(file2).splitlines(keepends=True),
        fromfile=file1,
        tofile=file2,
        n=n,
    )
    return "".join(diff)


diff = differ("data/2025-08-26.json", "data/2025-09-07.json", 2)
if diff:
  print(diff)
else:
    print("No changes detected")
