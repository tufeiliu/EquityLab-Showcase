# Methodology (public overview)

The private research engine assembles historical decision-date feature vectors from price history and available financial information; trains return-regression baselines (Ridge, Lasso and Elastic Net); and compares them with directly fitted constrained portfolio policies. Shared portfolio-rule parameters are fitted using **multiple completed historical holding periods**, not future outcomes. Monthly and quarterly decision schedules are evaluated separately against matched SPY holding intervals with estimated trading costs.

## Controls

- Train using only matured labels at each decision date; tune on earlier chronological periods.
- Use consistent long-only budget and maximum-weight assumptions.
- Compare with equal weight and SPY, including costs and turnover diagnostics.
- Keep market-derived and accounting-feature availability distinct; a carried-forward filing value is not a newly published observation.
- Examine holdings turnover, concentration, universe completeness and benchmark alignment.

The exact feature recipes, fitted parameters, optimisation routine, and nonpublic implementation are intentionally **not released**. The public figures and results are derived from saved notebook outputs, not recomputed by the presentation notebooks. This prevents full independent replication; see [limitations](limitations.md).

See [Data Sources and Coverage](data_sources_and_coverage.md) for provider context, inventory counts and the distinction between raw data, historical as-of values and realised return labels.
