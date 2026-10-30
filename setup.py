
from pathlib import Path

project_path = Path(r"D:\LiverDiseasePrediction")

folders = [
    "data/raw",
    "data/processed",
    "notebooks",
    "models",
    "reports/figures"
]

for folder in folders:
    (project_path / folder).mkdir(parents=True,exist_ok=True)

print("Project folders created successfully!")
