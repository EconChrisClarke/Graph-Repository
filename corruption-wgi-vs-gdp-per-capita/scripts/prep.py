"""Join the World Bank's WGI Control of Corruption score to GDP per capita (PPP).

Inputs (in ../data/, as downloaded from the World Bank API):
  wgi_cc_score.json     GOV_WGI_CC.SC: Control of Corruption, governance score (0-100),
                        Worldwide Governance Indicators, 2018-2025.
                        https://api.worldbank.org/v2/country/all/indicator/GOV_WGI_CC.SC?format=json&per_page=20000&date=2018:2025
  wgi_cc_estimate.json  GOV_WGI_CC.EST: the same indicator on its native scale (about -2.5
                        to +2.5). Kept for reference; not plotted.
  wb_gdp_ppp.json       NY.GDP.PCAP.PP.KD: GDP per capita, PPP (constant 2021 international $).
  wb_countries.json     World Bank country list, used to drop regional aggregates.

Output: ../data/wgi_vs_gdp_ppp.csv

Index year is 2025. GDP per capita is for 2025 where available, otherwise the latest
year from 2023-2024 (recorded in gdp_year).
"""
import csv, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
YEAR = 2025


def wb(name):
    return json.load(open(os.path.join(DATA, name)))[1]


real = {c["id"]: c["name"] for c in wb("wb_countries.json") if c["region"]["value"] != "Aggregates"}

wgi = {o["countryiso3code"]: o["value"] for o in wb("wgi_cc_score.json")
       if int(o["date"]) == YEAR and o["value"] is not None and o["countryiso3code"] in real}

gdp = {}
for o in wb("wb_gdp_ppp.json"):
    iso, yr, v = o["countryiso3code"], int(o["date"]), o["value"]
    if iso in real and v is not None and yr >= YEAR - 2 and yr <= YEAR:
        if iso not in gdp or yr > gdp[iso][0]:
            gdp[iso] = (yr, v)

rows = [dict(iso3=i, country=real[i], wgi_cc_score_2025=round(wgi[i], 1),
             gdp_pc_ppp=round(gdp[i][1]), gdp_year=gdp[i][0])
        for i in sorted(wgi, key=lambda i: real[i]) if i in gdp]
missing = sorted(real[i] for i in wgi if i not in gdp)

with open(os.path.join(DATA, "wgi_vs_gdp_ppp.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

xs = [math.log10(r["gdp_pc_ppp"]) for r in rows]; ys = [r["wgi_cc_score_2025"] for r in rows]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
r = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(
    sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
print(f"WGI economies {len(wgi)}, matched {len(rows)}, r(WGI, log GDP) = {r:.2f}")
print("older GDP:", [(x["country"], x["gdp_year"]) for x in rows if x["gdp_year"] != YEAR])
print("no GDP since 2023:", missing)
