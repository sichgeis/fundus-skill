# Fundus Codex Plugin Roadmap

Status: refined after DDD interview
Date: 2026-07-09

## Target Picture

Fundus should become Christian's personal Codex workbench for durable work knowledge. It should feel native in Codex, but it should remain explicit: the user invokes it to search, save, retrieve, update, or curate knowledge. During ticket and research work, Codex may also perform a read-only Fundus lookup when prior context is likely useful.

Fundus is evidence, not authority. Source code is the primary source of truth for implemented behavior. Jira, GitHub, source code, interviews, and user-provided context can all update Fundus, but Fundus should never silently override fresher primary evidence.

The first satisfying release should include:

- A canonical `Fundus/` corpus migrated from the existing `Wiki/` corpus.
- Strict enough OKF compatibility for active concept notes.
- Strict OKF reserved-file cleanup for `index.md` and `log.md`.
- Quiet preservation of archived notes under `Fundus/_archive/`.
- A compact, MCP-first Codex skill packaged as a local plugin.
- Snappy core workbench flows for search, save, update, and stale-note proposals.

Team sharing and complex graph visualization are explicitly out of scope for the first release.

## Current Corpus Findings

The live personal work knowledge base currently lives at:

```text
/Users/christian/vault/Hypatos/Wiki
```

The current Fundus config points to:

```text
/Users/christian/vault/Hypatos/Fundus
```

That `Fundus/` directory does not exist yet. The migration from `Wiki/` to `Fundus/` is therefore not optional; it is part of the setup path before the plugin can feel coherent.

Read-only inspection on 2026-07-09 found:

- 217 Markdown files under `Wiki/`.
- 158 active notes and 59 archived notes.
- No files missing frontmatter entirely.
- All active notes have `type`, `title`, `tags`, `scope`, `scope_path`, and timestamps.
- 49 archived legacy notes are missing `type`.
- Active project, domain, epic, decision, and operations areas already use useful folder structure.
- Existing `index.md` and `log.md` files have frontmatter today, but strict OKF treats them as reserved files rather than ordinary concept documents.
- No notes currently use `aliases`, `resource`, or `last_verified`.
- A few notes use "Sources used"; none use OKF's conventional `# Citations` heading.

Conclusion: the corpus is already agent-traversable, but it needs a canonical `Fundus/` location, an index, strict reserved-file cleanup, and a few metadata improvements for future retrieval.

## Product Decisions

### Workbench Role

Fundus is primarily an explicit workbench tool.

Core first-release intents:

- "Search Fundus for X."
- "Save this into Fundus."
- "Update the relevant Fundus note with what we learned."
- "This Fundus note seems stale; propose a correction."

Natural save intent should also work. Phrases such as "remember this", "document this", "save this", or "put this into Fundus" may create or update Fundus notes when the current context is clearly durable work knowledge.

If the save intent is casual, personal, or not clearly work-related, Codex should ask instead of writing to Fundus.

### Evidence Behavior

When Fundus is used in research:

- Treat Fundus as evidence when the note is current and directly relevant.
- Mention Fundus briefly when it materially influenced the answer.
- Prefer a short citation, for example: "Fundus has related context in `Prompt Authoring`; it frames this as an authoring-surface boundary."
- Do not include a large evidence block unless asked.
- If Fundus was checked opportunistically and nothing useful was found, silence is fine.
- If the user explicitly asks to search Fundus, report the result even when no relevant note exists.

### Source Hierarchy

Use this source hierarchy when Fundus and current work disagree:

1. Source code for implemented behavior.
2. Current primary work sources such as Jira, GitHub, Confluence, Slack, interviews, or the user's direct statement.
3. Fundus as contextual evidence and discussion history.

If Fundus appears stale or contradicted by code, Codex should propose a concise natural-language update. It should not patch Fundus by default during ordinary research.

Codex may update Fundus automatically when the user explicitly grants broad update intent, for example: "we learned X, update everything relevant", "update Jira and Fundus", or "document this in Fundus". In that case, Codex should summarize the Fundus changes afterward.

