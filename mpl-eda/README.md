# MPL Cambodia Season 6 — EDA Website

A complete **Quarto website** project performing end-to-end Exploratory Data Analysis
on the Mobile Legends Professional League Cambodia Season 6 dataset.

---

## Project Structure

```
mpl-eda/
├── _quarto.yml        ← Website configuration & global format settings
├── custom.scss        ← Dark theme stylesheet
├── utils.py           ← Reusable Python helpers (data loading, plotting, colours)
│
├── index.qmd          ← Home / Overview page
├── dataset.qmd        ← Dataset description & quality checks
├── univariate.qmd     ← Univariate analysis (distributions, summary stats)
├── bivariate.qmd      ← Bivariate analysis (correlations, role comparisons)
└── insights.qmd       ← Team & player insights (rankings, hero stats)
```

The **Data/** folder must remain at `../Data/` relative to this project root
(i.e. one level up from `mpl-eda/`).

---

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| **Quarto** | ≥ 1.4 | [quarto.org/docs/get-started](https://quarto.org/docs/get-started/) |
| **Python** | ≥ 3.9 | System or conda/venv |
| **Jupyter kernel** | any | `pip install ipykernel && python -m ipykernel install --user` |

### Python packages

```bash
pip install pandas numpy matplotlib seaborn scipy
```

---

## Rendering the Website

```bash
# From inside the mpl-eda/ directory:
quarto preview       # live-reload preview in your browser
quarto render        # build the full static site → _site/
```

The compiled site lands in `mpl-eda/_site/`. Open `_site/index.html` to browse
it offline, or deploy it to any static host (GitHub Pages, Netlify, Vercel, etc.).

---

## Key Design Decisions

- **All code is folded** (`code-fold: true`) — readers see results first and can expand code on demand.
- **Dark theme** — a custom SCSS stylesheet (`custom.scss`) pairs with Quarto's `cosmo` base theme to produce a clean, gaming-aesthetic dark UI.
- **`utils.py`** centralises the colour palette, the data-loading pipeline, and reusable plot helpers so every page is visually consistent.
- **Descriptive only** — no hypothesis tests or inferential statistics. Every section reports central tendency, spread, and visual patterns.

---

## Pages at a Glance

| Page | What's inside |
|---|---|
| **Home** | Tournament context, key numbers, analysis roadmap |
| **Dataset** | Column reference, data types, missing-value audit, distribution snapshot |
| **Univariate** | Match duration, kills, deaths, assists, gold, KDA, role shares, objectives |
| **Bivariate** | Kills ↔ Gold, KDA ↔ Gold, duration ↔ objectives, role boxplots, win/lose comparison, correlation matrix |
| **Insights** | Team win rates, gold efficiency, objective control, radar chart, player KDA/gold/MVP leaderboards, hero pick & win-rate charts |
