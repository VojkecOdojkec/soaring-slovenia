import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)

def _arrow_dxdy(dir_from_deg, L=0.9):
    theta = math.radians((dir_from_deg + 180) % 360)  # kam piha
    return L*math.cos(theta), L*math.sin(theta)

def save_minichart(path, base_m, top_m, climb_ms, wind_text=None, wind_profile=None, surface=None):
    fig, ax = plt.subplots(figsize=(6,8))
    ax.axhline(base_m, linestyle="--", color="#1f77b4", label=f"Baza ~{int(base_m)} m")
    ax.axhline(top_m,  linestyle="--", color="#d62728", label=f"Top ~{int(top_m)} m")
    ax.fill_betweenx([0, top_m], 0, climb_ms, alpha=0.25, label=f"Dvigi {climb_ms:.1f} m/s")

    if wind_profile:
        speeds = [w[2] for w in wind_profile if w[2] is not None]
        vmin, vmax = (0, max(8, max(speeds))) if speeds else (0,8)
        cmap = plt.cm.viridis
        norm = plt.Normalize(vmin, vmax)
        x0 = 3.5
        for h, ddeg, spd in wind_profile:
            if ddeg is None or spd is None: 
                continue
            dx, dy = _arrow_dxdy(ddeg, L=0.9)
            col = cmap(norm(spd))
            ax.annotate("", xy=(x0+dx, h+dy*60), xytext=(x0, h),
                        arrowprops=dict(arrowstyle="->", lw=2, color=col))
            ax.text(x0+dx+0.08, h, f"{int(ddeg)}°  {spd:.1f} m/s", va="center", fontsize=9)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, pad=0.02)
        cbar.set_label("Hitrost vetra [m/s]")

    ax.set_ylim(0, max(4000, top_m+300))
    ax.set_xlim(0, 5)
    ax.set_xlabel("Hitrost dviganja [m/s]")
    ax.set_ylabel("Višina [m]")
    if wind_text:
        ax.text(0.2, 200, wind_text, fontsize=10)
    ax.legend(loc="lower right")

    axc = fig.add_axes([0.72, 0.73, 0.22, 0.22], polar=True)
    axc.set_theta_zero_location("N"); axc.set_theta_direction(-1)
    axc.set_yticklabels([]); axc.grid(False)
    axc.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2]); axc.set_xticklabels(["N","E","S","W"])
    if surface and surface[0] is not None:
        ddeg, spd = surface
        theta = math.radians((ddeg + 180) % 360)
        axc.arrow(theta, 0, 0, 1.0, width=0.02, head_width=0.15, head_length=0.15)
        axc.set_title(f"{int(ddeg)}°  {spd:.1f} m/s", fontsize=10)

    plt.tight_layout(); plt.savefig(path, dpi=130); plt.close(fig)
    return path
