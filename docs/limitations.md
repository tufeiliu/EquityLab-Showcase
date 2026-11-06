# Limitations and ongoing development

**EquityLab is an active research programme.** The present public release illustrates research methods and results. It is not a finished investment product, audited track record or evidence of live alpha.

## Data quality and source provenance

- The input history has not been fully certified as **point-in-time**; some publication timestamps/vintages remain unverified, and the private run explicitly permitted that status.
- Provider identities, licensing/redistribution terms, corporate-action adjustments and delisting coverage must be checked against the raw records before making institutional claims.
- Archived **FX and currency** assumptions are not independently verified, so the starting account and ending figures should be treated as illustrative units, not audited GBP performance.
- Market benchmarks rely on return-alignment and cash-proxy assumptions; all require independent review.

## Experimental validity

- H1/H2 span only **36 monthly OOS decisions** and H3 only **27**, without a long, untouched forward sample.
- The **asset universe is a hand-picked, fixed list of 44 instruments** built from free public data, not verified as point-in-time. Large companies may be included because they did well, and a few winners can drive results. Removing NVDA removes every win over the fair passive benchmark.
- Three of the 12 own-risk MPT paths are incomplete with NVDA, and one without it, because the solver failed in some months.
- Grouped, Hierarchical and mandates share a common calendar; win counts are **correlated, not independent tests**.
- Some public dynamic examples were chosen after examining candidate models and are not prospectively selected winners.
- The exact ex-ante risk equality solver is **nonconvex** and its numerical success is not proof of a globally optimal MPT portfolio.
- Matching estimated volatility does not ensure identical realised volatility, factor exposures, tail losses or drawdowns.
- Retrospective realised-volatility scaling uses future information and is **not a feasible investable backtest**.

## Economic value and implementation

- The predeclared historical-mean EquityLab model has not shown a positive advantage over the simple SPY/T-bill benchmark in the displayed Grouped mandates.
- Some configurations favour risk-matched MPT, notably Hierarchical Growth.
- Costs are estimated; real spreads, market impact, capacity, order handling, borrow and taxes are not established.
- Private code and raw data are intentionally undisclosed; the public notebook reproduces analysis **from disclosed aggregates**, not end-to-end private predictions or holdings.

## Next work (open milestones)

1. Source-level PIT and vintage audit; corporate-action and total-return reconciliation; FX conventions.
2. Independent, untouched OOS window / prospective forward evaluation and statistical sensitivity.
3. Explicit static-versus-dynamic coefficient forecast ablation with model selection frozen before evaluation.
4. Independently check optimality/feasibility of MPT variants and portfolio risk constraints.
5. Point-in-time universe membership, and robustness to removing the largest holdings.
6. Robustness to costs, investability, turnover, sector concentrations and benchmark choice.

Please interpret every released figure within these limits. The most credible current claim is **rigorous ongoing independent quantitative research**, not a validated deployable strategy.

## Market-exposure diagnostics: interpretation boundaries

A full-window, volatility-matched SPY/T-bill mix is **hindsight**, not investable. The mix is unlevered; targets outside the feasible range are flagged instead of silently rescaled. No additional financing costs, execution slippage or rebalancing are imputed to that hypothetical constant mix. A positive historical one-factor regression intercept is not proof of alpha: its meaning depends on the benchmark, estimation errors, time-varying exposures and the fact that the models were evaluated on the same historical window. With just 36 months, confidence intervals are indicative, not decisive.

The 44-instrument universe is narrow relative to SPY. Until asset-class mapping and constituent-level returns are reconciled, the Balanced underperformance cannot be attributed to universe restriction or allocation alone. Public exposure exports are rounded and not a substitute for a private holdings audit.

## Proposed news/LLM research is not current evidence

Historical news acquisition, LLM-based event extraction and the use of structured event features as potential dynamic shocks are **future work**, not components of the reported v1.4 portfolio runs. Before that extension can support investment claims it will require licensed timestamped data, event-revision handling, leakage controls, extraction audits, chronologically frozen model selection, and a genuine news-versus-no-news ablation with costs. See [future research roadmap](future_research_roadmap.md).
