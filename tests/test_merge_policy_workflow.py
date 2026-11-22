"""Executable contract for the owner-only /merge workflow."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "merge-policy.yml"


class MergePolicyWorkflowTests(unittest.TestCase):
    def test_owner_only_command_requires_green_exact_head(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("issue_comment:", text)
        self.assertIn("github.event.comment.body == '/merge'", text)
        self.assertIn("github.actor == github.repository_owner", text)
        self.assertIn("checks: read", text)
        self.assertIn("statuses: read", text)
        self.assertIn("scripts/merge_policy.py", text)
        self.assertIn("check-runs?per_page=100", text)
        self.assertIn("group_by(.name)", text)
        self.assertIn("map(last)", text)
        self.assertIn('sha="$HEAD_SHA"', text)
        self.assertIn('merge_method="$METHOD"', text)

    def test_lane_lifecycle_is_policy_driven(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("DIRECT_PROMOTION", text)
        self.assertIn("CLEANUP_HEAD", text)
        self.assertIn("long-lived lane advanced to merge commit", text)
        self.assertIn("long-lived lane recreated at merge commit", text)
        self.assertIn("temporary head deleted", text)
        self.assertNotIn('HEAD_REF" = "dev-cad"', text)
        self.assertNotIn('HEAD_REF" = "dev-ci"', text)

    def test_accepted_source_refs_are_explicitly_dispatched(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("actions: write", text)
        self.assertIn("INTEGRATE_BASE", text)
        self.assertIn("actions/workflows/cad.yml/dispatches", text)
        self.assertIn('-f ref="$BASE_REF"', text)
        self.assertIn('-f ref="$HEAD_REF"', text)
        self.assertIn("Integration dispatched: %s", text)


if __name__ == "__main__":
    unittest.main()
