import importlib.util
import math
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

source = Path(__file__).resolve().parents[1] / 'analysis' / 'research_hypothesis_inference.py'
spec = importlib.util.spec_from_file_location('equitylab_inference_module', source)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

REPS = ('Grouped', 'Hierarchical')
MANDATES = ('Growth', 'Balanced', 'Defensive')


def month(i):
    return pd.Timestamp('2023-01-31') + pd.offsets.MonthEnd(i)


def synthetic_main(seed=57):
    rng = np.random.default_rng(seed)
    rows = []
    for rep in REPS:
        for man in MANDATES:
            market = rng.normal(.008, .03, 36)
            series = {h.SPY: market, h.TBILL: np.full(36, .002), h.CONTROL: market * .6 + .002,
                      'Plain MPT': market * .4 + .003, 'Corrected MPT': market * .3 + .002,
                      h.DYNAMIC[0]: market * .65 + .006, h.DYNAMIC[1]: market * .55 + .005}
            for strategy, values in series.items():
                rows += [dict(representation=rep, mandate=man, strategy=strategy, period_end=month(i),
                              net_return=float(v)) for i, v in enumerate(values)]
    return pd.DataFrame(rows)


class HypothesisTestingTests(unittest.TestCase):
    def test_hac_mean(self):
        x = np.array([0.01, -0.02, 0.03, 0.02, 0.01, -0.01] * 6)
        mu, se, beta = h.hac_intercept(x)
        self.assertAlmostEqual(mu, 1 / 150, places=8)
        self.assertTrue(se > 0)
        self.assertTrue(np.isnan(beta))

    def test_correction_matches_uncorrected_estimator(self):
        x = np.random.default_rng(3).normal(.003, .02, 36)
        e = x - x.mean()
        var = e @ e / 36 + sum(2 * (1 - k / 4) * (e[k:] @ e[:-k]) / 36 for k in range(1, 4))
        uncorrected = x.mean() / math.sqrt(var / 36)
        mu, se, _ = h.hac_intercept(x, lags=3)
        self.assertAlmostEqual(mu / se, h.corrected_pipeline_t(uncorrected, 36), places=10)

    def test_holm_monotone(self):
        out = h.holm_adjust(pd.Series([.03, .01, .05, np.nan]))
        self.assertAlmostEqual(out[1], .03)
        self.assertAlmostEqual(out[0], .06)
        self.assertAlmostEqual(out[2], .06)
        self.assertTrue(np.isnan(out[3]))

    def test_incomplete_panel_is_rejected(self):
        frame = pd.DataFrame([{'representation': 'Grouped', 'mandate': 'Growth', 'strategy': 'SPY',
                               'period_end': '2024-01-31', 'net_return': .01}])
        with self.assertRaisesRegex(ValueError, 'missing strategies'):
            h.panel_for(frame, 'Grouped', 'Growth', ('SPY', 'T-bills'), 36)

    def test_end_to_end_h1_h2(self):
        tests, notes = h.run(synthetic_main(), draws=220, seed=1)
        self.assertEqual(len(tests), 36)
        self.assertEqual(sum(tests.family == 'H1 conventional MPT'), 24)
        self.assertEqual(sum(tests.family == 'H2 forecasting'), 12)
        self.assertTrue(any('H3 NOT TESTED' in n for n in notes))
        self.assertTrue((tests.n_months == 36).all())

    def test_own_risk_and_h3_families(self):
        robust = pd.DataFrame([dict(universe=u, representation=rep, mandate=man, model=m, ending_wealth=12000.,
                                    own_risk_mpt_wealth=11000., model_sharpe=1., own_risk_mpt_sharpe=.8,
                                    own_risk_mpt_complete=(m == h.DYNAMIC[0]), paired_hac_t=1.5)
                               for u in ('with_nvda', 'without_nvda') for rep in REPS for man in MANDATES for m in h.DYNAMIC])
        rng = np.random.default_rng(65)
        rows = []
        for rep in REPS:
            for man in MANDATES:
                for i in range(27):
                    common = float(rng.normal(.005, .02))
                    for s, ret in ((h.HYBRID, common + .003), (h.CONVENTIONAL, common), (h.TBILL, .002)):
                        rows.append(dict(representation=rep, mandate=man, strategy=s, period_end=month(i), net_return=ret))
        tests, _ = h.run(synthetic_main(), pd.DataFrame(rows), robust, draws=220, seed=1)
        own = tests[tests.family == 'H1 own-risk MPT']
        self.assertEqual(len(own), 6)  # with-NVDA complete paths only
        self.assertAlmostEqual(own.hac_t.iloc[0], 1.5 * math.sqrt(35 / 36))
        h3 = tests[tests.family == 'H3 information in MPT']
        self.assertEqual(len(h3), 6)
        self.assertTrue(np.allclose(h3.annual_mean_net_return_difference, .036))
        # The synthetic H3 gap is constant, so its HAC t (and p) is undefined; others must be adjusted.
        self.assertTrue(h3.hac_t.isna().all())
        self.assertTrue(tests[tests.family != 'H3 information in MPT'].holm_adjusted_p_within_family.notna().all())


if __name__ == '__main__':
    unittest.main()
