"""Reproducible aggregate-data dynamic portfolio charts; no private algorithms or holdings."""
from pathlib import Path
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import chart_style as cs
cs.apply()
ROOT=Path(__file__).resolve().parents[1]
D=pd.read_csv(ROOT/'results'/'selected_dynamic_model_summary.csv')
FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
FEATURES=['hierarchical_state_space','quality_lowrank_kalman']
NAMES={'hierarchical_state_space':'Hierarchical state-space','quality_lowrank_kalman':'Quality low-rank Kalman','kalman':'Kalman filter','pooled_ridge':'Pooled ridge','ridge_arx':'ARX','mean':'Historical-mean control','spy':'SPY','spy_tbill':'SPY/T-bills','tbill':'Treasury bills'}
COLORS={'hierarchical_state_space':cs.STATE_SPACE,'quality_lowrank_kalman':cs.KALMAN,'mean':cs.CONTROL,'spy':cs.SPY,'spy_tbill':cs.SPY_TBILL,'tbill':cs.TBILL}
def save(fig,name):
 fig.tight_layout();fig.savefig(FIG/name,dpi=160,bbox_inches='tight');plt.close(fig)
def main():
 # portfolio performance: honest historical ranks within each mandate
 fig,axes=plt.subplots(2,3,figsize=(15,8.2),sharex=True)
 for i,rep in enumerate(['Grouped','Hierarchical']):
  for j,man in enumerate(['Growth','Balanced','Defensive']):
   ax=axes[i,j];q=D[(D.representation==rep)&(D.mandate==man)].sort_values('ending_wealth',ascending=False)
   ax.barh([NAMES[n] for n in q.model],q.ending_wealth,color=[COLORS[n] for n in q.model],height=.62)
   ax.invert_yaxis();ax.set_title(f'{rep} · {man}')
   ax.axvline(10000,ls=':',lw=.9,color=cs.AXIS);ax.grid(axis='x');ax.set_axisbelow(True)
   ax.spines['left'].set_visible(False)
   ax.set_xlim(0,25000);ax.set_xticks([0,10000,20000],['0','10k','20k'])
   for y,v in enumerate(q.ending_wealth):ax.text(v+250,y,f'{v:,.0f}',va='center',fontsize=8.5,color=cs.INK_2)
 fig.suptitle('Dynamic Phase 2 candidates versus passive benchmarks and historical-mean control',fontsize=15)
 fig.supxlabel('Modelled net ending wealth · 36 OOS months · initial 10,000 · rankings are historical')
 save(fig,'figure18_dynamic_model_ranked_wealth.png')
 # selected growth scatter: report metrics directly, NOT a volatility proxy
 fig,axes=plt.subplots(1,2,figsize=(14,5.5))
 for ax,rep in zip(axes,['Grouped','Hierarchical']):
  q=D[(D.representation==rep)&(D.mandate=='Growth')]
  for r in q.itertuples():
   ax.scatter(r.sharpe,r.net_cagr*100,s=95,color=COLORS[r.model],label=NAMES[r.model])
   if r.model in FEATURES or r.model in ['spy','mean']:
    ax.annotate(NAMES[r.model].replace('Hierarchical ','Hier. ').replace('Quality low-rank ','Low-rank '),(r.sharpe,r.net_cagr*100),xytext=(4,5),textcoords='offset points',fontsize=7)
  ax.set_title(f'{rep} Growth');ax.set_xlabel('Reported excess-return Sharpe');ax.set_ylabel('Net CAGR (%)');ax.grid(alpha=.16)
 fig.suptitle('Return versus risk-adjusted return: selected dynamic models',fontsize=15)
 save(fig,'figure19_dynamic_growth_cagr_sharpe_scatter.png')
 # model return advantage vs historical mean, 6 mandates
 fig,ax=plt.subplots(figsize=(12,6))
 q=D[D.model.isin(FEATURES)].copy(); baseline=D[D.model=='mean'][['representation','mandate','ending_wealth']].rename(columns={'ending_wealth':'baseline'})
 q=q.merge(baseline,on=['representation','mandate']);q['lift']=q.ending_wealth-q.baseline
 q['key']=q.representation.str[0]+' / '+q.mandate
 keys=['G / Growth','H / Growth','G / Balanced','H / Balanced','G / Defensive','H / Defensive']
 x=np.arange(len(keys));width=.32
 for k,mod in enumerate(FEATURES):
  z=q[q.model==mod].set_index('key').loc[keys];vals=z.lift.to_numpy()
  ax.bar(x+(k-(len(FEATURES)-1)/2)*width,vals,width=width,label=NAMES[mod],color=COLORS[mod])
 ax.set_xticks(x,keys);ax.axhline(0,c=cs.INK_2,lw=.8);ax.grid(axis='y');ax.set_axisbelow(True)
 ax.set_ylabel('Difference in ending wealth vs historical-mean coefficient control')
 ax.set_title('Do temporal coefficient forecasts help? Mixed results across mandates');ax.legend(ncol=3,frameon=False,fontsize=8)
 save(fig,'figure20_dynamic_vs_historical_mean.png')
 # drawdown risk versus CAGR, negative signs preserved
 fig,ax=plt.subplots(figsize=(11,6))
 q=D[(D.representation=='Grouped') & D.model.isin(FEATURES+['mean','spy','spy_tbill'])]
 for r in q.itertuples():
  ax.scatter(-r.max_drawdown*100,r.net_cagr*100,s=85,color=COLORS[r.model])
  ax.annotate(f'{NAMES[r.model]} ({r.mandate[0]})',(-r.max_drawdown*100,r.net_cagr*100),xytext=(4,4),textcoords='offset points',fontsize=7)
 ax.set_xlabel('Historical maximum drawdown magnitude (%) · smaller is better');ax.set_ylabel('Net CAGR (%) · higher is better')
 ax.set_title('Return–drawdown trade-offs · Grouped representation');ax.grid(alpha=.17)
 save(fig,'figure21_dynamic_cagr_drawdown_scatter.png')
 print('Generated verified aggregate model comparison figures 18–21.')
if __name__=='__main__':main()
