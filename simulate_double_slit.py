# simulate_double_slit.py
import os
os.environ["MPLBACKEND"] = "Agg"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from causal_kernel import causal_phase

def intensity(x, d, w, lam, L, gamma=0.04, sigma_rho=0.5e-3):
"""Normalized double-slit intensity under the CETOmega causal phase."""
phi = causal_phase(x, d, lam, L, gamma, sigma_rho)
slit1 = np.exp(-((x - d/2.0)**2) / (2.0 * w**2))
slit2 = np.exp(-((x + d/2.0)**2) / (2.0 * w**2)) * np.exp(1j * phi)
I = np.abs(slit1 + slit2)**2
return I / I.max()

def simulate_and_save():
lam = 633e-9
L = 1.0
d = 20e-6
w = 5e-6
gamma = 0.04
sigma_rho = 0.5e-3

x = np.linspace(-5e-3, 5e-3, 2000) # ±5 mm
I = intensity(x, d, w, lam, L, gamma, sigma_rho)

os.makedirs("data", exist_ok=True)
os.makedirs("figs", exist_ok=True)

df = pd.DataFrame({"x_mm": x*1e3, "I": I})
df.to_csv("data/results.csv", index=False)

plt.figure(figsize=(6,4))
plt.plot(x*1e3, I, lw=1.2)
plt.xlabel("x [mm]")
plt.ylabel("Normalized intensity")
plt.title("CETOmega double-slit pattern")
plt.tight_layout()
plt.savefig("figs/pattern.png", dpi=300, bbox_inches="tight")
plt.close()

if __name__ == "__main__":
simulate_and_save()


El El sáb, 8 nov 2025 a la(s) 5:46 a. m., christian balfagon <lyosranch@gmail.com> escribió:
name: Run CETOmega simulation

on:
push:
branches: [ "main" ]
workflow_dispatch:

jobs:
build:
runs-on: ubuntu-latest
steps:
- name: Checkout
uses: actions/checkout@v4

- name: Set up Python
uses: actions/setup-python@v5
with:
python-version: "3.11"

- name: Install dependencies
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt

- name: Debug repo tree
run: |
pwd
ls -la
echo "---- recursive ----"
ls -R || true

- name: Run simulation
env:
MPLBACKEND: Agg
PYTHONPATH: ${{ github.workspace }}
run: |
python - << 'PY'
import sys, os
print("Python:", sys.version)
import numpy, pandas, matplotlib
print("numpy:", numpy.__version__)
print("pandas:", pandas.__version__)
print("matplotlib:", matplotlib.__version__)
# ejecutar el script
import subprocess, shlex
cmd = shlex.split("python simulate_double_slit.py")
print("Running:", " ".join(cmd))
r = subprocess.run(cmd, check=True)
print("Return code:", r.returncode)
PY
echo "---- outputs ----"
ls -R data figs || true

- name: Upload artifacts
uses: actions/upload-artifact@v4
with:
name: outputs
path: |
data/results.csv
figs/pattern.png
if-no-files-found: warn
