
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

class PublicResultsTests(unittest.TestCase):
    def test_selected_shapes(self):
        p = pd.read_csv(ROOT / 'results' / 'selected_primary_results.csv')
        h = pd.read_csv(ROOT / 'results' / 'selected_hybrid_results.csv')
        self.assertEqual(len(p), 6)
        self.assertEqual(len(h), 6)

    def test_headlines_reconcile(self):
        p = pd.read_csv(ROOT / 'results' / 'selected_primary_results.csv')
        h = pd.read_csv(ROOT / 'results' / 'selected_hybrid_results.csv')
        self.assertEqual(int((p.equitylab_wealth > p.mpt_plain_wealth).sum()), 6)
        self.assertEqual(int((p.equitylab_wealth > p.mpt_corrected_wealth).sum()), 6)
        self.assertEqual(int((p.equitylab_wealth > p.mpt_exact_exante_wealth).sum()), 5)
        self.assertEqual(int((p.equitylab_excess_sharpe > p.exact_mpt_excess_sharpe).sum()), 5)
        self.assertEqual(int((h.equitylab_information_wealth > h.mpt_information_wealth).sum()), 4)

    def test_counterexample_is_preserved(self):
        p = pd.read_csv(ROOT / 'results' / 'selected_primary_results.csv')
        x = p[(p.representation=='Hierarchical') & (p.mandate=='Growth')].iloc[0]
        self.assertLess(x.equitylab_wealth, x.mpt_exact_exante_wealth)
        self.assertLess(x.equitylab_excess_sharpe, x.exact_mpt_excess_sharpe)


    @unittest.skipUnless((ROOT/'analysis'/'export_selected_monthly.py').exists(),'private exporter is not in the public repository')
    def test_public_exporter_is_strict(self):
        import ast
        from pathlib import Path
        script=(ROOT/'analysis'/'export_selected_monthly.py').read_text()
        ast.parse(script)
        self.assertIn('EXPECTED_N=36',script)
        self.assertIn('No security-level',script)

if __name__ == '__main__':
    unittest.main()
