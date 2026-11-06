import unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
class TestMarketBenchmarks(unittest.TestCase):
    def test_benchmarks_and_figures(self):
        bm=pd.read_csv(ROOT/'results'/'selected_market_benchmarks.csv').set_index('mandate')
        self.assertEqual(set(bm.index),{'Growth','Balanced','Defensive'})
        self.assertAlmostEqual(float(bm.loc['Growth','spy_wealth']),18516.0451,places=2)
        self.assertAlmostEqual(float(bm.loc['Defensive','spy_tbill_wealth']),13351.4869,places=2)
        self.assertTrue(all((ROOT/'figures'/p).exists() for p in ['figure01_market_benchmark_bars.png','figure02_against_simple_benchmark.png','figure03_market_exante_risk_scatter.png','figure07_dynamic_vs_market.png']))
    def test_market_benchmark_is_not_claimed_as_risk_matched(self):
        r=(ROOT/'README.md').read_text()
        self.assertIn('not an exact-risk-',r)
        self.assertIn('Hierarchical Growth',r)
        self.assertIn('SPY/T-bill',r)
if __name__=='__main__':unittest.main()
