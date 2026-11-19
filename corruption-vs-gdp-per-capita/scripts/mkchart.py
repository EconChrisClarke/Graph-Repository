"""Build the chart config (data/chart.json) from data/cpi_vs_gdp_ppp.csv.

Run prep.py first, then this, then from inside scripts/:
    python tools/build_chart.py --config ../data/chart.json \
        --template tools/chart-template.html --out ../../corruption-vs-gdp-per-capita.html
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# shorter display names than TI's
RENAME = {"United States of America": "United States", "Korea, South": "South Korea",
          "Russian Federation": "Russia"}

rows = list(csv.DictReader(open(os.path.join(DATA, "cpi_vs_gdp_ppp.csv"))))
for r in rows:
    r["name"] = RENAME.get(r["country"], r["country"])
pts = [[int(r["gdp_pc_ppp"]), int(r["cpi_2025"]), r["name"]] for r in rows]
by = {p[2]: p for p in pts}
older = sorted(r["name"] for r in rows if r["gdp_year"] != "2025")

labels = ["Denmark", "Finland", "Singapore", "Switzerland", "United States", "United Kingdom",
          "Germany", "Japan", "China", "India", "Brazil", "Nigeria", "Qatar", "Saudi Arabia",
          "Ireland", "Burundi", "Somalia", "Bhutan", "Uruguay", "Turkmenistan", "Libya",
          "Mexico", "South Korea", "Venezuela"]
labels = [l for l in labels if l in by]


cfg = {
    "type": "scatter",
    "headline": "Richer countries are seen as far less corrupt",
    "subhead": "Corruption Perceptions Index 2025 (0 = highly corrupt, 100 = very clean) vs "
               "GDP per capita at purchasing power parity",
    "source": "Transparency International, Corruption Perceptions Index 2025; World Bank, World "
              "Development Indicators, GDP per capita, PPP (constant 2021 international $), NY.GDP.PCAP.PP.KD",
    "sourceUrl": "https://www.transparency.org/en/cpi/2025",
    "note": (f"{len(pts)} countries scored in the CPI 2025 with World Bank GDP data. GDP per capita is "
             f"for 2025 except {', '.join(older)} (2024). Not shown for lack of recent GDP data: Cuba, "
             "Eritrea, North Korea, South Sudan, Syria, Taiwan, Venezuela, Yemen. The CPI measures how "
             "corrupt experts and business people perceive a country's public sector to be, not "
             "corruption itself. Horizontal axis is log scale."),
    "xType": "number",
    "xScale": "log",
    "xMin": 800, "xMax": 150000,
    "xFormat": {"prefix": "$", "compact": True},
    "xLabel": "GDP per capita, PPP (2021 international $, log scale)",
    "yLabel": "Corruption Perceptions Index score",
    "yMin": 0, "yMax": 100,
    "format": {"decimals": 0},
    "fit": True,
    "pointLabels": labels,
    "series": [{"name": "Countries", "data": pts}],
}
json.dump(cfg, open(os.path.join(DATA, "chart.json"), "w"), indent=1)
print(len(pts), "points;", len(labels), "labels; older GDP:", older)
