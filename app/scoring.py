import math

def dir_diff(a, b):
    d = abs(a-b) % 360
    return d if d <= 180 else 360-d

def o_to_deg(o):
    m = {'N':0,'NE':45,'E':90,'SE':135,'S':180,'SW':225,'W':270,'NW':315}
    return m.get(o, 180)

def score_site(site, base_m, top_m, climb_ms, wind_dir_deg, wind_ms):
    elev = site['elev_m']
    headroom = max(0.0, base_m - elev)
    term_score = max(0.0, min(1.0, headroom/1200.0))
    climb_score = max(0.0, min(1.0, (climb_ms-1.0)/3.0))
    best_align = min(dir_diff(wind_dir_deg, o_to_deg(o)) for o in site.get('orientations', [])) if site.get('orientations') else 90
    orient_score = max(0.0, 1.0 - best_align/90.0)
    wind_penalty = 0.0 if wind_ms <= 9 else min(0.5, (wind_ms-9)/6.0)
    total = 100*(0.45*term_score + 0.35*climb_score + 0.20*orient_score)
    total *= (1.0 - wind_penalty)
    return round(total, 1)
