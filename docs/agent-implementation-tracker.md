# Fundus Agent Implementation Tracker

Status: active remediation and second-release tracker
Date: 2026-07-10
First active phase: P11

## Agent read order

1. `README.md`
2. `docs/agent-implementation-tracker.md`
3. `docs/fundus-target-picture.md`
4. `docs/decision-record.md`
5. `docs/architecture-invariants.md`
6. `docs/implementation.md`
7. `docs/testing-and-validation.md`
8. source and tests

## Tracker rules

Status values:

```text
done
in_progress
ready
planned
blocked
deferred
superseded
```

Rules:

1. Work on the first `ready` phase unless the user names another.
2. Do not mark a phase done until all acceptance criteria pass.
3. Record commands, test results, and important manual evidence.
4. Add or update tests with every behavior change.
5. Update `docs/implementation.md` when current behavior changes.
6. Update `README.md`, `SKILL.md`, examples, and manifests only when user-facing behavior changes.
7. Change the target picture only for a durable decision change.
8. Never run implementation tests against the live Hypatos Fundus corpus.
9. Preserve CLI and MCP compatibility where practical, but do not preserve an unsafe or non-conformant behavior merely because it exists.
10. Keep each implementation pass scoped to one phase or a tightly coupled dependency.
11. Run focused tests during work and `task verify` before phase completion.
12. If official host or protocol documentation has changed, update the source references and record the resulting decision.

## Review correction

The previous tracker stated that no known first-release gaps remained. The 2026-07-10 review identified protocol, packaging, path, corpus, search, and concurrency gaps. That earlier statement is superseded by this tracker.

## Baseline retained from P0-P10

The existing project already delivered substantial capabilities:

| Historical phase | Status | Retained outcome |
| --- | --- | --- |
| P0 | done | staged Wiki-to-Fundus migration with backup and retirement |
| P1 | done | migration transformation and OKF-compatible concept metadata |
| P2 | done | corpus verification and smoke checks |
| P3 | done | lightweight index and compact ranked search |
| P4 | done | compact skill with progressive disclosure |
| P5 | done | dependency-free MCP wrapper over shared helper functions |
| P6 | done | plugin package and local marketplace skeleton |
| P7 | done | build, install, validation, and verification tasks |
| P8 | done | permission and vault-friction documentation |
| P9 | done | token/output footprint audit |
| P10 | done | first-release workbench examples and polish |

The historical implementation remains useful. P11-P20 harden and evolve it rather than discarding it.

## Current findings inventory

### Critical compatibility and correctness

- Ordinary path resolution is bounded by the vault rather than the Fundus root.
- Project overrides are not safe single-segment values.
- `area init` violates reserved-file rules.
- Search can trust stale index content.
- Indexed and unindexed search semantics differ.
- Writes have no optimistic concurrency check.
- Index read-modify-write is not locked.

### Important product and maintainability

- Move scope classification is heuristic and incomplete.
- Redirect stubs are not first-class search-excluded objects.
- Frontmatter parser is not a robust YAML implementation.
- Tool outputs lack output schemas and structured content.
- Tool annotations are absent.
- Normal and administrative operations share one large MCP surface.
- Package config embeds a personal path.
- Runtime interpreter selection differs between build and `.mcp.json`.
- Duplicate prevention exists mainly as skill guidance.
- Stale-note proposals are not first-class backend operations.
- Provenance is metadata, not yet an operational verification workflow.
- Core helper is a large module with several responsibilities.
- Manifest declares MIT but the reviewed repository did not expose a matching license file.

The P11 transport, lifecycle, package-shape, error-recovery, and independent-client findings are resolved. See the P11 completion evidence below.

## Phase board

