"""Load .env into os.environ without a shell (values are never printed)."""
import os, re
def load(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")):
    for line in open(path):
        m = re.match(r"^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*?)\s*$", line)
        if m and m.group(2):
            os.environ.setdefault(m.group(1), m.group(2))
