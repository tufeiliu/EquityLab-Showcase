# Dynamic Phase 2 model comparison (public analytical extract)

The **main design** uses temporally forecast economic coefficients in portfolio construction. Historical-mean (`mean`) coefficients are an ablation and comparison control.

The two featured public dynamic candidates are hierarchical state-space and quality low-rank Kalman. They were selected as historical examples with **different** temporal assumptions and their mixed historical outcomes, not by a validated prospective model-selection algorithm. The full private analysis includes other model candidates, including models that perform poorly or more favourably in individual cases.

## Evidence and interpretation

`results/selected_dynamic_model_summary.csv` is a curated transcription of the 36-month model summary printed by the complete private v1.4 run. Figures 18–21 are generated from this exact table by `analysis/plot_dynamic_candidates.py`. Metrics contain modelled costs, use an illustrative initial account of 10,000, and have outstanding historical point-in-time and currency validation concerns.

The independent conventional MPT variants estimate expected returns from historical data, with a sample-mean estimator or a shrinkage estimator. They do not use EquityLab coefficients. The exact-risk MPT implementation in the v1.4 archive matches the **historical-mean coefficient control** at each date, **not the dynamic candidates**. A separate run matches MPT to each dynamic candidate's own risk; see `results/nvda_and_own_risk_robustness.csv`.

The private-to-public monthly export is allowlisted and verifies that each selected dynamic candidate's full 36-month wealth path reconciles with the model summary before generating line plots. Missing monthly data must never be replaced by interpolation or synthetic curves.

## Remaining work

Prospectively define the dynamic model-selection policy; resolve solver failures in the incomplete own-risk MPT paths; verify point-in-time macro and asset data and FX conversion; expand and validate the investable universe; assess financing/turnover/capacity; and test proposed timestamped LLM-derived event shocks as external model features.

## Selected public asset-composition diagnostics

The optional portfolio-membership exporter defaults to the featured **hierarchical state-space** dynamic candidate, not the historical-mean control. Published summaries omit exact weights and security names. The outputs are descriptive historical holdings, not a complete explanation of how securities were chosen.
