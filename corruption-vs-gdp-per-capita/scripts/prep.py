"""Join TI's Corruption Perceptions Index 2025 to World Bank GDP per capita (PPP).

Inputs (in ../data/, as downloaded):
  CPI2025_Results.xlsx  Transparency International, CPI 2025 results workbook,
                        sheet "CPI2025" (country, ISO3, region, score 0-100).
                        https://www.transparency.org/en/cpi/2025
  wb_gdp_ppp.json       World Bank WDI, NY.GDP.PCAP.PP.KD: GDP per capita, PPP
                        (constant 2021 international $), 2020-2025, all economies.
                        https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.KD?format=json&per_page=20000&date=2020:2025
  wb_countries.json     World Bank country list, used to drop regional aggregates.

Output: ../data/cpi_vs_gdp_ppp.csv

GDP per capita is for 2025 where the World Bank has it; otherwise the latest year
from 2023-2024 is used and recorded in the gdp_year column. Countries with no GDP
figure since 2023 are dropped.

The workbook is saved in "strict" OOXML, which openpyxl cannot read, so the
sheet is parsed directly from its XML with the standard library.
"""
import csv, json, math, os, zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
# TI codes that differ from the World Bank's
ISO_ALIASES = {"KSV": "XKX"}  # Kosovo
NS = "{http://purl.oclc.org/ooxml/spreadsheetml/main}"


def read_cpi():
    z = zipfile.ZipFile(os.path.join(DATA, "CPI2025_Results.xlsx"))
    ss = ["".join(t.text or "" for t in si.iter(NS + "t"))
          for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")]
    rows = []
    for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "row"):
        r = {}
        for c in row.findall(NS + "c"):
            v = c.find(NS + "v")
            if v is None:
                continue
            col = "".join(ch for ch in c.get("r") if ch.isalpha())
            r[col] = ss[int(v.text)] if c.get("t") == "s" else v.text
        rows.append(r)
    hdr = next(i for i, r in enumerate(rows) if r.get("A") == "Country / Territory")
    assert rows[hdr]["D"] == "CPI 2025 score", rows[hdr]
    out = {}
    for r in rows[hdr + 1:]:
        if r.get("B") and r.get("D"):
            iso = ISO_ALIASES.get(r["B"], r["B"])
            out[iso] = dict(country=r["A"], region=r["C"], cpi=int(float(r["D"])))
    return out


def read_gdp():
    countries = json.load(open(os.path.join(DATA, "wb_countries.json")))[1]
    real = {c["id"] for c in countries if c["region"]["value"] != "Aggregates"}
    obs = json.load(open(os.path.join(DATA, "wb_gdp_ppp.json")))[1]
    best = {}
    for o in obs:
        iso, yr, v = o["countryiso3code"], int(o["date"]), o["value"]
        if iso in real and v is not None and yr >= 2023:
            if iso not in best or yr > best[iso][0]:
                best[iso] = (yr, v)
    return best


cpi, gdp = read_cpi(), read_gdp()
rows = []
for iso, c in sorted(cpi.items(), key=lambda kv: kv[1]["country"]):
    if iso in gdp:
        yr, v = gdp[iso]
        rows.append(dict(iso3=iso, country=c["country"], region=c["region"], cpi_2025=c["cpi"],
                         gdp_pc_ppp=round(v), gdp_year=yr))
missing = sorted(c["country"] for i, c in cpi.items() if i not in gdp)

with open(os.path.join(DATA, "cpi_vs_gdp_ppp.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

# correlation of CPI with log GDP per capita, for the headline
xs = [math.log10(r["gdp_pc_ppp"]) for r in rows]; ys = [r["cpi_2025"] for r in rows]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
r = sxy / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
print(f"CPI countries {len(cpi)}, matched {len(rows)}, r(CPI, log GDP) = {r:.2f}")
print("gdp years:", {y: sum(1 for x in rows if x['gdp_year'] == y) for y in (2023, 2024, 2025)})
print("no GDP since 2023:", missing)
