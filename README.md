# Soaring Slovenia (v2 – brez Telegrama)

Dnevni predlog vzletišč za jadralno padalstvo v Sloveniji.

## Hiter zagon
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

Ustvari se `SoaringSlovenia.ics` (uvozi v Apple Calendar) in PNG graf v `charts/`.

## Cron (macOS)
```
0 7 * * * /usr/bin/env bash -lc 'cd ~/Projects/soaring-slovenia && source .venv/bin/activate && python -m app.main'
```
