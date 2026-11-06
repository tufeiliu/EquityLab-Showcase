# Selected findings

All figures are modelled net results from 36 monthly decisions. The [README](../README.md) has the full tables.

## Dynamic models against MPT

The hierarchical state-space and quality low-rank Kalman models ended above both conventional MPT variants in every configuration. This is the main goal of the project, and the result is encouraging, but it is not risk-adjusted: the dynamic portfolios were more volatile than MPT in all 36 comparisons, including those against MPT matched to the control's risk.

Against MPT matched to the control's risk, the models finished ahead in 10 of 12 comparisons and lost both in Hierarchical Growth. Against MPT matched to each model's own risk, which is the like-for-like test, they finished ahead in 8 of 9 complete comparisons and had the higher Sharpe in 5 of 9. No gap is clearly above zero.

## Passive benchmarks

Beating passive investing would be a bonus. SPY is the fair comparison for Growth, and the SPY/T-bill blend is the fair comparison for Balanced and Defensive.

- **Growth:** both models beat SPY in Grouped, and neither did in Hierarchical.
- **Balanced:** neither model beat the blend in either representation.
- **Defensive:** both models beat the blend in Hierarchical, and neither did in Grouped.

After adjusting for SPY exposure, none of the 12 dynamic results has a 95% interval above zero.

## Removing NVDA

Rerunning the whole pipeline without NVDA gives two opposite results. Against MPT the models hold up, finishing ahead in 11 of 11 complete own-risk comparisons. Against passive benchmarks they fall from 4 of 12 to 0 of 12, and Grouped Growth state-space drops from 21,175 to 14,784. The Growth lead over SPY depended on one stock.

## Does forecasting add value?

The dynamic models beat the non-dynamic historical-mean control in 6 of 12 comparisons. The control itself beat both conventional MPT variants in 6 of 6 configurations, so much of the advantage over MPT may come from the framework rather than the forecasting.

## EquityLab information inside MPT

In a separate 27-month experiment, EquityLab information improved a shared MPT optimiser in 4 of 6 configurations and hurt in both Balanced configurations.

## What can be claimed

EquityLab is serious ongoing research with an encouraging result against MPT. It is not a validated source of alpha or a production strategy. The main open questions are the fixed [asset universe](../README.md#asset-universe), statistical strength against risk-matched MPT, and model selection made with hindsight.
