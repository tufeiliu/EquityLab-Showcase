# Research questions, benchmarks and chart terminology

The three hypotheses ask **different questions**. A good performance result in one experiment is not automatically evidence for the others.

| Question | In plain English | Appropriate comparison | Current status |
|---|---|---|---|
| **H1 — Complete system** | Does the **intended dynamic Phase 2 EquityLab strategy** produce better net investment outcomes than conventional MPT, after accounting for realised risk? | Pre-specified dynamic forecasting policy versus conventional MPT, with consistent dates, costs, universe and risk analysis | **Promising, not established.** Dynamic models mostly lead MPT matched to their own risk without a statistically clear gap. The archived complete ex-ante-matched MPT runs are matched to the historical-mean **control**, not to the dynamic models. |
| **H2 — Why does it work (or not)?** | Are differences caused by forecasting changing coefficients, asset choices, allocation, or equity-market exposure? | Dynamic Phase 2 candidates versus the **historical-mean coefficient control**; matched-equity and matched-risk diagnostic variants | **Exploratory comparisons completed**, but causal attribution is incomplete. |
| **H3 — Can the information help MPT?** | If we keep an MPT allocation engine, can EquityLab-derived information improve its decisions? | Same MPT engine, different information inputs | **Separate, 27-month hybrid experiment**; mixed findings. Not the complete EquityLab strategy. |

**Phase 1** identifies historical economic coefficient structure. **Phase 2** forecasts how those coefficients evolve over time and uses the predictions in portfolio decisions. **Historical mean** means the average-coefficient *control*; it is not the proposed dynamic Phase 2 system. Dynamic candidates are shown separately by forecasting method, and any asterisk indicates **retrospective selection for presentation**, not a prospectively certified winner.

## Chart legend and benchmark glossary

| Label you may see | Meaning | How to interpret it |
|---|---|---|
| **EL / Hierarchical state-space\*** | EquityLab using a hierarchical dynamic state-space coefficient forecast | Selected dynamic Phase 2 candidate; exploratory result. |
| **EL / Quality low-rank Kalman\*** | EquityLab using a dynamic Kalman-style, low-rank, quality-adjusted forecast | Different temporal forecasting assumption; exploratory. |
| **EL / Historical-mean coefficient control** | EquityLab allocation fed by historical-average coefficients (`mean`) | **Non-dynamic baseline/ablation**, not the intended Phase 2 system. Previously labelled simply “EquityLab” or “static EquityLab”. |
| **SPY** | S&P 500-tracking exchange-traded fund, used as a US equity-market proxy | A fully equity-exposed passive comparator. Fair for Growth, and too risky a yardstick for Balanced or Defensive. |
| **T-bills** | Short-term US Treasury-bill return proxy | Cash-like, low-risk reference and excess-return benchmark, not literally zero-risk in every currency. |
| **SPY / T-bills** | Simple mandate-adjusted combination of SPY and the T-bill proxy | The fair passive comparison for Balanced and Defensive; **not** an EquityLab strategy. |
| **MPT / Historical mean** (formerly **Plain MPT**) | Mean–variance portfolio optimiser using historically estimated asset-return means | Independent conventional MPT comparator; no EquityLab coefficients. |
| **MPT / Shrinkage** (formerly **Corrected MPT**) | Conventional MPT with more regularised estimates of expected returns and implementation fixes versus an earlier solver | “Corrected” describes the legacy implementation; not a new theoretical version of MPT. |
| **MPT / Ex-ante risk-matched** | Diagnostic MPT constrained to match the **historical-mean EquityLab control's decision-time estimated volatility** | Not automatically matched to the dynamic candidates; matching forecasts does not guarantee equal realised risk. |

### How to read the graphs

**Monthly wealth line:** Each line starts at an illustrative 10,000 account units and compounds the *observed monthly net backtest returns*. Higher ending wealth means higher absolute return **for that particular risk and mandate**. These are modelled portfolio paths, not audited trading statements.  
**Drawdown line:** The percentage fall from a strategy's previous wealth peak. Values nearer **0%** mean a smaller ongoing loss from the prior high; deeper negative values mean a worse decline.  
**Sorted ending-wealth bars:** Compare final outcomes for a fixed horizon; they **do not** establish equal risk.  
**Risk–return scatter:** The x-axis is the indicated volatility or drawdown measure and the y-axis the stated return/wealth measure. **Estimated (ex-ante) risk** and **realised (ex-post) risk** are different.  
**Sharpe ratio:** Mean return above the T-bill reference, scaled by variation in excess returns. It is sensitive to the evaluation window and the chosen risk-free proxy.  
**Net:** Returns after the modelled transaction costs in the backtest; financing, market impact and data provenance have not all been independently validated.  
**Growth / Balanced / Defensive:** Separate portfolio mandates, not three stages of a single growing portfolio. Their equity and defensive allocations differ. **Grouped / Hierarchical** identify different feature representations, not time periods.

**Reading warning:** An asterisk (`*`) on a dynamic model means it was selected for this *public showcase after inspecting historical model results*. A dagger (`†`) on risk-matched MPT means its risk target comes from the historical-mean coefficient **control**. Neither mark should be interpreted as a statistically proven, independently validated investment edge.

