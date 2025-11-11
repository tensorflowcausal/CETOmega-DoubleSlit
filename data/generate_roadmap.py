
"""
generate_roadmap.py — CETOmega falsification curves and design table
Outputs:
  - data/visibility_curves.csv
  - data/phase_curves.csv
  - data/design_table_deltaV1e-3.csv
  - figs/fig_visibility_vs_dt.png
  - figs/fig_phase_vs_omega.png
  - figs/fig_design_table.png
Usage:
  python scripts/generate_roadmap.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Physical constants
HBAR_eVs = 6.582119569e-16  # ħ in eV·s
c = 299792458.0             # m/s

def visibility_vs_dt(M_eV, dt_s, units="SI"):
    """V(Δt) = exp[-Δt/ℓ_c], with ℓ_c^{-1} = M_*/ħ in SI. 
       If units='natural', exponent = -Δt * M_eV (assuming ħ=1)."""
    if units == "SI":
        exponent = -dt_s * (M_eV / HBAR_eVs)
    else:
        exponent = -dt_s * M_eV
    return np.exp(exponent)

def phase_vs_omega(M_eV, omega_s, units="SI"):
    """Δφ(ω) = ħ ω / M_* in SI; = ω / M_* in natural units."""
    if units == "SI":
        return (HBAR_eVs * omega_s) / M_eV
    else:
        return omega_s / M_eV

def required_dt_for_deltaV(deltaV, M_eV, units="SI"):
    """For small x, 1 - e^{-x} ≈ x → x ≈ deltaV → Δt ≈ deltaV * ħ / M_* (SI)."""
    if units == "SI":
        return deltaV * (HBAR_eVs / M_eV)
    else:
        return deltaV / M_eV

def design_table(deltaV=1e-3, M_grid_eV=(0.01,0.03,0.1,0.3,1.0), 
                 v_electron=1.0e7, v_neutron=2200.0, units="SI"):
    """Compute Δt and ΔL needed to produce ~deltaV drop in visibility for various platforms."""
    rows = []
    for M in M_grid_eV:
        dt = required_dt_for_deltaV(deltaV, M, units=units)
        rows += [
            {"platform":"photon","M_eV":M,"deltaV":deltaV,"dt_s":dt,"dL_m":c*dt},
            {"platform":"electron","M_eV":M,"deltaV":deltaV,"dt_s":dt,"dL_m":v_electron*dt},
            {"platform":"neutron","M_eV":M,"deltaV":deltaV,"dt_s":dt,"dL_m":v_neutron*dt},
        ]
    return pd.DataFrame(rows)

def main(units="SI"):
    os.makedirs("data", exist_ok=True)
    os.makedirs("figs", exist_ok=True)

    # Curves setup
    M_list = [0.01, 0.03, 0.1, 0.3, 1.0]          # eV
    dt_grid = np.logspace(-15, -9, 400)           # s
    omega_grid = np.logspace(12, 16, 400)         # s^-1 (THz to ~PHz)

    # Build visibility curves
    vis_rows = []
    for M in M_list:
        V = visibility_vs_dt(M, dt_grid, units=units)
        for t, v in zip(dt_grid, V):
            vis_rows.append({"M_eV":M, "dt_s":t, "visibility":v})
    df_vis = pd.DataFrame(vis_rows)
    df_vis.to_csv("data/visibility_curves.csv", index=False)

    # Build phase curves
    ph_rows = []
    for M in M_list:
        ph = phase_vs_omega(M, omega_grid, units=units)
        for w, p in zip(omega_grid, ph):
            ph_rows.append({"M_eV":M, "omega_s":w, "delta_phi_rad":p})
    df_ph = pd.DataFrame(ph_rows)
    df_ph.to_csv("data/phase_curves.csv", index=False)

    # Figures
    plt.figure(figsize=(6,4))
    for M in M_list:
        dfx = df_vis[df_vis["M_eV"]==M]
        plt.loglog(dfx["dt_s"], dfx["visibility"], label=f"M*={M} eV")
    plt.xlabel("Δt [s]")
    plt.ylabel("Visibility V")
    plt.title("CETOmega: V(Δt) for various M* (SI units)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figs/fig_visibility_vs_dt.png", dpi=200)
    plt.close()

    plt.figure(figsize=(6,4))
    for M in M_list:
        dfx = df_ph[df_ph["M_eV"]==M]
        plt.loglog(dfx["omega_s"], dfx["delta_phi_rad"], label=f"M*={M} eV")
    plt.xlabel("ω [s$^{-1}$]")
    plt.ylabel("Δφ [rad]")
    plt.title("CETOmega: Δφ(ω) for various M* (SI units)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figs/fig_phase_vs_omega.png", dpi=200)
    plt.close()

    # Design table for deltaV ~ 1e-3
    df_design = design_table(deltaV=1e-3, M_grid_eV=M_list, units=units)
    df_design.to_csv("data/design_table_deltaV1e-3.csv", index=False)

    # Pretty table plot
    from matplotlib.table import Table

    fig, ax = plt.subplots(figsize=(7.0, 2.8))
    ax.axis("off")
    cols = ["platform","M_eV","deltaV","dt_s","dL_m"]
    tab = Table(ax, bbox=[0,0,1,1])
    cell_w = [0.18,0.17,0.12,0.26,0.27]
    x = np.cumsum([0]+cell_w)
    h = 0.12
    # header
    for i, (c, w) in enumerate(zip(cols, cell_w)):
        tab.add_cell(0, i, w, h, text=c, loc="center", facecolor="#eeeeee")
    # rows
    for r, row in enumerate(df_design[cols].values, start=1):
        for i, (val, w) in enumerate(zip(row, cell_w)):
            if i in (1,3,4):
                sval = f"{val:,.3e}"
            else:
                sval = str(val)
            tab.add_cell(r, i, w, h, text=sval, loc="center")
    tab.set_fontsize(9)
    ax.add_table(tab)
    fig.suptitle("Design targets for ΔV ≈ 1e-3 (SI units)", y=0.98, fontsize=11)
    plt.tight_layout()
    plt.savefig("figs/fig_design_table.png", dpi=200)
    plt.close()

if __name__ == "__main__":
    main(units="SI")
