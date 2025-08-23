import os
import matplotlib.pyplot as plt

os.makedirs('charts', exist_ok=True)

def save_minichart(path, base_m, top_m, climb_ms, wind_text):
    fig, ax = plt.subplots(figsize=(6,8))
    ax.axhline(base_m, linestyle='--', label=f'Baza ~{int(base_m)} m')
    ax.axhline(top_m, linestyle='--', label=f'Top ~{int(top_m)} m')
    ax.fill_betweenx([0, top_m], 0, climb_ms, alpha=0.3, label=f'Dvigi {climb_ms:.1f} m/s')
    ax.set_ylim(0, 4000); ax.set_xlim(0,5)
    ax.set_xlabel('Hitrost dviganja [m/s]'); ax.set_ylabel('Višina [m]')
    ax.text(2, 600, wind_text)
    ax.legend(loc='lower right')
    plt.tight_layout(); plt.savefig(path); plt.close(fig)
    return path
