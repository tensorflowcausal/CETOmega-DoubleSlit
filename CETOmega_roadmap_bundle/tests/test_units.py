import numpy as np
from scripts.generate_roadmap import visibility_vs_dt, phase_vs_omega

def test_visibility_limits():
    M = 0.1  # eV
    dt = np.array([0.0, 1e-15, 1e-12])
    V = visibility_vs_dt(M, dt, units="SI")
    assert abs(V[0]-1) < 1e-12
    assert np.all(np.diff(V) <= 0), "Visibility must decrease with Δt"

def test_phase_scaling():
    M1, M2 = 0.1, 1.0
    w = np.array([1e14])
    phi1 = phase_vs_omega(M1, w, units="SI")[0]
    phi2 = phase_vs_omega(M2, w, units="SI")[0]
    ratio = phi1 / phi2
    assert abs(ratio - (M2/M1)) < 1e-9, "Phase should scale inversely with M_*"
