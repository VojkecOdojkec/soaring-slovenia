import os, shutil, datetime as dt

CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#0b1220;color:#e6edf3;margin:0}
.wrap{max-width:960px;margin:0 auto;padding:24px}
.card{background:#111a2b;border:1px solid #233047;border-radius:14px;padding:20px;margin-bottom:18px;box-shadow:0 6px 18px rgba(0,0,0,.25)}
h1{margin:0 0 8px;font-size:26px}
h2{margin:6px 0 12px;font-size:18px;color:#9ecbff}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;margin-left:8px;background:#1f6feb;color:#fff}
.meta{color:#9fb3c8;font-size:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
table{width:100%;border-collapse:collapse}
th,td{padding:10px;border-bottom:1px solid #233047;text-align:left}
th{color:#9ecbff}
tr:hover td{background:#0e1726}
.score{font-weight:700}
.go{color:#2ecc71}.local{color:#f1c40f}.border{color:#e67e22}.nogo{color:#ff6b6b}
.tag{padding:2px 8px;border-radius:6px;background:#1b2738;margin-left:6px;color:#9fb3c8}
.kv{display:flex;gap:12px;flex-wrap:wrap}
.kv div{background:#0e1726;border:1px solid #233047;border-radius:10px;padding:8px 12px}
.chart{border-radius:10px;border:1px solid #233047;display:block;max-width:100%}
.footer{color:#9fb3c8;font-size:13px;margin-top:6px}
a{color:#9ecbff;text-decoration:none}a:hover{text-decoration:underline}
"""

def deg_to_card8(d):
    dirs=["N","NE","E","SE","S","SW","W","NW","N"]
    return dirs[round(((d%360)/45))]

def badge_for(score):
    if score>=70: return '<span class="badge">GO • XC</span>'
    if score>=50: return '<span class="badge">GO • lokalno</span>'
    if score>=35: return '<span class="badge">MEJNO</span>'
    return '<span class="badge" style="background:#b42323">NO-GO</span>'

def cls_for(score):
    if score>=70: return "go"
    if score>=50: return "local"
    if score>=35: return "border"
    return "nogo"

def render_html(date_iso, region, base, top, climb, wdir, wspd, ranked, chart_rel, raw_png_url, ics_raw_url):
    wind_txt=f"{int(wdir)}° ({deg_to_card8(wdir)}) / {wspd:.1f} m/s"
    rows=[]
    for s in ranked[:10]:
        rows.append(f"<tr><td>{s['name']}</td><td class='score {cls_for(s['score'])}'>{s['score']}</td><td>{badge_for(s['score'])}</td></tr>")
    rows_html="\n".join(rows)

    return f"""<!doctype html><html lang="sl"><meta charset="utf-8">
<title>Soaring Slovenia — {date_iso}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{CSS}</style>
<div class="wrap">
  <div class="card">
    <h1>Soaring Slovenia — dnevno poročilo <span class="badge">{date_iso}</span></h1>
    <div class="meta">{region} • Baza ~{int(base)} m • Top ~{int(top)} m • Dvigi ~{climb:.1f} m/s • Veter {wind_txt}</div>
  </div>

  <div class="grid">
    <div class="card">
      <h2>Predlogi vzletišč (TOP 10)</h2>
      <table>
        <thead><tr><th>Vzletišče</th><th>Ocena</th><th>Letljivost</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
      <div class="footer">Legenda: <span class="tag">GO • XC</span><span class="tag">GO • lokalno</span><span class="tag">MEJNO</span><span class="tag">NO-GO</span></div>
    </div>

    <div class="card">
      <h2>Mini graf</h2>
      <a href="{raw_png_url}" target="_blank"><img class="chart" src="{chart_rel}" alt="dnevni graf"></a>
      <div class="footer">Klik na graf odpre PNG v polni velikosti. <a href="{ics_raw_url}" target="_blank">ICS</a></div>
      <div class="kv" style="margin-top:10px">
        <div>Veter: <b>{wind_txt}</b></div>
        <div>Baza: <b>~{int(base)} m</b></div>
        <div>Top: <b>~{int(top)} m</b></div>
        <div>Dvigi: <b>~{climb:.1f} m/s</b></div>
      </div>
    </div>
  </div>

  <div class="footer">© Soaring Slovenia • Generirano samodejno ob 07:00 • Vir: Open-Meteo (+ prilagoditve)</div>
</div></html>"""

def write_report(docs_dir, date_iso, region, base, top, climb, wdir, wspd, ranked, chart_src_path, repo_slug, branch):
    os.makedirs(docs_dir, exist_ok=True)
    assets = os.path.join(docs_dir, "assets", "charts")
    os.makedirs(assets, exist_ok=True)
    fname = os.path.basename(chart_src_path)
    dst = os.path.join(assets, fname)
    if os.path.abspath(chart_src_path) != os.path.abspath(dst):
        shutil.copyfile(chart_src_path, dst)

    owner, repo = repo_slug.split("/")
    site_base = f"https://{owner}.github.io/{repo}"
    chart_rel = f"assets/charts/{fname}"
    raw_png_url = f"https://raw.githubusercontent.com/{repo_slug}/{branch}/charts/{fname}"
    ics_raw_url = f"https://raw.githubusercontent.com/{repo_slug}/{branch}/SoaringSlovenia.ics"

    html = render_html(date_iso, region, base, top, climb, wdir, wspd, ranked, chart_rel, raw_png_url, ics_raw_url)

    day_file = os.path.join(docs_dir, f"{date_iso}.html")
    with open(day_file, "w", encoding="utf-8") as f:
        f.write(html)

    index_html = f'<!doctype html><meta http-equiv="refresh" content="0; url={date_iso}.html">'
    with open(os.path.join(docs_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    return f"{site_base}/{date_iso}.html", f"{site_base}/"
