"""Exploratory statistical tests of H1, H2 and H3 from released portfolio-level results.

Inputs (all in results/):
- selected_monthly_net_wealth.csv: 36 dated monthly net returns per strategy (H1, H2).
- nvda_and_own_risk_robustness.csv: paired HAC t-statistics against MPT matched to each
  dynamic model's own estimated risk (the direct H1 test). Monthly own-risk MPT returns
  are not released, so this family has t-statistics and p-values but no bootstrap intervals.
- h3_paired_monthly_net_returns.csv: 27 dated monthly net returns for the H3 experiment.

Every paired test uses the same dated months for both strategies. Nothing is interpolated
or rebuilt from ending wealth. The featured dynamic models were chosen after seeing these
results, so all p-values are exploratory.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'
DYNAMIC = ('EL / Hierarchical state-space', 'EL / Quality low-rank Kalman')
CONTROL = 'EquityLab'  # Identifier in the released CSV; displayed as the historical-mean control.
MPT = {'Plain MPT': 'MPT / Historical mean', 'Corrected MPT': 'MPT / Shrinkage'}
SPY = 'SPY'
TBILL = 'T-bills'
HYBRID, CONVENTIONAL = 'Hybrid MPT', 'Conventional MPT'
REQUIRED = {'representation', 'mandate', 'strategy', 'period_end', 'net_return'}

# Each family is Holm-corrected on its own. Order sets the report order.
FAMILIES = {
    'H1 own-risk MPT': ('H1', 'Dynamic model vs MPT matched to its own estimated risk. The direct H1 test.'),
    'H1 conventional MPT': ('H1', 'Dynamic model vs conventional MPT, not risk-matched.'),
    'H2 forecasting': ('H2', 'Dynamic model vs the historical-mean control: the contribution of forecasting.'),
    'H3 information in MPT': ('H3', 'One MPT optimiser with EquityLab-derived vs conventional inputs.'),
}


def read_monthly(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f'Missing monthly returns: {path}')
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f'{path}: missing columns {sorted(missing)}')
    df = df.copy()
    df['period_end'] = pd.to_datetime(df['period_end'], errors='raise')
    df['net_return'] = pd.to_numeric(df['net_return'], errors='raise')
    if not np.isfinite(df['net_return'].to_numpy(float)).all():
        raise ValueError(f'{path}: non-finite net returns')
    if (df['net_return'] <= -1).any():
        raise ValueError(f'{path}: net returns at or below -100%')
    keys = ['representation', 'mandate', 'strategy', 'period_end']
    if df.duplicated(keys).any():
        raise ValueError(f'{path}: duplicate strategy/month rows')
    return df.sort_values(keys).reset_index(drop=True)


def panel_for(df: pd.DataFrame, rep: str, mandate: str, needed: tuple[str, ...], expected: int) -> pd.DataFrame:
    """Wide month x strategy panel; fails unless every strategy has the same `expected` months."""
    subset = df[(df.representation == rep) & (df.mandate == mandate) & df.strategy.isin(needed)]
    wide = subset.pivot(index='period_end', columns='strategy', values='net_return').sort_index()
    missing = sorted(set(needed) - set(wide.columns))
    if missing:
        raise ValueError(f'{rep}/{mandate}: missing strategies: {missing}')
    if len(wide) != expected or wide[list(needed)].isna().any().any():
        raise ValueError(f'{rep}/{mandate}: not a complete common {expected}-month panel (rows={len(wide)})')
    return wide.loc[:, list(needed)]


def hac_intercept(y: np.ndarray, x: np.ndarray | None = None, lags: int = 3) -> tuple[float, float, float]:
    """OLS intercept, its Newey-West standard error, and the slope (NaN if intercept-only).

    Bartlett weights with a fixed lag and the n / (n - k) small-sample correction.
    """
    y = np.asarray(y, dtype=float)
    X = np.ones((len(y), 1)) if x is None else np.column_stack((np.ones(len(y)), np.asarray(x, dtype=float)))
    n, k = X.shape
    if n <= max(k + 3, lags + 2):
        raise ValueError('Too few observations for HAC estimation')
    if np.linalg.matrix_rank(X) < k:
        raise ValueError('Rank-deficient regression')
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    scores = X * (y - X @ beta)[:, None]
    S = scores.T @ scores
    for j in range(1, min(lags, n - 2) + 1):
        C = scores[j:].T @ scores[:-j]
        S += (1 - j / (lags + 1)) * (C + C.T)
    bread = np.linalg.pinv(X.T @ X)
    cov = n / (n - k) * bread @ S @ bread
    se = math.sqrt(max(0.0, float(cov[0, 0])))
    slope = float(beta[1]) if x is not None else float('nan')
    return float(beta[0]), se, slope


def corrected_pipeline_t(t: float, n: int) -> float:
    """Apply the n / (n - 1) correction to a mean t-statistic computed without it."""
    return t * math.sqrt((n - 1) / n)


def one_sided_p(t: float) -> float:
    return float(norm.sf(t)) if np.isfinite(t) else float('nan')


def sharpe_annual(r: np.ndarray, cash: np.ndarray) -> float:
    vol = float(np.std(r, ddof=1))
    return float(np.sqrt(12) * np.mean(np.asarray(r) - np.asarray(cash)) / vol) if vol > 1e-12 else float('nan')


def circular_block_indices(n: int, block: int, rng: np.random.Generator) -> np.ndarray:
    starts = rng.integers(0, n, size=int(np.ceil(n / block)))
    return (starts[:, None] + np.arange(block)[None, :]).reshape(-1)[:n] % n


def bootstrap_effects(a: np.ndarray, b: np.ndarray, cash: np.ndarray, rng: np.random.Generator,
                      draws: int = 3000, block: int = 3) -> dict:
    """Paired circular block bootstrap: the same resampled months for both strategies and cash."""
    n = len(a)
    mean_diff = np.empty(draws)
    sharpe_diff = np.empty(draws)
    for i in range(draws):
        j = circular_block_indices(n, min(block, n), rng)
        mean_diff[i] = 12 * np.mean(a[j] - b[j])
        sharpe_diff[i] = sharpe_annual(a[j], cash[j]) - sharpe_annual(b[j], cash[j])
    lo, hi = np.quantile(mean_diff, [0.025, 0.975])
    valid = sharpe_diff[np.isfinite(sharpe_diff)]
    s_lo, s_hi = np.quantile(valid, [0.025, 0.975]) if len(valid) > 0.9 * draws else (np.nan, np.nan)
    return {'return_ci_low_annual': float(lo), 'return_ci_high_annual': float(hi),
            'sharpe_diff_ci_low': float(s_lo), 'sharpe_diff_ci_high': float(s_hi)}


def test_pair(a: np.ndarray, b: np.ndarray, cash: np.ndarray, spy: np.ndarray | None,
              rng: np.random.Generator, draws: int, block: int, lags: int) -> dict:
    a, b, cash = (np.asarray(v, dtype=float) for v in (a, b, cash))
    diff = a - b
    mu, se, _ = hac_intercept(diff, lags=lags)
    t = mu / se if se > 1e-15 else float('nan')
    result = {
        'n_months': len(a),
        'annual_mean_net_return_difference': 12 * mu,
        'annual_mean_net_return_difference_hac_se': 12 * se,
        'hac_t': t,
        'p_one_sided_exploratory': one_sided_p(t),
        'active_annual_realised_vol': float(np.std(diff, ddof=1) * np.sqrt(12)),
        'candidate_annual_realised_vol': float(np.std(a, ddof=1) * np.sqrt(12)),
        'comparator_annual_realised_vol': float(np.std(b, ddof=1) * np.sqrt(12)),
        'candidate_excess_sharpe': sharpe_annual(a, cash),
        'comparator_excess_sharpe': sharpe_annual(b, cash),
        'sharpe_difference': sharpe_annual(a, cash) - sharpe_annual(b, cash),
        'candidate_ending_wealth': float(10000 * np.prod(1 + a)),
        'comparator_ending_wealth': float(10000 * np.prod(1 + b)),
    }
    result.update(bootstrap_effects(a, b, cash, rng, draws=draws, block=block))
    if spy is not None:
        alpha, alpha_se, beta = hac_intercept(diff, np.asarray(spy) - cash, lags=lags)
        result.update(market_adjusted_active_alpha_annual=12 * alpha,
                      market_adjusted_active_alpha_hac_se_annual=12 * alpha_se,
                      market_adjusted_active_beta=beta,
                      market_adjusted_active_alpha_p_one_sided_exploratory=one_sided_p(alpha / alpha_se) if alpha_se > 1e-15 else float('nan'))
    return result


def holm_adjust(pvalues: pd.Series) -> pd.Series:
    """Holm step-down adjustment within one family; missing values stay missing."""
    valid = pvalues.dropna().sort_values()
    m = len(valid)
    out = pd.Series(np.nan, index=pvalues.index, dtype=float)
    running = 0.0
    for rank, (idx, p) in enumerate(valid.items()):
        running = max(running, min(1.0, (m - rank) * float(p)))
        out.loc[idx] = running
    return out


def own_risk_rows(robust: pd.DataFrame, n_months: int = 36) -> list[dict]:
    """Direct H1 test from released paired t-statistics (with-NVDA run, complete paths only)."""
    rows = []
    done = robust[(robust.universe == 'with_nvda') & robust.own_risk_mpt_complete.astype(bool)]
    for r in done.itertuples():
        t = corrected_pipeline_t(float(r.paired_hac_t), n_months)
        rows.append({'family': 'H1 own-risk MPT', 'representation': r.representation, 'mandate': r.mandate,
                     'candidate': r.model, 'comparator': 'MPT matched to own risk', 'n_months': n_months,
                     'hac_t': t, 'p_one_sided_exploratory': one_sided_p(t),
                     'candidate_excess_sharpe': r.model_sharpe, 'comparator_excess_sharpe': r.own_risk_mpt_sharpe,
                     'sharpe_difference': r.model_sharpe - r.own_risk_mpt_sharpe,
                     'candidate_ending_wealth': r.ending_wealth, 'comparator_ending_wealth': r.own_risk_mpt_wealth})
    return rows


def run(main_data: pd.DataFrame, hybrid_data: pd.DataFrame | None = None, robust: pd.DataFrame | None = None,
        draws: int = 3000, block: int = 3, lags: int = 3, seed: int = 20261107) -> tuple[pd.DataFrame, list[str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict] = []
    notes: list[str] = []

    if robust is not None:
        rows += own_risk_rows(robust)
        notes.append('H1 own-risk MPT: monthly own-risk MPT returns are not released, so this family uses the '
                     'released paired t-statistics (rescaled by sqrt(35/36) to match the small-sample correction) '
                     'and has no bootstrap intervals. Incomplete solver paths are excluded.')
    else:
        notes.append('H1 own-risk MPT NOT TESTED: nvda_and_own_risk_robustness.csv not supplied.')

    groups = sorted(set(zip(main_data.representation, main_data.mandate)))
    if len(groups) != 6:
        raise ValueError(f'Expected six representation/mandate groups, found {len(groups)}: {groups}')
    for rep, mandate in groups:
        w = panel_for(main_data, rep, mandate, (*DYNAMIC, CONTROL, *MPT, SPY, TBILL), 36)
        cash, spy = w[TBILL].to_numpy(), w[SPY].to_numpy()
        for candidate in DYNAMIC:
            a = w[candidate].to_numpy()
            for comparator, label in MPT.items():
                rows.append({'family': 'H1 conventional MPT', 'representation': rep, 'mandate': mandate,
                             'candidate': candidate, 'comparator': label,
                             **test_pair(a, w[comparator].to_numpy(), cash, spy, rng, draws, block, lags)})
            rows.append({'family': 'H2 forecasting', 'representation': rep, 'mandate': mandate,
                         'candidate': candidate, 'comparator': 'Historical-mean control',
                         **test_pair(a, w[CONTROL].to_numpy(), cash, spy, rng, draws, block, lags)})

    if hybrid_data is None:
        notes.append('H3 NOT TESTED: dated 27-month H3 returns not supplied.')
    else:
        h3_groups = sorted(set(zip(hybrid_data.representation, hybrid_data.mandate)))
        if len(h3_groups) != 6:
            raise ValueError(f'H3: expected six groups, found {h3_groups}')
        for rep, mandate in h3_groups:
            w = panel_for(hybrid_data, rep, mandate, (HYBRID, CONVENTIONAL, TBILL), 27)
            rows.append({'family': 'H3 information in MPT', 'representation': rep, 'mandate': mandate,
                         'candidate': HYBRID, 'comparator': CONVENTIONAL,
                         **test_pair(w[HYBRID].to_numpy(), w[CONVENTIONAL].to_numpy(), w[TBILL].to_numpy(),
                                     None, rng, draws, block, lags)})
        notes.append('H3 covers a separate 27-month window (Oct 2023 to Dec 2025); its effect sizes are not '
                     'comparable with the 36-month H1 and H2 estimates.')

    df = pd.DataFrame(rows)
    df.insert(0, 'hypothesis', df.family.map(lambda f: FAMILIES[f][0]))
    for family in FAMILIES:
        idx = df.index[df.family == family]
        if len(idx):
            df.loc[idx, 'holm_adjusted_p_within_family'] = holm_adjust(df.loc[idx, 'p_one_sided_exploratory'])
    df['family'] = pd.Categorical(df.family, categories=list(FAMILIES), ordered=True)
    df = df.sort_values(['family', 'representation', 'mandate', 'candidate'], kind='stable').reset_index(drop=True)
    df['family'] = df.family.astype(str)
    return df, notes


def fmt(value: float, spec: str) -> str:
    return '—' if not np.isfinite(value) else format(value, spec)


def write_report(df: pd.DataFrame, notes: list[str], out: Path, sources: dict[str, str | None],
                 draws: int, block: int, lags: int, seed: int) -> None:
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / 'hypothesis_tests_exploratory.csv', index=False, float_format='%.10g')
    (out / 'hypothesis_testing_provenance.json').write_text(json.dumps({
        'sources': sources, 'bootstrap_draws': draws, 'bootstrap_block_months': block,
        'hac_lags': lags, 'seed': seed, 'confirmatory': False, 'notes': notes}, indent=2) + '\n')

    lines = ['# EquityLab: exploratory hypothesis tests', '',
             '**Exploratory, not confirmatory.** The featured dynamic models were chosen after seeing these results. '
             'H1 and H2 use 36 monthly out-of-sample net returns; H3 uses 27.', '',
             '## Summary', '',
             '| Family | Tests | Raw p < 0.05 | Holm p < 0.05 | What it compares |', '|---|---:|---:|---:|---|']
    for family, (_, description) in FAMILIES.items():
        g = df[df.family == family]
        if len(g):
            lines.append(f'| {family} | {len(g)} | {int((g.p_one_sided_exploratory < .05).sum())} | '
                         f'{int((g.holm_adjusted_p_within_family < .05).sum())} | {description} |')
        else:
            lines.append(f'| {family} | 0 | — | — | NOT TESTED: input not supplied |')
    lines += ['',
              'p-values are one-sided (candidate better), from Newey–West HAC t-statistics with '
              f'{lags} lags and a normal reference. Holm correction is applied within each family. It does not '
              'correct for the earlier search across forecasting candidates.', '',
              '## All tests', '',
              'Return difference is 12 × the mean monthly paired net-return difference (arithmetic, not CAGR). '
              f'Intervals are 95% paired circular block-bootstrap percentiles ({block}-month blocks, {draws} draws).', '',
              '| Family | Representation / mandate | Model | Comparator | Return diff. / yr | 95% CI | HAC t | Sharpe diff. | Holm p |',
              '|---|---|---|---|---:|---|---:|---:|---:|']
    for r in df.itertuples():
        ci = '—' if not np.isfinite(r.return_ci_low_annual) else f'[{r.return_ci_low_annual:+.1%}, {r.return_ci_high_annual:+.1%}]'
        lines.append(f'| {r.family} | {r.representation} / {r.mandate} | {r.candidate.replace("EL / ", "")} | {r.comparator} | '
                     f'{fmt(r.annual_mean_net_return_difference, "+.1%")} | {ci} | {fmt(r.hac_t, ".2f")} | '
                     f'{fmt(r.sharpe_difference, "+.2f")} | {fmt(r.holm_adjusted_p_within_family, ".3f")} |')
    lines += ['', '## Limitations', '',
              '- A non-significant result is not evidence of equivalence.',
              '- 27 to 36 monthly observations are few; HAC and bootstrap intervals can be unstable. Check sensitivity to block length and lags.',
              '- The comparisons share market months, asset list and models, so they are strongly dependent.',
              '- Conventional MPT took less equity risk than the dynamic models, so wins in that family partly reflect risk taken. The own-risk family is the direct H1 test.',
              '- The SPY-adjusted active alpha is a one-factor diagnostic, not a multi-factor attribution.', '',
              '## Notes', '', *[f'- {n}' for n in notes], '']
    (out / 'hypothesis_testing_report.md').write_text('\n'.join(lines))


def relative(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return path.name


def optional(path: Path | None) -> Path | None:
    return path if path is not None and path.is_file() else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--monthly', type=Path, default=RESULTS / 'selected_monthly_net_wealth.csv')
    p.add_argument('--own-risk', type=Path, default=RESULTS / 'nvda_and_own_risk_robustness.csv')
    p.add_argument('--h3-monthly', type=Path, default=RESULTS / 'h3_paired_monthly_net_returns.csv')
    p.add_argument('--output-dir', type=Path, default=RESULTS / 'statistical_testing')
    p.add_argument('--draws', type=int, default=3000)
    p.add_argument('--block-months', type=int, default=3)
    p.add_argument('--hac-lags', type=int, default=3)
    p.add_argument('--seed', type=int, default=20261107)
    a = p.parse_args()
    if a.draws < 200 or a.block_months < 1 or a.hac_lags < 0:
        p.error('--draws must be >= 200, --block-months >= 1 and --hac-lags >= 0')

    own_risk, h3 = optional(a.own_risk), optional(a.h3_monthly)
    result, notes = run(read_monthly(a.monthly),
                        read_monthly(h3) if h3 else None,
                        pd.read_csv(own_risk) if own_risk else None,
                        draws=a.draws, block=a.block_months, lags=a.hac_lags, seed=a.seed)
    sources = {'monthly': relative(a.monthly), 'own_risk': relative(own_risk), 'h3_monthly': relative(h3)}
    write_report(result, notes, a.output_dir, sources, a.draws, a.block_months, a.hac_lags, a.seed)
    print(f'Wrote {len(result)} exploratory tests to {relative(a.output_dir)}')
    print(result.groupby('family', sort=False).size().to_string())


if __name__ == '__main__':
    main()
