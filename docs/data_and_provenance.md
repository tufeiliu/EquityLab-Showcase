# Data and provenance — public research disclosure

**Status: ongoing and partly unverified.** This document intentionally separates known functions of data from provider-level assertions that have not been independently confirmed.

## Information flow

1. **Point-in-time decision calendar:** month-end or scheduled portfolio decisions. Information must be available **before the investment decision**, not merely appear in an updated historical dataset.
2. **Investable universe:** a fixed list of 44 instruments (31 large-cap US stocks, 11 US sector ETFs, SPY and one Treasury-bill instrument), available at all 36 decisions. The stocks are a hand-picked pilot sample of large US companies across the 11 sectors, limited by what free public data was available. Membership is not verified as point-in-time, so survivorship bias has not been ruled out. The named list is not published. See [Asset universe](../README.md#asset-universe).
3. **Market prices / return panel:** supplies trailing return history and subsequently realised instrument returns. Missing quotes, delistings, distributions, adjustments and corporate actions may affect historical credibility and must be audited.
4. **Cash / Treasury-bill proxy:** supplies risk-free returns and a simple market-plus-cash benchmark. Instrument conventions and alignment need verification.
5. **Economic/macroeconomic series and any dated fundamentals:** sources of potential predictive information in private work. Data revisions, public release timestamps and vintage alignment need further verification.
6. **Execution ledger:** sequential wealth, hypothetical costs, turnover and benchmark comparison. This is modelled P&L, not live broker-account results.

## Scope and limitations

- H1/H2: **36 monthly observations**, three mandates and overlapping representations. Results are strongly dependent and not independent replications.
- H3: **27 monthly observations**, with a common allocator but differing information sources. Do not compare its terminal values directly with the 36-month study.
- **Provider and licensing audit incomplete:** the published portfolio summaries are derived from the private dataset, and this repository deliberately does not claim that every raw input has independently established provider, timestamp or redistribution rights.
- **PIT limitations:** the private run used an explicit unverified point-in-time override. This is an exploratory research result, not a certified leakage-free institutional dataset.
- **Currency and FX:** archived currency labels are illustrative, and historical FX conversion is not fully independently verified. No claim of audited GBP wealth.
- **Benchmark assumptions:** SPY, T-bill proxy and mandate-adjusted blends are separate comparisons; no claim they share EquityLab's exact ex-ante or realised volatility.
- **Slippage and capacity:** costs are modelled. Fill constraints, borrow, capacity, market impact and live fees need further testing.
- **Security snapshots:** optional snapshots are a limited set of publicly chosen disclosures, not a complete holdings history. Ranks and membership depend on a 0.5% materiality threshold.

This document should be updated with exact providers, licences, version hashes, release lags, sample coverage and treatment of revised macro data **once verified**. Do not fill missing provider details with assumptions.

## Proposed future data family — news/event logs

Historical news and corporate/event text **has not been included in these public backtest results**. A future phase may use licensed logs with original issue and revision timestamps to derive structured event features using an LLM. News source rights, time-zone normalization, dissemination latency, revisions, entity linking and hindsight leakage must all be audited before such features are eligible for testing. See [future research roadmap](future_research_roadmap.md).
