"""Used merchandise store sales as a share of GAFO sales, 1992 onward.

Reads the Census Bureau's Monthly Retail Trade workbook
(data/mrtssales92-present.xlsx, "Estimates of Monthly Retail and Food Services
Sales by Kind of Business", one sheet per year) and pulls two NOT seasonally
adjusted monthly series, in millions of nominal dollars:

  * NAICS 4533  Used merchandise stores
  * GAFO        Census aggregate of NAICS 442, 443, 448, 451, 452 and 4532
                (furniture and home furnishings; electronics and appliances;
                clothing and accessories; sporting goods, hobby, musical
                instrument and book; general merchandise; office supplies,
                stationery and gift stores). Used merchandise stores are NOT
                part of GAFO.

Both series are nominal and in the same dollars, so the ratio needs no
inflation adjustment. Because the data are not seasonally adjusted (and GAFO
spikes every December), the charted share is a trailing 12-month ratio:
sum of the last 12 months of used-merchandise sales divided by the sum of the
last 12 months of GAFO sales.

Writes data/used_merch_gafo_monthly.csv. Run from inside scripts/:
    python prep.py
"""
import csv
import datetime
import os
import re

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
WANT = {"Used merchandise stores": "used", "GAFO(1)": "gafo"}


def read_workbook(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = {}
    for sheet in wb.sheetnames:
        header, in_nsa = None, False
        for row in wb[sheet].iter_rows(values_only=True):
            if header is None and isinstance(row[2], str) and re.match(r"[A-Z][a-z]{2}\.? \d{4}", row[2]):
                header = row
            if row[1] == "NOT ADJUSTED":
                in_nsa = True
                continue
            if row[1] and str(row[1]).startswith("ADJUSTED"):
                break  # seasonally adjusted block follows; we want NSA only
            if in_nsa and row[1] in WANT:
                for j, h in enumerate(header):
                    # "Sep. 2026(p)" marks a preliminary estimate; keep it
                    m = re.match(r"([A-Z][a-z]{2})\.? (\d{4})(\(p\))?$", h or "") if isinstance(h, str) else None
                    if j < 2 or not m or not isinstance(row[j], (int, float)):
                        continue  # skips the annual TOTAL column and (S)/(NA) cells
                    d = datetime.datetime.strptime(f"{m.group(1)} {m.group(2)}", "%b %Y").date()
                    out.setdefault(d, {})[WANT[row[1]]] = row[j]
    return out


def main():
    data = read_workbook(os.path.join(DATA, "mrtssales92-present.xlsx"))
    months = sorted(data)
    assert all(len(data[m]) == 2 for m in months), "a month is missing one of the two series"
    # months must be consecutive for the rolling sum to be valid
    for a, b in zip(months, months[1:]):
        assert (b.year * 12 + b.month) - (a.year * 12 + a.month) == 1, f"gap between {a} and {b}"

    rows = []
    for i, m in enumerate(months):
        u, g = data[m]["used"], data[m]["gafo"]
        r = {"month": m.strftime("%Y-%m"), "used_merch_musd": u, "gafo_musd": g,
             "share_monthly_pct": round(100 * u / g, 4), "share_trailing12_pct": ""}
        if i >= 11:
            win = months[i - 11:i + 1]
            r["share_trailing12_pct"] = round(
                100 * sum(data[k]["used"] for k in win) / sum(data[k]["gafo"] for k in win), 4)
        rows.append(r)

    with open(os.path.join(DATA, "used_merch_gafo_monthly.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} months, {rows[0]['month']} to {rows[-1]['month']}")


if __name__ == "__main__":
    main()
