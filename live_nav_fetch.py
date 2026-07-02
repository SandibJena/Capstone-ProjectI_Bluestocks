"""
live_nav_fetch.py

Fetch historical NAV data for mutual fund schemes from the MFAPI
and save the response as both JSON and CSV files.

Author: Sandib Jena
Project: Bluestocks Data Analyst Internship
"""

import argparse
import csv
import json
import os

import requests

API_URL = "https://api.mfapi.in/mf/{}"


def fetch_and_save(amfi_code: str, out_dir: str = "data/raw") -> None:
    """
    Fetch NAV history for a given AMFI scheme code and save it
    as both JSON and CSV files.

    Args:
        amfi_code (str): Mutual fund AMFI scheme code.
        out_dir (str): Output directory for generated files.
    """
    os.makedirs(out_dir, exist_ok=True)

    url = API_URL.format(amfi_code)

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    # Save raw JSON response
    json_path = os.path.join(out_dir, f"live_nav_{amfi_code}.json")

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    rows = data.get("data", [])

    if not rows:
        print(f"⚠ No NAV data found for AMFI code {amfi_code}")
        return

    csv_path = os.path.join(out_dir, f"live_nav_{amfi_code}.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "nav"])
        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    "date": row.get("date"),
                    "nav": row.get("nav"),
                }
            )

    print(f"✓ AMFI Code : {amfi_code}")
    print(f"✓ NAV Records : {len(rows)}")
    print(f"✓ JSON Saved : {json_path}")
    print(f"✓ CSV Saved  : {csv_path}")
    print("-" * 60)


def main() -> None:
    """
    Parse command-line arguments and fetch NAV data.
    """
    parser = argparse.ArgumentParser(
        description="Fetch historical NAV data from mfapi.in"
    )

    parser.add_argument(
        "--codes",
        nargs="+",
        required=True,
        help="One or more AMFI scheme codes",
    )

    parser.add_argument(
        "--out",
        default="data/raw",
        help="Output directory",
    )

    args = parser.parse_args()

    for code in args.codes:
        try:
            fetch_and_save(code, out_dir=args.out)

        except requests.exceptions.RequestException as error:
            print(f"✗ Failed to fetch AMFI code {code}")
            print(f"Reason: {error}")
            print("-" * 60)


if __name__ == "__main__":
    main()