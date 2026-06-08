import csv
from pathlib import Path
from typing import Any, Dict


CSV_DIRECTORY = "csv"
CSV_FILE_NAME = "sensor_data.csv"

CSV_FIELDS = [
    "node_id",
    "node_name",
    "lamp_status",
    "relay_status",
    "energy",
    "power",
    "current",
    "rsl_out",
    "rsl_in",
    "disconnectivity",
    "connectivity",
    "availability",
    "rpl_rank",
    "ipv6",
    "temperature",
    "relative_humidity",
    "ambient_light",
]


def append_sensor_row(record: Dict[str, Any]) -> Path:
    base_path = Path(__file__).resolve().parent
    csv_dir = base_path / CSV_DIRECTORY
    csv_dir.mkdir(parents=True, exist_ok=True)

    csv_file_path = csv_dir / CSV_FILE_NAME
    should_write_header = (not csv_file_path.exists()) or csv_file_path.stat().st_size == 0

    row = {field: record.get(field, "") for field in CSV_FIELDS}

    with csv_file_path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        if should_write_header:
            writer.writeheader()
        writer.writerow(row)

    return csv_file_path
