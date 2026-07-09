---
name: document
description: Document a project topic into Fundus
---

Document the requested topic for the current project in the Fundus.

Use the command arguments as the topic. If the arguments are unavailable, infer the topic from the text after `document` in the user's message.

Use the `fundus` skill. Inspect the current repository enough to document the topic accurately, then scan existing Fundus pages before deciding whether to update or create a note.

Default to the current project scope. If the user explicitly asks for an epic, domain, capability, interview, story-map, or other cross-repository area, use the helper with `--area "..."` and scan that area before creating or updating a note.

For requests like "all unit tests of the project", document the test layout, frameworks, major test groups, fixtures/helpers, and relevant commands. Summarize tests by behavior or subsystem instead of listing every assertion unless the project is small.

Never write Fundus files directly. Use the installed `scripts/fundus.py` scan/read/create/update workflow from the `fundus` skill. End by telling the user which vault-relative Fundus note path was created or updated.
