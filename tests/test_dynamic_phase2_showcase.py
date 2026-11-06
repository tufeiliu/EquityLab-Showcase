import unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
class DynamicPhase2Showcase(unittest.TestCase):
    def test_six_mandates_all_selected_models(self):
        d=pd.read_csv(ROOT/'results'/'selected_dynamic_model_summary.csv')
        self.assertEqual(len(d),36)
        self.assertTrue((d.groupby(['representation','mandate']).size()==6).all())
        self.assertEqual(set(d.model),{'hierarchical_state_space','quality_lowrank_kalman','mean','spy','spy_tbill','tbill'})
        self.assertAlmostEqual(float(d.query('representation=="Grouped" and mandate=="Growth" and model=="hierarchical_state_space"').ending_wealth.iloc[0]),21174.9812,places=2)
    def test_readme_distinguishes_design_and_baseline(self):
        t=(ROOT/'README.md').read_text()
        self.assertIn('dynamic forecasting system is the intended research design',t)
        self.assertIn('Historical-mean coefficients',t)
        self.assertIn('not the dynamic portfolios',t)
    def test_dynamic_assets_rendered(self):
        for n in ['figure18_dynamic_model_ranked_wealth.png','figure19_dynamic_growth_cagr_sharpe_scatter.png','figure20_dynamic_vs_historical_mean.png','figure21_dynamic_cagr_drawdown_scatter.png']:
            p=ROOT/'figures'/n
            self.assertTrue(p.is_file() and p.stat().st_size>5000,n)
    @unittest.skipUnless((ROOT/'analysis'/'export_selected_monthly.py').exists(),'private exporter is not in the public repository')
    def test_all_dynamic_candidates_exported_by_name(self):
        from importlib.util import spec_from_file_location,module_from_spec
        s=spec_from_file_location('export_selected_monthly',ROOT/'analysis'/'export_selected_monthly.py')
        m=module_from_spec(s);s.loader.exec_module(m)
        selected=m.MODEL_NAMES['phase2_periods.csv']
        for name in ['hierarchical_state_space','quality_lowrank_kalman']:
            self.assertIn(name,selected)
if __name__=='__main__':unittest.main()
