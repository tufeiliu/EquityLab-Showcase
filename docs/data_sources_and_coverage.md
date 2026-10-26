# Data sources, provenance and coverage

**Status: exploratory; not a publishable market-data release.** This document describes the research assets at a high level and aggregates from earlier local audit outputs. The private underlying datasets, exact model features and proprietary optimisation implementations are not included.

## Sources and what they supply

| Data family | Sources / context | Intended role | Verification status |
| --- | --- | --- | --- |
| Daily equity prices | Cached provider-adjusted OHLCV/price histories, including Tiingo-based files and other local price-provider exports | Historical return endpoints; momentum, realised volatility, beta and drawdown | Selected one consistent series per ticker; adjustment/corporate action coverage not independently certified |
| SPY benchmark | Local historical SPY adjusted-price series (Tiingo-labelled in previous audit) | Same-period comparison against portfolios | Endpoint matching was implemented, but USD/GBP currency treatment is not a complete execution model |
| Accounting information | Historical company financial records/SEC-oriented acquisition and dated feature exports | Operating margin, revenue growth, net margin, net-income growth where dated records exist | Availability-date handling is reported, but full per-company filing and amendment certification is not established |
| Sector/security metadata | Existing local reference exports, partly conflicting | Descriptive sectors and universe coverage auditing | Conflicting sector labels remain; historical membership not certified |
| Macro context | FRED/ALFRED acquisition infrastructure exists in the wider private project | Potential research inputs | **Not established as a fitted input in the reported portfolio comparison** |

Provider labels describe the existing research context. They do not establish that every record or returned adjustment has been independently checked or that every provider was used in every fitted model.

## Two different stock cohorts

**The current daily adjusted-price experiment:** 31 candidate stock tickers; 74,592 price rows drawn from 36 source files/series, spanning 2005-01-03 to 2026-10-23 in aggregate. Not every ticker has that full range. Four minor source differences were reported by the dry run. The selected candidate universe is not certified point-in-time or delisting-complete.

**The older quarterly factor panel:** 113 stocks across 903 stock-period rows on 23 quarterly dates. The number of represented companies increases from 8 before 2024 to about 111 around 2024 Q1. This reflects changed data coverage, **not** an observed change in the total investable market. Neither the older cohort nor the newer one is a certified historical universe.

![Earlier panel data availability](../figures/historical_panel_coverage.png)

## Monthly and quarterly evaluation

![Candidate, evaluated and invalid intervals](../figures/evaluation_interval_summary.png)

| Field | Monthly | Quarterly |
| --- | ---: | ---: |
| Candidate intervals | 95 | 31 |
| Evaluated intervals | 77 | 21 |
| Invalid intervals | 12 | 4 |
| Joined accounting feature values | 1,356 | 446 |

The 77 and 21 evaluated holding intervals cover different calendar windows (July 2019–December 2025 and September 2020–December 2025 respectively). Candidate, evaluated and invalid categories **do not necessarily partition the total** because early windows may lack sufficient training history or satisfy other exclusion logic. Do not calculate a fake success rate by subtracting these counts.

![Reported accounting joins](../figures/accounting_join_summary.png)

An accounting join is a **feature value joined to a decision-date row**, not a new independent financial statement. A previously available filing value can legitimately be carried into later decisions. The 1,356/446 counts do not show the number of distinct reporting events, reliable contemporary cross-sectional coverage or incremental predictive power. Earlier selected-portfolio diagnostics found considerably lower financial indicator coverage than market-signal coverage.

## Data integrity and audit results

- A reconciliation check reported four minor price-source differences across cached series; selecting a single source prevents accidental within-ticker vendor mixing, but does not validate every adjustment.
- The older panel had **six extreme return labels** that could not be independently reconstructed from compatible cached adjusted-price files. This is an unresolved verification problem, not evidence that those six returns are false.
- Historical delistings, listing membership, capital actions, filing timestamps and security master completeness remain uncertified; survivor-selection bias could be material.
- Full data are not redistributed because of licence/privacy considerations and to protect proprietary research inputs. The public `results/data_inventory_summary.csv` and `results/historical_panel_coverage.csv` contain only safe aggregated information.

## Processing at a high level

1. Inventory cached raw price, benchmark and financial sources.
2. Reconcile duplicate series and select one consistent adjusted-price history per ticker; audit conflicts.
3. Construct decision-date market features using historical price windows; join dated accounting information only when available at that decision time.
4. Define next-period holding returns with matched stock/SPY endpoints; reject/flag problematic intervals.
5. Fit historical-only regression controls and jointly learned allocation policies; evaluate subsequent periods under explicit constraints and cost assumptions.
6. Publish **only aggregate**, carefully labelled presentation charts and tables. Private code and files are not needed to view these exports.

## What remains unknown

The public materials do **not** prove that the stock cohort is representative, that every financial observation was publication-date verified, that stock returns are independently corporate-action certified, or that apparent net outperformance generalises. They do not permit reproduction of the private backtest. See [Limitations](limitations.md).
