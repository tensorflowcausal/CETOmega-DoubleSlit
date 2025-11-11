# CETΩ Experimental Roadmap Add‑On

This package adds **falsification curves** and an **experimental design table** to your repo.

## What’s included
- `scripts/generate_roadmap.py`: CLI to generate
  - `data/visibility_curves.csv`: V(Δt) for several M_* (SI units with ħ)
  - `data/phase_curves.csv`: Δφ(ω) for several M_*
  - `data/design_table_deltaV1e-3.csv`: required Δt and ΔL for ΔV≈1e-3 (photons/electrons/neutrons)
  - `figs/fig_visibility_vs_dt.png`, `figs/fig_phase_vs_omega.png`, `figs/fig_design_table.png`
- `tests/test_units.py`: quick physical sanity tests

## Usage
```bash
pip install -r requirements.txt
python scripts/generate_roadmap.py --Mlist 0.03 0.1 0.3 --deltaV 1e-3 --noise 1e-4 --units SI
```
> Defaults: `Mlist=[0.01,0.03,0.1,0.3,1.0]`, `deltaV=1e-3`, `noise=0`, `units=SI`.

## Equations (SI)
- Visibility: `V(Δt) = exp[-Δt · M_* / ħ]`, with `ħ = 6.582119569e-16 eV·s`
- Phase: `Δφ(ω) = ħ ω / M_*`
- Design target for ΔV≈1e-3: `Δt ≈ ΔV · ħ / M_*`; 
  - photons: `ΔL = c Δt` 
  - electrons: `ΔL ≈ v_e Δt` (default `v_e=1e7 m/s`) 
  - neutrons: `ΔL ≈ v_n Δt` (default `v_n=2200 m/s`).

## Numerical simulations with realism
- Noise switches: `--noise` applies Gaussian multiplicative noise to V and Δφ.
- Extend easily to include **timing jitter** and **environment decoherence** by convolving `Δt` with a Gaussian kernel or multiplying V by an extra `exp[-(Δt/τ_env)^2]` factor.

## Optical design for ΔV≈10^-3
Use `data/design_table_deltaV1e-3.csv`:
- pick `M_*` → read required `Δt` and `ΔL` per platform.
- For photons at `M_*=0.1 eV`: `Δt ~ 6.58e-18 s` → `ΔL ~ 2.0 μm` (order‑of‑magnitude path control).
- For electrons (v≈1e7 m/s) same `Δt` → `ΔL ~ 6.6e-11 m` (use temporal gating / phase plates).

## Collaboration pointers
- **Quantum optics** labs for Mach–Zehnder stabilized (Δφ≤10^-3 rad).
- **Electron interferometry** groups (biprism/dual‑slit, UHV).
- Share the CSVs and the script with collaborators; they can plug in their own `M_*`, `Δt`, `ω` ranges.

## Reproducibility
All outputs are generated from a single CLI command and saved under `data/` and `figs/`.
