
import os
os.environ["MPLBACKEND"] = "Agg"
import numpy as np
import matplotlib.pyplot as plt

# ------------ Configurable parameters --------------
# Visibility law: "gauss" => exp(-(dt/tau)^2), "exp" => exp(-dt/tau)
VISIBILITY_LAW = os.getenv("VISIBILITY_LAW", "gauss").lower()
TAU_LIST_S = [float(x) for x in os.getenv("TAU_LIST_S", "0.3e-12,0.7e-12,1.5e-12,3.0e-12").split(",")]
DT_MIN_S = float(os.getenv("DT_MIN_S", "0"))
DT_MAX_S = float(os.getenv("DT_MAX_S", "5e-12"))
V_SENS = float(os.getenv("V_SENS", "1e-3"))
# Phase shift: Δφ(ω) ≈ ω/M*
MSTAR = float(os.getenv("MSTAR", "1.0e17"))
W_MIN = float(os.getenv("W_MIN", "1e6"))
W_MAX = float(os.getenv("W_MAX", "1e10"))
PHASE_SENS = float(os.getenv("PHASE_SENS", "1e-17"))

# Ensure output dirs
os.makedirs("figs", exist_ok=True)

# ------------ FIG S1: Visibility curve --------------
def vis(dt, tau):
    if VISIBILITY_LAW.startswith("exp"):
        return np.exp(-dt/tau)
    return np.exp(-(dt/tau)**2)

dt = np.linspace(DT_MIN_S, DT_MAX_S, 600)
plt.figure(figsize=(6,4))
for tau in TAU_LIST_S:
    V = vis(dt, tau)
    plt.plot(dt*1e12, V, label=rf"$\tau_c={tau*1e12:.1f}$ ps")
plt.axhline(V_SENS, ls="--")
plt.xlabel(r"$\Delta t$ (ps)")
plt.ylabel(r"$V(\Delta t)$")
plt.ylim(-0.02,1.05)
plt.legend(frameon=False, fontsize=9)
plt.title("FIGURE S1: Visibility law $V(\\Delta t,\\tau_c)$")
plt.tight_layout()
plt.savefig("figs/fig_visibility.pdf", bbox_inches="tight")
plt.savefig("figs/fig_visibility.png", dpi=300, bbox_inches="tight")
plt.close()

# ------------ FIG S2: Causal phase shift --------------
w = np.linspace(W_MIN, W_MAX, 600)
dphi = w / MSTAR

plt.figure(figsize=(6,4))
plt.plot(w, dphi)
plt.fill_between(w, -PHASE_SENS, PHASE_SENS, alpha=0.2)
plt.xscale("log"); plt.yscale("log")
plt.xlabel(r"$\omega$ (rad/s)")
plt.ylabel(r"$\Delta\phi(\omega)$ (rad)")
plt.title("FIGURE S2: Causal phase shift $\\Delta\\phi(\\omega)$")
plt.tight_layout()
plt.savefig("figs/fig_phase.pdf", bbox_inches="tight")
plt.savefig("figs/fig_phase.png", dpi=300, bbox_inches="tight")
plt.close()

print("OK -> figs/fig_visibility.pdf & figs/fig_phase.pdf")
