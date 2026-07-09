# OKF-Compatible Cross-Repo Knowledge Base Plan

Status: planned
Date: 2026-07-09

This document is the working plan for evolving the Fundus skill from a repository-local wiki helper into an OKF-compatible, cross-repository knowledge base workflow.

The chosen direction is Option B: keep the existing Obsidian-first workflow, preserve current `Fundus/{project}/` notes, and add first-class support for cross-repo areas such as epics, business domains, functional capabilities, interviews, user stories, decisions, and research logs.

## Goals

- Keep the current project discovery workflow working by default.
- Add explicit non-project scopes for epics, domains, capabilities, business processes, and other cross-repo knowledge.
- Make new and migrated notes compatible with the Open Knowledge Format v0.1 shape: Markdown files, YAML frontmatter, ordinary Markdown links, optional `index.md`, and optional `log.md`.
- Keep the wiki local, human-readable, and useful in Obsidian.
- Make the wiki easy for agents to scan, update, and reason over without loading too much context.
- Add a safe backup and curation workflow before any migration.
- Migrate existing notes deliberately, with reviewable decisions about keep, move, summarize, archive, or discard.

## Non-Goals

- Do not replace Obsidian with a hosted knowledge service.
- Do not require strict OKF-only conformance for every old note before the skill can work.
- Do not automatically migrate existing notes as part of the Option B implementation.
- Do not model a full Data Commons-style knowledge graph with formal entities, properties, observations, and provenance.
- Do not delete old notes during migration unless the user explicitly confirms deletion. Prefer archive or supersession.

## Design Principles

1. Backward compatible by default.
   Existing `Fundus/{project}/...` notes remain valid and searchable.

2. Helper-mediated writes.
   Agents must continue to use `scripts/fundus.py` or the MCP server. They should not write wiki notes directly.

3. Scopes, not fake projects.
   A cross-repo epic should be represented as an area scope, not by pretending the epic is a detected repository.

4. OKF-compatible, not OKF-rigid.
   New notes should have useful OKF-style frontmatter, but the local profile may add fields such as `id`, `scope`, `scope_path`, `projects`, `repos`, `status`, `aliases`, and `last_verified`.

5. Human first, agent friendly.
   Notes should read well in Obsidian and also be easy for agents to traverse through indexes, links, snippets, and stable metadata.

6. Migration is curation.
   Moving knowledge is a semantic decision. The migration phase must inspect existing notes, classify them, and apply reviewed changes.

7. Backup before mutation.
   Any migration or large-scale path rewrite starts with a restorable backup of the current wiki state.

## Vocabulary

- Project scope: the existing default scope. It is derived from the current repository and maps to `Fundus/{project}/`.
- Area scope: an explicit cross-repo scope selected by a path such as `Epics/AI Agent Templates`, `Domains/Invoicing`, or `Capabilities/Agent Templates`.
- Scope path: the path under `Fundus/` that bounds scans, creates, archive candidates, and curation work.
- Concept document: a normal Markdown note with frontmatter. This follows OKF language.
- Area index: an `index.md` file that explains what is inside an area and links to important notes.
- Area log: a `log.md` file that records meaningful changes and research activity for an area.
- Resource: an external asset represented by a note, such as a GitHub repository, Jira issue, Confluence page, API spec, dashboard, or source file.
- Curation decision: a migration action for an old note: keep, move, summarize, split, merge, archive, or delete after explicit confirmation.

## Target Fundus Shape

Keep the current project folders:

```text
Fundus/
  prompting-service/
  enrichment-hub/
```

Add cross-repo areas:

```text
Fundus/
  Epics/
    AI Agent Templates/
      index.md
      log.md
      overview.md
      decisions/
      open-questions/
      stories/
      interviews/
      domain-model/
      implementation-map/
      references/
  Domains/
    Invoicing/
      index.md
      log.md
  Capabilities/
    Agent Templates/
      index.md
      log.md
```

Project-local notes should describe repository-specific implementation details. Area notes should describe work that crosses repositories, stories, domains, teams, or product decisions.

## OKF-Compatible Local Profile

