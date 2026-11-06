import unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]

class FeaturedTimeseriesReleaseTest(unittest.TestCase):
    def test_notebook_has_actionable_export_error(self):
        import json
        notebook=json.loads((ROOT/'notebooks/01_public_readout.ipynb').read_text())
        cells='\n'.join(''.join(c.get('source',[])) for c in notebook['cells'])
        self.assertIn('raise FileNotFoundError',cells)
    def test_generator_must_fail_when_monthly_source_missing(self):
        source=(ROOT/'analysis/generate_public_figures.py').read_text()
        self.assertIn('Cannot produce genuine wealth/drawdown line charts',source)
        self.assertIn('FEATURED_TIME_SERIES_START',source)
    def test_readme_prominent_featured_markers(self):
        readme=(ROOT/'README.md').read_text()
        self.assertIn('<!-- FEATURED_TIME_SERIES_START -->',readme)

if __name__=='__main__':unittest.main()
