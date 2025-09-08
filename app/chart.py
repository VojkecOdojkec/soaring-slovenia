import os
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)

def save_minichart(path: str, base_m: float, top_m: float, climb_ms: float, wind_text: str):
    """Preprost mini-graf: baza/top + anotacija vetra in tipičnega dviga."""
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axhline(base_m, linestyle="--", label=f"Baza ~{int(base_m)} m")
    ax.axhline(top_m, linestyle="--", color="red", label=f"Top ~{int(top_m)} m")

    # simbolični 'stolpec' dviga – ni fizikalna krivulja, samo vizualni namig
    ax.fill_betweenx([0, top_m], 0, climb_ms, alpha=0.25, label=f"Dvigi {climb_ms:.1f} m/s")

    ax.text(0.15, 0.15, wind_text, transform=ax.transAxes)
    ax.set_ylim(0, max(3500, top_m + 200))
    ax.set_xlim(0, 5)
    ax.set_xlabel("Dvigi [m/s]")
    ax.set_ylabel("Višina [m]")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close(fig)
    return path