### Scope Inference

Low friction matters. When scope is not explicit, Codex should infer the likely Fundus placement from the whole conversation, then report where it saved.

Signals:

- Conversation intent is the strongest signal.
- Current repository is a strong signal for implementation-local knowledge.
- Ticket IDs, epic names, domain terms, and area names are supporting signals.
- Discovery, interview, strategy, domain, or cross-repository work should usually go to an area.
- Code behavior, repo architecture, tests, and implementation details should usually go to the current project.

The user can correct placement later through a move workflow.

### Retrieval Behavior

Start with tiered retrieval:

- Use the best active Fundus match when confidence is good.
- If confidence is uncertain and the task matters, inspect a bounded number of additional plausible matches automatically.
- Do not interrupt the user to ask whether to search wider.
- Keep the final answer compact.
- Mention additional candidates only briefly when relevant.

Archived notes are preserved but quiet:

- Migrate archives to `Fundus/_archive/`.
- Exclude archives from normal search.
- Include archived notes only when the user explicitly asks for archived, stale, historical, or recovery context.
- Archived notes should not be treated as normal evidence.

### Write Completion

The human-facing confirmation after a write should be short, often just the title or path.

The note itself must be good enough for agents:

- OKF-compatible frontmatter on active concept notes.
- Strong title and useful description.
- Scope and tags that make later lookup easy.
- Ordinary Markdown links for relationships.
- Citations or source sections when the note body relies on important source material.

## OKF And Local Profile

The public OKF v0.1 shape is intentionally small: Markdown files, YAML frontmatter, a required non-empty `type` field for concept documents, optional recommended metadata, ordinary Markdown links, optional `index.md`, and optional `log.md`.

Fundus should be OKF-compatible, but stricter for active concept notes because agents traverse the corpus.

Required for new active non-reserved notes:

```yaml
---
type: Research
title: Example Title
description: Short useful retrieval summary.
id: project/example-repo/example-title
scope: project
scope_path: example-repo
created: 2026-07-09T00:00:00+02:00
updated: 2026-07-09T00:00:00+02:00
timestamp: 2026-07-09T00:00:00+02:00
project: example-repo
tags:
  - fundus
  - project/example-repo
---
```

Area notes omit `project` and use area scope:

```yaml
---
type: Domain
title: Prompt Authoring
description: Stable domain context for prompt authoring concepts and boundaries.
id: area/domains/prompt-authoring/overview
scope: area
scope_path: Domains/Prompt Authoring
created: 2026-07-09T00:00:00+02:00
updated: 2026-07-09T00:00:00+02:00
timestamp: 2026-07-09T00:00:00+02:00
tags:
  - fundus
  - area/domains/prompt-authoring
  - prompt-authoring
---
```

Recommended optional fields:

```yaml
aliases:
  - BACKEND-2291
resource: https://jira.example/browse/BACKEND-2291
status: active
owner: Christian
last_verified: 2026-07-09
projects:
  - prompting-service
repos:
  - prompting-service
```

Rules:

- Preserve unknown frontmatter keys.
- Do not force strict normalization on archived legacy notes unless it is cheap and automatic.
- Active `index.md` and `log.md` are reserved files and should not have frontmatter after cleanup.
- Concept metadata belongs in regular notes such as `overview.md`, not in reserved files.
- Use normal Markdown links for graph relationships.
- Prefer `# Citations` when a note needs source provenance.

## Target Architecture

```text
Fundus corpus
├── project-name/
│   ├── index.md              # reserved, no frontmatter
│   ├── overview.md           # concept note with frontmatter
│   └── research-note.md      # concept note with frontmatter
├── Domains/
│   └── Prompt Authoring/
│       ├── index.md          # reserved, no frontmatter
│       ├── log.md            # reserved, no frontmatter
│       ├── overview.md       # concept note with frontmatter
│       └── domain-model/
└── _archive/
    └── ...
```

Plugin package:

