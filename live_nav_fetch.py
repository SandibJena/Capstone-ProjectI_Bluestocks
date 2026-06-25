import os
import argparse
import requests
import csv
import json

API_URL = "https://api.mfapi.in/mf/{}"


def fetch_and_save(amfi_code, out_dir="data/raw"):
    os.makedirs(out_dir, exist_ok=True)
    url = API_URL.format(amfi_code)
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    # save raw json
    json_path = os.path.join(out_dir, f"live_nav_{amfi_code}.json")
    with open(json_path, 'w', encoding='utf8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    # parse data -> save CSV
    rows = data.get('data', [])
    csv_path = os.path.join(out_dir, f"live_nav_{amfi_code}.csv")
    if rows:
        with open(csv_path, 'w', newline='', encoding='utf8') as fh:
            writer = csv.DictWriter(fh, fieldnames=['date', 'nav'])
            writer.writeheader()
            for rrow in rows:
                writer.writerow({'date': rrow.get('date'), 'nav': rrow.get('nav')})
    print(f"Saved {len(rows)} NAV rows to {csv_path} and raw json to {json_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch NAVs from mfapi.in for given AMFI codes')
    parser.add_argument('--codes', nargs='+', required=True, help='AMFI codes to fetch')
    parser.add_argument('--out', default='data/raw', help='output directory')
    args = parser.parse_args()
    for c in args.codes:
        try:
            fetch_and_save(c, out_dir=args.out)
        except Exception as e:
            print(f"Failed to fetch {c}: {e}")
