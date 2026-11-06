"""Publication-only market-exposure diagnostics from reconciled MONTHLY net-return exports.

Uses the released monthly results. No private predictor/holdings data used.
Retrospective volatility matching uses ALL 36 outcomes and is NOT INVESTABLE.
Alpha is an intercept in a one-factor historical regression, NOT causal skill.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import chart_style as cs
cs.apply()

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'
STRATEGY_COLOR={'EL / Hierarchical state-space':cs.STATE_SPACE,'EL / Quality low-rank Kalman':cs.KALMAN}
# These are the exact strategy names used in results/selected_monthly_net_wealth.csv.
STRATEGIES=['EquityLab','EL / Hierarchical state-space','EL / Quality low-rank Kalman']
REPRESENTATIONS=['Grouped','Hierarchical']
MANDATES=['Growth','Balanced','Defensive']

def nw_hac_mean(z,lags=3):
    """Newey-West standard error for OLS intercept & beta, fixed small lag."""
    x=np.asarray(z['x'],float); y=np.asarray(z['y'],float)
    n=len(y); X=np.column_stack([np.ones(n),x]); b=np.linalg.lstsq(X,y,rcond=None)[0]
    e=y-X@b; bread=np.linalg.pinv(X.T@X)
    U=X*e[:,None]; omega=U.T@U
    for lag in range(1,min(lags,n-2)+1):
        cross=U[lag:].T@U[:-lag]
        omega+=(1-lag/(lags+1))*(cross+cross.T)
    cov=bread@omega@bread*n/(n-2)
    se=np.sqrt(np.maximum(0,np.diag(cov)))
    r2=1-(e@e)/np.sum((y-y.mean())**2) if np.std(y)>1e-12 else np.nan
    return b,se,float(r2)

def unlevered_matched_blend(spy,cash,target_vol):
    """Find constant weight [0,1] whose FULL-SAMPLE realised vol matches target.

    If target outside attainable range, return nearest endpoint/vertex tagged UNMATCHED.
    """
    s=np.asarray(spy,float); c=np.asarray(cash,float)
    d=s-c; var_d=float(np.var(d,ddof=1)); cov=float(np.cov(c,d,ddof=1)[0,1]); vc=float(np.var(c,ddof=1))
    candidate=[0.,1.]
    if var_d>1e-15:
        candidate.append(float(np.clip(-cov/var_d,0,1)))
        roots=np.roots([var_d,2*cov,vc-target_vol**2/12])
        for r in roots:
            if abs(r.imag)<1e-8 and -1e-9<=r.real<=1+1e-9:candidate.append(float(np.clip(r.real,0,1)))
    def deviation(w):return abs(np.std(c+w*d,ddof=1)*np.sqrt(12)-target_vol)
    # Choose exact solution with least equity if multiple satisfy; otherwise nearest attainable.
    chosen=min(candidate,key=lambda w:(deviation(w),w))
    actual=np.std(c+chosen*d,ddof=1)*np.sqrt(12)
    status='matched_retrospectively' if abs(actual-target_vol)<1e-5 else 'unattainable_unlevered'
    return chosen,float(actual),status

def get_panel(raw,rep,mand):
    t=raw[(raw.representation==rep)&(raw.mandate==mand)]
    keys={name:g.sort_values('period_end').reset_index(drop=True) for name,g in t.groupby('strategy')}
    needed=['SPY','T-bills',*STRATEGIES]
    missing=[name for name in needed if name not in keys]
    incomplete={name:len(keys[name]) for name in needed if name in keys and len(keys[name])!=36}
    if missing or incomplete:
        raise ValueError(
            f'Incomplete market-exposure panel for {rep}/{mand}. '
            f'Missing strategies: {missing}; incomplete paths: {incomplete}. '
            f'Available strategies: {sorted(keys)}. '
            'Regenerate the portfolio-level monthly export using the matching public package.'
        )
    dates=keys['SPY'].period_end.to_numpy()
    if any(not np.array_equal(keys[k].period_end.to_numpy(),dates) for k in needed):
        raise ValueError(f'Calendar misalignment for {rep}/{mand}')
    return keys

def compute(raw):
    required={'representation','mandate','strategy','period_end','net_return','wealth_end'}
    if not required.issubset(raw):raise ValueError(f'Missing {required-set(raw)}')
    if raw.duplicated(['representation','mandate','strategy','period_end']).any():raise ValueError('Duplicated month')
    if not np.isfinite(raw[['net_return','wealth_end']].to_numpy(float)).all():raise ValueError('Nonfinite series')
    rows=[];series=[]
    for rep in REPRESENTATIONS:
        for mand in MANDATES:
            panel=get_panel(raw,rep,mand)
            spy=panel['SPY'].net_return.to_numpy(float)
            cash=panel['T-bills'].net_return.to_numpy(float)
            for name in STRATEGIES:
                r=panel[name].net_return.to_numpy(float)
                vol=float(np.std(r,ddof=1)*np.sqrt(12))
                weight,blendvol,status=unlevered_matched_blend(spy,cash,vol)
                blend=cash+weight*(spy-cash)
                excess=r-cash;market_excess=spy-cash
                b,se,r2=nw_hac_mean({'x':market_excess,'y':excess})
                ew=10000*float(np.prod(1+r)); bw=10000*float(np.prod(1+blend))
                row={'representation':rep,'mandate':mand,'strategy':name,'n_months':36,
                     'equitylab_ending_wealth':ew,'spy_ending_wealth':10000*float(np.prod(1+spy)),
                     'equitylab_annual_realised_vol':vol,'blend_spy_weight':weight,
                     'blend_tbill_weight':1-weight,'blend_annual_realised_vol':blendvol,
                     'blend_match_status':status,'blend_hindsight_ending_wealth':bw,
                     'wealth_minus_blend':ew-bw,
                     'monthly_alpha':b[0],'annualised_arithmetic_alpha':12*b[0],
                     'alpha_hac_se_annual':12*se[0],'alpha_hac_t':b[0]/se[0] if se[0]>0 else np.nan,
                     'market_beta':b[1],'beta_hac_se':se[1], 'market_r_squared':r2,
                     'alpha_95ci_low_annual':12*(b[0]-1.96*se[0]),
                     'alpha_95ci_high_annual':12*(b[0]+1.96*se[0])}
                rows.append(row)
                for date,v in zip(panel[name].period_end,blend):
                    series.append({'representation':rep,'mandate':mand,'strategy':name,'period_end':date,
                                   'hindsight_blend_net_return':float(v)})
    return pd.DataFrame(rows),pd.DataFrame(series)

def plots(d):
    FIG.mkdir(exist_ok=True)
    # Two readable panels, sorting by excess wealth (unmatched bars explicitly excluded).
    matched=d[d.blend_match_status=='matched_retrospectively'].copy()
    fig,axs=plt.subplots(1,3,figsize=(19,6.8),sharex=True)
    for ax,name in zip(axs,STRATEGIES):
        z=matched[matched.strategy==name].sort_values('wealth_minus_blend',ascending=False)
        if z.empty:ax.text(.5,.5,'No feasible matches',ha='center',transform=ax.transAxes)
        else:
            values=z.wealth_minus_blend.to_numpy()
            ax.barh(z.representation+' / '+z.mandate,values,color=[cs.POSITIVE if x>=0 else cs.NEGATIVE for x in values])
            ax.invert_yaxis();ax.axvline(0,color=cs.INK_2,lw=.8)
        ax.set_title('Historical-mean control' if name=='EquityLab' else name.replace('EL / ',''))
        ax.set_xlabel('EL minus hindsight blend wealth')
        ax.grid(axis='x',alpha=.13);ax.set_axisbelow(True)
    fig.suptitle('SPY/T-bill realised-vol matched diagnostic | NOT INVESTABLE',fontsize=14)
    fig.text(.5,.01,'Full-window weights use future outcomes; no leverage, no additional trading/financing costs. *Retrospectively selected model.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,.94]);fig.savefig(FIG/'figure13_hindsight_volmatched_blends.png',dpi=175,bbox_inches='tight');plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(19,6.2))
    for ax,name in zip(axs,STRATEGIES):
        z=d[d.strategy==name].sort_values('market_beta')
        y=np.arange(len(z))
        ax.errorbar(z.market_beta,y,xerr=1.96*z.beta_hac_se,fmt='o',capsize=3,color=STRATEGY_COLOR.get(name,cs.CONTROL))
        ax.set_yticks(y,z.representation+' / '+z.mandate);ax.axvline(1,ls='--',color=cs.AXIS,lw=.8)
        ax.set_title('Historical-mean control' if name=='EquityLab' else name.replace('EL / ',''))
        ax.set_xlabel('SPY excess-return beta (95% HAC interval)');ax.grid(axis='x',alpha=.12)
    fig.suptitle('Market sensitivity | one-factor SPY regression · 36 months')
    fig.tight_layout();fig.savefig(FIG/'figure14_spy_beta_intervals.png',dpi=175,bbox_inches='tight');plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(19,6.2))
    for ax,name in zip(axs,STRATEGIES):
        z=d[d.strategy==name].sort_values('annualised_arithmetic_alpha',ascending=False)
        y=np.arange(len(z));alpha=z.annualised_arithmetic_alpha.to_numpy()*100
        lo=(z.annualised_arithmetic_alpha-z.alpha_95ci_low_annual).to_numpy()*100
        hi=(z.alpha_95ci_high_annual-z.annualised_arithmetic_alpha).to_numpy()*100
        ax.errorbar(alpha,y,xerr=[lo,hi],fmt='o',capsize=3,color=STRATEGY_COLOR.get(name,cs.CONTROL))
        ax.set_yticks(y,z.representation+' / '+z.mandate);ax.axvline(0,color=cs.AXIS,lw=.8)
        ax.set_title('Historical-mean control' if name=='EquityLab' else name.replace('EL / ',''))
        ax.set_xlabel('Annualised arithmetic alpha (% points; 95% HAC CI)');ax.grid(axis='x',alpha=.12)
    fig.suptitle('Market-adjusted residual return | NOT verified investment alpha')
    fig.tight_layout();fig.savefig(FIG/'figure15_market_alpha_intervals.png',dpi=175,bbox_inches='tight');plt.close(fig)

def update_readme():
    path=ROOT/'README.md';s=path.read_text()
    a='<!-- MARKET_DIAGNOSTICS_START -->';b='<!-- MARKET_DIAGNOSTICS_END -->'
    if a not in s or b not in s:raise ValueError('README missing diagnostic anchors')
    body='''\n\n![Retrospective SPY/T-bill realised-volatility comparison](figures/figure13_hindsight_volmatched_blends.png)\n\n![SPY beta with uncertainty intervals](figures/figure14_spy_beta_intervals.png)\n\n![Market-regression residual return and HAC confidence intervals](figures/figure15_market_alpha_intervals.png)\n\nThe blend uses a constant **full-sample hindsight** weight, constrained to 0–100% SPY, to match realised volatility. This is **not an investable strategy**; infeasible targets are explicitly recorded as `unattainable_unlevered`. The regression uses monthly portfolio returns above the monthly T-bill proxy and a one-factor SPY excess-return benchmark. The intercept is an *estimated* residual return, not proof of causal alpha. HAC standard errors (Newey–West, 3 lags) give rough uncertainty intervals with only 36 observations; model selection and multiple testing remain concerns. Both featured dynamic candidates are selected retrospectively for presentation; neither is a prospectively validated H1 policy.\n\n[Inspect the complete numeric audit](results/public_market_exposure_diagnostics.csv).\n\n'''
    start=s.index(a)+len(a)
    end=s.index(b,start)
    s=s[:start]+body+s[end:]
    path.write_text(s)

def main():
    path=ROOT/'results/selected_monthly_net_wealth.csv'
    if not path.is_file():
        print('Monthly export not found; market-exposure diagnostics not generated. Run export_selected_monthly.py --write first.');return
    raw=pd.read_csv(path)
    d,series=compute(raw)
    d.to_csv(ROOT/'results/public_market_exposure_diagnostics.csv',index=False,float_format='%.10g')
    series.to_csv(ROOT/'results/public_hindsight_blend_monthly.csv',index=False,float_format='%.10g')
    plots(d);update_readme()
    print('Generated market-exposure diagnostics:',len(d),'strategies; feasible retrospective matches:',sum(d.blend_match_status=='matched_retrospectively'))
if __name__=='__main__':main()
