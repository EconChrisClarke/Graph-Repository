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
