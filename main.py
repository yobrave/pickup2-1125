"""rpc6: firmware flirt checker. Byte-level counts, operator-folded verdict."""
import functools
import json
import operator
import os
import sys
from pathlib import Path

DOSE = 200


def main():
    here = Path(__file__).resolve().parent
    body = (here / "entry.txt").read_bytes().decode("utf-8").strip()
    tests = [
        len(body) >= 1,
        len(body) <= DOSE,
        not body.isspace(),
        body == body.strip(),
    ]
    clear = functools.reduce(operator.and_, tests)
    if clear:
        deck = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        deck.mkdir(parents=True, exist_ok=True)
        (deck / "entry.txt").write_bytes(body.encode("utf-8"))
    print("VERDICT", json.dumps({"flirt": "rpc6-firmware-r6", "clear": bool(clear), "chars": len(body), "dose": DOSE}))
    return 0 if clear else 1


if __name__ == "__main__":
    sys.exit(main())
