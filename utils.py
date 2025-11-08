import numpy as np
import matplotlib.pyplot as plt
from simulate_double_slit import intensity

def visibility(d_values, w, lam, L, gamma=0.04, sigma_rho=0.5e-3):
    V = []
    for d in d_values:
        x = np.linspace(-2e-3, 2e-3, 1500)
        I = intensity(x, d, w, lam, L, gamma, sigma_rho)
        v = (I.max() - I.min()) / (I.max() + I.min())
        V.append(v)
    return np.array(V)

def plot_visibility():
    lam = 633e-9
    L = 1.0
    w = 5e-6
    d_values = np.linspace(5e-6, 40e-6, 30)
    gammas = [0.00, 0.02, 0.04, 0.06]

    plt.figure(figsize=(6,4))
    for g in gammas:
        V = visibility(d_values, w, lam, L, gamma=g)
        plt.plot(d_values*1e6, V, label=f"gamma={g:.2f}")
    plt.xlabel("Slit separation d [μm]")
    plt.ylabel("Visibility V")
    plt.title("CETOmega visibility vs d")
    plt.legend()
    plt.tight_layout()
    plt.savefig("../figs/visibility.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_visibility()
