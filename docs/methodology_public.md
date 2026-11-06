
# Public methodology note

This public repository deliberately separates **what is being claimed** from **how the private engine works**.

## H1 — original system versus conventional MPT

Beating conventional MPT is the main goal. EquityLab is compared against it using the same decision calendar, the same broad investable universe concept, and the same cost-accounting convention. The public release shows two conventional baselines:

- **MPT: historical mean** uses individual trailing historical sample means as expected-return estimates.
- **MPT: shrinkage** blends each risky asset's trailing mean with a pooled risky-asset return estimate, while treating the Treasury-bill/cash input separately. Earlier code names used "corrected MPT" because this variant was introduced alongside solver and cash-accounting fixes. This is a baseline **estimator choice**, not a claim that shrinkage is universally superior.

## H2 — risk-controlled comparison

Historical return differences alone are not enough, because a higher-return strategy may simply be taking more risk. The core control in this release is the **exact ex-ante risk-matched MPT** portfolio. In that comparison, MPT is required to match the historical-mean control's estimated annual volatility at each decision point.

This target comes from the control, not the dynamic portfolios. A separate run applies the same solver to each dynamic model's own risk. Paths with solver failures are reported as incomplete.

## NVDA robustness

The full Phase 1 and Phase 2 pipeline was rerun on the same code with NVDA removed from the input, leaving 43 instruments, so the coefficients do not carry information learned from it.

## H3 — hybrid extension

The hybrid test asks a different question: if the allocation engine is held common, can EquityLab-derived information still improve an MPT-style optimiser?

This is a secondary extension. It is not used as the main evidence for EquityLab-versus-MPT.

## Asset universe

The 36-month evaluation uses a fixed list of 44 instruments: 31 large-cap US stocks, 11 US sector ETFs, SPY and one Treasury-bill instrument. The stocks were chosen by hand as a pilot sample across sectors, limited by free public data, and membership is not verified as point-in-time. See [Asset universe](../README.md#asset-universe) for why this matters.

## What is intentionally not public

The public repository does not disclose:

- coefficient-identification logic,
- signal-generation formulas,
- detailed optimiser structure,
- tuned parameters,
- the named universe list and historical stock-level weights,
- security-level score histories,
- full research data.

The released code is purely for **auditing the published aggregate evidence**.
