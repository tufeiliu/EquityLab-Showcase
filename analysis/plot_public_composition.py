"""Plot public-approved portfolio composition snapshots and membership dynamics."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import chart_style as cs
cs.apply()
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results';FIG=ROOT/'figures'

def plot():
    counts=RES/'public_asset_turnover_counts.csv'
    if not counts.exists():
        print('No portfolio-composition data in results/.')
        return False
    d=pd.read_csv(counts)
    needed={'representation','mandate','decision_month','selected_asset_count','added_asset_count','removed_asset_count'}
    if not needed.issubset(d):raise ValueError('Asset count CSV schema invalid')
    if d.duplicated(['representation','mandate','decision_month']).any():raise ValueError('Duplicate asset counts')
    # Six-panel with chronological dynamics for each mandate/representation
    fig,axs=plt.subplots(3,2,figsize=(13,10),sharex=False)
    for row,mand in enumerate(['Growth','Balanced','Defensive']):
        for col,rep in enumerate(['Grouped','Hierarchical']):
            ax=axs[row,col]
            z=d[d.mandate.eq(mand)&d.representation.eq(rep)].sort_values('decision_month')
            if len(z)!=36:raise ValueError(f'Incomplete {rep}/{mand} counts: {len(z)}')
            dates=pd.to_datetime(z.decision_month)
            ax.plot(dates,z.selected_asset_count,color=cs.STATE_SPACE,lw=2,label='Held assets')
            ax.set_title(f'{mand} · {rep}',fontsize=11);ax.set_ylabel('Material positions (≥0.5%)')
            ax.grid(alpha=.15);ax.tick_params(axis='x',rotation=25)
    fig.suptitle('How portfolio breadth evolves across the 36 monthly decisions',fontsize=15)
    fig.tight_layout(rect=[0,.0,1,.96]);fig.savefig(FIG/'figure11_asset_count_evolution.png',dpi=175,bbox_inches='tight');plt.close(fig)
    fig,axs=plt.subplots(3,2,figsize=(13,10))
    for row,mand in enumerate(['Growth','Balanced','Defensive']):
        for col,rep in enumerate(['Grouped','Hierarchical']):
            ax=axs[row,col]
            z=d[d.mandate.eq(mand)&d.representation.eq(rep)].sort_values('decision_month')
            x=np.arange(1,len(z))
            ax.bar(x-.18,z.added_asset_count.iloc[1:],width=.36,label='Newly included',color=cs.POSITIVE)
            ax.bar(x+.18,z.removed_asset_count.iloc[1:],width=.36,label='No longer included',color=cs.NEGATIVE)
            ax.set_title(f'{mand} · {rep}',fontsize=11);ax.set_ylabel('Ticker membership changes')
            ax.set_xlabel('Decision month index');ax.grid(axis='y',alpha=.13)
    axs[0,0].legend(fontsize=8,frameon=False)
    fig.suptitle('Position membership changes month to month (0.5% materiality cutoff)',fontsize=15)
    fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(FIG/'figure12_asset_membership_changes.png',dpi=175,bbox_inches='tight');plt.close(fig)
    snap=RES/'public_selected_ticker_snapshots.csv'; heat=RES/'public_selected_ticker_presence.csv'
    if snap.exists() and heat.exists():
        s=pd.read_csv(snap);h=pd.read_csv(heat)
        # Public-facing one featured composition: Grouped Growth, 6 snapshots
        sub=s[s.representation.eq('Grouped')&s.mandate.eq('Growth')].copy()
        if sub.empty:raise ValueError('No selected snapshots for featured portfolio')
        fig,ax=plt.subplots(figsize=(13,6.8));ax.axis('off')
        columns=[]
        for date,z in sub.groupby('decision_month',sort=True):
            names=', '.join(z.sort_values('display_rank').ticker.astype(str))
            columns.append((date,names))
        table=ax.table(cellText=[[date,names] for date,names in columns],colLabels=['Decision month','Selected tickers (unweighted, ranked)'],cellLoc='left',colLoc='left',loc='center',colWidths=[.17,.83])
        table.auto_set_font_size(False);table.set_fontsize(9);table.scale(1,2.2)
        ax.set_title('Selected holdings snapshots · Grouped Growth · 6 of 36 decisions',fontsize=14,pad=24)
        fig.savefig(FIG/'figure13_selected_ticker_snapshots.png',dpi=175,bbox_inches='tight');plt.close(fig)
        hh=h[h.representation.eq('Grouped')&h.mandate.eq('Growth')]
        z=hh.pivot(index='ticker',columns='decision_month',values='present').fillna(0)
        fig,ax=plt.subplots(figsize=(13,5.7));im=ax.imshow(z.values,aspect='auto',interpolation='nearest',vmin=0,vmax=1,cmap='Blues')
        ax.set_yticks(range(len(z.index)),z.index);xt=np.arange(0,len(z.columns),max(1,len(z.columns)//9))
        ax.set_xticks(xt,[z.columns[i] for i in xt],rotation=35,ha='right');ax.set_xlabel('Decision month')
        ax.set_title('Which disclosed assets remained in the portfolio? · Grouped Growth')
        fig.colorbar(im,ax=ax,ticks=[0,1],label='Presence (0/1)')
        fig.tight_layout();fig.savefig(FIG/'figure14_selected_ticker_presence.png',dpi=175,bbox_inches='tight');plt.close(fig)
    else:
        print('Ticker-specific figures omitted: opt-in named export not supplied.')
    rd=ROOT/'README.md'
    old=rd.read_text()
    start='<!-- COMPOSITION_FIGURES_START -->';end='<!-- COMPOSITION_FIGURES_END -->'
    if start not in old or end not in old:raise ValueError('Missing composition markers')
    inserted=(
       '![](figures/figure11_asset_count_evolution.png)\n\n'
       '*Selected portfolio breadth over time; a 0.5% minimum position size defines a material asset.*\n\n'
       '![](figures/figure12_asset_membership_changes.png)\n\n'
       '*Monthly membership additions and removals; this is NOT turnover by traded value.*\n\n'
    )
    if snap.exists() and heat.exists():
        inserted+=('![](figures/figure13_selected_ticker_snapshots.png)\n\n'
                   '*Six spaced decisions, top eight disclosed names only. No weights or scores.*\n\n'
                   '![](figures/figure14_selected_ticker_presence.png)\n\n'
                   '*Binary membership for up to twelve disclosed names; 0.5% position floor.*\n\n')
    else: inserted+='*Security names and position weights are not published.*\n\n'
    updated=old[:old.index(start)+len(start)]+'\n'+inserted+old[old.index(end):]
    rd.write_text(updated)
    return True
if __name__=='__main__':plot()
