# Data sources, coverage and provenance

## Data families

| Data family | Role | Verification boundary |
| --- | --- | --- |
| Historical adjusted equity prices | Return endpoints, market statistics and risk characteristics | Vendor adjustments and all security events not independently certified |
| SPY historical prices | Matching market benchmark and daily time-series diagnostics | Currency and execution conventions simplified |
| Dated company accounts | Company-characteristic research where available | Filing availability dates and completeness not fully audited |
| Security descriptors | Coverage and grouping analysis | Historical membership and descriptive metadata may be incomplete |
| Macroeconomic series | Broader potential research context | No claim that every available series entered published models |

## Coverage

The price audit describes **31 candidate stock tickers**, approximately **74,592 adjusted-price rows** from **36 source series**, spanning January 2005 to October 2026 in aggregate. Individual stocks have shorter and differing histories. This inventory is not the evaluation sample and does not imply that all assets traded continuously throughout the full range.

The matched portfolio-policy analysis uses **65 monthly** and **nine quarterly** intervals. Only selected historical stock-period observations have dated accounting fields; a carry-forward accounting value is not a distinct company filing.

An additional data inventory from a different stock cohort is preserved in [historical panel coverage](../results/historical_panel_coverage.csv), but its stock counts should **not** be merged with the 31-stock portfolio evaluation. The coverage plot below shows a composition discontinuity reflecting data availability, not market-wide listings.

![Historical panel coverage](../figures/historical_panel_coverage.png)

![Universe coverage](../figures/universe_coverage.png)

## Reconciliation and point-in-time limitations

Some cached price sources differed marginally in adjustment or representation. Selecting a consistent series reduces accidental mixing but does not certify adjustment correctness. Historical delistings, company filings, security master completeness, effective timestamps and exchange eligibility are not fully reconstructed.

Published CSVs are aggregate-only and do not provide vendor data, ticker-level return histories or feature vectors. [Limitations](limitations.md) apply to every reported result.