| Phase | Status | Priority | Depends on |
| --- | --- | --- | --- |
| P11 — MCP and Codex package conformance | done | critical | none |
| P12 — Fundus path safety and corpus invariants | ready | critical | none |
| P13 — Search consistency and index freshness | planned | critical | P12 |
| P14 — Revisions, locking, and recoverable mutations | planned | critical | P12 |
| P15 — Frontmatter correctness | planned | high | none |
| P16 — Canonical scope and move semantics | planned | high | P12, P15 |
| P17 — Explicit operation and MCP tool contracts | planned | high | P11 |
| P18 — Proposal/apply, duplicates, and provenance | planned | high | P14, P17 |
| P19 — Configuration, portability, and packaging | planned | high | P11 |
| P20 — Modularization, CI, and release readiness | planned | medium | P13-P19 |

Parallel work is allowed only when branches do not change the same contracts. P11, P12, P15, and part of P19 are conceptually parallel, but a single agent should complete P11 first.

---

## P11 — MCP and Codex package conformance

Status: done

### Goal

Make the built plugin launch a protocol-conformant MCP server through the documented Codex plugin configuration.

### Required implementation

- [x] Replace stdio output framing with compact newline-delimited UTF-8 JSON.
- [x] Simplify stdio input to one message per line, with deliberate handling of blank and malformed lines.
- [x] Ensure stdout contains MCP messages only.
- [x] Change `.mcp.json` to a documented direct server map or `mcp_servers` wrapper.
- [x] Update `scripts/validate_plugin_package.py` for the documented shape.
- [x] Maintain an explicit supported protocol-version list.
- [x] Negotiate versions according to MCP lifecycle rules.
- [x] Track initialization state.
- [x] Return protocol errors for unknown tools and malformed requests.
- [x] Ensure recoverable request errors do not terminate the server.
- [x] Validate basic JSON-RPC envelope types.
- [x] Keep server capabilities limited to implemented features.
- [x] Add one independent MCP-client integration test.
- [x] Add one built-package test that launches the exact `.mcp.json` command.
- [x] Confirm compatibility with the current Codex host and record the negotiated version.
- [x] Synchronize `serverInfo.version` with the plugin version or record the temporary follow-up.

### Focused tests

See P11 in `docs/testing-and-validation.md`.

Minimum commands:

```text
python -m unittest tests.test_fundus_mcp
task build:plugin
python scripts/validate_plugin_package.py dist/fundus-plugin
```

Add an integration command that uses an independent client.

### Acceptance criteria

- [x] Newline-delimited stdio passes an independent client.
- [x] `initialize -> notifications/initialized -> tools/list -> tools/call` succeeds.
- [x] Unsupported protocol versions are negotiated or rejected correctly.
- [x] Unknown tools return an error and the next ping succeeds.
- [x] Built `.mcp.json` launches from the plugin root.
- [x] The custom validator accepts only a documented shape.
- [x] `task verify` passes.
- [x] Codex local-plugin smoke test succeeds or a reproducible host blocker is recorded.

### Exit evidence

Record:

```text
negotiated protocol version
client used
packaged command
commands and test counts
sample initialize response
sample unknown-tool response
Codex smoke-test result
```

### Completion evidence — 2026-07-10

Commit:

- Base commit `c3f3580`; P11 changes are present in the working tree.

Files changed:

- `.mcp.json`
- `scripts/fundus_mcp.py`
- `scripts/validate_plugin_package.py`
- `tests/test_fundus_mcp.py`
- `tests/test_fundus_mcp_integration.py`
- `tests/test_plugin_package_validator.py`
- `Taskfile.yml`
- `README.md`
- remediation and implementation documents under `docs/`

Commands:

```text
python -m unittest tests.test_fundus_mcp tests.test_fundus_mcp_integration tests.test_plugin_package_validator
task build:plugin
python scripts/validate_plugin_package.py dist/fundus-plugin
FUNDUS_PLUGIN_ROOT=dist/fundus-plugin python -m unittest tests.test_fundus_mcp_integration
task verify
task install
codex plugin list
codex mcp list
codex exec --ephemeral --sandbox read-only -C /Users/christian/projects/fundus-skill "...call the Fundus doctor MCP tool exactly once..."
```

