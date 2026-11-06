"""Charts for the full pipeline rerun without NVDA, from released portfolio-level results."""
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as cs
cs.apply()

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT/'figures'
STATE, KALMAN = 'EL / Hierarchical state-space', 'EL / Quality low-rank Kalman'
REPS = ['Grouped', 'Hierarchical']
MANDATES = ['Growth', 'Balanced', 'Defensive']
BARS = {STATE: ('Hierarchical state-space', cs.STATE_SPACE), KALMAN: ('Quality low-rank Kalman', cs.KALMAN),
        'EquityLab': ('Historical-mean control', cs.CONTROL), 'SPY': ('SPY', cs.SPY),
        'SPY / T-bills': ('SPY/T-bills', cs.SPY_TBILL), 'Ex-ante-matched MPT': ('MPT ex-ante matched†', cs.MPT_MATCHED),
        'Plain MPT': ('MPT historical', cs.MPT_MEAN), 'Corrected MPT': ('MPT shrinkage', cs.MPT_SHRINK),
        'T-bills': ('T-bills', cs.TBILL)}
LINES = [(STATE, '-', 2.4), (KALMAN, '-', 2.4), ('SPY', '--', 2.4), ('EquityLab', '-.', 1.6),
         ('Ex-ante-matched MPT', '--', 1.6), ('T-bills', ':', 1.6)]


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG/name, dpi=175, bbox_inches='tight')
    plt.close(fig)


def ranked(monthly):
    final = monthly.sort_values('period_end').groupby(['representation', 'mandate', 'strategy']).wealth_end.last()
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.8), sharex=True)
    for i, rep in enumerate(REPS):
        for j, mandate in enumerate(MANDATES):
            ax = axes[i, j]
            q = final.loc[(rep, mandate)].sort_values(ascending=False)
            ax.barh([BARS[s][0] for s in q.index], q.values, color=[BARS[s][1] for s in q.index], height=.66)
            ax.invert_yaxis()
            ax.set_title(f'{rep} · {mandate}')
            ax.axvline(10000, ls=':', lw=.9, color=cs.AXIS)
            ax.grid(axis='x')
            ax.set_axisbelow(True)
            ax.spines['left'].set_visible(False)
            ax.set_xlim(0, 22000)
            ax.set_xticks([0, 10000, 20000], ['0', '10k', '20k'])
            for y, v in enumerate(q.values):
                ax.text(v+250, y, f'{v:,.0f}', va='center', fontsize=8.5, color=cs.INK_2)
    fig.suptitle('Without NVDA: dynamic models, control, MPT and benchmarks')
    fig.supxlabel('Modelled net ending wealth · 43 instruments · 36 OOS months · initial 10,000')
    save(fig, 'figure22_without_nvda_ranked_wealth.png')


def growth_paths(monthly):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), sharey=True)
    for ax, rep in zip(axes, REPS):
        sub = monthly[(monthly.representation == rep) & (monthly.mandate == 'Growth')]
        for name, style, width in LINES:
            s = sub[sub.strategy == name].sort_values('period_end')
            dates = pd.to_datetime([s.period_end.iloc[0]-pd.offsets.MonthEnd(), *s.period_end])
            colour = BARS[name][1]
            ax.plot(dates, np.r_[10000., s.wealth_end.to_numpy(float)], color=colour, ls=style, lw=width,
                    label=BARS[name][0])
        ax.set_title(f'{rep} / Growth')
        ax.grid(axis='y')
        ax.set_axisbelow(True)
    axes[0].set_ylabel('Modelled net wealth (initial 10,000 units)')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncol=6, loc='lower center')
    fig.suptitle('Without NVDA: Growth wealth over 36 months')
    fig.tight_layout(rect=(0, .07, 1, 1))
    fig.savefig(FIG/'figure23_without_nvda_growth_wealth.png', dpi=175, bbox_inches='tight')
    plt.close(fig)


def labels(frame):
    short = {STATE: 'State-space', KALMAN: 'Kalman'}
    return frame.representation+' / '+frame.mandate+' · '+frame.model.map(short)


def wealth_effect(robust):
    w = robust.pivot_table(index=['representation', 'mandate', 'model'], columns='universe', values='ending_wealth').reset_index()
    order = {m: i for i, m in enumerate(MANDATES)}
    w = w.sort_values(['representation', 'mandate', 'model'], key=lambda c: c.map(order) if c.name == 'mandate' else c).reset_index(drop=True)
    y = np.arange(len(w))
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.hlines(y, w.without_nvda, w.with_nvda, color=cs.GRID, lw=2.5, zorder=1)
    ax.scatter(w.with_nvda, y, s=60, color=cs.MPT_MEAN, label='With NVDA', zorder=3)
    ax.scatter(w.without_nvda, y, s=60, color=cs.STATE_SPACE, marker='s', label='Without NVDA', zorder=3)
    ax.axvline(18516.05, ls='--', lw=1, color=cs.SPY, label='SPY')
    ax.set_yticks(y, labels(w))
    ax.invert_yaxis()
    ax.set_xlabel('Modelled net ending wealth (initial 10,000 units)')
    ax.set_title('Effect of removing NVDA on the dynamic models')
    ax.grid(axis='x')
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc='lower right')
    save(fig, 'figure24_nvda_effect_on_wealth.png')


def own_risk_lead(robust):
    r = robust.assign(lead=robust.ending_wealth-robust.own_risk_mpt_wealth)
    w = r.pivot_table(index=['representation', 'mandate', 'model'], columns='universe', values='lead', dropna=False).reset_index()
    order = {m: i for i, m in enumerate(MANDATES)}
    w = w.sort_values(['representation', 'mandate', 'model'], key=lambda c: c.map(order) if c.name == 'mandate' else c).reset_index(drop=True)
    y = np.arange(len(w))
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    ax.barh(y-.19, w.with_nvda, height=.36, color=cs.MPT_MEAN, label='With NVDA')
    ax.barh(y+.19, w.without_nvda, height=.36, color=cs.STATE_SPACE, label='Without NVDA')
    ax.axvline(0, color=cs.INK_2, lw=.8)
    for k, row in w.iterrows():
        for offset, value in ((-.19, row.with_nvda), (.19, row.without_nvda)):
            if pd.isna(value):
                ax.text(30, k+offset, 'incomplete', va='center', fontsize=7.5, color=cs.INK_2)
    ax.set_yticks(y, labels(w))
    ax.invert_yaxis()
    ax.set_xlabel('Dynamic model minus MPT matched to its own risk: ending wealth (units)')
    ax.set_title('Lead over own-risk MPT, with and without NVDA')
    ax.grid(axis='x')
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc='lower right')
    save(fig, 'figure25_own_risk_mpt_lead.png')


def main():
    monthly = pd.read_csv(ROOT/'results/without_nvda_monthly_net_wealth.csv', parse_dates=['period_end'])
    robust = pd.read_csv(ROOT/'results/nvda_and_own_risk_robustness.csv')
    ranked(monthly)
    growth_paths(monthly)
    wealth_effect(robust)
    own_risk_lead(robust)
    print('Generated four without-NVDA figures.')


if __name__ == '__main__':
    main()
