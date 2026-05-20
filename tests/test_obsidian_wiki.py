from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "obsidian_wiki.py"
SPEC = importlib.util.spec_from_file_location("obsidian_wiki", SCRIPT_PATH)
assert SPEC and SPEC.loader
obsidian_wiki = importlib.util.module_from_spec(SPEC)
sys.modules["obsidian_wiki"] = obsidian_wiki
SPEC.loader.exec_module(obsidian_wiki)


class WikiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name).resolve()
        self.config = obsidian_wiki.Config(
            vault_path=self.vault_path,
            wiki_dir="Wiki",
            default_tags=["wiki"],
            redaction_enabled=True,
            redaction_patterns=["API_KEY", "SECRET", "TOKEN", "PASSWORD"],
        )
        self.path = self.vault_path / "Wiki" / "demo" / "article.md"
        self.path.parent.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def read_document_body(self, path: Path) -> str:
        _, body = obsidian_wiki.parse_frontmatter(path.read_text())
        return body.strip()


class CreateDocumentTest(WikiTestCase):
    def create_article(self, title: str, body: str) -> Path:
        result = obsidian_wiki.create_document(self.config, "demo", title, body, None)
        return self.vault_path / result["path"]

    def test_create_removes_duplicate_leading_title_heading(self) -> None:
        path = self.create_article("Authentication Flow", "# Authentication Flow\n\n## Overview\n\nDetails")

        self.assertEqual(
            self.read_document_body(path),
            "# Authentication Flow\n\n## Overview\n\nDetails",
        )

    def test_create_removes_duplicate_title_heading_case_insensitively(self) -> None:
        path = self.create_article("Authentication Flow", "# authentication flow\n\nDetails")

        self.assertEqual(self.read_document_body(path), "# Authentication Flow\n\nDetails")

    def test_create_preserves_non_matching_leading_h1(self) -> None:
        path = self.create_article("Authentication Flow", "# Session Flow\n\nDetails")

        self.assertEqual(self.read_document_body(path), "# Authentication Flow\n\n# Session Flow\n\nDetails")

    def test_create_preserves_lower_level_heading_content(self) -> None:
        path = self.create_article("Authentication Flow", "## Overview\n\nDetails")

        self.assertEqual(self.read_document_body(path), "# Authentication Flow\n\n## Overview\n\nDetails")

    def test_create_preserves_plain_body_content(self) -> None:
        path = self.create_article("Authentication Flow", "Details")

        self.assertEqual(self.read_document_body(path), "# Authentication Flow\n\nDetails")


class UpdateDocumentTest(WikiTestCase):
    def write_article(self, body: str, frontmatter: str | None = None) -> None:
        metadata = frontmatter or "\n".join(
            [
                "---",
                "title: Article",
                "created: 2026-01-01T00:00:00+00:00",
                "updated: 2026-01-01T00:00:00+00:00",
                "project: demo",
                "tags:",
                "  - wiki",
                "  - project/demo",
                "---",
            ]
        )
        self.path.write_text(f"{metadata}\n\n{body}\n")

    def read_body(self) -> str:
        return self.read_document_body(self.path)

    def read_frontmatter(self) -> dict[str, object]:
        frontmatter, _ = obsidian_wiki.parse_frontmatter(self.path.read_text())
        return frontmatter

    def test_append_mode_adds_content_to_existing_body(self) -> None:
        self.write_article("# Article\n\nExisting")

        obsidian_wiki.update_document(
            self.config,
            "demo",
            "Wiki/demo/article.md",
            "append",
            "## New Findings\n\nMore detail",
            None,
        )

        self.assertEqual(self.read_body(), "# Article\n\nExisting\n\n## New Findings\n\nMore detail")

    def test_replace_mode_replaces_named_section(self) -> None:
        self.write_article("# Article\n\n## Details\n\nOld\n\n## Other\n\nKeep")

        obsidian_wiki.update_document(
            self.config,
            "demo",
            "Wiki/demo/article.md",
            "replace",
            "New",
            "Details",
        )

        self.assertEqual(self.read_body(), "# Article\n\n## Details\n\nNew\n## Other\n\nKeep")

    def test_replace_mode_requires_section(self) -> None:
        self.write_article("# Article")

        with self.assertRaisesRegex(obsidian_wiki.WikiError, "--section is required"):
            obsidian_wiki.update_document(
                self.config,
                "demo",
                "Wiki/demo/article.md",
                "replace",
                "New",
                None,
            )

    def test_rewrite_mode_replaces_complete_body(self) -> None:
        self.write_article("# Article\n\n## Old\n\nStale")

        result = obsidian_wiki.update_document(
            self.config,
            "demo",
            "Wiki/demo/article.md",
            "rewrite",
            "## Overview\n\nNew complete article body.",
            None,
        )

        self.assertEqual(result["mode"], "rewrite")
        self.assertIsNone(result["section"])
        self.assertEqual(self.read_body(), "## Overview\n\nNew complete article body.")

    def test_rewrite_mode_preserves_frontmatter_and_refreshes_updated(self) -> None:
        self.write_article("# Article\n\nOld")

        obsidian_wiki.update_document(
            self.config,
            "demo",
            "Wiki/demo/article.md",
            "rewrite",
            "New",
            None,
        )

        frontmatter = self.read_frontmatter()
        self.assertEqual(frontmatter["title"], "Article")
        self.assertEqual(frontmatter["created"], "2026-01-01T00:00:00+00:00")
        self.assertEqual(frontmatter["project"], "demo")
        self.assertEqual(frontmatter["tags"], ["wiki", "project/demo"])
        self.assertNotEqual(frontmatter["updated"], "2026-01-01T00:00:00+00:00")

    def test_rewrite_mode_fills_missing_project_and_tags(self) -> None:
        self.write_article(
            "# Article\n\nOld",
            "\n".join(
                [
                    "---",
                    "title: Article",
                    "created: 2026-01-01T00:00:00+00:00",
                    "updated: 2026-01-01T00:00:00+00:00",
                    "---",
                ]
            ),
        )

        obsidian_wiki.update_document(
            self.config,
            "demo",
            "Wiki/demo/article.md",
            "rewrite",
            "New",
            None,
        )

        frontmatter = self.read_frontmatter()
        self.assertEqual(frontmatter["project"], "demo")
        self.assertEqual(frontmatter["tags"], ["wiki", "project/demo"])

    def test_rewrite_mode_redacts_secrets(self) -> None:
        self.write_article("# Article\n\nOld")

        obsidian_wiki.update_document(
            self.config,
            "demo",
            "Wiki/demo/article.md",
            "rewrite",
            "API_KEY=super-secret-token",
            None,
        )

        self.assertEqual(self.read_body(), "API_KEY: [REDACTED]")

    def test_update_missing_document_raises_error(self) -> None:
        with self.assertRaisesRegex(obsidian_wiki.WikiError, "Document does not exist"):
            obsidian_wiki.update_document(
                self.config,
                "demo",
                "Wiki/demo/missing.md",
                "rewrite",
                "New",
                None,
            )

    def test_update_document_without_frontmatter_raises_error(self) -> None:
        self.path.write_text("# Article\n\nNo frontmatter\n")

        with self.assertRaisesRegex(obsidian_wiki.WikiError, "missing expected frontmatter"):
            obsidian_wiki.update_document(
                self.config,
                "demo",
                "Wiki/demo/article.md",
                "rewrite",
                "New",
                None,
            )


if __name__ == "__main__":
    unittest.main()
