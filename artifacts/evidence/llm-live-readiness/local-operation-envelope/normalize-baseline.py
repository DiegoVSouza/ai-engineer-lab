from pathlib import Path

path = Path(__file__).resolve().parent / "policy-before.json"
path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
