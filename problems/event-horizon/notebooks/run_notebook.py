#!/usr/bin/env python
"""Execute notebooks/event_horizon.ipynb in place (nbclient) and report the wall time."""
import os, subprocess, sys, time, nbformat
from nbclient import NotebookClient
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "event_horizon.ipynb")
nb = nbformat.read(p, as_version=4)
# register a kernel that uses THIS interpreter (the venv), so the system site-packages kernel is not picked up
subprocess.run([sys.executable, "-m", "ipykernel", "install", "--sys-prefix", "--name", "eh-venv"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
t0 = time.time()
NotebookClient(nb, timeout=600, kernel_name="eh-venv", resources={"metadata": {"path": here}}).execute()
nbformat.write(nb, p)
errs = sum(1 for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error")
print(f"executed {sum(c.cell_type == 'code' for c in nb.cells)} code cells in {time.time() - t0:.1f} s, errors: {errs}")