The written OKF v0.1 spec requires only a non-empty `type` field for concept documents. This local profile should be stricter for newly created notes while remaining tolerant of older notes.

Required for new notes:

```yaml
---
type: Epic
title: AI Agent Templates
description: Cross-repository knowledge for the AI Agent Templates epic.
id: epic/ai-agent-templates
scope: area
scope_path: Epics/AI Agent Templates
tags:
  - wiki
  - epic
  - ai-agent-templates
timestamp: 2026-07-09T00:00:00+02:00
created: 2026-07-09T00:00:00+02:00
updated: 2026-07-09T00:00:00+02:00
---
```

Recommended optional fields:

```yaml
resource: https://jira.example/browse/BACKEND-1234
projects:
  - prompting-service
  - enrichment-hub
repos:
  - prompting-service
  - enrichment-hub
aliases:
  - BACKEND-1234
status: active
owner: Christian
last_verified: 2026-07-09
```

Compatibility rules:

- Existing notes with only `title`, `created`, `updated`, `project`, and `tags` must continue to work.
- Unknown frontmatter keys must be preserved on update, archive, restore, and migration.
- `timestamp` should represent the last meaningful OKF-style content update.
- `updated` can remain the helper's operational timestamp.
- `id` should be stable across renames when possible.
- Canonical graph links should be normal Markdown links, because OKF consumers understand them. Funduslinks may exist as an extra convenience, but they should not be the only machine-readable link form.

## Note Types

Initial type vocabulary:

- `Project`: repository-local project or codebase overview.
- `Repo`: Git repository as a resource.
- `Service`: deployed service or runtime component.
- `Epic`: cross-story implementation or product initiative.
- `User Story`: Jira story or product slice.
- `Decision`: durable decision or ADR-like note.
- `Open Question`: unresolved product, domain, or implementation question.
- `Interview`: domain or stakeholder interview note.
- `Domain Concept`: business or technical domain concept.
- `Business Process`: business workflow or operational flow.
- `Capability`: functional capability spanning systems.
- `Implementation Map`: mapping from goal to repositories, modules, APIs, and tickets.
- `Runbook`: operational or repeatable procedure.
- `Research Note`: investigation findings.
- `Reference`: mirrored or summarized external material.

The type list is a local convention, not a registry. Consumers must tolerate unknown types.

## Workflow Model

### Project Discovery

Default behavior remains:

```bash
python scripts/fundus.py scan --query "authentication"
python scripts/fundus.py create --title "Authentication Flow" --content-file /tmp/note.md
```

Without an explicit area selector, the helper detects the current repository and targets `Fundus/{project}/`.

Project discovery should answer:

- What does this repository do?
- What are the main modules, APIs, jobs, and data flows?
- What local implementation details matter for future work?
- Which area notes, epics, decisions, and domain concepts does this project relate to?

### Area Discovery

Area behavior should be explicit:

```bash
python scripts/fundus.py scan --area "Epics/AI Agent Templates" --query "lineage"
python scripts/fundus.py create --area "Epics/AI Agent Templates" --title "Story Map" --content-file /tmp/story-map.md
```

Area discovery should answer:

- What is the overarching goal?
- Which repositories, services, tickets, decisions, and people are involved?
- What has been learned across stories?
- What remains unresolved?
- Where should future agents start?

### Business and Functional Discovery

Business/domain/capability areas use the same mechanism:

```bash
python scripts/fundus.py create --area "Domains/Invoicing" --title "Invoice Matching" --content-file /tmp/invoice-matching.md
python scripts/fundus.py create --area "Capabilities/Agent Templates" --title "Template Selection Flow" --content-file /tmp/template-selection.md
```

These areas are for knowledge that is not owned by one repository:

- domain language
- business processes
- cross-system capabilities
- stakeholder interviews
- product rules
- examples and edge cases

### Interviews

Interview notes should live under an area:

```text
Fundus/Epics/AI Agent Templates/interviews/2026-07-09-product-discovery.md
Fundus/Domains/Invoicing/interviews/2026-07-09-ap-clerk-workflow.md
```

