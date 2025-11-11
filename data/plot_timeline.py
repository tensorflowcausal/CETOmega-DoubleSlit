import matplotlib.pyplot as plt

# Datos del roadmap experimental
stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4"]
years = [1, 3, 5, 8]
systems = [
    ("Photons (Mach–Zehnder)", 0.5, "lightblue"),
    ("Electrons (biprism/double-slit)", 2.0, "cornflowerblue"),
    ("Neutrons (Rauch–Zeilinger)", 4.0, "mediumseagreen"),
    ("Molecules (C60+ / organics)", 6.0, "gold")
]

plt.figure(figsize=(8, 5))

# Ejes
plt.xlabel("Years from project start", fontsize=11)
plt.ylabel("Stage", fontsize=11)
plt.title("CETOmega Experimental Roadmap", fontsize=13, weight="bold")

# Líneas de referencia para cada stage
for i, stage in enumerate(stages, 1):
    plt.axhline(i, color="gray", linestyle="--", alpha=0.4)
    plt.text(-0.3, i, stage, va="center", fontsize=10, weight="bold")

# Bloques con bounding boxes
for label, x, color in systems:
    plt.text(
        x, systems.index((label, x, color)) + 1,
        label,
        ha="left",
        va="center",
        fontsize=9,
        color="black",
        bbox=dict(facecolor=color, alpha=0.8, edgecolor="black", boxstyle="round,pad=0.3")
    )

plt.ylim(0.5, len(stages) + 0.5)
plt.xlim(0, 9)
plt.grid(alpha=0.3)

# Ajustes de layout para evitar superposición
plt.tight_layout()
plt.subplots_adjust(left=0.25, right=0.95, bottom=0.15, top=0.9)

plt.savefig("figs/fig_timeline.png", dpi=300)
plt.show()
