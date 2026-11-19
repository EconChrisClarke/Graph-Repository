"""Build the chart config (data/chart.json) from data/vdem_vs_gdp_ppp.csv.

Run prep.py first, then this, then from inside scripts/:
    python tools/build_chart.py --config ../data/chart.json \
        --template tools/chart-template.html --out ../../corruption-vdem-vs-gdp-per-capita.html
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

rows = list(csv.DictReader(open(os.path.join(DATA, "vdem_vs_gdp_ppp.csv"))))
pts = [[int(r["gdp_pc_ppp"]), float(r["vdem_corruption_2025"]), r["country"]] for r in rows]
names = {p[2] for p in pts}
older = [f'{r["country"]} ({r["gdp_year"]})' for r in rows if r["gdp_year"] != "2025"]

# same orientation labels as the CPI chart
labels = ["Denmark", "Finland", "Singapore", "Switzerland", "United States", "United Kingdom",
          "Germany", "Japan", "China", "India", "Brazil", "Nigeria", "Qatar", "Saudi Arabia",
          "Ireland", "Burundi", "Somalia", "Bhutan", "Uruguay", "Turkmenistan", "Libya",
          "Mexico", "South Korea"]
assert all(l in names for l in labels), [l for l in labels if l not in names]

cfg = {
    "type": "scatter",
    "headline": "Richer countries have far less political corruption",
    "subhead": "V-Dem Political Corruption Index, 2025 (0 = least corrupt, 1 = most corrupt) vs "
               "GDP per capita at purchasing power parity",
    "source": "V-Dem Institute, V-Dem dataset v16 (March 2026), Political Corruption Index "
              "(v2x_corr), via Our World in Data; World Bank, World Development Indicators, GDP per "
              "capita, PPP (constant 2021 international $), NY.GDP.PCAP.PP.KD",
    "sourceUrl": "https://ourworldindata.org/grapher/political-corruption-index",
    "note": (f"{len(pts)} countries with both a 2025 V-Dem score and recent World Bank GDP data. GDP "
             f"per capita is for 2025 except {', '.join(older)}. Not shown for lack of recent GDP "
             "data: Cuba, Eritrea, North Korea, South Sudan, Syria, Venezuela, Yemen. Taiwan, Somaliland "
             "and Zanzibar have no World Bank GDP series, and Palestine is left out because V-Dem "
             "scores Gaza and the West Bank separately. The "
             "index is built from country experts' ratings of bribery and embezzlement in the "
             "executive, legislature, judiciary and public sector. Higher means more corrupt, the "
             "opposite direction to the CPI. Horizontal axis is log scale."),
    "xType": "number",
    "xScale": "log",
    "xMin": 800, "xMax": 150000,
    "xFormat": {"prefix": "$", "compact": True},
    "xLabel": "GDP per capita, PPP (2021 international $, log scale)",
    "yLabel": "Political Corruption Index (higher = more corrupt)",
    "yMin": 0, "yMax": 1,
    "format": {"decimals": 2},
    "hoverDecimals": 2,
    "fit": True,
    "pointLabels": labels,
    "series": [{"name": "Countries", "data": pts}],
}
json.dump(cfg, open(os.path.join(DATA, "chart.json"), "w"), indent=1)
print(len(pts), "points;", len(labels), "labels")
