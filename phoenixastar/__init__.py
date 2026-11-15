"""Phoenixastar: an AI lab that gets better at discovering mathematics by doing it."""
import os as _os
import sys as _sys

ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if ROOT not in _sys.path:          # so `import envload` works however the package is started
    _sys.path.insert(0, ROOT)
