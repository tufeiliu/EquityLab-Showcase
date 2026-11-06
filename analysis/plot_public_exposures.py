"""Graph approximate public allocation percentages (do not infer absent classifications)."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]

def main():
    src=ROOT/'results/public_monthly_asset_class_mix_approx.csv'
    if not src.is_file():
        print('Optional monthly asset-class mix not released.');return
    d=pd.read_csv(src)
    fig,axs=plt.subplots(2,3,figsize=(16,8),sharey=True)
    categories=[('equity','Equity','#2563eb'),('fixed_income','Fixed income','#64748b'),
                ('cash','Cash / T-bills','#0f766e'),('alternatives','Other assets','#b45309'),
                ('unclassified','Unclassified','#d1d5db')]
    for i,rep in enumerate(['Grouped','Hierarchical']):
        for j,mand in enumerate(['Growth','Balanced','Defensive']):
            ax=axs[i,j]
            t=d[(d.representation==rep)&(d.mandate==mand)].sort_values('decision_month')
            if len(t)!=36:raise ValueError(f'Missing exposure months: {rep}/{mand}')
            y=np.array([t[c+'_pct_approx'].to_numpy(float) for c,_,_ in categories])
            # Rounded components may total 95 or 105; display as lines, not a false 100% stacked chart.
            for (cat,label,col),line in zip(categories,y):
                ax.plot(np.arange(len(t)),line,label=label,color=col,lw=1.7,alpha=.9)
            ax.set_title(f'{rep} / {mand}');ax.set_ylim(0,105);ax.grid(alpha=.12)
            ax.set_xlim(0,35);ax.set_xticks([0,6,12,18,24,30,35]);ax.set_xlabel('Decision month index')
    axs[0,0].set_ylabel('Approximate allocation (%)');axs[1,0].set_ylabel('Approximate allocation (%)')
    handles,labels=axs[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',ncol=5,frameon=False)
    fig.suptitle('Asset-class composition over time | 5-point rounded, classified tickers only',fontsize=14)
    fig.text(.5,.035,'Unclassified includes unknown instruments and any unrepresented account weight. Totals may differ from 100% due to independent rounding.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.08,1,.96])
    out=ROOT/'figures/figure16_asset_class_evolution.png';fig.savefig(out,dpi=175,bbox_inches='tight');plt.close(fig)
    readme=ROOT/'README.md';text=readme.read_text();a='<!-- ALLOCATION_CHARTS_START -->';b='<!-- ALLOCATION_CHARTS_END -->'
    if a not in text or b not in text:raise ValueError('README allocation anchors missing')
    content='\n\n![Coarse monthly equity, fixed-income, cash, alternative and unclassified allocation](figures/figure16_asset_class_evolution.png)\n\n*Approximate, five-percentage-point-rounded class allocations for the six selected static EquityLab portfolios. Unknown symbols and weights not explicitly represented in the holdings export are **unclassified**, not automatically labelled cash. Chart is descriptive, not a causal explanation for benchmark performance.*\n\n'
    readme.write_text(text[:text.index(a)+len(a)]+content+text[text.index(b):])
    print('WROTE',out)
if __name__=='__main__':main()