Results:

- Negotiated protocol version: `2025-11-25`; compatibility coverage: `2025-06-18`.
- Independent client: repository-owned test client that shares no Fundus transport or lifecycle code.
- Packaged command: `python ./skills/fundus/scripts/fundus_mcp.py`, `cwd: .`, read directly from `dist/fundus-plugin/.mcp.json`.
- Focused suite: 27 tests passed with one package-only skip when `FUNDUS_PLUGIN_ROOT` was absent; the explicit package run executed both integrations with no skips.
- `task verify`: packaged integration 2/2 passed; full suite 84 tests passed with one expected package-only skip during the later environment-free discovery run.
- Custom package validator accepted the direct server map and rejects the old camel-case wrapper.
- The optional external plugin validator was unavailable because PyYAML was not installed for Task's selected interpreter; the current Codex host accepted and loaded the package.

Sample initialize result:

```json
{"protocolVersion":"2025-11-25","capabilities":{"tools":{"listChanged":false}},"serverInfo":{"name":"fundus","version":"0.1.0"}}
```

Sample unknown-tool response:

```json
{"jsonrpc":"2.0","id":4,"error":{"code":-32602,"message":"Unknown tool: does_not_exist"}}
```

Manual verification:

- Installed `fundus@fundus-local` as `0.1.0+codex.20260710083041`.
- `codex mcp list` reported `fundus` enabled and resolved the installed cache command and working directory.
- A fresh ephemeral Codex 0.144.1 host completed one read-only `fundus/doctor` MCP call and returned scope `project`.
- No live corpus mutation or maintenance command was run.

Residual risks:

- P17 still owns output schemas, structured content, annotations, the operation registry, and normal/admin tool separation.
- P19 still owns interpreter portability and a single build-time version source; P11 synchronizes runtime `serverInfo.version` by reading the nearest packaged manifest.

Next phase:

- P12 — Fundus path safety and corpus invariants is ready.

---

## P12 — Fundus path safety and corpus invariants

Status: ready

### Goal

Ensure normal Fundus operations can affect only correctly classified paths inside the Fundus root and that newly generated corpora satisfy their own verifier.

### Required implementation

- [ ] Introduce operation-specific path constructors or value objects.
- [ ] Validate project names as safe single segments.
- [ ] Constrain ordinary note read/write paths to the Fundus root.
- [ ] Constrain archive operations to active or archive roots as appropriate.
- [ ] Validate restore `original_path` as an active Fundus path.
- [ ] Require Markdown suffix for note operations unless explicitly justified.
- [ ] Reject directories and reserved paths where notes are expected.
- [ ] Add symlink escape protections and tests.
- [ ] Make allowed area roots explicit or configurable.
- [ ] Ensure global project enumeration excludes area roots.
- [ ] Generate `index.md` and `log.md` without frontmatter in `area init`.
- [ ] Make `area init` followed by corpus verification pass.
- [ ] Return stable path-related error codes.
- [ ] Update doctor output for resolved roots and classifications.

### Acceptance criteria

- [ ] Traversal and vault-outside-Fundus fixtures fail without writes.
- [ ] Another Obsidian note inside the vault but outside Fundus cannot be read or mutated through note tools.
- [ ] Archive metadata cannot redirect restore outside active Fundus.
- [ ] `area init` produces valid reserved and concept files.
- [ ] Project and area enumeration are not conflated.
- [ ] Existing valid project and area workflows remain compatible.
- [ ] `task verify` passes.

---

## P13 — Search consistency and index freshness

Status: planned

### Goal

Make the JSON index a safe acceleration cache whose presence never changes search semantics or causes stale results.

### Required implementation

