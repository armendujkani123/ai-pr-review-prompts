import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pr_review_cli


class PRReviewCLITests(unittest.TestCase):
    def test_list_modes_contains_general(self) -> None:
        self.assertIn("general", pr_review_cli.list_modes())

    def test_load_mode_raises_for_invalid_mode(self) -> None:
        with self.assertRaises(ValueError):
            pr_review_cli.load_mode("invalid")

    def test_build_prompt_payload_contains_review_mode(self) -> None:
        payload = pr_review_cli.build_prompt_payload(
            title="Add JWT refresh endpoint",
            summary="Introduces refresh token flow",
            mode="security",
            changed_files="app/auth.py\ntests/test_auth.py",
            context="Used by web and mobile clients",
        )
        self.assertEqual(payload["review_mode"], "security")
        self.assertIn("JWT refresh", payload["pull_request_title"])
        self.assertIn("web and mobile clients", payload["context"])
        self.assertIn("authentication and authorization", payload["mode_guidance"])

    def test_main_lists_modes(self) -> None:
        buffer = StringIO()
        with redirect_stdout(buffer):
            exit_code = pr_review_cli.main(["--list-modes"])
        self.assertEqual(exit_code, 0)
        self.assertIn("release_risk", buffer.getvalue())

    def test_main_renders_json(self) -> None:
        buffer = StringIO()
        with redirect_stdout(buffer):
            exit_code = pr_review_cli.main(
                [
                    "--title",
                    "Refactor checkout flow",
                    "--summary",
                    "Moves discount logic into a service object",
                    "--output-format",
                    "json",
                ]
            )
        self.assertEqual(exit_code, 0)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["review_mode"], "general")
        self.assertIn("Refactor checkout flow", payload["pull_request_title"])

    def test_main_reads_summary_from_file_and_writes_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            summary_path = Path(tmpdir) / "summary.txt"
            output_path = Path(tmpdir) / "prompt.md"
            summary_path.write_text("Backfills a nullable column and updates reads", encoding="utf-8")

            buffer = StringIO()
            with redirect_stdout(buffer):
                exit_code = pr_review_cli.main(
                    [
                        "--title",
                        "Update data migration",
                        "--from-file",
                        str(summary_path),
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertIn("Prompt written to", buffer.getvalue())
            self.assertIn("Update data migration", output_path.read_text(encoding="utf-8"))

    def test_parse_args_supports_version_flag(self) -> None:
        with self.assertRaises(SystemExit) as exc:
            pr_review_cli.parse_args(["--version"])
        self.assertEqual(exc.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
