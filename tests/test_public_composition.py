import sys,unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
try:
    from export_public_research import prepare_disclosure,snapshot_indices
except ImportError:
    raise unittest.SkipTest('private exporter is not in the public repository')
class DisclosureTests(unittest.TestCase):
 def setUp(self):
  dates=pd.date_range('2022-01-31',periods=36,freq='ME')
  self.df=pd.DataFrame([{'representation':'economic_grouped','mandate':'growth','model':'hierarchical_state_space',
    'decision_date':d,'ticker':tick,'weight':.1} for i,d in enumerate(dates)
    for tick in ['SPY','AAPL'] if not (tick=='AAPL' and i%2)])
 def test_default_zero_ticker_disclosure(self):
  counts,snaps,heat=prepare_disclosure(self.df,False)
  self.assertEqual(len(counts),36);self.assertTrue(snaps.empty);self.assertTrue(heat.empty)
  self.assertEqual(set(counts.columns),{'representation','mandate','decision_month','selected_asset_count','added_asset_count','removed_asset_count'})
 def test_opt_in_limits_snapshots(self):
  counts,snaps,heat=prepare_disclosure(self.df,True)
  self.assertEqual(snaps.snapshot.nunique(),6)
  self.assertLessEqual(len(snaps),12)
  self.assertFalse('weight' in snaps.columns)
  self.assertTrue(set(heat.present.unique()).issubset({0,1}))
 def test_refuse_partial(self):
  with self.assertRaisesRegex(ValueError,'36 months'):prepare_disclosure(self.df.iloc[:-2],False)
 def test_refuse_bad_ticker(self):
  d=self.df.copy();d.loc[d.index[0],'ticker']='secret/password'
  with self.assertRaisesRegex(ValueError,'Ticker'):prepare_disclosure(d,False)
if __name__=='__main__':unittest.main()