- [ ] Extract one common document-to-search-record path.
- [ ] Use one scorer for indexed and direct search.
- [ ] Store content revision and sufficient fast-fingerprint metadata.
- [ ] Detect changed, added, and removed paths for the relevant scope before search.
- [ ] Refresh or bypass stale records before returning results.
- [ ] Define whether search persists repair or performs it in memory.
- [ ] Align MCP read-only annotations with the chosen repair policy.
- [ ] Handle corrupt and incompatible indexes safely.
- [ ] Exclude redirect records from ordinary results.
- [ ] Preserve explicit archive search.
- [ ] Version the new index shape.
- [ ] Add deterministic search fixtures and equivalence tests.
- [ ] Add performance benchmark output to verification or a dedicated task.

### Acceptance criteria

- [ ] No-index and current-index fixtures produce equivalent result identities and ordering.
- [ ] External edit, add, and delete are visible on the next search.
- [ ] Corrupt index does not produce incorrect results.
- [ ] Archived and redirect policies hold.
- [ ] 2,000-note benchmark is measured and documented.
- [ ] Initial p95 target is met or a decision-record adjustment is approved.
- [ ] `task verify` passes.

---

## P14 — Revisions, locking, and recoverable mutations

Status: planned

### Goal

Prevent lost updates and index corruption and make multi-step file operations recoverable.

### Required implementation

- [ ] Return SHA-256 revision from read and relevant search results.
- [ ] Add `expected_revision` to overwrite-like operations.
- [ ] Return `REVISION_CONFLICT` without writing on mismatch.
- [ ] Add a corpus mutation lock abstraction.
- [ ] Lock note-plus-index mutations as one logical operation.
- [ ] Add bounded lock timeouts and diagnostics.
- [ ] Ensure locks release on exceptions.
- [ ] Define stale-lock recovery.
- [ ] Update archive, restore, and move for recoverable sequencing.
- [ ] Prefer atomic rename over copy/unlink when safe.
- [ ] Add rollback or a mutation journal for multi-step failures.
- [ ] Add backup verification.
- [ ] Add an explicit backup restore workflow or document why it is deferred.
- [ ] Add multi-process tests.

### Acceptance criteria

- [ ] Human edit between read and update cannot be overwritten silently.
- [ ] Concurrent updates to different notes preserve both index entries.
- [ ] Concurrent updates to the same note result in one success and one conflict.
- [ ] Failure injection leaves either original state or a documented recoverable journal.
- [ ] Backup corruption is detected before restore.
- [ ] `task verify` passes.

---

## P15 — Frontmatter correctness

Status: planned

### Goal

Make frontmatter parsing and rendering explicit, safe, and lossless for the supported corpus.

### Decision gate

First perform a short packaging spike:

- official or common YAML library,
- round-trip requirements,
- plugin dependency provisioning,
- artifact size,
- licensing.

Default direction: use a real, pinned YAML implementation. A strict custom subset is allowed only when the spike proves dependency provisioning unsuitable and the subset is validated rigorously.

### Required implementation

- [ ] Document the supported frontmatter model.
- [ ] Parse booleans, lists, strings, dates, nulls, and unknown fields deliberately.
- [ ] Normalize known fields through typed helpers.
- [ ] Reject unsupported constructs explicitly.
- [ ] Serialize values with correct quoting.
- [ ] Preserve unknown supported keys.
- [ ] Preserve note body bytes during metadata-only changes.
- [ ] Support LF/CRLF and BOM according to a documented policy.
- [ ] Fix scalar/list ambiguity such as `tags: ticket`.
- [ ] Add corpus fixtures and property-style round-trip tests.
- [ ] Update package dependencies and build tasks if required.
- [ ] Update migration and normalization tests.

### Acceptance criteria

- [ ] Supported fixture values round trip semantically.
- [ ] Unsupported YAML does not silently lose data.
- [ ] Body preservation tests pass.
- [ ] Existing live-corpus shapes are covered by sanitized fixtures.
- [ ] Package installation includes required dependencies reliably.
- [ ] `task verify` passes.

---

## P16 — Canonical scope and move semantics

Status: planned

### Goal

Use one logical scope model for all operations and make every move direction correct.

