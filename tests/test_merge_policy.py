"""Keep the CAD merge-policy wrapper thin and pinned to the accepted owner release."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "merge-policy.yml"
LOCAL_POLICY = ROOT / "scripts" / "merge_policy.py"
ACCEPTED_TOOL_SHA = "eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9"


class MergePolicyTests(unittest.TestCase):
    def test_wrapper_uses_exact_released_shared_policy(self):
        workflow = WORKFLOW.read_text()
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
        workflow = WORKFLOW.read_text()
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
        self.assertNotIn("merge_method", workflow)

    def test_no_cad_local_merge_policy_engine_remains(self):
        self.assertFalse(LOCAL_POLICY.exists())


if __name__ == "__main__":
    unittest.main()