Interview notes should include:

- context and participant role
- vocabulary used by the expert
- goals and pain points
- process steps
- rules and exceptions
- examples
- open questions
- follow-up actions

Interview outputs should be distilled into domain concepts, decisions, story maps, or open questions. The raw interview note should not be the only place where durable knowledge lives.

### User Stories

Story notes should live under the epic when they contribute to a cross-repo goal:

```text
Fundus/Epics/AI Agent Templates/stories/backend-2291.md
Fundus/Epics/AI Agent Templates/stories/backend-2292.md
```

Story notes should link to project-local implementation notes instead of duplicating every detail.

Recommended story sections:

- Goal
- Current Understanding
- Relevant Repos
- Implementation Touchpoints
- Decisions
- Open Questions
- Links

### Decisions

Decision notes should be small, durable, and easy to scan:

```text
Fundus/Epics/AI Agent Templates/decisions/0001-use-area-scopes.md
```

Recommended sections:

- Context
- Decision
- Consequences
- Alternatives Considered
- Links

### Logs

Every long-lived area may have a `log.md`.

The log is not a dumping ground. It records meaningful changes:

```markdown
# Area Log

## 2026-07-09

* **Discovery**: Created the initial AI Agent Templates epic area and linked existing project notes.
* **Decision**: Adopted area scopes for cross-repo knowledge.
* **Migration**: Classified old prompting-service notes related to BACKEND-2291 and BACKEND-2292.
```

Agents should update `log.md` when they materially change an area, complete a migration step, or synthesize an interview/story finding.

## Implementation Plan

### Phase 0: Backup Support

Add backup support before any migration or bulk rewrite.

Recommended helper commands:

```bash
python scripts/fundus.py backup create --label okf-option-b-pre-migration
python scripts/fundus.py backup list
python scripts/fundus.py backup inspect --id 2026-07-09T120000-okf-option-b-pre-migration
```

Recommended backup behavior:

- Snapshot the configured `Fundus/` directory.
- Store the backup outside the indexed wiki tree, for example `.fundus-backups/`.
- Include a manifest with timestamp, source vault, wiki dir, file count, byte count, and checksums.
- Never overwrite an existing backup.
- Exclude generated cache files when safe, but include Markdown notes and the current wiki index.
- Add restore planning support, but require explicit confirmation before restoring over active files.

Acceptance criteria:

- A backup can be created before migration.
- The backup path is reported clearly.
- The backup manifest can be inspected.
- Backup files are not included in normal wiki scans or index rebuilds.

### Phase 1: Scope Model

Introduce a scope abstraction in the helper.

Recommended model:

```text
project scope:
  selector: default or --project prompting-service
  path: Fundus/prompting-service

area scope:
  selector: --area "Epics/AI Agent Templates"
  path: Fundus/Epics/AI Agent Templates
```

Implementation tasks:

- Add a `Scope` dataclass or equivalent internal structure.
- Add safe area path resolution under `fundus_root_dir(config)`.
- Reject absolute area paths and paths containing `..`.
- Preserve the default project behavior when no area is passed.
- Add `scope`, `scope_path`, and `area` metadata to index entries.

Acceptance criteria:

- Existing project-mode tests still pass.
- `--area` cannot escape the configured wiki root.
- Area scope paths may contain nested directories and spaces.

### Phase 2: Recursive Scan and Index

Current scanning and indexing assume one Markdown level under `Fundus/{project}`. Area scopes need recursive traversal.

Implementation tasks:

- Replace `root.glob("*/*.md")` style indexing with recursive traversal.
- Exclude `_archive`, backup directories, generated visualizations, and other reserved helper files.
- Treat `index.md` and `log.md` as reserved OKF files. They may be indexed for search if useful, but they should not be treated as normal concept documents in strict OKF validation.
- Allow scans to filter by project scope or area path prefix.
- Keep archived notes excluded by default.

Acceptance criteria:

- `Fundus/Epics/AI Agent Templates/stories/backend-2292.md` appears in area scans.
- Project scans do not accidentally return unrelated area notes.
- Global or explicit broad scans can find both project and area notes.
- Index freshness detects nested notes.

