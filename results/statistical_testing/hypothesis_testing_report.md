# EquityLab: exploratory hypothesis tests

**Exploratory, not confirmatory.** The featured dynamic models were chosen after seeing these results. H1 and H2 use 36 monthly out-of-sample net returns; H3 uses 27.

## Summary

| Family | Tests | Raw p < 0.05 | Holm p < 0.05 | What it compares |
|---|---:|---:|---:|---|
| H1 own-risk MPT | 9 | 0 | 0 | Dynamic model vs MPT matched to its own estimated risk. The direct H1 test. |
| H1 conventional MPT | 24 | 13 | 4 | Dynamic model vs conventional MPT, not risk-matched. |
| H2 forecasting | 12 | 1 | 0 | Dynamic model vs the historical-mean control: the contribution of forecasting. |
| H3 information in MPT | 6 | 1 | 1 | One MPT optimiser with EquityLab-derived vs conventional inputs. |

p-values are one-sided (candidate better), from Newey–West HAC t-statistics with 3 lags and a normal reference. Holm correction is applied within each family. It does not correct for the earlier search across forecasting candidates.

## All tests

Return difference is 12 × the mean monthly paired net-return difference (arithmetic, not CAGR). Intervals are 95% paired circular block-bootstrap percentiles (3-month blocks, 3000 draws).

