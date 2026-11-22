"""Keep the Forge-style lane and merge discipline executable."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "merge_policy.py"
SPEC = importlib.util.spec_from_file_location("cad_merge_policy", PATH)
policy = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
import sys
sys.modules[SPEC.name] = policy
SPEC.loader.exec_module(policy)


class MergePolicyTests(unittest.TestCase):
    def test_direct_lane_promotions_use_normal_merge_and_retain_head(self):
        for lane in ("dev-cad", "dev-ci"):
            with self.subTest(lane=lane):
                got = policy.evaluate(base="main", head=lane)
                self.assertEqual(got.merge_method, "merge")
                self.assertTrue(got.direct_lane_promotion)
                self.assertFalse(got.cleanup_head)
                self.assertTrue(got.integrate_base)

    def test_feature_work_is_squashed_into_development_lanes(self):
        for lane in ("dev-cad", "dev-ci"):
            with self.subTest(lane=lane):
                got = policy.evaluate(base=lane, head="feature/abc")
                self.assertEqual(got.merge_method, "squash")
                self.assertFalse(got.direct_lane_promotion)
                self.assertTrue(got.cleanup_head)
                self.assertTrue(got.integrate_base)

    def test_temporary_ci_and_documentation_branches_can_be_cleaned(self):
        for head in ("ci/174-stage0-lanes-contract", "docs/site", "fix/abc"):
            got = policy.evaluate(base="dev-ci", head=head)
            self.assertTrue(got.cleanup_head)

    def test_permanent_and_backup_branches_never_cleaned(self):
        for head in ("main", "dev-cad", "dev-ci", "build", "gh-pages", "backup/old-pages"):
            got = policy.evaluate(base="main", head=head)
            self.assertFalse(got.cleanup_head)

    def test_non_lane_pr_into_main_is_not_promoted_as_normal_merge(self):
        got = policy.evaluate(base="main", head="feature/sample")
        self.assertEqual(got.merge_method, "squash")
        self.assertFalse(got.direct_lane_promotion)

    def test_unrelated_pr_does_not_require_lane_integration(self):
        got = policy.evaluate(base="topic", head="feature/sample")
        self.assertFalse(got.integrate_base)


if __name__ == "__main__":
    unittest.main()
