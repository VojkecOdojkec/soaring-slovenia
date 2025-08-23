from dataclasses import dataclass
import os

@dataclass
class Config:
    region: str = os.getenv('REGION', 'Slovenija')
    daily_hour: str = os.getenv('DAILY_HOUR', '07:00')  # lokalni čas
    ics_path: str = os.getenv('ICS_PATH', './SoaringSlovenia.ics')
    chart_dir: str = os.getenv('CHART_DIR', './charts')
    provider: str = os.getenv('PROVIDER', 'openmeteo')

CFG = Config()
