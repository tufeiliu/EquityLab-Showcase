"""Inspect only disclosed portfolio-level aggregates. No investment engine is included."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def load():
    return (pd.read_csv(ROOT/'results/selected_primary_results.csv'),
            pd.read_csv(ROOT/'results/selected_hybrid_results.csv'))
def summary():
    p,h=load()
    print('Selected public configurations:',len(p),'(2 representations x 3 mandates)')
    print('H1: EquityLab net wealth vs plain MPT:',int((p.equitylab_wealth>p.mpt_plain_wealth).sum()),'/6')
    print('H1: EquityLab net wealth vs corrected MPT:',int((p.equitylab_wealth>p.mpt_corrected_wealth).sum()),'/6')
    print('H2: EquityLab net wealth vs ex-ante-matched MPT:',int((p.equitylab_wealth>p.mpt_exact_exante_wealth).sum()),'/6')
    print('H2: EquityLab realised Sharpe vs exact-risk MPT:',int((p.equitylab_excess_sharpe>p.exact_mpt_excess_sharpe).sum()),'/6')
    print('H3: EquityLab information > conventional information:',int((h.equitylab_information_wealth>h.mpt_information_wealth).sum()),'/6')
    x=p[(p.representation=='Hierarchical')&(p.mandate=='Growth')].iloc[0]
    print('Negative case: Hierarchical/Growth EL %.0f vs exact-risk MPT %.0f' %(x.equitylab_wealth,x.mpt_exact_exante_wealth))
    print('These are correlated historical scenarios, not independent trials.')
if __name__=='__main__':summary()