### Phase 3: Create, Update, and Frontmatter Preservation

Implementation tasks:

- Add `--area` to `create`.
- Create area notes inside the selected area path.
- Add OKF-compatible frontmatter for new notes.
- Preserve unknown frontmatter keys during update, archive, restore, and migration operations.
- Keep `project` tags for project notes.
- Add area tags for area notes, for example `area/Epics/AI-Agent-Templates` or `epic/ai-agent-templates`.

Acceptance criteria:

- Old project note creation remains unchanged unless explicitly configured otherwise.
- New area notes get `type`, `title`, `description`, `id`, `scope`, `scope_path`, `tags`, `timestamp`, `created`, and `updated`.
- Existing OKF/local extension fields survive section replacement and rewrite.

### Phase 4: MCP Server

Mirror the helper behavior in `scripts/fundus_mcp.py`.

Implementation tasks:

- Add optional `area` parameters to scan, create, archive candidates, archive status, cleanup, and doctor tools where relevant.
- Return scope metadata in MCP responses.
- Keep project and project_root overrides.
- Keep MCP tools thin. The MCP server should call the same core helper functions, not reimplement path logic.

Acceptance criteria:

- MCP project scans match CLI project scans.
- MCP area scans match CLI area scans.
- MCP create can create an area note.
- MCP doctor can show the resolved project scope and selected area scope.

### Phase 5: Area Initialization and Logging

Add support for safely creating area skeletons.

Recommended command:

```bash
python scripts/fundus.py area init --area "Epics/AI Agent Templates" --type Epic --title "AI Agent Templates"
```

Generated structure:

```text
Fundus/Epics/AI Agent Templates/
  index.md
  log.md
  overview.md
  decisions/
  open-questions/
  stories/
  interviews/
  domain-model/
  implementation-map/
  references/
```

Acceptance criteria:

- Existing files are not overwritten.
- Initial files use the local OKF-compatible profile.
- `index.md` links to the key files.
- `log.md` records initialization.

### Phase 6: Archive and Move Semantics

Area notes need path-preserving archive behavior.

Implementation tasks:

- Archive area notes by mirroring the original path under `_archive`.
- Add or extend a helper-level move operation for curation.
- Record migration metadata such as `moved_from`, `moved_to`, or `supersedes` when useful.
- Decide whether moved notes leave stubs. Recommended default: leave a short stub for high-value notes and skip stubs for low-value or noisy notes.

Acceptance criteria:

- `Fundus/Epics/AI Agent Templates/foo.md` archives to `Fundus/_archive/Epics/AI Agent Templates/foo.md`.
- Restore returns the note to its original nested path.
- Move operations are atomic and update the index.
- Archive and move never escape the configured wiki root.

### Phase 7: Documentation and Skill Instructions

Update documentation after the code behavior is in place.

Files to update:

- `SKILL.md`
- `README.md`
- `docs/implementation.md`
- command docs in `commands/`
- MCP docs, if split out later

Documentation topics:

- when to use project scope
- when to use area scope
- OKF-compatible frontmatter profile
- area initialization
- log workflow
- interviews and story notes
- backup and migration workflow
- archive and restore behavior for nested areas
- MCP tool parity

Acceptance criteria:

- A future agent can use the updated skill without reading this plan.
- A human can understand the project vs area model from the README.
- The migration workflow is explicit and does not imply automatic migration.

### Phase 8: Verification

Expected test coverage:

- project scan/create/update remains backward compatible
- area path validation rejects unsafe paths
- area create writes to nested scope
- area scan works with and without index
- recursive index includes nested area notes
- index status detects stale nested notes
- unknown frontmatter keys are preserved
- archive mirrors nested area paths
- restore returns nested notes to original paths
- backup create/list/inspect works
- MCP parity for project and area tools

Run:

```bash
task verify
```

After implementation and approval, install the updated skill:

```bash
task install
```

## Migration Plan

Migration is a separate curation phase after Option B is implemented and verified.

