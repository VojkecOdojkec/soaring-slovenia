import os

# Matplotlib v "headless" načinu (nujno za GitHub Actions)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# kam shranjujemo grafe
os.makedirs("charts", exist_ok=True)

def save_minichart(path, base_m, top_m, climb_ms, wind_text):
    """
    Nariše enostaven mini-graf:
      - črtkana linija na bazi in topu
      - sencen stolpec, ki prikazuje tipično moč dviganja (climb_ms)
      - besedilni opis vetra (wind_text)
    """
    fig, ax = plt.subplots(figsize=(6, 8))

    # Baza in top
    ax.axhline(base_m, linestyle="--", label=f"Baza ~{int(base_m)} m")
    ax.axhline(top_m,  linestyle="--", label=f"Top ~{int(top_m)} m")

    # "stolpec" za dvige
    ymax = max(4000, top_m + 300)
    ax.fill_betweenx([0, ymax], 0, climb_ms, alpha=0.3, label=f"Dvigi {climb_ms:.1f} m/s")

    # Osi in opombe
    ax.set_ylim(0, ymax)
    ax.set_xlim(0, max(4.0, climb_ms + 1.0))
    ax.set_xlabel("Hitrost dviganja [m/s]")
    ax.set_ylabel("Višina [m]")

    # tekst o vetru
    ax.text(0.2, 0.15 * ymax, wind_text)

    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(path, dpi=130)
    plt.close(fig)
    return path
