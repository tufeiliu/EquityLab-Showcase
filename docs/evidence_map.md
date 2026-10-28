# Evidence map

This repository republishes aggregated results from the supplied historical research notebooks. Public files are not direct exports of the private training datasets.

| Public output | Notebook evidence | Scope |
| --- | --- | --- |
| `portfolio_policy_summary.csv`, `solver_reliability.csv` | Portfolio-policy notebook, completed solver-metadata and matched-scorecard section | 65 monthly / 9 quarterly |
| `selection_and_weighting.csv` | Portfolio-policy notebook, stock-selection and weighting ablation | Same samples as above |
| `forecast_allocation_comparison.csv` | Portfolio-integration notebook, matched-family outcome table | 59 monthly / 3 quarterly |
| `rolling_forecast_accuracy.csv` | Time-series notebook, monthly and daily rolling evaluation | 12 monthly / 126 daily holdout targets |
| `volatility_model_selection.csv` | Time-series notebook, conditional-variance selection report | 12 monthly observations |
| `scenario_stress_summary.csv` | Time-series notebook, correlated-GBM and block-bootstrap summary | Historical snapshots, 12 simulated months |
| `monthly_return_diagnostics.csv` | Time-series notebook, historical SPY summary | 65 monthly observations |

**Important:** Some separate allocation-engine experiments use overlapping dates but differing fitting procedures. Their results are not a controlled experiment unless the fitting and eligibility conditions are matched. No saved private solver coefficients, model states, security-level holdings, market-price histories or cache paths are included.

## Stock ranking and allocation

The public ablation is supported by `results/selection_and_weighting.csv`. See [interpretation and limitations](selection_and_weighting_explained.md). It varies portfolio composition and possibly weight sizes, so it must not be described as a pure causal sizing effect.