### Migration Phase 0: Create Backup

Run the backup command and record the result:

```bash
python scripts/fundus.py backup create --label pre-okf-curation
```

Do not proceed until the backup exists and its manifest can be inspected.

### Migration Phase 1: Inventory

Create a machine-readable and human-readable inventory of current wiki notes.

Inventory fields:

- path
- title
- project
- tags
- created
- updated
- detected ticket IDs
- headings
- excerpt
- links
- candidate type
- candidate target scope
- curation decision

Recommended output:

```text
Fundus/_curation/2026-07-okf-migration/inventory.md
Fundus/_curation/2026-07-okf-migration/inventory.json
```

The `_curation` area should be excluded from normal project/area note creation unless explicitly requested.

### Migration Phase 2: Classify

Classify every current note into one of these actions:

- keep project-local
- move to area
- summarize into area and keep original
- split into multiple notes
- merge into an existing note
- archive as stale
- delete only after explicit confirmation

Suggested classification dimensions:

- repo-specific implementation detail
- cross-repo epic knowledge
- business/domain concept
- decision
- open question
- story/ticket detail
- temporary investigation
- stale or superseded content

### Migration Phase 3: Design Target Areas

Before moving notes, create the target area skeletons.

Initial target areas:

```text
Fundus/Epics/AI Agent Templates/
Fundus/Domains/Invoicing/
Fundus/Capabilities/Agent Templates/
```

Only create areas that are backed by discovered notes or current work.

### Migration Phase 4: Apply Curation in Batches

Apply migration in small batches.

Recommended batch order:

1. Create area skeletons and indexes.
2. Move or summarize high-confidence epic notes.
3. Link project notes to epic notes.
4. Extract durable decisions and open questions.
5. Move or summarize story notes.
6. Archive stale investigations.
7. Rebuild the index.
8. Review scan results and links.

Each batch should update the area `log.md`.

### Migration Phase 5: Review

Review after each batch:

- Can project scans still find repo-local knowledge?
- Can area scans find cross-repo knowledge?
- Does the area index provide a good starting point?
- Are old paths either still useful, archived, or linked to their replacement?
- Did any important context get duplicated in a confusing way?
- Does the log explain what changed?

### Migration Phase 6: Finalize

After curation:

- rebuild the index
- inspect index freshness
- run link checks if implemented
- archive or remove curation scratch files only after review
- document the final area structure in the relevant `index.md`

## Handling Intertwined Knowledge

Project and area notes should link to each other rather than duplicating everything.

Recommended pattern:

- Project note: "This repo implements part of [AI Agent Templates](../Epics/AI%20Agent%20Templates/overview.md)."
- Epic note: "The prompting-service implementation details live in [Prompting Service Agent Templates](../../prompting-service/agent-templates.md)."
- Story note: link to both the epic and project implementation notes.
- Decision note: link to affected projects, stories, and domain concepts.

Ownership rule:

- Put stable business meaning in domain or business areas.
- Put cross-story goal and status in epic areas.
- Put code-specific facts in project areas.
- Put raw discovery in interviews or research notes, then distill durable conclusions into concept, decision, story, or implementation-map notes.

## Open Questions

These should be decided before implementation or during the first implementation PR:

1. Backup location.
   Recommended: `.fundus-backups/` under the vault root, outside `Fundus/`, so backups are local but not indexed.

2. Area path casing.
   Recommended: keep human-friendly Obsidian paths such as `Epics/AI Agent Templates` rather than forcing lowercase OKF-style paths.

3. Move stubs.
   Recommended: leave stubs only for high-value moved notes whose old paths are likely to be remembered or linked.

4. Strictness of frontmatter for old notes.
   Recommended: validate new notes strictly, tolerate old notes, and add an optional repair/migration command.

5. Whether to add a dedicated curation command.
   Recommended: start with inventory and move support, then add higher-level curation automation only after one manual migration pass.

## Source References

- Google Cloud OKF announcement: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- OKF spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- OKF repository: https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
- Data Commons data model, for contrast with heavy graph modeling: https://docs.datacommons.org/data_model.html