```text
fundus plugin
├── .codex-plugin/plugin.json
├── skills/fundus/SKILL.md
├── skills/fundus/agents/openai.yaml
├── scripts/fundus.py
├── scripts/fundus_mcp.py
├── config.example.json
├── requirements.txt
└── docs/reference/*.md
```

Runtime flow:

```text
user asks to save or consult durable knowledge
  -> Codex selects Fundus skill
  -> Fundus skill prefers MCP
  -> MCP scans indexed active Fundus metadata
  -> Codex reads only likely matches
  -> MCP create/update writes through Fundus domain functions
  -> affected index entry refreshes
  -> Codex confirms briefly
```

Fallback flow:

```text
MCP unavailable
  -> skill uses installed helper directly
  -> read-only commands run normally
  -> write-like commands use explicit sandbox escalation when vault is outside workspace
```

## Implementation Roadmap

### P0 - Migration Design And Safety

Status: planned

Spec:

- Add a one-time Wiki to Fundus migration workflow outside normal plugin usage.
- Source: `/Users/christian/vault/Hypatos/Wiki`.
- Destination: `/Users/christian/vault/Hypatos/Fundus`.
- Create a backup before mutating or removing any source files.
- Stage migration into a temporary destination before promotion.
- Preserve active notes and archived notes.
- Exclude archived notes from normal retrieval after migration.
- Remove or retire old `Wiki/` as a live source after successful verification, keeping backup recovery.

Acceptance criteria:

- Backup exists and can be inspected.
- Migration can run without hand-reviewing every note.
- `Fundus/` becomes canonical after verification.
- Old `Wiki/` no longer remains as a parallel live source.

### P1 - Migration Transformation Rules

Status: planned

Spec:

- Copy all active non-archive notes into equivalent `Fundus/` paths.
- Copy archived notes under `Fundus/_archive/`.
- For active non-reserved notes, ensure the local OKF-compatible profile:
  - `type`
  - `title`
  - `description`
  - `id`
  - `scope`
  - `scope_path`
  - `created`
  - `updated`
  - `timestamp`
  - `tags`
  - `project` for project scope only
- For active reserved files named `index.md` or `log.md`, remove frontmatter and preserve body.
- Preserve unknown fields on concept notes.
- Convert `wiki` default tags to `fundus` where appropriate.
- Preserve existing Markdown links.
- Do not over-normalize archived legacy notes unless cheap.

Acceptance criteria:

- Active concept files parse cleanly and have non-empty `type`.
- Active reserved `index.md` and `log.md` have no frontmatter.
- Archive files are present under `Fundus/_archive/`.
- Archive metadata remains enough to identify archived status.

### P2 - Migration Verification

Status: planned

Spec:

- Add structural verification:
  - file counts by active/archive/reserved/concept
  - parseable frontmatter for active concept notes
  - no active concept note missing `type`
  - no active reserved file with frontmatter
  - no path escapes
- Add retrieval smoke tests:
  - project lookup, for example `prompting-service`
  - ticket lookup, for example `BACKEND-2291`
  - epic lookup, for example `AI Agent Templates`
  - domain lookup, for example `Prompt Authoring`
  - archive lookup with explicit archive flag
- Build or rebuild the search index after migration.

Acceptance criteria:

- Structural verification passes.
- Smoke searches return expected active notes.
- Archive lookup works only when explicitly requested.
- `doctor` reports the canonical `Fundus/` root and a valid index.

### P3 - Core Helper And Index Behavior

Status: planned

Spec:

- Make `Fundus/` the canonical configured directory.
- Ensure `scan` defaults to active notes only.
- Keep `--include-archived` explicit.
- Index headings, title, description, tags, ticket IDs, aliases, resource, path, scope, scope path, and a short body excerpt.
- Add or improve confidence/reason metadata so Codex can decide whether to read one or a few candidates.
- Keep scan outputs compact by default.
- Make snippets opt-in or tightly bounded.

Acceptance criteria:

- Common scans return compact JSON.
- Relevant active notes rank above archive or weak matches.
- Ticket IDs and aliases are strong retrieval signals.
- Scan output supports brief Fundus citation without reading many files.