### Required implementation

- [ ] Implement a canonical scope classifier.
- [ ] Make `scope_path` the logical root.
- [ ] Keep physical parent information in path-derived fields.
- [ ] Update create, normalize, migration, index, archive, and move to use the classifier.
- [ ] Preserve stable note ID during move.
- [ ] Correct project-to-project moves.
- [ ] Correct project-to-area moves.
- [ ] Correct area-to-project moves.
- [ ] Correct area-to-area moves.
- [ ] Preserve neutral tags and replace old scope tags.
- [ ] Introduce first-class redirect metadata.
- [ ] Generate a correct relative or validated canonical redirect target.
- [ ] Exclude redirects from ordinary search and resolve them on read.
- [ ] Detect redirect loops.
- [ ] Add a dry-run normalization plan for existing subfolder-valued `scope_path` notes.

### Acceptance criteria

- [ ] Full move matrix passes.
- [ ] Stable IDs behave according to the target.
- [ ] Redirects are safe and quiet.
- [ ] Normalization dry-run identifies affected existing notes without writing.
- [ ] Corpus verification passes after every move fixture.
- [ ] `task verify` passes.

---

## P17 — Explicit operation and MCP tool contracts

Status: planned

### Goal

Make operation metadata, validation, output schemas, and MCP behavior derive from one registry.

### Required implementation

- [ ] Introduce an operation registry or equivalent single source.
- [ ] Store handler, schemas, descriptions, and behavior metadata together.
- [ ] Validate tool arguments server-side.
- [ ] Add output schemas where practical.
- [ ] Return `structuredContent` conforming to output schemas.
- [ ] Retain text JSON for backward compatibility where useful.
- [ ] Add `title` and tool behavior annotations.
- [ ] Audit read-only, destructive, idempotent, and open-world hints.
- [ ] Add stable error-code mapping.
- [ ] Shorten and improve tool descriptions.
- [ ] Define deprecation wrappers for existing tool names.
- [ ] Separate normal workbench tools from admin operations.
- [ ] Keep CLI and MCP over one application layer.

### Acceptance criteria

- [ ] Runtime validation matches advertised schemas.
- [ ] Structured outputs validate.
- [ ] An annotation-consistency test passes.
- [ ] Default tool list is compact and workbench-oriented.
- [ ] Admin operations remain available through an explicit path.
- [ ] Existing normal workflows retain a documented compatibility route.
- [ ] `task verify` passes.

---

## P18 — Proposal/apply, duplicate prevention, and provenance

Status: planned

### Goal

Turn safe curation behavior from prompt guidance into backend-supported workflows.

### Required implementation

- [ ] Add propose-create.
- [ ] Add apply-create.
- [ ] Add propose-update.
- [ ] Add apply-update with expected revision.
- [ ] Represent section replace, append, rewrite, and metadata changes in proposals.
- [ ] Produce deterministic diffs or structured before/after summaries.
- [ ] Add duplicate checks for title, ID, alias, ticket, resource, and high-confidence similarity.
- [ ] Require explicit override for reviewed duplicate creation.
- [ ] Add provenance fields and source fingerprints.
- [ ] Add verification status.
- [ ] Add mark-stale, verify-note, or equivalent operations.
- [ ] Update SKILL behavior for implicit read-only versus explicit mutation.
- [ ] Add agent-evaluation fixtures.
- [ ] Keep human-facing confirmations compact.

### Acceptance criteria

- [ ] Proposal operations never write.
- [ ] Apply operations reject stale proposals.
- [ ] Duplicate candidates prevent accidental duplicate creation.
- [ ] Explicit broad write intent can complete safely in one turn.
- [ ] Ordinary research produces a stale-note proposal rather than a silent rewrite.
- [ ] Provenance can indicate current, stale, and unverified states.
- [ ] Agent evaluation set meets documented expectations.
- [ ] `task verify` passes.

---

## P19 — Configuration, portability, and packaging

