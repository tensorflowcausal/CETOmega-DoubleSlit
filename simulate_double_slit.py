# simulate_double_slit.py
import os
os.environ["MPLBACKEND"] = "Agg"  # necesario en GitHub Actions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# carpetas de salida en la raíz
os.makedirs("data", exist_ok=True)
os.makedirs("figs", exist_ok=True)

# parámetros mínimos (auto-contenidos)
lam = 632.8e-9     # m
d   = 200e-6       # m
L   = 1.0          # m

# malla (±5 mm)
x = np.linspace(-5e-3, 5e-3, 2000)

# patrón de interferencia ideal (sin difracción, simple y robusto)
beta = (np.pi * d * x) / (lam * L)
I = (np.cos(beta))**2
I = (I - I.min()) / (I.max() - I.min() + 1e-12)

# CSV
pd.DataFrame({"x_mm": x*1e3, "I": I}).to_csv("data/results.csv", index=False)

# PNG
plt.figure(figsize=(6,4))
plt.plot(x*1e3, I, lw=1.2)
plt.xlabel("x [mm]")
plt.ylabel("Normalized intensity")
plt.title("Double-slit interference (minimal)")
plt.tight_layout()
plt.savefig("figs/pattern.png", dpi=300, bbox_inches="tight")
plt.close()

print("OK -> data/results.csv")
print("OK -> figs/pattern.png")
