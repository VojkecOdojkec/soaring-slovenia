# app/chart.py
import os
import math
import matplotlib

# poskrbi za "headless" okolje (tudi lokalno bo delalo brez GUI)
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def _parse_wind_profile(wind_profile):
    """
    Vračamo tuple (z_m, spd_ms). Sprejmemo več oblik:
      - dict: {"z": [...], "spd": [...]} ali {"z_m":[...], "spd_ms":[...]} itd.
      - list[tuple]: [(z, spd), ...]
      - list[dict]:  [{"z":..,"spd":..}, ...]
    Če ne prepoznamo, vrnemo prazni listi.
    """
    if wind_profile is None:
        return [], []

    # dict varianta
    if isinstance(wind_profile, dict):
        z = (
            wind_profile.get("z")
            or wind_profile.get("z_m")
            or wind_profile.get("height")
            or wind_profile.get("height_m")
            or []
        )
        spd = (
            wind_profile.get("spd")
            or wind_profile.get("spd_ms")
            or wind_profile.get("speed")
            or wind_profile.get("speed_ms")
            or []
        )
        try:
            return list(map(float, z)), list(map(float, spd))
        except Exception:
            return [], []

    # seznam tuple-ov ali dict-ov
    if isinstance(wind_profile, (list, tuple)):
        z_list, s_list = [], []
        for it in wind_profile:
            if isinstance(it, (list, tuple)) and len(it) >= 2:
                z_list.append(float(it[0]))
                s_list.append(float(it[1]))
            elif isinstance(it, dict):
                z_val = it.get("z") or it.get("z_m") or it.get("height") or it.get("height_m")
                s_val = it.get("spd") or it.get("spd_ms") or it.get("speed") or it.get("speed_ms")
                if z_val is not None and s_val is not None:
                    z_list.append(float(z_val))
                    s_list.append(float(s_val))
        return z_list, s_list

    return [], []


def save_minichart(path, base_m, top_m, climb_ms, wind_text=None, wind_profile=None):
    """
    Nariše preprost "mini" graf:
      - črtkani liniji za bazo in top,
      - polje moči dviganj (simbolično),
      - opcijsko desna os z vertikalnim profilom hitrosti vetra (če podan).
    Parametri:
      path        : izhodna PNG pot
      base_m/top_m: višine [m]
      climb_ms    : tipični dvigi [m/s]
      wind_text   : kratko besedilo (npr. 'Veter 180° / 4.5 m/s')
      wind_profile: glej _parse_wind_profile; lahko tudi None
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 8), dpi=110)

    # Termika: baza/top
    ax.axhline(float(base_m), linestyle="--", color="tab:blue", label=f"Baza ~{int(base_m)} m")
    ax.axhline(float(top_m), linestyle="--", color="tab:red", label=f"Top ~{int(top_m)} m")

    # Simbolično polje "dviganj" (climb)
    y_max = max(4000, float(top_m) + 300)
    ax.fill_betweenx([0, float(top_m)], 0, float(climb_ms), alpha=0.25, label=f"Dvigi {climb_ms:.1f} m/s")

    ax.set_ylim(0, y_max)
    ax.set_xlim(0, max(5.0, float(climb_ms) + 1.0))
    ax.set_xlabel("Hitrost dviganja [m/s]")
    ax.set_ylabel("Višina [m]")

    if wind_text:
        ax.text(0.05, 0.02, wind_text, transform=ax.transAxes)

    # Desna os: profil hitrosti vetra (če je podan)
    z_m, spd_ms = _parse_wind_profile(wind_profile)
    if z_m and spd_ms and len(z_m) == len(spd_ms):
        ax2 = ax.twiny()
        ax2.plot(spd_ms, z_m, linestyle="-", marker=".", alpha=0.8)
        ax2.set_xlim(0, max(10.0, max(spd_ms) + 1.0))
        ax2.set_xlabel("Veter [m/s]")
        ax2.grid(False)

    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close(fig)
    return path
