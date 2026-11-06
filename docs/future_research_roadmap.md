# Future research roadmap: event-aware dynamic modelling

> **Planned extension — not implemented, not tested, and not included in any reported backtest.** EquityLab is an ongoing independent research programme.

## Motivation

The current historical forecasting framework primarily uses structured market and economic information. Real markets also respond to discontinuous changes: monetary-policy announcements, corporate disclosures, geopolitical developments and unanticipated industry news. A model that extrapolates historical dynamics may react too slowly, but it is an open empirical question whether text-based event information helps.

## Planned approach (high level)

1. **Build a timestamped event archive.** Acquire appropriately licensed historical news/event logs with article identifiers, publisher, initial publication time, subsequent update times, instrument/industry coverage and ingestion delay. Deduplicate near-identical articles. Avoid inferring a historical publication date from a later scraped or revised page.
2. **Create LLM-extracted features.** Convert contemporaneously available text into structured event features: broad type, exposure scope, direction, approximate magnitude, uncertainty, novelty and relevance. Keep the output schema fixed, record model/prompt versions and audit a human-labelled sample. These are *candidate* features, not investment recommendations.
3. **Represent shocks in the forecasting system.** Compare a baseline dynamic model with one that allows lagged, date-available event measurements to act as external inputs or shock indicators. Document how stale information, missing events and low-confidence extractions are handled; do not publish the proprietary transition or coefficient-identification details.
4. **Evaluate incremental benefit.** Use chronologically nested model choice and untouched forward test windows. Run the same asset universe, rebalance calendar, costs, constraints and risk controls for news/no-news comparisons. Compare SPY, T-bills, simple SPY/T-bill mixes and conventional MPT, and report absolute and risk-adjusted returns, drawdowns, turnover, and forecast calibration.

## Validation gates

| Gate | What must be demonstrated |
|---|---|
| Timestamp integrity | Feature content existed before the decision and any realistic latency cutoff |
| Data rights | Licensed collection, retention and disclosure appropriate to each provider |
| Extraction reliability | Stable and auditable mappings; error analysis including contradictory and revised news |
| Causal comparison | News/no-news ablation holding portfolio construction and test periods fixed |
| Economic usefulness | Incremental net value over costs, with confidence intervals and failure cases |
| Robustness | No material collapse across regimes, source outages, entity ambiguity or shifted language |

## Known risks and scope

News may be priced in before a model can react; strong textual sentiment can simply proxy market momentum; event archives may contain survivorship and retrospective labeling; LLMs can hallucinate events or use knowledge acquired after publication; expensive inference can outweigh gains. Each risk needs an explicit measurement rather than a qualitative assurance.

**No news-LLM feature, identified shock effect or performance enhancement is claimed in the current public results.** The first priority remains auditing the existing market/macro/FX data and testing the present strategy prospectively. If the new extension succeeds, the public portfolio can show a dated ablation and research findings without releasing proprietary model internals or raw licensed news content.
