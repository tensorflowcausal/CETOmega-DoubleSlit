# CETOmega-DoubleSlit

Reproducible simulation of the double-slit experiment under the **CETOmega** (Causal–Informational) kernel.

## Overview
This repository generates:
- The **interference pattern** `figs/pattern.png`
- The **visibility curves** `figs/visibility.png`
- The **raw data** `data/results.csv`

The causal phase is modeled as
\[
\Phi(x)=\frac{2\pi x d}{\lambda L}\,\big[1+\gamma\, e^{-x^2 / (2\sigma_\rho^2)}\big].
\]

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python simulate_double_slit.py   # generates pattern.png and results.csv
python utils.py                  # generates visibility.png
```

## Parameters
Edit them directly in `src/simulate_double_slit.py`:
- `lam` (wavelength, m)
- `L` (distance to screen, m)
- `d` (slit separation, m)
- `w` (slit width, m)
- `gamma` (causal coupling)
- `sigma_rho` (memory width)

## Citation
Please cite the associated manuscript:
> Balfagón, C. *A Causal–Informational Reconstruction of the Double–Slit Experiment within the CETOmega Framework* (2025).

## License
MIT
