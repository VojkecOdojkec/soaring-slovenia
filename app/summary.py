def go_no_go(score):
    if score >= 70: return 'GO (XC)'
    if score >= 50: return 'GO (lokalno)'
    if score >= 35: return 'MEJNO'
    return 'NO-GO'

def build_message(date_str, region, sites_ranked, base_m, top_m, climb_ms, wind_deg, wind_ms):
    header = (f'📅 {date_str} – {region}\n'
              f'Baza ~{int(base_m)} m | Top ~{int(top_m)} m | Dvigi ~{climb_ms:.1f} m/s | '
              f'Veter {int(wind_deg)}° / {wind_ms:.1f} m/s\n')
    lines = ['— Predlogi vzletišč —']
    for s in sites_ranked[:8]:
        lines.append(f"{s['name']}: {s['score']} – {go_no_go(s['score'])}")
    return header + '\n'.join(lines)
