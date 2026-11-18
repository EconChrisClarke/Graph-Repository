"""Build the chart config (data/chart.json) from data/used_merch_gafo_monthly.csv.

Run prep.py first, then this, then from inside scripts/:
    python tools/build_chart.py --config ../data/chart.json \
        --template tools/chart-template.html --out ../../used-merchandise-share-of-gafo.html
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

rows = list(csv.DictReader(open(os.path.join(DATA, "used_merch_gafo_monthly.csv"))))
pts = [[r["month"] + "-01", round(float(r["share_monthly_pct"]), 4)] for r in rows]
peak = max(pts, key=lambda p: p[1])
assert peak == pts[-1], "headline claims the latest month is the record; it no longer is"

cfg = {
    "type": "area",
    "headline": "Secondhand stores' sales are the highest share of merchandise sales on record",
    "subhead": "US used merchandise store sales as a share of GAFO store sales, monthly",
    "source": "US Census Bureau, Monthly Retail Trade Survey, Estimates of Monthly Retail and "
              "Food Services Sales by Kind of Business (not seasonally adjusted); author's calculations",
    "sourceUrl": "https://www.census.gov/retail/sales.html",
    "note": ("GAFO (general merchandise, apparel and accessories, furniture, and other) is a Census "
             "grouping of stores that sell department-store-type goods: furniture and home furnishings "
             "(NAICS 442), electronics and appliances (443), clothing and accessories (448), sporting "
             "goods, hobby, musical instrument and book (451), general merchandise (452), and office "
             "supply, stationery and gift stores (4532). Used merchandise stores (4533), such as thrift, "
             "consignment and antique shops, are not part of GAFO. Share = monthly used merchandise sales "
             "divided by monthly GAFO sales, both in nominal dollars and not seasonally adjusted, so the "
             "share dips every December when GAFO holiday sales peak. Excludes online resale platforms. "
             "Latest month (Sep 2026) is preliminary."),
    "xType": "date",
    "format": {"suffix": "%", "decimals": 1},
    "hoverDecimals": 2,
    "yZero": True,
    "series": [{"name": "Used merchandise share of GAFO", "data": pts}],
}
json.dump(cfg, open(os.path.join(DATA, "chart.json"), "w"), indent=1)
print("peak", peak, len(pts), "points")
