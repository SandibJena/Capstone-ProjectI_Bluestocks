"""
Live NAV Fetch

Description:
Fetch historical NAV data for mutual fund schemes from MFAPI
and save the response as both JSON and CSV files.

Author: Sandib Jena
Project: Bluestocks Data Analyst Capstone
"""

from pathlib import Path
import argparse
import csv
import json

import requests

# ==========================================================
# Project Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://api.mfapi.in/mf/{}"


# ==========================================================
# Fetch NAV Data
# ==========================================================

def fetch_and_save(amfi_code: str, out_dir: Path = RAW_DATA_DIR) -> None:
    """
    Fetch NAV history for a given AMFI scheme code and save it
    as both JSON and CSV files.

    Args:
        amfi_code (str): Mutual fund AMFI scheme code.
        out_dir (Path): Output directory.
    """

    out_dir.mkdir(parents=True, exist_ok=True)

    url = API_URL.format(amfi_code)

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    # ----------------------------------------------------------
    # Save JSON
    # ----------------------------------------------------------

    json_path = out_dir / f"live_nav_{amfi_code}.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    rows = data.get("data", [])

    if not rows:
        print(f"No NAV data found for AMFI code {amfi_code}")
        return

    # ----------------------------------------------------------
    # Save CSV
    # ----------------------------------------------------------

    csv_path = out_dir / f"live_nav_{amfi_code}.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["date", "nav"]
        )

        writer.writeheader()

        for row in rows:

            writer.writerow(
                {
                    "date": row.get("date"),
                    "nav": row.get("nav"),
                }
            )

    print("=" * 70)
    print(f"AMFI Code      : {amfi_code}")
    print(f"NAV Records    : {len(rows)}")
    print(f"JSON Saved To  : {json_path}")
    print(f"CSV Saved To   : {csv_path}")
    print("=" * 70)


# ==========================================================
# Main
# ==========================================================

def main():

    parser = argparse.ArgumentParser(
        description="Fetch historical NAV data from MFAPI"
    )

    parser.add_argument(
        "--codes",
        nargs="+",
        required=True,
        help="One or more AMFI scheme codes"
    )

    parser.add_argument(
        "--out",
        default=str(RAW_DATA_DIR),
        help="Output directory"
    )

    args = parser.parse_args()

    output_directory = Path(args.out)

    for code in args.codes:

        try:

            fetch_and_save(
                code,
                output_directory
            )

        except requests.exceptions.RequestException as error:

            print("=" * 70)
            print(f"Failed to fetch AMFI code {code}")
            print(error)
            print("=" * 70)


if __name__ == "__main__":
    main()