"""Contract for the CAD wrapper around the released shared merge policy."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "merge-policy.yml"
LOCAL_POLICY = ROOT / "scripts" / "merge_policy.py"
ACCEPTED_TOOL_SHA = "b1474f6be66dc0236f2a5c2555af07a100447255"


class MergePolicyTests(unittest.TestCase):
    def test_owner_only_merge_command_calls_exact_released_policy(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("issue_comment:", workflow)
        self.assertIn("github.event.comment.body == '/merge'", workflow)
        self.assertIn("github.actor == github.repository_owner", workflow)
        self.assertIn("checks: read", workflow)
        self.assertIn("statuses: read", workflow)
        self.assertIn("actions: write", workflow)
        self.assertIn(
            "uses: brainboxemb/tool.cad.ci/.github/workflows/"
            f"reusable-merge-policy.yml@{ACCEPTED_TOOL_SHA}",
            workflow,
        )
        self.assertIn("command: ${{ github.event.comment.body }}", workflow)
        self.assertIn(
            "pull_request_number: ${{ github.event.issue.number }}",
            workflow,
        )

    def test_wrapper_supplies_only_cad_repository_configuration(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for value in (
            "stable_ref: main",
            """lane_refs_json: '["dev-cad","dev-ci"]'""",
            """permanent_refs_json: '["build","gh-pages"]'""",
            """temporary_prefixes_json: '["issue/","fix/","feature/","accept/","promote/","ci/","docs/","chore/"]'""",
            "integration_workflow: cad.yml",
        ):
            self.assertIn(value, workflow)

        self.assertNotIn("runs-on:", workflow)
        self.assertNotIn("gh api ", workflow)
        self.assertNotIn("check-runs?per_page=100", workflow)
        self.assertNotIn("merge_method", workflow)

    def test_no_cad_local_merge_policy_engine_remains(self):
        self.assertFalse(LOCAL_POLICY.exists())


if __name__ == "__main__":
    unittest.main()
