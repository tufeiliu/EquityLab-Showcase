"""Reproducible publication charts from disclosed aggregate data only."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import chart_style as cs
cs.apply()
ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'
FIG.mkdir(exist_ok=True)
COL={'Historical-mean control':cs.CONTROL,'EquityLab':cs.CONTROL,'Plain MPT':cs.MPT_MEAN,'Corrected MPT':cs.MPT_SHRINK,'Risk-matched MPT':cs.MPT_MATCHED}
p=pd.read_csv(ROOT/'results'/'selected_primary_results.csv')
h=pd.read_csv(ROOT/'results'/'selected_hybrid_results.csv')
order=['Growth','Balanced','Defensive']

def save(fig,name):
    fig.tight_layout();fig.savefig(FIG/name,dpi=175,bbox_inches='tight');plt.close(fig)

def market_figures(p, b):
    # The benchmark CSV records separately audited, full-window historical results.
    # Estimated volatilities are NOT realised volatilities: titles and labels say so.
    order=['Growth','Balanced','Defensive']
    z=p[p.representation.eq('Grouped')].merge(b,on='mandate').set_index('mandate').loc[order]
    # Sorted individually within each mandate: ranks are not comparable across mandates.
    series=[('equitylab_wealth','EL / Historical-mean control',cs.CONTROL),
            ('spy_wealth','SPY',cs.SPY),
            ('spy_tbill_wealth','SPY / T-bills',cs.SPY_TBILL),
            ('tbill_wealth','T-bills',cs.TBILL),
            ('mpt_plain_wealth','MPT: historical mean',cs.MPT_MEAN),
            ('mpt_corrected_wealth','MPT: shrinkage',cs.MPT_SHRINK),
            ('mpt_exact_exante_wealth','MPT: risk matched',cs.MPT_MATCHED)]
    fig,axes=plt.subplots(1,3,figsize=(16,6.3),sharex=True)
    for ax,mandate in zip(axes,order):
        vals=sorted(((float(z.loc[mandate,key]),label,color) for key,label,color in series),reverse=True)
        yy=np.arange(len(vals))
        ax.barh(yy,[v[0] for v in vals],color=[v[2] for v in vals],height=.7)
        ax.set_yticks(yy,[v[1] for v in vals],fontsize=8)
        ax.invert_yaxis()
        ax.set_xlim(9500,20500)
        ax.set_title(f'{mandate} | descending wealth',fontsize=11)
        ax.axvline(10000,ls=':',c=cs.AXIS,lw=.9)
        ax.grid(axis='x',alpha=.14);ax.set_axisbelow(True)
        for i,(v,lab,col) in enumerate(vals):
            ax.text(v+110,i,f'{v/1000:.2f}k',va='center',fontsize=8)
    fig.suptitle('Historical-mean control versus practical benchmarks | 36 OOS months',fontsize=15,y=1.01)
    fig.supxlabel('Illustrative net ending wealth (initial 10,000)')
    save(fig,'figure01_market_benchmark_bars.png')

    # A fairer simple comparator is the mandate-adjusted SPY/T-bill benchmark.
    fig,ax=plt.subplots(figsize=(10,4.8))
    ranks=sorted(((m,float(z.loc[m,'equitylab_wealth']-z.loc[m,'spy_tbill_wealth'])) for m in order),key=lambda item:item[1],reverse=True)
    dif=np.array([r[1] for r in ranks]);labels=[r[0] for r in ranks]
    bars=ax.barh(labels,dif,color=[cs.NEGATIVE if v<0 else cs.POSITIVE for v in dif],height=.58)
    ax.invert_yaxis();ax.axvline(0,color=cs.INK_2,lw=.9)
    for bar,v in zip(bars,dif):
        ax.text(v-70 if v<0 else v+70,bar.get_y()+bar.get_height()/2,f'{v:+,.0f}',ha='right' if v<0 else 'left',va='center',fontsize=10)
    ax.set_xlim(min(dif)*1.4,700);ax.set_xlabel('Historical-mean control minus SPY/T-bills: ending wealth')
    ax.set_title('A harder baseline: simple SPY/T-bill blend beat the static EquityLab model')
    ax.grid(axis='x',alpha=.14);ax.set_axisbelow(True)
    save(fig,'figure02_against_simple_benchmark.png')

    # Estimated risk/ending wealth scatter including actual market baselines.
    fig,ax=plt.subplots(figsize=(11.8,6.4))
    pointdata=[('Historical-mean control','matched_exante_annual_vol','equitylab_wealth',cs.CONTROL,'o'),
               ('MPT: risk matched','matched_exante_annual_vol','mpt_exact_exante_wealth',cs.MPT_MATCHED,'s'),
               ('MPT: historical mean',None,'mpt_plain_wealth',cs.MPT_MEAN,'D'),
               ('SPY','spy_mean_estimated_annual_vol','spy_wealth',cs.SPY,'^'),
               ('SPY / T-bills','spy_tbill_mean_estimated_annual_vol','spy_tbill_wealth',cs.SPY_TBILL,'v'),
               ('T-bills','tbill_mean_estimated_annual_vol','tbill_wealth',cs.TBILL,'P')]
    # sample-mean MPT mean estimated volatility by mandate from v1.4 report.
    mpt_est={'Growth':.085115,'Balanced':.043270,'Defensive':.026717}
    for label,riskcol,wealthcol,color,marker in pointdata:
        xx=np.array([mpt_est[m] for m in order]) if riskcol is None else z[riskcol].to_numpy()
        yy=z[wealthcol].to_numpy()
        ax.scatter(xx*100,yy,label=label,c=color,marker=marker,s=80,zorder=3)
        for i,m in enumerate(order):
            if label in ('EquityLab','SPY / T-bills','MPT: risk matched'):
                ax.annotate(m[0],(xx[i]*100,yy[i]),xytext=(4,4),textcoords='offset points',fontsize=8)
    ax.set_xlabel('Mean decision-time estimated annual volatility (%)')
    ax.set_ylabel('Net illustrative ending wealth (initial 10,000)')
    ax.set_title('Risk exposure changes the story | Grouped')
    ax.legend(frameon=False,fontsize=8,ncol=3,loc='upper left');ax.grid(alpha=.15);ax.set_axisbelow(True)
    save(fig,'figure03_market_exante_risk_scatter.png')

    # Public two-candidate snapshot from the curated reported historical summary.
    # Both dynamic candidates are retrospectively featured; the mean control is NOT a dynamic strategy.
    model_summary=pd.read_csv(ROOT/'results'/'selected_dynamic_model_summary.csv')
    q=model_summary[(model_summary.representation=='Grouped')&(model_summary.mandate=='Growth')]
    presentation=[('hierarchical_state_space','EL / Hierarchical state-space',cs.STATE_SPACE),
                  ('quality_lowrank_kalman','EL / Quality low-rank Kalman',cs.KALMAN),
                  ('spy','SPY',cs.SPY),('mean','EL / Historical-mean control',cs.CONTROL),
                  ('tbill','Treasury-bill proxy',cs.TBILL)]
    records=[]
    for model,label,color in presentation:
        match=q[q.model.eq(model)]
        if len(match)!=1:raise ValueError(f'Missing curated model benchmark row: {model}')
        records.append((label,float(match.ending_wealth.iloc[0]),color))
    records.sort(key=lambda item:item[1],reverse=True)
    fig,ax=plt.subplots(figsize=(11.2,5.9))
    ax.barh([r[0] for r in records],[r[1] for r in records],color=[r[2] for r in records],height=.64)
    ax.invert_yaxis();ax.set_xlim(9900,24000)
    ax.set_xlabel('Modelled net ending wealth (10,000 initial units)')
    ax.set_title('Two selected dynamic models vs SPY and historical-mean control | Grouped Growth')
    ax.grid(axis='x',alpha=.16);ax.set_axisbelow(True)
    for i,(_,v,_) in enumerate(records):ax.text(v+130,i,f'{v:,.0f}',va='center',fontsize=9)
    fig.text(.5,.015,'Both dynamic candidates selected retrospectively; not a prospective H1 comparison.',ha='center',fontsize=9)
    save(fig,'figure07_dynamic_vs_market.png')


def equity_allocation_figure():
    """Archived v1.4 report mean equity exposure (no ticker information)."""
    labels=['Growth','Balanced','Defensive']
    grouped=[92.9188,61.9385,26.3452]
    hier=[95.7649,43.1484,24.7406]
    plain=[70.0000,30.0481,13.8837]
    x=np.arange(3);w=.23
    fig,ax=plt.subplots(figsize=(9.6,5.1))
    ax.bar(x-w,grouped,width=w,label='Historical-mean control · Grouped',color=cs.CONTROL)
    ax.bar(x,hier,width=w,label='Historical-mean control · Hierarchical',color=cs.CONTROL_2)
    ax.bar(x+w,plain,width=w,label='MPT · Historical mean',color=cs.MPT_LIGHT)
    ax.set_xticks(x,labels);ax.set_ylabel('Mean decision-period equity allocation (%)')
    ax.set_ylim(0,110);ax.set_title('Observed equity exposure differs by strategy and mandate')
    ax.legend(frameon=False,fontsize=9,ncol=3,loc='upper center');ax.grid(axis='y',alpha=.14);ax.set_axisbelow(True)
    for xx,values in [(x-w,grouped),(x,hier),(x+w,plain)]:
        for xx0,v in zip(xx,values):ax.text(xx0,v+1.3,f'{v:.1f}%',ha='center',fontsize=8)
    save(fig,'figure17_reported_mean_equity_exposure.png')

def make():
    equity_allocation_figure()
    market_figures(p,pd.read_csv(ROOT/"results"/"selected_market_benchmarks.csv"))
    grouped=p[p.representation.eq('Grouped')].set_index('mandate').loc[order]
    fig,axes=plt.subplots(1,3,figsize=(13.5,5.4),sharex=True)
    names=[('equitylab_wealth','Historical-mean control'),('mpt_plain_wealth','Plain MPT'),('mpt_corrected_wealth','Corrected MPT')]
    for ax,man in zip(axes,order):
        ranked=sorted(((float(grouped.loc[man,k]),lab) for k,lab in names),reverse=True)
        ax.barh([v[1] for v in ranked],[v[0] for v in ranked],color=[COL[v[1]] for v in ranked])
        ax.invert_yaxis();ax.set_title(man)
        ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
        for yy,(v,_) in enumerate(ranked):ax.text(v+100,yy,f'{v:,.0f}',va='center',fontsize=8)
    axes[0].set_xlim(10000,19000)
    fig.suptitle('Historical-mean control vs conventional MPT (ablation) · sorted within mandate')
    fig.supxlabel('Ending illustrative net wealth (initial 10,000)')
    save(fig,'figure1_grouped_h1_bar.png')
    fig,ax=plt.subplots(figsize=(10,5.6))
    names=[];deltas=[]
    for m in order:
        for rep in ['Grouped','Hierarchical']:
            z=p[(p.mandate==m)&(p.representation==rep)].iloc[0]
            names.append(f'{m} / {rep}');deltas.append(z.equitylab_wealth-z.mpt_exact_exante_wealth)
    ranked=sorted(zip(names,deltas),key=lambda t:t[1],reverse=True)
    names,deltas=zip(*ranked)
    ax.barh(names,deltas,color=[cs.POSITIVE if x>=0 else cs.NEGATIVE for x in deltas]);ax.invert_yaxis()
    ax.axvline(0,color=cs.INK_2,linewidth=.8);ax.set_xlabel('Historical-mean control minus matched-risk MPT ending wealth (units)')
    ax.set_title('H2 · Estimated-risk-matched wealth differences · 36 periods')
    save(fig,'figure2_exact_risk_bars.png')
    fig,ax=plt.subplots(figsize=(9.8,5.6))
    for rep,marker in [('Grouped','o'),('Hierarchical','s')]:
        z=p[p.representation==rep]
        for lab,x,y,color in [('Historical-mean control','equitylab_realised_annual_vol','equitylab_wealth',COL['EquityLab']),
                              ('Risk-matched MPT','exact_mpt_realised_annual_vol','mpt_exact_exante_wealth',COL['Risk-matched MPT'])]:
            ax.scatter(z[x]*100,z[y],label=f'{rep} / {lab}',marker=marker,color=color,s=82,alpha=.85)
            for _,r in z.iterrows():ax.annotate(r.mandate[0],(r[x]*100,r[y]),xytext=(3,4),textcoords='offset points',fontsize=8)
    ax.set_xlabel('Realised annual volatility (%)');ax.set_ylabel('Ending net illustrative wealth (units)')
    ax.set_title('H2 · Realised risk and ending wealth');ax.legend(frameon=False,fontsize=8,ncol=2)
    save(fig,'figure4_risk_return_scatter.png')
    fig,ax=plt.subplots(figsize=(10,5.6))
    for i,m in enumerate(order):
        for j,rep in enumerate(['Grouped','Hierarchical']):
            r=p[(p.mandate==m)&(p.representation==rep)].iloc[0]
            y=2*i+j; a=r.equitylab_excess_sharpe;b=r.exact_mpt_excess_sharpe
            ax.plot([a,b],[y,y],color=cs.GRID,linewidth=2.5)
            ax.scatter(a,y,color=COL['EquityLab'],s=65,zorder=4)
            ax.scatter(b,y,color=COL['Risk-matched MPT'],s=65,zorder=4,marker='s')
    labels=[f'{m} / {rep}' for m in order for rep in ['Grouped','Hierarchical']]
    ax.set_yticks(range(len(labels)),labels);ax.invert_yaxis();ax.set_xlabel('Annualised excess-return Sharpe')
    ax.set_title('H2 · Realised risk-adjusted efficiency')
    ax.scatter([],[],color=COL['EquityLab'],label='Historical-mean control');ax.scatter([],[],color=COL['Risk-matched MPT'],marker='s',label='Risk-matched MPT')
    ax.legend(frameon=False);save(fig,'figure5_sharpe_dumbbell.png')
    fig,ax=plt.subplots(figsize=(9.8,5.3))
    hs=h.copy();labels=[];delta=[]
    for m in order:
        for rep in ['Grouped','Hierarchical']:
            r=hs[(hs.mandate==m)&(hs.representation==rep)].iloc[0]
            labels.append(f'{m} / {rep}');delta.append(r.equitylab_information_wealth-r.mpt_information_wealth)
    ranked=sorted(zip(labels,delta),key=lambda t:t[1],reverse=True)
    labels,delta=zip(*ranked)
    ax.barh(labels,delta,color=[cs.POSITIVE if v>=0 else cs.NEGATIVE for v in delta]);ax.axvline(0,color=cs.INK_2,linewidth=.8)
    ax.invert_yaxis();ax.set_xlabel('EquityLab-informed minus conventional-information wealth (units)')
    ax.set_title('H3 · Information inside common MPT allocator · 27 periods')
    save(fig,'figure6_h3_hybrid_bars.png')
    # Exploratory forecast-family illustration, pre-excluded from H1 winner counts.
    # Values transcribed from the separately archived private v1.4 OOS report.
    fig,ax=plt.subplots(figsize=(8.8,4.8))
    labels=['Historical-mean\ncontrol','Dynamic state-space\n(exploratory)','SPY benchmark']
    vals=[17020.411494,21174.9812,18516.0451]
    colors=[cs.CONTROL,cs.STATE_SPACE,cs.SPY]
    ax.bar(labels,vals,color=colors,width=.63)
    ax.set_ylim(10000,22500);ax.set_ylabel('Ending illustrative net wealth (units)')
    ax.set_title('Forecast-family illustration · Grouped Growth · NOT a selected primary result')
    for i,x in enumerate(vals):ax.text(i,x+120,f'{x:,.0f}',ha='center',fontsize=10)
    save(fig,'figure9_dynamic_exploratory.png')
    monthly=ROOT/'results'/'selected_monthly_net_wealth.csv'
    if not monthly.exists():
        raise FileNotFoundError(
            f'Cannot produce genuine wealth/drawdown line charts: {monthly} is missing.\n'
            'results/selected_monthly_net_wealth.csv is required.\n'
            'Do not publish this repository without reviewing the dated monthly figures.'
        )
    s=pd.read_csv(monthly,parse_dates=['period_end'])
    expected={'representation','mandate','strategy','period_end','wealth_end','net_return'}
    if not expected.issubset(s):raise ValueError('Monthly file missing public columns')
    if s.duplicated(['representation','mandate','strategy','period_end']).any():raise ValueError('Duplicate public monthly dates')
    # Export schema names remain unchanged for backward compatibility; labels are explicit.
    # Three focused charts avoid the unreadable twelve-line wealth figure.
    styles={
        'EquityLab':('-.', cs.CONTROL),
        'Plain MPT':('--', cs.MPT_MEAN),
        'Corrected MPT':(':', cs.MPT_MEAN),
        'Ex-ante-matched MPT':('--', cs.MPT_MATCHED),
        'SPY':('--', cs.SPY),
        'T-bills':(':', cs.TBILL),
        'SPY / T-bills':('-.', cs.SPY),
        'EL / Hierarchical state-space':('-', cs.STATE_SPACE),
        'EL / Quality low-rank Kalman':('-', cs.KALMAN),
        }
    label_map={
        'EquityLab':'EL / Historical-mean control',
        'Plain MPT':'MPT / Historical mean',
        'Corrected MPT':'MPT / Shrinkage',
        'Ex-ante-matched MPT':'MPT / Risk-matched to control†',
        'SPY':'SPY / S&P 500 ETF',
        'T-bills':'US Treasury-bill proxy',
        'SPY / T-bills':'SPY + T-bill blend'}
    dynamic_names=['EL / Hierarchical state-space','EL / Quality low-rank Kalman']
    main_names=['EL / Hierarchical state-space','EL / Quality low-rank Kalman',
                'EquityLab','SPY','T-bills','Ex-ante-matched MPT']
    benchmark_names=['EL / Hierarchical state-space','EL / Quality low-rank Kalman','EquityLab','SPY',
                     'SPY / T-bills','T-bills','Plain MPT','Corrected MPT',
                     'Ex-ante-matched MPT']
    def plot_path(ax,sub,name,drawdown=False):
        v=sub[sub.strategy==name].sort_values('period_end')
        if len(v)!=36:
            raise ValueError(f'Partial monthly wealth path: {name} ({len(v)} periods)')
        date=pd.to_datetime([v.period_end.iloc[0]-pd.offsets.MonthEnd(),*v.period_end])
        wealth=np.r_[10000.,v.wealth_end.to_numpy(float)]
        y=100*(wealth/np.maximum.accumulate(wealth)-1) if drawdown else wealth
        ls,c=styles[name]
        ax.plot(date,y,label=label_map.get(name,name),color=c,ls=ls,
                lw=2.8 if name in dynamic_names[:2] or name=='SPY' else 1.8,
                alpha=1 if name in main_names else .8)
    for rep in ['Grouped','Hierarchical']:
        for man in order:
            sub=s[(s.representation==rep)&(s.mandate==man)]
            for names,filename,title,size in [
                (main_names,f'figure7_{rep.lower()}_{man.lower()}_monthly_wealth.png',
                 'Featured dynamic Phase 2 and practical references',(12.6,6.6)),
                (dynamic_names+['EquityLab'],f'figure7_{rep.lower()}_{man.lower()}_dynamic_models.png',
                 'Dynamic forecasting models and historical-mean control',(12.6,6.6)),
                (benchmark_names,f'figure7_{rep.lower()}_{man.lower()}_benchmarks.png',
                 'State-space example and benchmark families',(12.6,6.6))]:
                fig,ax=plt.subplots(figsize=size)
                for name in names:plot_path(ax,sub,name)
                ax.set_title(f'{rep} / {man} · {title} · 36 months')
                ax.set_ylabel('Modelled net wealth (initial 10,000 units)')
                ax.grid(alpha=.14);ax.set_axisbelow(True)
                ax.legend(frameon=False,fontsize=8,ncol=2,loc='upper left')
                ax.text(.01,-.13,'* Retrospectively selected for presentation. † Risk target matches historical-mean CONTROL, not dynamic models.',
                        transform=ax.transAxes,fontsize=8,color=cs.INK_2)
                save(fig,filename)
            fig,ax=plt.subplots(figsize=(12.6,5.9))
            for name in main_names:plot_path(ax,sub,name,drawdown=True)
            ax.axhline(0,color=cs.AXIS,lw=.8)
            ax.set_title(f'{rep} / {man} · Drawdown of featured strategies')
            ax.set_ylabel('Decline from previous wealth peak (%)')
            ax.grid(alpha=.14);ax.set_axisbelow(True)
            ax.legend(frameon=False,fontsize=8,ncol=2)
            save(fig,f'figure8_{rep.lower()}_{man.lower()}_drawdown.png')
    # End-of-window comparisons use real dated observations from the private archive.
    selected_dynamic=['EL / Hierarchical state-space','EL / Quality low-rank Kalman']
    records=[]
    expected=['EquityLab',*selected_dynamic,'SPY','SPY / T-bills','T-bills','Plain MPT','Corrected MPT','Ex-ante-matched MPT']
    for rep in ['Grouped','Hierarchical']:
        for man in order:
            t=s[(s.representation==rep)&(s.mandate==man)]
            by={name:g.sort_values('period_end') for name,g in t.groupby('strategy')}
            if any(name not in by or len(by[name])!=36 for name in expected):
                raise ValueError(f'Incomplete comparative paths for {rep}/{man}')
            v={name:float(by[name].wealth_end.iloc[-1]) for name in expected}
            cash=by['T-bills'].net_return.to_numpy(float)
            for dynamic in selected_dynamic:
                dyn=by[dynamic].net_return.to_numpy(float)
                x=dyn-cash
                records.append(dict(representation=rep,mandate=man,model=dynamic,dynamic_wealth=v[dynamic],
                static_wealth=v['EquityLab'],spy_wealth=v['SPY'],spy_tbill_wealth=v['SPY / T-bills'],
                tbill_wealth=v['T-bills'],historical_mpt_wealth=v['Plain MPT'],
                shrinkage_mpt_wealth=v['Corrected MPT'],exact_risk_mpt_wealth=v['Ex-ante-matched MPT'],
                dynamic_realised_vol=float(np.std(dyn,ddof=1)*np.sqrt(12)),
                dynamic_excess_sharpe=float(np.mean(x)/np.std(x,ddof=1)*np.sqrt(12)) if np.std(x,ddof=1)>0 else np.nan))
    dyn_results=pd.DataFrame(records)
    dyn_results.to_csv(ROOT/'results'/'exploratory_dynamic_all_comparisons.csv',index=False,float_format='%.9g')
    fig,axes=plt.subplots(2,3,figsize=(18,10))
    for i,rep in enumerate(['Grouped','Hierarchical']):
        for j,man in enumerate(order):
            ax=axes[i,j]
            r=dyn_results[(dyn_results.representation==rep)&(dyn_results.mandate==man)&(dyn_results.model=='EL / Hierarchical state-space')].iloc[0]
            vals=[('EL / Hierarchical state-space',r.dynamic_wealth,cs.STATE_SPACE),('EL / Historical-mean control',r.static_wealth,cs.CONTROL),
                 ('SPY',r.spy_wealth,cs.SPY),('SPY/T-bills',r.spy_tbill_wealth,cs.SPY_TBILL),
                 ('T-bills',r.tbill_wealth,cs.TBILL),('MPT historical',r.historical_mpt_wealth,cs.MPT_MEAN),
                 ('MPT shrinkage',r.shrinkage_mpt_wealth,cs.MPT_SHRINK),('MPT ex-ante matched†',r.exact_risk_mpt_wealth,cs.MPT_MATCHED)]
            vals.sort(key=lambda z:z[1],reverse=True)
            ax.barh([v[0] for v in vals],[v[1] for v in vals],color=[v[2] for v in vals],height=.7)
            ax.invert_yaxis();ax.set_title(f'{rep} / {man}');ax.tick_params(axis='y',labelsize=8)
            ax.grid(axis='x',alpha=.13);ax.set_axisbelow(True)
    fig.suptitle('Dynamic Phase 2 vs historical-mean control and market benchmarks | 36 months',fontsize=15)
    fig.supxlabel('*Exploratory model highlighted retrospectively. † MPT matches historical-mean control estimated risk, not dynamic risk.')
    save(fig,'figure10_dynamic_all_comparisons.png')
    fig,ax=plt.subplots(figsize=(10.5,5.5))
    focus=dyn_results[dyn_results.model=='EL / Hierarchical state-space'].copy()
    names=[f'{r.representation} / {r.mandate}' for r in focus.itertuples()]
    changes=(focus.dynamic_wealth-focus.spy_wealth).to_numpy()
    ranking=np.argsort(-changes)
    ax.barh([names[k] for k in ranking],changes[ranking],color=[cs.POSITIVE if changes[k]>=0 else cs.NEGATIVE for k in ranking])
    ax.invert_yaxis();ax.axvline(0,color=cs.INK_2,lw=.8)
    ax.set_title('Exploratory dynamic EquityLab minus SPY | six configurations')
    ax.set_xlabel('Ending wealth difference (initial 10,000)')
    save(fig,'figure11_dynamic_vs_spy.png')
    fig,ax=plt.subplots(figsize=(10.5,5.5))
    for rep,marker in [('Grouped','o'),('Hierarchical','s')]:
        q=dyn_results[(dyn_results.representation==rep)&(dyn_results.model=='EL / Hierarchical state-space')]
        ax.scatter(q.dynamic_realised_vol*100,q.dynamic_wealth,label=rep,s=95,marker=marker)
        for r in q.itertuples():ax.annotate(r.mandate[0],(r.dynamic_realised_vol*100,r.dynamic_wealth),xytext=(5,5),textcoords='offset points')
    ax.set_xlabel('Realised annualised portfolio volatility (%)')
    ax.set_ylabel('Illustrative ending wealth')
    ax.set_title('Dynamic EquityLab | realised risk versus ending wealth')
    ax.legend(frameon=False);ax.grid(alpha=.16)
    save(fig,'figure12_dynamic_realised_risk.png')
    lines=['| Representation | Mandate | State-space | Control | SPY | SPY/T-bills | Exact-risk MPT† | State-space Sharpe |',
           '|---|---|---:|---:|---:|---:|---:|---:|']
    for r in dyn_results[dyn_results.model=='EL / Hierarchical state-space'].itertuples():
        lines.append(f'| {r.representation} | {r.mandate} | {r.dynamic_wealth:,.0f} | {r.static_wealth:,.0f} | {r.spy_wealth:,.0f} | {r.spy_tbill_wealth:,.0f} | {r.exact_risk_mpt_wealth:,.0f} | {r.dynamic_excess_sharpe:.2f} |')
    fragment=('\n\n### Dynamic model across the six selected configurations\n\n'
        'The table shows hierarchical state-space; [the model-level CSV](results/selected_dynamic_model_summary.csv) has both candidates. These results are exploratory, not a predeclared H1 test.\n\n'
                '![Dynamic performance relative to SPY](figures/figure11_dynamic_vs_spy.png)\n\n'
        '![Dynamic realised volatility versus wealth](figures/figure12_dynamic_realised_risk.png)\n\n'
        +'\n'.join(lines)+'\n\n'
        '† This MPT control matches the **historical-mean control** ex-ante risk, NOT the dynamic portfolio risk. A like-for-like risk-matched dynamic MPT comparison is not established. Dynamic Sharpe uses the monthly T-bill excess return and is for descriptive analysis.\n\n')
    readme=ROOT/'README.md';t=readme.read_text()
    a='<!-- DYNAMIC_ALL_COMPARISONS_START -->';b='<!-- DYNAMIC_ALL_COMPARISONS_END -->'
    if a not in t or b not in t:raise ValueError('Missing README dynamic markers')
    t=t[:t.index(a)+len(a)]+fragment+t[t.index(b):]
    readme.write_text(t)
    # Flag the post-hoc model selection conspicuously on the featured charts.
    # Embed only verified, genuinely dated charts after the exporter succeeds.
    readme=ROOT/'README.md'
    original=readme.read_text()
    a='<!-- MONTHLY_WEALTH_CHARTS_START -->';b='<!-- MONTHLY_WEALTH_CHARTS_END -->'
    charts='\n\n'.join(
        f'**{rep} / {man}**\n\n' +
        f'![{rep} {man} dated monthly net wealth](figures/figure7_{rep.lower()}_{man.lower()}_monthly_wealth.png)\n\n'
        f'![{rep} {man} dated monthly drawdown](figures/figure8_{rep.lower()}_{man.lower()}_drawdown.png)'
        for rep in ['Grouped','Hierarchical'] for man in order)
    if a not in original or b not in original:raise ValueError('README monthly graph insertion markers missing')
    original=original[:original.index(a)+len(a)]+'\n'+charts+'\n'+original[original.index(b):]
    readme.write_text(original)
    featured = (
        '\n\n### Grouped Growth: monthly net wealth\n\n'
        'Two dynamic forecasting candidates are shown; both were retrospectively selected for presentation. '
        'All curves use the same 36 monthly dates. Amounts are illustrative, with unverified historical FX provenance.\n\n'
        '![Actual monthly portfolio wealth, including dynamic EquityLab, SPY, T-bills and MPT](figures/figure7_grouped_growth_monthly_wealth.png)\n\n'
        '### Grouped Growth: drawdowns\n\n'
        '![Actual monthly portfolio drawdown comparison](figures/figure8_grouped_growth_drawdown.png)\n\n'
    )
    feature_a='<!-- FEATURED_TIME_SERIES_START -->'
    feature_b='<!-- FEATURED_TIME_SERIES_END -->'
    readme=ROOT/'README.md'; intro=readme.read_text()
    if feature_a not in intro or feature_b not in intro:
        raise ValueError('README featured chart markers missing')
    intro=intro[:intro.index(feature_a)+len(feature_a)]+featured+intro[intro.index(feature_b):]
    readme.write_text(intro)
    print('Generated 12 genuine date-based wealth/drawdown charts and embedded them in README, including featured charts near the top.')
if __name__=='__main__':
    from plot_dynamic_candidates import main as dynamic_candidate_figures
    dynamic_candidate_figures()
    make()
    from plot_public_composition import plot
    plot()
    from market_exposure_diagnostics import main as diagnostics
    diagnostics()
    from plot_without_nvda import main as without_nvda_figures
    without_nvda_figures()
    from plot_public_exposures import main as allocation_plots
    allocation_plots()