| Family | Representation / mandate | Model | Comparator | Return diff. / yr | 95% CI | HAC t | Sharpe diff. | Holm p |
|---|---|---|---|---:|---|---:|---:|---:|
| H1 own-risk MPT | Grouped / Balanced | Hierarchical state-space | MPT matched to own risk | — | — | 0.73 | +0.15 | 1.000 |
| H1 own-risk MPT | Grouped / Balanced | Quality low-rank Kalman | MPT matched to own risk | — | — | 0.68 | +0.18 | 1.000 |
| H1 own-risk MPT | Grouped / Defensive | Hierarchical state-space | MPT matched to own risk | — | — | 0.10 | -0.09 | 1.000 |
| H1 own-risk MPT | Grouped / Defensive | Quality low-rank Kalman | MPT matched to own risk | — | — | -0.28 | -0.27 | 1.000 |
| H1 own-risk MPT | Grouped / Growth | Hierarchical state-space | MPT matched to own risk | — | — | 0.43 | -0.09 | 1.000 |
| H1 own-risk MPT | Hierarchical / Balanced | Hierarchical state-space | MPT matched to own risk | — | — | 0.94 | +0.39 | 1.000 |
| H1 own-risk MPT | Hierarchical / Balanced | Quality low-rank Kalman | MPT matched to own risk | — | — | 0.76 | +0.11 | 1.000 |
| H1 own-risk MPT | Hierarchical / Defensive | Hierarchical state-space | MPT matched to own risk | — | — | 1.30 | +0.02 | 0.876 |
| H1 own-risk MPT | Hierarchical / Defensive | Quality low-rank Kalman | MPT matched to own risk | — | — | 0.93 | -0.06 | 1.000 |
| H1 conventional MPT | Grouped / Balanced | Hierarchical state-space | MPT / Historical mean | +5.5% | [-3.0%, +13.7%] | 1.25 | +0.13 | 0.596 |
| H1 conventional MPT | Grouped / Balanced | Hierarchical state-space | MPT / Shrinkage | +7.6% | [-0.9%, +16.0%] | 1.72 | +0.80 | 0.554 |
| H1 conventional MPT | Grouped / Balanced | Quality low-rank Kalman | MPT / Historical mean | +4.9% | [-4.4%, +14.3%] | 1.03 | +0.04 | 0.596 |
| H1 conventional MPT | Grouped / Balanced | Quality low-rank Kalman | MPT / Shrinkage | +7.0% | [-2.4%, +16.5%] | 1.49 | +0.72 | 0.596 |
| H1 conventional MPT | Grouped / Defensive | Hierarchical state-space | MPT / Historical mean | +1.1% | [-2.4%, +4.2%] | 0.66 | -0.59 | 0.596 |
| H1 conventional MPT | Grouped / Defensive | Hierarchical state-space | MPT / Shrinkage | +3.5% | [-0.5%, +7.1%] | 1.81 | +0.70 | 0.493 |
| H1 conventional MPT | Grouped / Defensive | Quality low-rank Kalman | MPT / Historical mean | +1.2% | [-2.2%, +4.6%] | 0.74 | -0.59 | 0.596 |
| H1 conventional MPT | Grouped / Defensive | Quality low-rank Kalman | MPT / Shrinkage | +3.5% | [-0.4%, +7.3%] | 1.93 | +0.71 | 0.400 |
| H1 conventional MPT | Grouped / Growth | Hierarchical state-space | MPT / Historical mean | +21.2% | [+7.3%, +33.6%] | 3.19 | +1.46 | 0.016 |
| H1 conventional MPT | Grouped / Growth | Hierarchical state-space | MPT / Shrinkage | +21.1% | [+7.7%, +34.3%] | 3.10 | +1.45 | 0.021 |
| H1 conventional MPT | Grouped / Growth | Quality low-rank Kalman | MPT / Historical mean | +19.7% | [+5.2%, +33.0%] | 2.77 | +1.32 | 0.056 |
| H1 conventional MPT | Grouped / Growth | Quality low-rank Kalman | MPT / Shrinkage | +19.6% | [+4.8%, +33.3%] | 2.75 | +1.31 | 0.057 |
| H1 conventional MPT | Hierarchical / Balanced | Hierarchical state-space | MPT / Historical mean | +6.0% | [-1.2%, +12.6%] | 1.71 | +0.42 | 0.554 |
| H1 conventional MPT | Hierarchical / Balanced | Hierarchical state-space | MPT / Shrinkage | +8.1% | [+1.6%, +14.4%] | 2.53 | +1.10 | 0.102 |
| H1 conventional MPT | Hierarchical / Balanced | Quality low-rank Kalman | MPT / Historical mean | +5.7% | [-2.4%, +13.8%] | 1.37 | +0.18 | 0.596 |
| H1 conventional MPT | Hierarchical / Balanced | Quality low-rank Kalman | MPT / Shrinkage | +7.9% | [-0.1%, +15.5%] | 2.02 | +0.85 | 0.361 |
| H1 conventional MPT | Hierarchical / Defensive | Hierarchical state-space | MPT / Historical mean | +3.2% | [-0.0%, +6.0%] | 2.03 | -0.11 | 0.361 |
| H1 conventional MPT | Hierarchical / Defensive | Hierarchical state-space | MPT / Shrinkage | +5.5% | [+2.4%, +8.7%] | 3.35 | +1.19 | 0.010 |
| H1 conventional MPT | Hierarchical / Defensive | Quality low-rank Kalman | MPT / Historical mean | +2.8% | [-1.0%, +6.1%] | 1.52 | -0.27 | 0.596 |
| H1 conventional MPT | Hierarchical / Defensive | Quality low-rank Kalman | MPT / Shrinkage | +5.1% | [+1.6%, +8.4%] | 2.83 | +1.02 | 0.048 |
| H1 conventional MPT | Hierarchical / Growth | Hierarchical state-space | MPT / Historical mean | +11.6% | [-1.5%, +23.9%] | 1.61 | +0.82 | 0.596 |
| H1 conventional MPT | Hierarchical / Growth | Hierarchical state-space | MPT / Shrinkage | +11.5% | [-1.8%, +24.7%] | 1.57 | +0.81 | 0.596 |
| H1 conventional MPT | Hierarchical / Growth | Quality low-rank Kalman | MPT / Historical mean | +10.1% | [-2.7%, +22.9%] | 1.45 | +0.73 | 0.596 |
| H1 conventional MPT | Hierarchical / Growth | Quality low-rank Kalman | MPT / Shrinkage | +10.0% | [-3.5%, +23.6%] | 1.41 | +0.72 | 0.596 |
| H2 forecasting | Grouped / Balanced | Hierarchical state-space | Historical-mean control | +2.2% | [-3.5%, +7.4%] | 0.73 | +0.10 | 1.000 |
| H2 forecasting | Grouped / Balanced | Quality low-rank Kalman | Historical-mean control | +1.6% | [-4.8%, +7.9%] | 0.48 | +0.01 | 1.000 |
| H2 forecasting | Grouped / Defensive | Hierarchical state-space | Historical-mean control | -0.3% | [-3.3%, +2.8%] | -0.18 | -0.23 | 1.000 |
| H2 forecasting | Grouped / Defensive | Quality low-rank Kalman | Historical-mean control | -0.2% | [-2.4%, +1.7%] | -0.20 | -0.22 | 1.000 |
| H2 forecasting | Grouped / Growth | Hierarchical state-space | Historical-mean control | +7.7% | [+0.6%, +14.7%] | 2.03 | +0.38 | 0.257 |
| H2 forecasting | Grouped / Growth | Quality low-rank Kalman | Historical-mean control | +6.1% | [-1.7%, +13.0%] | 1.60 | +0.24 | 0.604 |
| H2 forecasting | Hierarchical / Balanced | Hierarchical state-space | Historical-mean control | +2.3% | [-1.8%, +7.7%] | 0.96 | +0.19 | 1.000 |
| H2 forecasting | Hierarchical / Balanced | Quality low-rank Kalman | Historical-mean control | +2.0% | [-4.0%, +9.1%] | 0.62 | -0.05 | 1.000 |
| H2 forecasting | Hierarchical / Defensive | Hierarchical state-space | Historical-mean control | -0.7% | [-2.7%, +1.4%] | -0.70 | -0.42 | 1.000 |
| H2 forecasting | Hierarchical / Defensive | Quality low-rank Kalman | Historical-mean control | -1.1% | [-3.4%, +1.2%] | -0.89 | -0.59 | 1.000 |
| H2 forecasting | Hierarchical / Growth | Hierarchical state-space | Historical-mean control | -3.1% | [-13.5%, +6.7%] | -0.57 | -0.23 | 1.000 |
| H2 forecasting | Hierarchical / Growth | Quality low-rank Kalman | Historical-mean control | -4.6% | [-14.0%, +5.0%] | -0.87 | -0.31 | 1.000 |
| H3 information in MPT | Grouped / Balanced | Hybrid MPT | Conventional MPT | -0.4% | [-1.4%, +0.7%] | -0.68 | -0.14 | 1.000 |
| H3 information in MPT | Grouped / Defensive | Hybrid MPT | Conventional MPT | +0.8% | [-1.2%, +3.1%] | 0.79 | -0.05 | 0.644 |
| H3 information in MPT | Grouped / Growth | Hybrid MPT | Conventional MPT | +1.9% | [+0.3%, +3.5%] | 2.77 | +0.23 | 0.017 |
| H3 information in MPT | Hierarchical / Balanced | Hybrid MPT | Conventional MPT | -1.1% | [-2.4%, +0.3%] | -1.73 | -0.42 | 1.000 |
| H3 information in MPT | Hierarchical / Defensive | Hybrid MPT | Conventional MPT | +1.9% | [-1.0%, +4.7%] | 1.36 | +0.19 | 0.345 |
| H3 information in MPT | Hierarchical / Growth | Hybrid MPT | Conventional MPT | +1.2% | [-0.4%, +2.9%] | 1.57 | +0.12 | 0.291 |

## Limitations

- A non-significant result is not evidence of equivalence.
- 27 to 36 monthly observations are few; HAC and bootstrap intervals can be unstable. Check sensitivity to block length and lags.
- The comparisons share market months, asset list and models, so they are strongly dependent.
- Conventional MPT took less equity risk than the dynamic models, so wins in that family partly reflect risk taken. The own-risk family is the direct H1 test.
- The SPY-adjusted active alpha is a one-factor diagnostic, not a multi-factor attribution.

## Notes

- H1 own-risk MPT: monthly own-risk MPT returns are not released, so this family uses the released paired t-statistics (rescaled by sqrt(35/36) to match the small-sample correction) and has no bootstrap intervals. Incomplete solver paths are excluded.
- H3 covers a separate 27-month window (Oct 2023 to Dec 2025); its effect sizes are not comparable with the 36-month H1 and H2 estimates.