Status: planned

### Goal

Remove machine-specific assumptions and make a built plugin reproducible on another supported machine.

### Required implementation

- [ ] Remove personal vault path from distributable config.
- [ ] Add user-level configuration.
- [ ] Add `FUNDUS_CONFIG_PATH`.
- [ ] Report configuration provenance in doctor.
- [ ] Preserve `OBSIDIAN_VAULT_PATH` compatibility.
- [ ] Resolve the `python` versus `python3` launcher mismatch.
- [ ] Test environments with only one interpreter command.
- [ ] Add an artifact scan for personal paths.
- [ ] Establish one version source.
- [ ] Synchronize manifest, MCP server info, and marketplace metadata.
- [ ] Add the license file declared by the manifest.
- [ ] Review dependency licenses.
- [ ] Add first-install/setup documentation.
- [ ] Clarify personal-first versus public distribution in README.
- [ ] Update privacy and terms links only if publication intent requires owner-specific documents.

### Acceptance criteria

- [ ] Built plugin contains no known personal path.
- [ ] New-machine temporary setup can resolve config and run doctor.
- [ ] Packaged launcher works on supported interpreter layouts.
- [ ] Versions agree.
- [ ] Declared license exists.
- [ ] `task verify` passes.

---

## P20 — Modularization, CI, and release readiness

Status: planned

### Goal

Reduce maintenance risk, enforce the new contracts continuously, and prepare the next release.

### Required implementation

- [ ] Extract modules incrementally behind compatibility entrypoints.
- [ ] Keep CLI and MCP thin.
- [ ] Add CI for supported Python versions.
- [ ] Add package integration job.
- [ ] Add personal-path artifact scan.
- [ ] Add frontmatter and path-security fixtures.
- [ ] Add concurrency tests appropriate for CI.
- [ ] Add performance reporting.
- [ ] Add documentation consistency checks.
- [ ] Update README, SKILL, reference docs, and examples.
- [ ] Archive or condense completed migration instructions from normal onboarding.
- [ ] Write release notes.
- [ ] Select and apply the next version.
- [ ] Reinstall the local plugin and execute the host smoke checklist.
- [ ] Update this tracker to reflect remaining deferred work.

### Acceptance criteria

- [ ] Target module boundaries exist or equivalent boundaries are documented.
- [ ] CI passes on the supported matrix.
- [ ] Clean temporary-vault end-to-end passes.
- [ ] Local Codex plugin smoke test passes.
- [ ] All P11-P19 release-blocking criteria are done.
- [ ] Documentation describes actual behavior.
- [ ] Release artifact is versioned and reproducible.
- [ ] `task verify` passes.

---

## Deferred backlog

These are intentionally not release blockers unless new evidence changes priority:

- vector or embedding search,
- remote sync,
- team sharing and access control,
- graph visualization,
- web UI,
- networked MCP transport,
- autonomous global curation,
- complex task-augmented MCP execution,
- real-time filesystem watchers instead of on-demand freshness checks.

## Pass protocol

### Start

1. Check `git status --short --branch`.
2. Record the current commit.
3. Read the required documents.
4. Reproduce the phase's primary finding before editing.
5. Inspect official documentation for unstable protocol or host behavior.
6. Select focused tests.

### During

1. Add failing tests for confirmed behavior gaps.
2. Implement through shared operations.
3. Keep compatibility wrappers small.
4. Avoid live-corpus writes.
5. Update docs with code when behavior changes.
6. Share partial findings early.

### End

1. Run focused tests.
2. Run package integration where applicable.
3. Run `task verify`.
4. Review the diff for unrelated changes.
5. Record evidence in the phase.
6. Update phase status honestly.
7. Summarize residual risks and the next ready phase.

## Evidence log template

Add beneath the completed phase:

```markdown
### Completion evidence — YYYY-MM-DD

Commit:

Files changed:

Commands:

Results:

Manual verification:

Residual risks:

Next phase:
```