### P4 - Compact Skill For Progressive Disclosure

Status: planned

Spec:

- Rewrite `SKILL.md` as a compact workbench contract.
- Keep only trigger rules, source hierarchy, scope inference, retrieval behavior, write behavior, stale-note behavior, and fallback behavior in the main skill.
- Move command catalogs and maintenance instructions to references.
- Include the four core intents:
  - search Fundus
  - save into Fundus
  - update relevant Fundus note
  - propose correction for stale Fundus note
- Make the first 20 lines enough for Codex to choose correctly.

Acceptance criteria:

- `SKILL.md` is materially shorter.
- Natural durable save intent triggers Fundus when appropriate.
- The skill says source code wins over Fundus.
- The skill says stale notes are proposed, not silently rewritten, unless broad update intent is explicit.

### P5 - MCP Happy Path

Status: planned

Spec:

- Add concise MCP server instructions.
- Keep the first 512 characters self-contained:
  - scan first
  - prefer update over duplicate create
  - write only through Fundus tools
  - respect project/area scoping
  - source code wins over Fundus
- Review MCP tool names and descriptions for compactness.
- Return compact write results: title, path, scope, changed mode, updated timestamp, and warnings.
- Keep maintenance tools available, but make normal workflows prefer search/read/create/update/doctor.

Acceptance criteria:

- Normal search/save/update flows complete through MCP without shell commands.
- MCP output is compact enough for repeated use.
- Tests cover representative read/write wrappers and server construction.

### P6 - Plugin Package Skeleton

Status: planned

Spec:

- Add `.codex-plugin/plugin.json`.
- Generate plugin runtime layout in `dist/fundus-plugin`.
- Package the Fundus skill under `skills/fundus/`.
- Bundle the local stdio MCP server in the plugin manifest.
- Add local marketplace metadata for testing.
- Keep direct skill install available until plugin install is proven.

Acceptance criteria:

- Codex can see Fundus as a local plugin.
- Installing the plugin exposes the Fundus skill.
- Plugin-provided MCP config launches `fundus_mcp.py` without manual global MCP config.
- Direct skill install still works during transition.

### P7 - Snappy Install And Dev Loop

Status: planned

Spec:

- Add build tasks for:
  - skill package
  - plugin package
  - local marketplace refresh
  - migration dry-run
  - migration apply
  - verification
- Add a tiny MCP smoke check using `fundus_mcp.py --check`.
- Add dependency diagnostics for missing Python MCP SDK.
- Update README with the direct skill path, migration path, and plugin install path.

Acceptance criteria:

- `task verify` checks helper, MCP, tests, and plugin package shape.
- A local plugin refresh is one command.
- README explains what requires restart or approval.

### P8 - Permission And Vault Friction

Status: planned

Spec:

- Document command approval, filesystem sandboxing, MCP tool approval, and plugin install as separate concerns.
- Recommend a personal setup:
  - either add the vault as a writable Codex root, or
  - keep explicit write escalation for write-like operations.
- Provide Codex Rules examples for helper fallback.
- Provide MCP tool approval guidance for read-only and write-like tools.
- Keep permission prompts stable by avoiding shell wrappers and inline multiline content.

Acceptance criteria:

- Routine Fundus writes do not surprise the user with repeated differently shaped approval prompts.
- Read-only search does not need write escalation.
- Write-like fallback commands use the exact installed helper shape.

### P9 - Token Budget And Output Audit

Status: planned

Spec:

- Measure loaded `SKILL.md` size.
- Measure MCP instructions and tool metadata footprint.
- Measure representative scan/read/update outputs.
- Reduce noisy fields in scan output.
- Keep final answers compact:
  - brief Fundus citation when used
  - brief write confirmation after saves
  - brief stale-note suggestion when needed

Acceptance criteria:

- Common save/update flows read no more than one to three candidate notes.
- Common research flows cite Fundus briefly when relevant.
- No-result opportunistic checks can remain silent.

### P10 - First-Release Workbench Polish

Status: planned

Spec:

