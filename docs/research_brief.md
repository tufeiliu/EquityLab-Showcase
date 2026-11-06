# EquityLab research brief

## What this repository is

This is a curated public research portfolio, not a release of the private EquityLab engine. It shows the research question, experimental controls and results without disclosing signal construction or portfolio construction.

## Research question

Can an economically structured forecasting-and-allocation framework beat conventional mean-variance optimisation (MPT) after trading costs and risk? Beating passive benchmarks such as SPY would be a further bonus.

## What was built privately

1. Identify a portfolio-related economic coefficient representation.
2. Forecast that representation through time using historical information only.
3. Translate the forecast into constrained portfolios for Growth, Balanced and Defensive mandates.

The portfolios draw on a fixed list of 44 instruments. See [Asset universe](../README.md#asset-universe).

## Questions tested

- **H1:** does a dynamic EquityLab strategy beat conventional MPT after accounting for risk?
- **H2:** what explains the differences: forecasting, asset choice, allocation or market exposure?
- **H3:** can EquityLab-derived information improve a shared MPT optimiser?

## Findings so far

- The two featured dynamic models beat both conventional MPT variants on ending wealth in 12 of 12 comparisons each.
- Against MPT matched to their own estimated risk, they finished ahead in 8 of 9 complete comparisons, with no gap clearly above zero, so H1 is promising but not established.
- They beat the fair passive benchmark in 4 of 12 comparisons: 2 of 4 in Growth against SPY, 0 of 4 in Balanced and 2 of 4 in Defensive against the SPY/T-bill blend.
- They beat the non-dynamic historical-mean control in 6 of 12 comparisons, so the value of forecasting itself is unclear.
- Without NVDA, they still beat MPT, including 11 of 11 own-risk comparisons, but none beats its fair passive benchmark.

The results are exploratory. The sample is 36 months, the models were chosen with hindsight, and the universe is not verified as point-in-time.
