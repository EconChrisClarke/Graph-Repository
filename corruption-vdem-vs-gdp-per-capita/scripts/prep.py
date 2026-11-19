"""Join V-Dem's Political Corruption Index to World Bank GDP per capita (PPP).

Inputs (in ../data/):
  owid_vdem_political_corruption.csv   V-Dem Political Corruption Index (v2x_corr), central
                        estimate, 0 (least corrupt) to 1 (most corrupt), V-Dem dataset v16
                        (March 2026) as republished by Our World in Data:
                        https://ourworldindata.org/grapher/political-corruption-index
                        (metadata in owid_vdem_political_corruption.metadata.json)
  wb_gdp_ppp.json       World Bank NY.GDP.PCAP.PP.KD: GDP per capita, PPP (constant 2021
                        international $), 2020-2025.
  wb_countries.json     World Bank country list, used to drop regional aggregates.

Output: ../data/vdem_vs_gdp_ppp.csv

Index year is 2025. GDP per capita is for 2025 where available, otherwise the latest
year from 2023-2024 (recorded in gdp_year). Countries are joined on ISO3 code.
"""
import csv, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
YEAR = 2025
# OWID codes that differ from the World Bank's
ISO_ALIASES = {"OWID_KOS": "XKX"}  # Kosovo


def wb(name):
    return json.load(open(os.path.join(DATA, name)))[1]


real = {c["id"] for c in wb("wb_countries.json") if c["region"]["value"] != "Aggregates"}

vdem, unmatched_codes = {}, []
for r in csv.DictReader(open(os.path.join(DATA, "owid_vdem_political_corruption.csv"))):
    if int(r["year"]) != YEAR or r["corruption_vdem__estimate_best"] == "":
        continue
    iso = ISO_ALIASES.get(r["code"], r["code"])
    if iso in real:
        vdem[iso] = (r["entity"], float(r["corruption_vdem__estimate_best"]))
    elif r["code"]:  # rows without a code are OWID's regional averages
        unmatched_codes.append(r["entity"])

gdp = {}
for o in wb("wb_gdp_ppp.json"):
    iso, yr, v = o["countryiso3code"], int(o["date"]), o["value"]
    if iso in real and v is not None and YEAR - 2 <= yr <= YEAR:
        if iso not in gdp or yr > gdp[iso][0]:
            gdp[iso] = (yr, v)

rows = [dict(iso3=i, country=vdem[i][0], vdem_corruption_2025=round(vdem[i][1], 3),
             gdp_pc_ppp=round(gdp[i][1]), gdp_year=gdp[i][0])
        for i in sorted(vdem, key=lambda i: vdem[i][0]) if i in gdp]
missing = sorted(vdem[i][0] for i in vdem if i not in gdp)

with open(os.path.join(DATA, "vdem_vs_gdp_ppp.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

xs = [math.log10(r["gdp_pc_ppp"]) for r in rows]; ys = [r["vdem_corruption_2025"] for r in rows]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
r = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(
    sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
print(f"V-Dem countries {len(vdem) + len(unmatched_codes)}, matched {len(rows)}, r(V-Dem, log GDP) = {r:.2f}")
print("not World Bank economies (dropped):", unmatched_codes)
print("older GDP:", [(x["country"], x["gdp_year"]) for x in rows if x["gdp_year"] != YEAR])
print("no GDP since 2023:", missing)
