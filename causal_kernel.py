import numpy as np

def causal_phase(x, d, lam, L, gamma=0.04, sigma_rho=0.5e-3):
    """
    Causal phase Phi(x) for the CETOmega kernel.
    Parameters
    ----------
    x : ndarray
        Screen coordinate (m)
    d : float
        Slit separation (m)
    lam : float
        Wavelength (m)
    L : float
        Source-to-screen distance (m)
    gamma : float
        Causal coupling strength (dimensionless, ~0.0–0.1 typical)
    sigma_rho : float
        Memory width (m), controls spectral/causal broadening
    Returns
    -------
    phi : ndarray
        Causal phase in radians
    """
    # Memory profile (Gaussian)
    f = np.exp(-(x**2) / (2.0 * sigma_rho**2))
    # Paraxial phase plus causal correction
    phi = (2.0 * np.pi * x * d) / (lam * L) * (1.0 + gamma * f)
    return phi
