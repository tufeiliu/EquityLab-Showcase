import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PublicConceptsTests(unittest.TestCase):
    def test_glossary_is_filled(self):
        txt=(ROOT/'README.md').read_text()
        for phrase in ('H1 — Complete system','H2 — Why does it work','H3 — Can the information help MPT',
                       'SPY / T-bills','Historical-mean coefficient control','MPT / Shrinkage',
                       'Ex-ante risk-matched','Drawdown line'):
            self.assertIn(phrase,txt)
    def test_no_generic_equitylab_label_in_monthly_plot_display(self):
        txt=(ROOT/'analysis/generate_public_figures.py').read_text()
        self.assertIn("'EquityLab':'EL / Historical-mean control'",txt)
        self.assertIn('dynamic_models.png',txt)
        self.assertIn('benchmarks.png',txt)
