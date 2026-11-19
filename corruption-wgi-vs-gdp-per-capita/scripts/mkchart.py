"""Build the chart config (data/chart.json) from data/wgi_vs_gdp_ppp.csv.

Run prep.py first, then this, then from inside scripts/:
    python tools/build_chart.py --config ../data/chart.json \
        --template tools/chart-template.html --out ../../corruption-wgi-vs-gdp-per-capita.html
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# plainer display names than the World Bank's
RENAME = {"Bahamas, The": "Bahamas", "Congo, Dem. Rep.": "DR Congo", "Congo, Rep.": "Congo",
          "Egypt, Arab Rep.": "Egypt", "Gambia, The": "Gambia", "Hong Kong SAR, China": "Hong Kong",
          "Iran, Islamic Rep.": "Iran", "Korea, Rep.": "South Korea", "Macao SAR, China": "Macao",
          "Micronesia, Fed. Sts.": "Micronesia", "Somalia, Fed. Rep.": "Somalia",
          "Russian Federation": "Russia", "Turkiye": "Turkey", "Viet Nam": "Vietnam",
          "Lao PDR": "Laos", "Kyrgyz Republic": "Kyrgyzstan", "Slovak Republic": "Slovakia",
          "Brunei Darussalam": "Brunei", "Yemen, Rep.": "Yemen", "Venezuela, RB": "Venezuela",
          "Syrian Arab Republic": "Syria", "St. Lucia": "Saint Lucia",
          "St. Kitts and Nevis": "Saint Kitts and Nevis",
          "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines"}

rows = list(csv.DictReader(open(os.path.join(DATA, "wgi_vs_gdp_ppp.csv"))))
for r in rows:
    r["name"] = RENAME.get(r["country"], r["country"])
pts = [[int(r["gdp_pc_ppp"]), float(r["wgi_cc_score_2025"]), r["name"]] for r in rows]
names = {p[2] for p in pts}
older = [f'{r["name"]} ({r["gdp_year"]})' for r in rows if r["gdp_year"] != "2025"]

# same orientation labels as the CPI chart
labels = ["Denmark", "Finland", "Singapore", "Switzerland", "United States", "United Kingdom",
          "Germany", "Japan", "China", "India", "Brazil", "Nigeria", "Qatar", "Saudi Arabia",
          "Ireland", "Burundi", "Somalia", "Bhutan", "Uruguay", "Turkmenistan", "Libya",
          "Mexico", "South Korea"]
assert all(l in names for l in labels), [l for l in labels if l not in names]

cfg = {
    "type": "scatter",
    "headline": "Richer countries score far better on control of corruption",
    "subhead": "World Bank Control of Corruption score, 2025 (0 = worst, 100 = best) vs GDP per "
               "capita at purchasing power parity",
    "source": "World Bank, Worldwide Governance Indicators 2026 update, Control of Corruption, "
              "governance score (GOV_WGI_CC.SC); World Bank, World Development Indicators, GDP per "
              "capita, PPP (constant 2021 international $), NY.GDP.PCAP.PP.KD",
    "sourceUrl": "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
    "note": (f"{len(pts)} economies with both a 2025 Control of Corruption score and recent World Bank "
             f"GDP data. GDP per capita is for 2025 except {', '.join(older)}. Not shown for lack of "
             "recent GDP data include Cuba, Eritrea, Liechtenstein, Monaco, North Korea, South Sudan, "
             "Syria, Venezuela and Yemen. The indicator combines about 30 surveys of firms, households "
             "and experts on the extent to which public power is used for private gain. Horizontal "
             "axis is log scale."),
    "xType": "number",
    "xScale": "log",
    "xMin": 800, "xMax": 150000,
    "xFormat": {"prefix": "$", "compact": True},
    "xLabel": "GDP per capita, PPP (2021 international $, log scale)",
    "yLabel": "Control of Corruption score",
    "yMin": 0, "yMax": 100,
    "format": {"decimals": 0},
    "hoverDecimals": 1,
    "fit": True,
    "pointLabels": labels,
    "series": [{"name": "Economies", "data": pts}],
}
json.dump(cfg, open(os.path.join(DATA, "chart.json"), "w"), indent=1)
print(len(pts), "points;", len(labels), "labels")
