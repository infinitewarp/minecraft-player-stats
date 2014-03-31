#!/usr/bin/env python
from __future__ import print_function
import sys

try:
    from app import app
except ImportError as e:
    print("WARNING: Did you forget to set up and activate your virtual environment?", file=sys.stderr)
    raise

app.run(host='0.0.0.0', debug=True)
