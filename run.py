#!/usr/bin/env python
from __future__ import print_function
import sys

try:
    from mcstats import app
except ImportError as e:
    print("WARNING: Did you forget to set up and activate your virtual environment?", file=sys.stderr)
    raise

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
