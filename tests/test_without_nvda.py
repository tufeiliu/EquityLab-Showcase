import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


class WithoutNvdaTests(unittest.TestCase):
    def setUp(self):
        self.monthly = pd.read_csv(ROOT/'results/without_nvda_monthly_net_wealth.csv')
        self.robust = pd.read_csv(ROOT/'results/nvda_and_own_risk_robustness.csv')

    def test_monthly_paths_are_complete_and_reconcile(self):
        keys = ['representation', 'mandate', 'strategy']
        ordered = self.monthly.sort_values('period_end').groupby(keys)
        self.assertTrue(ordered.size().eq(36).all())
        compounded = ordered.net_return.apply(lambda r: 10_000*(1+r).prod())
        self.assertLess((compounded-ordered.wealth_end.last()).abs().max(), .5)

    def test_monthly_paths_match_the_robustness_table(self):
        final = self.monthly.sort_values('period_end').groupby(['representation', 'mandate', 'strategy']).wealth_end.last()
        rows = self.robust[self.robust.universe == 'without_nvda']
        for r in rows.itertuples():
            self.assertAlmostEqual(final[(r.representation, r.mandate, r.model)], r.ending_wealth, delta=.15)

    def test_only_aggregate_columns_are_released(self):
        self.assertEqual(list(self.monthly.columns),
                         ['representation', 'mandate', 'strategy', 'period_end', 'net_return', 'wealth_end'])

    def test_figures_are_rendered_and_shown(self):
        readme = (ROOT/'README.md').read_text(encoding='utf8')
        for name in ['figure22_without_nvda_ranked_wealth.png', 'figure23_without_nvda_growth_wealth.png',
                     'figure24_nvda_effect_on_wealth.png', 'figure25_own_risk_mpt_lead.png']:
            self.assertTrue((ROOT/'figures'/name).is_file(), name)
            self.assertIn(name, readme)


if __name__ == '__main__':
    unittest.main()
