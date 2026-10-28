# Research design and methodological controls

## Objective

Evaluate whether structured equity signals and statistical models can inform tradable portfolio construction relative to simple controls and a broad-market exchange-traded fund benchmark. The focus is economic outcomes after illustrative trading costs, with drawdown, concentration and robustness considered alongside cumulative returns.

## Information timing

For each decision period, data available at the decision cutoff are the only permissible model inputs. The realised holding-period return is a subsequent outcome, not a contemporaneously known feature. Forecast experiments use past-only chronological estimation, and the public rolling time-series experiment predicts a single next observation at each origin.

This is the **intended research timing contract**. It is not proof that each upstream financial record was independently certified as available at the historical cutoff.

## Comparators

- Broad-market SPY over matching holding-period boundaries.
- Equal weighting across the eligible sample.
- A simple ranked-stock equal-weight selection control.
- Regularised portfolio-allocation families with common budget and concentration constraints.
- Forecast-supported allocation and temporally conditioned allocation approaches, assessed descriptively in a separate matched sample.

## Portfolio measurement

Wealth is compounded from successive net holding-period returns: \(W_T=W_0\prod_{t=1}^T(1+R^{net}_t)\). Costs are modelled using estimated portfolio turnover. Reported cost rates do not represent complete slippage, taxes, capacity, currency conversion or market-impact modelling.

Metrics include matched-window terminal notional, drawdown, realised volatility, turnover and scorecards relative to SPY. Comparisons across different sample windows or underlying allocation engines are descriptive rather than causal.

## Robustness

The research investigates solver convergence, fallback use, coefficient magnitude availability, stock selection versus capital allocation, sensitivity to illustrative transaction costs, and chronological subsamples. More elaborate learning mechanisms are judged against simpler predictors and portfolio controls.

## Proprietary boundary

The exact signal construction, parameter calibration, training objective, optimiser implementation, learned policy coefficients, security-level decisions and research infrastructure remain private. Published materials disclose sufficient *evaluation logic and limitations* to support an interview discussion without releasing the investment methodology itself.

See [portfolio results](portfolio_research.md), [return modelling](returns_and_volatility.md) and [limitations](limitations.md).
