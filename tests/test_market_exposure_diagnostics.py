import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
from market_exposure_diagnostics import compute,nw_hac_mean,unlevered_matched_blend,STRATEGIES,get_panel
try:
    from export_selected_monthly import MODEL_NAMES
    from export_public_exposures import prepare
except ImportError:
    MODEL_NAMES=prepare=None
needs_exporters=unittest.skipIf(prepare is None,'private exporters are not in the public repository')

class TestExposureDiagnostics(unittest.TestCase):
    def test_alpha_beta_known(self):
        x=np.linspace(-.04,.05,36)
        b,se,r2=nw_hac_mean({'x':x,'y':.002+1.3*x})
        self.assertAlmostEqual(b[0],.002,places=9)
        self.assertAlmostEqual(b[1],1.3,places=9)
        self.assertAlmostEqual(r2,1,places=9)
    def test_blend_exact_match(self):
        spy=np.linspace(-.05,.07,36)
        cash=np.repeat(.002,36)
        target=np.std(.4*spy+.6*cash,ddof=1)*np.sqrt(12)
        w,vol,status=unlevered_matched_blend(spy,cash,target)
        self.assertAlmostEqual(w,.4,places=5)
        self.assertEqual(status,'matched_retrospectively')
    def test_blend_unattainable(self):
        spy=np.linspace(-.05,.07,36);cash=np.repeat(.002,36)
        w,vol,status=unlevered_matched_blend(spy,cash,1.)
        self.assertEqual(status,'unattainable_unlevered')
        self.assertLessEqual(w,1.)
    @needs_exporters
    def test_diagnostics_use_exporter_strategy_identifiers(self):
        self.assertEqual(STRATEGIES, [MODEL_NAMES['phase2_periods.csv']['mean'],
                                      MODEL_NAMES['phase2_periods.csv']['hierarchical_state_space'],
                                      MODEL_NAMES['phase2_periods.csv']['quality_lowrank_kalman']])

    def test_market_diagnostics_on_six_complete_exported_panels(self):
        # Synthetic diagnostic fixture, never published as investment results.
        dates=pd.date_range('2023-01-31',periods=36,freq='ME')
        records=[]
        for rep in ['Grouped','Hierarchical']:
            for mand in ['Growth','Balanced','Defensive']:
                for strategy in ['SPY','T-bills',*STRATEGIES]:
                    for i,date in enumerate(dates):
                        cash=.002
                        spy=.012+.015*np.sin(i*.4)
                        ret={'SPY':spy,'T-bills':cash,
                             STRATEGIES[0]:cash+.65*(spy-cash)+.002*np.cos(i*.7),
                             STRATEGIES[1]:cash+.75*(spy-cash)+.003*np.cos(i*.3),
                             STRATEGIES[2]:cash+.7*(spy-cash)+.004*np.cos(i*.25)}[strategy]
                        records.append(dict(representation=rep,mandate=mand,strategy=strategy,
                                            period_end=date.strftime('%Y-%m-%d'),net_return=ret,
                                            wealth_end=10000.0))
        results,paths=compute(pd.DataFrame(records))
        self.assertEqual(len(results),18)
        self.assertEqual(len(paths),18*36)
        self.assertEqual(set(results.strategy),set(STRATEGIES))

    def test_missing_panel_error_names_actual_absent_strategy(self):
        frame=pd.DataFrame([dict(representation='Grouped',mandate='Growth',strategy='SPY',
                                 period_end='2023-01-31')])
        with self.assertRaisesRegex(ValueError,'Missing strategies:'):
            get_panel(frame,'Grouped','Growth')

    @needs_exporters
    def test_asset_class_unclassified_not_cash(self):
        dates=pd.date_range('2023-01-31',periods=36,freq='ME')
        rows=[]
        for date in dates:
            rows.extend([dict(representation='economic_grouped',mandate='growth',decision_date=date,model='mean',ticker='SPY',weight=.4),dict(representation='economic_grouped',mandate='growth',decision_date=date,model='mean',ticker='PRIVATE_STOCK',weight=.3)])
        out=prepare(pd.DataFrame(rows))
        self.assertEqual(len(out),36)
        self.assertEqual(out.iloc[0].equity_pct_approx,40)
        self.assertEqual(out.iloc[0].unclassified_pct_approx,60)
        self.assertEqual(out.iloc[0].cash_pct_approx,0)
if __name__=='__main__':unittest.main()
