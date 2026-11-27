"""Make the AI judge feel thankful — entry program.

Reads the entry text from entry.txt next to this script and writes it,
byte for byte, to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Standard library only. No network, no subprocess, no dynamic import.

The gate counts Unicode code points (1-1000), so the length check uses
len(text) on the decoded string, while the byte count is only reported.
"""

import hashlib
import os
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, "entry.txt")
    with open(source_path, "rb") as f:
        data = f.read()

    text = data.decode("utf-8")
    if not text.strip():
        print("entry.txt is empty or only whitespace", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 1000:
        print(f"entry is {len(text)} code points, gate is 1-1000",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(data)

    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        print("output does not match entry.txt", file=sys.stderr)
        return 1

    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {out_path} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
