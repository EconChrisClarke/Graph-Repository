# Graph Repository

A running collection of standalone, interactive graphs. Each graph is a single
self-contained HTML file (built with the `econ-chart-style` house chart
engine) that can be opened directly from GitHub Pages, embedded, or downloaded
as a PNG.

Every graph gets its own row in the table below and, where the underlying
analysis required more than reading a published table off the shelf, its own
subfolder with the source data and the script used to compute the numbers.

## Live interactive graphs

| Graph | Live page | Files |
|---|---|---|
| The poorest fifth of households get the smallest share of Social Security spending | [social-security-by-income-quintile.html](https://econchrisclarke.github.io/Graph-Repository/social-security-by-income-quintile.html) | [folder](social-security-by-income-quintile/) |
| China continues to grow faster than average at a similar stage of development | [china-solow-growth-since-15k.html](https://econchrisclarke.github.io/Graph-Repository/china-solow-growth-since-15k.html) | [folder](china-solow-growth-since-15k/) |
| China's growth has slowed as incomes rose, as it did for peers, but it stays ahead of them | [china-solow-growth-vs-income.html](https://econchrisclarke.github.io/Graph-Repository/china-solow-growth-vs-income.html) | [folder](china-solow-growth-vs-income/) |

## Repo layout

```
<graph-name>.html                        the live, self-contained chart (open this to view/interact/download PNG)
<graph-name>/
  data/                                  raw source data as downloaded from the original agency/publisher
  scripts/                               script(s) that reproduce the chart's numbers from the raw data
```

Only graphs that required real computation (not just plotting numbers already
published in a table) get a subfolder — a graph built straight from a
published series may just be the `.html` file on its own.

## Social Security by income quintile

- **Live page:** https://econchrisclarke.github.io/Graph-Repository/social-security-by-income-quintile.html
- **Data:** [`social-security-by-income-quintile/data/cbo_61911_supplemental_data.xlsx`](social-security-by-income-quintile/data/cbo_61911_supplemental_data.xlsx) — CBO's *The Distribution of Household Income, 2022* (January 2026), Supplemental Data workbook, as published at [cbo.gov/publication/61911](https://www.cbo.gov/publication/61911).
- **Script:** [`social-security-by-income-quintile/scripts/compute_ss_shares.py`](social-security-by-income-quintile/scripts/compute_ss_shares.py) — reads Tables 1 and 5 of the workbook and computes each income quintile's share of aggregate Social Security benefits. Run with `python scripts/compute_ss_shares.py` from inside the `social-security-by-income-quintile/` folder.
- **Methodology summary:** households are ranked into equal-population fifths by CBO's "income before transfers and taxes" (market income plus Social Security, Medicare, unemployment insurance, and workers' compensation), adjusted for household size. Each quintile's share of total Social Security benefits is its average benefit per household (Table 5) times its household count (Table 1), as a share of the sum across all five quintiles. Full detail is in the script's docstring and in the chart's own footnote.

## China and the Solow model: growth since reaching $15,000

- **Live page:** https://econchrisclarke.github.io/Graph-Repository/china-solow-growth-since-15k.html ([file in repo](china-solow-growth-since-15k.html))
- **Question:** is China's slowdown in GDP per capita growth what the Solow model would lead us to expect at this income level? This first step is descriptive: it lines China up against 26 other economies by years since each reached $15,000 GDP per capita, so growth is compared at the same stage of development rather than the same calendar year. It is not yet a test of the Solow model's predictions.
- **Data:** [`china-solow-growth-since-15k/data/owid_maddison_gdp_per_capita.csv`](china-solow-growth-since-15k/data/owid_maddison_gdp_per_capita.csv) — GDP per capita from the Maddison Project Database 2023 (2011 international dollars), as republished by [Our World in Data](https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database). The original release is at [rug.nl/ggdc/historicaldevelopment/maddison](https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023). Derived series: [`growth_since_15k.csv`](china-solow-growth-since-15k/data/growth_since_15k.csv).
- **Scripts:** [`china-solow-growth-since-15k/scripts/`](china-solow-growth-since-15k/scripts/) — `prep.py` computes each country's crossing year and growth; `mkchart.py` builds the chart config; `tools/` holds the chart builder and (modified) chart template. Run `python prep.py`, then `python mkchart.py`, then `python tools/build_chart.py --config ../data/chart.json --template tools/chart-template.html --out ../../china-solow-growth-since-15k.html` from inside the `scripts/` folder.
- **Methodology summary:** year 0 for a country is the first year after which its GDP per capita stays at or above $15,000 (China: 2017). The vertical axis is the trailing 5-year compound annual growth rate, `(GDPpc_t / GDPpc_{t-5})^(1/5) - 1`. The 26 comparison economies were chosen by hand (advanced economies plus East Asian, Southern and Eastern European and Latin American catch-up cases); oil states, tiny economies, successor states and countries that fell back below $15,000 are excluded. The black median line is taken across the comparison countries with data at each x value, so its country mix shifts at longer horizons. China has only five years of data past $15,000 (through 2022).

## China and the Solow model: growth against income level

- **Live page:** https://econchrisclarke.github.io/Graph-Repository/china-solow-growth-vs-income.html ([file in repo](china-solow-growth-vs-income.html))
- **Question:** the companion to the [growth-since-$15,000 chart](china-solow-growth-since-15k/): instead of years since reaching $15,000, the horizontal axis is GDP per capita itself (log scale, $5k to $85k). Each line is one economy traced through income space; China is in red and the black line is the cross-country median at each income level. It is descriptive, not yet a test of the Solow model.
- **Data:** [`china-solow-growth-vs-income/data/owid_maddison_gdp_per_capita.csv`](china-solow-growth-vs-income/data/owid_maddison_gdp_per_capita.csv) — GDP per capita from the Maddison Project Database 2023 (2011 international dollars), as republished by [Our World in Data](https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database); original release at [rug.nl/ggdc](https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023). Derived series: [`growth_vs_income.csv`](china-solow-growth-vs-income/data/growth_vs_income.csv).
- **Scripts:** [`china-solow-growth-vs-income/scripts/`](china-solow-growth-vs-income/scripts/) — `prep_income.py` computes growth and keeps observations from 1955 with GDP per capita of at least $5,000 (and asserts that no year in any window is interpolated); `mkchart_income.py` computes the median and builds the chart config; `tools/` holds the chart builder and template. From inside `scripts/`: `python prep_income.py`, `python mkchart_income.py`, then `python tools/build_chart.py --config ../data/chart_income.json --template tools/chart-template.html --out ../../china-solow-growth-vs-income.html`.
- **Methodology summary:** growth is the trailing 5-year compound annual rate ending in each year, `(GDPpc_t / GDPpc_{t-5})^(1/5) - 1`, plotted against GDP per capita in year t. The median is built by cutting income into log-spaced bands about 15% wide, averaging each country's growth within a band, and taking the median across countries (each country counts once), shown only where at least 8 countries are in the band. The 26 comparison economies are the same hand-picked set as the growth-since-$15,000 chart, all of which eventually passed $15,000; that leaves out countries that stayed poor, so the median is biased upward at lower incomes. High-income bands contain only recent decades, so the country mix shifts along the axis.
