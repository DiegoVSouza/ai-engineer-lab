"""Load the service's generated credentials before replacing the launcher process."""

import json
import os
from pathlib import Path
import sys

os.environ.update(json.loads(Path('/run/lab/runtime.json').read_text()))
os.execvp(sys.argv[1], sys.argv[1:])