- Make the four core intents feel excellent:
  - search
  - save
  - update
  - stale-note proposal
- Add examples/tests for natural save intent.
- Add examples/tests for scope inference.
- Add examples/tests for tiered retrieval.
- Add examples/tests for stale-note proposal behavior.

Acceptance criteria:

- "Search Fundus for BACKEND-2291" returns concise relevant context.
- "Remember this domain rule" saves or updates the inferred area note in work contexts.
- "Update the relevant Fundus note with what we learned" updates and summarizes briefly.
- A stale note found during code research produces a concise proposal, not an automatic mutation.

## Backlog Checklist

### Migration

- [ ] Add Wiki to Fundus migration dry-run.
- [ ] Add pre-migration backup.
- [ ] Add staged migration apply.
- [ ] Copy active notes to `Fundus/`.
- [ ] Copy archived notes to `Fundus/_archive/`.
- [ ] Remove frontmatter from active `index.md` and `log.md`.
- [ ] Normalize active concept frontmatter to the Fundus local OKF-compatible profile.
- [ ] Preserve unknown concept-note frontmatter fields.
- [ ] Convert default `wiki` tags to `fundus` tags where appropriate.
- [ ] Build the Fundus index after migration.
- [ ] Verify structure and retrieval smoke tests.
- [ ] Retire old `Wiki/` as a live source after successful migration.

### Retrieval And Evidence

- [ ] Ensure normal scans exclude archives.
- [ ] Keep archive lookup explicit.
- [ ] Add compact match reasons and confidence signals.
- [ ] Index aliases, resources, ticket IDs, headings, links, and short excerpts.
- [ ] Add brief Fundus citation guidance to the skill.
- [ ] Add stale-note proposal guidance to the skill.

### Writes

- [ ] Make create/update output compact.
- [ ] Support natural durable save intent in skill instructions.
- [ ] Encode source hierarchy in skill instructions.
- [ ] Keep direct note editing forbidden.
- [ ] Add optional `aliases`, `resource`, `status`, `owner`, and `last_verified` support where useful.

### Plugin

- [ ] Add plugin manifest.
- [ ] Generate plugin runtime layout in `dist/fundus-plugin`.
- [ ] Bundle skill and MCP server.
- [ ] Add local marketplace metadata.
- [ ] Add plugin verification task.
- [ ] Keep direct skill install until plugin path is proven.

### Documentation

- [ ] Keep README current as migration and plugin packaging land.
- [ ] Keep implementation docs current as helper, MCP, migration, and plugin architecture land.
- [ ] Split long skill reference material into `docs/reference/`.
- [ ] Document permission model clearly.
- [ ] Document first-release out-of-scope items: team sharing and complex graph visualization.

## Open Implementation Choices

These are implementation choices, not product/domain blockers:

1. Whether migration is a `fundus.py migrate wiki-to-fundus` subcommand or a separate one-time script.
2. The exact old `Wiki/` retirement shape after successful migration. Prefer the simplest safe option after backup and verification; do not spend effort on elaborate archive curation.
3. Whether archived legacy notes missing `type` get a cheap `type: Note` during migration or remain as-is.
4. Whether `last_verified` should be automatically set only after source-code inspection, or also after Jira/GitHub/Confluence verification.
5. Whether plugin packaging should include all maintenance MCP tools enabled by default or rely on guidance to keep normal workflows focused.

## Source References

- Google Cloud OKF announcement: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- OKF specification: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- OKF repository: https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
- Data Commons data model, used only as contrast for heavier graph modeling: https://docs.datacommons.org/data_model.html

## Suggested Execution Order

1. Implement migration dry-run, backup, apply, and verification.
2. Run migration from `Wiki/` to `Fundus/` and verify.
3. Rebuild the index and make `Fundus/` canonical.
4. Compact `SKILL.md` and move long references out.
5. Make MCP the happy path and compact tool outputs.
6. Add plugin packaging and local marketplace metadata.
7. Update README and implementation docs.
8. Run token/output audit.
9. Polish the four first-release workbench intents.
