# Statistical hypothesis testing: H1, H2 and H3

This is an **exploratory** analysis of dated, out-of-sample monthly **net** portfolio returns. It reads only the released portfolio-level CSVs in `results/` and does not rerun forecasting or optimisation. The featured dynamic models were chosen after seeing these results, so the p-values are **not confirmatory evidence** for a prospectively selected strategy.

## Running it

```bash
python -m pip install -r requirements.txt
python analysis/research_hypothesis_inference.py
python -m unittest discover -s tests
```

Outputs, in `results/statistical_testing/`:

- `hypothesis_testing_report.md`: summary and every test in one table.
- `hypothesis_tests_exploratory.csv`: all statistics, one row per test.
- `hypothesis_testing_provenance.json`: inputs and settings.

Sensitivity check with longer blocks and lags:

```bash
python analysis/research_hypothesis_inference.py --block-months 6 --hac-lags 6 \
  --output-dir results/statistical_testing_block6
```

## Inputs

| File | Used for | Content |
|---|---|---|
| `selected_monthly_net_wealth.csv` | H1 conventional MPT, H2 | 36 monthly net returns per strategy, Jan 2023 to Dec 2025 |
| `nvda_and_own_risk_robustness.csv` | H1 own-risk MPT | Ending wealth, Sharpe and paired HAC t against MPT matched to each model's own risk |
| `h3_paired_monthly_net_returns.csv` | H3 | 27 monthly net returns for hybrid MPT, conventional MPT and T-bills, Oct 2023 to Dec 2025 |

All three contain portfolio-level returns only: no holdings, weights, tickers, coefficients or signals. Every paired test uses the same dated months for both strategies. Nothing is interpolated or rebuilt from ending wealth, and an incomplete panel stops the script.

## Test families

These follow the H1–H3 questions in the [README](../README.md#the-research-question).

| Family | Tests | Question |
|---|---:|---|
| H1 own-risk MPT | 9 | Does each dynamic model beat MPT matched to its own estimated risk? This is the direct H1 test. Three of the 12 paths are excluded because the MPT solver failed in some months. |
| H1 conventional MPT | 24 | Does each dynamic model beat MPT / Historical mean and MPT / Shrinkage? Not risk-matched: conventional MPT took less equity risk. |
| H2 forecasting | 12 | Does each dynamic model beat the historical-mean control, which uses the same framework without forecasting? This isolates one part of H2's attribution question. |
| H3 information in MPT | 6 | Does one MPT optimiser do better with EquityLab-derived inputs than with conventional inputs? Separate 27-month window. |

The count of 12 configurations is 2 dynamic models × 2 representations × 3 mandates. Holm's correction is applied separately within each family.

## Definitions

- **Effect:** `12 × mean(monthly return A − monthly return B)`, an arithmetic annual difference, not a CAGR difference.
- **HAC t:** intercept of the paired monthly difference, with Newey–West (Bartlett) standard errors, 3 lags and the `n / (n − k)` small-sample correction. The notebook uses the same estimator.
- **p-value:** one-sided (candidate better), normal reference. With 27–36 months this is approximate. One-sided p < 0.05 corresponds to t > 1.645. The README's "clearly above zero" uses the stricter t > 1.96.
- **Own-risk family:** monthly returns for own-risk MPT are not released, so this family uses the paired t-statistics from the private pipeline, rescaled by √((n−1)/n) to apply the same small-sample correction. It has no bootstrap intervals. Other t-statistics in the released CSVs (`paired_excess_hac_t`, `paired_hac_t`) are uncorrected and about 1.4% (36 months) to 1.9% (27 months) larger. No published conclusion changes either way.
- **Bootstrap interval:** 95% paired circular block bootstrap, 3-month blocks and 3,000 draws. The same resampled months are used for both strategies and for the T-bill rate.
- **Sharpe:** `√12 × mean(return − T-bill) / sd(return)`. The Sharpe difference is descriptive, with a bootstrap interval.
- **SPY-adjusted active alpha:** intercept of `A − B = α + β(SPY − T-bills) + ε`. A one-factor diagnostic, not attribution.

## Current results

| Family | Tests | p < 0.05 | After Holm |
|---|---:|---:|---:|
| H1 own-risk MPT | 9 | 0 | 0 |
| H1 conventional MPT | 24 | 13 | 4 |
| H2 forecasting | 12 | 1 | 0 |
| H3 information in MPT | 6 | 1 | 1 |

The direct H1 test finds no significant gap, so H1 remains promising but not established.

**Statistical power.** For a paired test of active return, t ≈ IR × √T, where IR is the annual information ratio (mean active return / tracking error) and T is in years. With T = 3, reaching t = 1.96 needs IR ≈ 1.96 / √3 ≈ 1.13. Good active strategies typically run at an IR of 0.3–0.7. An IR of 0.5 would need (1.96 / 0.5)² ≈ 15 years. This sample can therefore detect only a very large edge, and a non-significant result here is inconclusive rather than evidence of no edge.

## What would make this confirmatory

- A dynamic model-selection rule fixed in advance on training and validation data.
- Evaluation on dates not used for any design choice.
- Own-risk MPT monthly paths released, so the direct H1 test can carry bootstrap intervals too.

Not rejecting the null is not evidence that the strategies are equivalent.
