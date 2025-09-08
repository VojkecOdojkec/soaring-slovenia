# app/chart.py
import os
import matplotlib
matplotlib.use("Agg")  # deluje brez GUI (npr. na GitHub Actions)
import matplotlib.pyplot as plt


def _parse_wind_profile(wind_profile):
    """
    Vrne (z_m, spd_ms). Sprejme:
      - dict: {"z":[...], "spd":[...]} ali {"z_m":[...], "spd_ms":[...]} ...
      - list[tuple]: [(z, spd), ...]
      - list[dict]:  [{"z":..,"spd":..}, ...]
    """
    if not wind_profile:
        return [], []

    if isinstance(wind_profile, dict):
        z = (wind_profile.get("z") or wind_profile.get("z_m")
             or wind_profile.get("height") or wind_profile.get("height_m") or [])
        s = (wind_profile.get("spd") or wind_profile.get("spd_ms")
             or wind_profile.get("speed") or wind_profile.get("speed_ms") or [])
        try:
            return list(map(float, z)), list(map(float, s))
        except Exception:
            return [], []

    if isinstance(wind_profile, (list, tuple)):
        zz, ss = [], []
        for it in wind_profile:
            if isinstance(it, (list, tuple)) and len(it) >= 2:
                zz.append(float(it[0])); ss.append(float(it[1]))
            elif isinstance(it, dict):
                z = it.get("z") or it.get("z_m") or it.get("height") or it.get("height_m")
                s = it.get("spd") or it.get("spd_ms") or it.get("speed") or it.get("speed_ms")
                if z is not None and s is not None:
                    zz.append(float(z)); ss.append(float(s))
        return zz, ss

    return [], []


def save_minichart(path, base_m, top_m, climb_ms, wind_text=None,
                   wind_profile=None, **kwargs):
    """
    Preprost mini-graf:
      • črtkani liniji za bazo in top,
      • polje 'moč dviganj',
      • (opcijsko) desna os z vertikalnim profilom hitrosti vetra.
    Argument **kwargs namenoma pogoltnemo (združljivost s starejšimi klici).
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 8), dpi=110)

    # baza/top
    ax.axhline(float(base_m), linestyle="--", color="tab:blue",
               label=f"Baza ~{int(base_m)} m")
    ax.axhline(float(top_m), linestyle="--", color="tab:red",
               label=f"Top ~{int(top_m)} m")

    # simbolično polje dviganj
    y_max = max(4000, float(top_m) + 300)
    ax.fill_betweenx([0, float(top_m)], 0, float(climb_ms), alpha=0.25,
                     label=f"Dvigi {float(climb_ms):.1f} m/s")

    ax.set_ylim(0, y_max)
    ax.set_xlim(0, max(5.0, float(climb_ms) + 1.0))
    ax.set_xlabel("Hitrost dviganja [m/s]")
    ax.set_ylabel("Višina [m]")

    if wind_text:
        ax.text(0.05, 0.02, wind_text, transform=ax.transAxes)

    # (opcijsko) profil vetra
    z_m, spd_ms = _parse_wind_profile(wind_profile)
    if z_m and spd_ms and len(z_m) == len(spd_ms):
        ax2 = ax.twiny()
        ax2.plot(spd_ms, z_m, marker=".", linewidth=1.2, alpha=0.85)
        ax2.set_xlim(0, max(10.0, max(spd_ms) + 1.0))
        ax2.set_xlabel("Veter [m/s]")
        ax2.grid(False)

    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close(fig)
    return path
