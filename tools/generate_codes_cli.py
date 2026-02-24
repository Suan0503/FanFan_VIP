#!/usr/bin/env python3
"""
簡單 CLI：呼叫 /admin/generate_codes 並將結果存成 CSV
使用：
  python tools/generate_codes_cli.py --host http://localhost:8080 --token <ADMIN_TOKEN> --count 10 --days 30 --out codes.csv
"""
import argparse
import requests
import csv

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--host', required=True)
    p.add_argument('--token', required=True)
    p.add_argument('--count', type=int, default=1)
    p.add_argument('--days', type=int, default=30)
    p.add_argument('--out', default='codes.csv')
    args = p.parse_args()

    url = args.host.rstrip('/') + '/admin/generate_codes'
    headers = {
        'Content-Type': 'application/json',
        'X-Admin-Token': args.token
    }
    resp = requests.post(url, json={'count': args.count, 'days': args.days}, headers=headers, timeout=30)
    if resp.status_code != 200:
        print('Error:', resp.status_code, resp.text)
        return
    data = resp.json()
    codes = data.get('codes', [])
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['code', 'days'])
        for c in codes:
            w.writerow([c, data.get('days', args.days)])
    print(f'已儲存 {len(codes)} 個序號到 {args.out}')

if __name__ == '__main__':
    main()
