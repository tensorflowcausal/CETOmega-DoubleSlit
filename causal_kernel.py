import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Crear carpetas si no existen
os.makedirs("data", exist_ok=True)
os.makedirs("figs", exist_ok=True)

# Parámetros físicos básicos
wavelength = 500e-9       # 500 nm
slit_distance = 50e-6     # separación entre rendijas (50 µm)
screen_distance = 1.0     # distancia a la pantalla (1 m)
num_points = 1000

x = np.linspace(-0.01, 0.01, num_points)  # coordenada en la pantalla
beta = (np.pi * slit_distance * x) / (wavelength * screen_distance)
intensity = (np.cos(beta))**2             # interferencia de doble rendija

# Guardar datos
df = pd.DataFrame({"x (m)": x, "intensity": intensity})
df.to_csv("data/results.csv", index=False)

# Graficar patrón
plt.figure(figsize=(6,4))
plt.plot(x*1e3, intensity, color='blue')
plt.title("CETOmega Double Slit Pattern")
plt.xlabel("x [mm]")
plt.ylabel("Intensity (a.u.)")
plt.grid(True)
plt.tight_layout()
plt.savefig("figs/pattern.png")

print("✅ Simulation complete.")
print(f"Max intensity: {intensity.max():.3f}")
print(f"Min intensity: {intensity.min():.3f}")
