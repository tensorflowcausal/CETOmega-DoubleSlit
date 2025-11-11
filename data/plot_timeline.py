#!/usr/bin/env python3
"""plot_timeline.py - Experimental roadmap: photons -> electrons -> neutrons -> molecules
Generates figs/fig_timeline.png
"""
import matplotlib.pyplot as plt

stages = [
    {"name":"Photons (Mach-Zehnder)", "start":0.0, "end":1.0, "target":"Δφ ≈ 1e-3 rad"},
    {"name":"Electrons (biprism/double-slit)", "start":1.0, "end":2.5, "target":"ΔV ≈ 1e-3"},
    {"name":"Neutrons (Rauch-Zeilinger)", "start":2.0, "end":4.0, "target":"Δφ ≈ 1e-3 rad"},
    {"name":"Molecules (C60+ / organics)", "start":5.0, "end":10.0, "target":"Fringe loss (ℓ_c < 1e-10 m)"},
]

def main():
    fig = plt.figure(figsize=(8, 3.2))
    ax = fig.add_subplot(111)
    height = 0.35
    yticks = []
    ylabels = []
    for i, s in enumerate(stages):
        y = i
        ax.barh(y, s["end"]-s["start"], left=s["start"], height=height)
        ax.text(s["start"] + 0.05, y, s["name"], va="center", ha="left")
        ax.text(s["end"] + 0.1, y, s["target"], va="center", ha="left")
        yticks.append(y)
        ylabels.append(f"Stage {i+1}")
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)
    ax.set_xlabel("Years from project start")
    ax.set_xlim(-0.2, 10.8)
    ax.set_ylim(-0.6, len(stages)-0.4)
    ax.set_title("CETOmega Experimental Roadmap")
    ax.grid(True, axis="x", linestyle=":", linewidth=0.8)
    fig.tight_layout()
    fig.savefig("figs/fig_timeline.png", dpi=200)

if __name__ == "__main__":
    main()
