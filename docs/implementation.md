# Fundus Implementation Notes

Status: current baseline plus target implementation contract
Reviewed: 2026-07-10

## Document role

This document has two deliberately separate purposes:

1. Describe confirmed current repository behavior as observed during review.
2. Define the technical contract that planned phases will implement.

A planned item is not current behavior until its phase is completed and this document is updated.

Use:

- `docs/fundus-target-picture.md` for product and architecture decisions.
- `docs/agent-implementation-tracker.md` for phase order and progress.
- `docs/architecture-invariants.md` for normative rules.
- `docs/testing-and-validation.md` for release evidence.

## Current implementation baseline

### Repository surfaces

The current repository contains:

```text
.codex-plugin/plugin.json
.mcp.json
SKILL.md
agents/openai.yaml
config.json
config.example.json
scripts/fundus.py
scripts/fundus_mcp.py
scripts/build_plugin_marketplace.py
scripts/validate_plugin_package.py
scripts/audit_token_budget.py
Taskfile.yml
tests/
docs/
```

The direct skill package is built under:

```text
dist/fundus
```

The plugin package and local marketplace are built under:

```text
dist/fundus-plugin
dist/fundus-marketplace
```

### Current domain behavior

`scripts/fundus.py` currently implements a large shared domain/helper module covering:

- config resolution,
- project and area scopes,
- frontmatter parsing and formatting,
- secret redaction,
- atomic file writes,
- create, read, update, and move,
- index rebuild and entry refresh,
- archive candidates, archive, restore, and cleanup,
- backup creation and manifest inspection,
- Wiki-to-Fundus migration,
- frontmatter normalization,
- corpus verification,
- CLI parsing and output.

`scripts/fundus_mcp.py` wraps the same functions in a custom stdio JSON-RPC/MCP adapter.

This shared-domain direction is correct and should be preserved during refactoring.

### Current corpus state

The current personal corpus is under:

```text
/Users/christian/vault/Hypatos/Fundus
```

The legacy `Wiki/` source was migrated and retired on 2026-07-09. Migration and backup functionality remain useful for recovery, but migration is no longer an everyday workbench action.

### Current configuration

Current precedence is:

1. `OBSIDIAN_VAULT_PATH`,
2. project `.codex/fundus.json`,
3. packaged `config.json`,
4. built-in defaults.

The packaged `config.json` currently contains Christian's absolute vault path. This is accepted as a current local implementation fact but is a portability gap.

### Current search

The index is:

```text
{vault_path}/{fundus_dir}/.fundus-index.json
```

It stores metadata, excerpts, tokens, ticket IDs, archive state, and `mtime_ns`.

Current behavior:

- index rebuild scans active and archived Markdown,
- create and update refresh an existing index entry,
- archive and restore refresh source and destination entries,
- scan uses the index whenever it exists and has a recognized version,
- index status can separately report stale paths.

Known semantic discrepancy:

- indexed search considers body and heading tokens plus metadata,
- direct fallback search considers title, tags, and filename.

### Current write behavior

`atomic_write()` writes a temporary file in the destination directory and replaces the destination.

Current writes do not carry an expected revision and there is no corpus lock. Concurrent read-modify-write operations can therefore overwrite human changes or each other's index updates.

### Current frontmatter behavior

The current frontmatter implementation is a custom YAML-like parser. It supports basic scalar lines and indented lists.

Known limits include:

- quoted and multiline YAML,
- inline lists,
- nested values,
- comments,
- robust CRLF/BOM handling,
- safe serializer quoting,
- scalar/list type ambiguity.

Unknown keys are retained in dictionary form when parsed successfully, but unsupported YAML may be reinterpreted or lost.

### Current MCP behavior

The server currently:

- constructs tools from Python function signatures,
- returns tool results as JSON serialized into text content,
- exposes no output schemas or structured content,
- uses compact newline-delimited UTF-8 JSON-RPC messages on stdio,
- accepts `initialize`, `notifications/initialized`, `ping`, `tools/list`, and `tools/call`,
- supports and negotiates the explicit protocol versions `2025-11-25` and `2025-06-18`,
- gates normal operations until the initialization lifecycle completes,
- validates basic JSON-RPC envelopes and `tools/call` request types,
- validates required, unexpected, typed, and enumerated tool arguments against the generated input schemas,
- returns unknown tools and malformed calls as protocol errors,
- returns handler and input-validation failures as tool results with `isError: true`,
- continues serving after recoverable parse, protocol, and tool errors,
- derives `serverInfo.version` from the nearest plugin manifest when packaged.

An independent subprocess client exercises the source server and exact packaged command through initialize, initialized notification, tools/list, a real temporary-vault tool call, unknown-tool recovery, and a final ping.

Remaining MCP contract work belongs to P17: output schemas, structured content, titles, behavior annotations, a single explicit operation registry, and the compact normal-versus-admin tool split.

### Current plugin configuration

The plugin manifest points to `.mcp.json` through its `mcpServers` field.

The current `.mcp.json` uses the documented direct server-map shape:

```json
{
  "fundus": {
    "command": "python",
    "args": ["./skills/fundus/scripts/fundus_mcp.py"],
    "cwd": "."
  }
}
```

Current Codex plugin documentation accepts a direct server map or a wrapped `mcp_servers` object. The repository validator accepts those documented shapes and rejects the old camel-case wrapper.

### Current path behavior

Area paths receive explicit traversal checks.

Several project and note operations currently resolve against the whole vault, not the Fundus root:

- a project override is not constrained to one safe segment,
- `resolve_doc_path()` accepts any path inside the vault,
- archived `original_path` is resolved with the same vault-wide rule.

This is a target safety gap even though writes remain bounded by the vault.

### Current reserved-file behavior

The documented corpus contract says active `index.md` and `log.md` have no frontmatter.

Migration and verification enforce that rule.

`area_init()` currently generates `overview.md`, `index.md`, and `log.md` through the same frontmatter-producing path. Newly initialized reserved files can therefore violate the verifier's contract.

### Current scope move behavior

Move currently infers an area when the destination parent does not match the existing project prefix. This can misclassify project-to-project moves and does not provide one canonical project/area classifier.

### Current tests

The test suite has broad unit coverage for helper and wrapper behavior. It includes newline framing and lifecycle tests plus an independent stdio client for both source and packaged commands.

The current tests do not prove that:

- stale indexes repair before search,
- lost updates are rejected,
- concurrent writes preserve every index change,
- path escapes through project overrides and archive metadata are blocked,
- area initialization passes corpus verification,
- supported YAML round trips safely.

## Target source architecture

Refactor incrementally. Do not perform a big-bang rewrite.

Target boundaries:

```text
fundus/
├── config.py
├── models.py
├── errors.py
├── paths.py
├── frontmatter.py
├── repository.py
├── revisions.py
├── locking.py
├── search.py
├── operations.py
├── cli.py
├── mcp_server.py
└── admin/
    ├── backup.py
    ├── migration.py
    ├── normalization.py
    └── verification.py
```

Compatibility entrypoints may remain:

```text
scripts/fundus.py
scripts/fundus_mcp.py
```

They should become thin launchers once the core package exists.

## Target value objects

### Scope

```python
@dataclass(frozen=True)
class Scope:
    kind: Literal["project", "area"]
    path: str
    display_name: str
```

Scope construction validates its own invariants.

### NotePath

Use explicit constructors:

```python
NotePath.active(config, value)
NotePath.archived(config, value)
NotePath.any_fundus(config, value)
```

Do not expose one generic vault-relative resolver to ordinary note operations.

### Revision

```python
@dataclass(frozen=True)
class Revision:
    algorithm: Literal["sha256"]
    value: str
```

Revision is computed from canonical file bytes.

### Operation result

Operation results are structured dictionaries or typed data that can be serialized consistently by CLI and MCP. They include stable error codes and avoid full note content unless requested.

## Target operation contracts

### Search

Input:

```text
query
scope
limit
include archived
include snippet
```

Behavior:

1. Resolve and validate scope.
2. Load index metadata.
3. detect changed, new, and removed files in the relevant scope,
4. refresh in memory or persist under the correct mutation policy,
5. run the common scorer,
6. exclude redirects and archives unless requested,
7. return compact results with revisions.

### Read

Input:

```text
active or explicitly archived Fundus path
```

Output:

```json
{
  "path": "...",
  "content": "...",
  "revision": "sha256:...",
  "metadata": {},
  "archived": false,
  "redirected_from": null
}
```

Read follows a validated redirect with a bounded hop count.

### Propose create

Behavior:

1. Validate desired scope and metadata.
2. search for normalized title, ID, aliases, ticket keys, and canonical resource,
3. return duplicate candidates or a create proposal,
4. do not write.

### Apply create

Input includes a proposal or equivalent validated fields. It fails on path or stable-ID conflict.

### Propose update

Input:

```text
path
base revision
mode
section if applicable
new content
evidence and metadata changes
```

It returns a diff-like structured proposal and does not write.

### Apply update

Requires `expected_revision`. It:

1. acquires the mutation lock,
2. re-reads and verifies revision,
3. applies redaction with warnings,
4. writes atomically,
5. updates the index under the same lock,
6. returns the new revision.

### Move

Move uses the canonical scope classifier for the destination. It preserves stable ID, updates scope metadata, and optionally creates a first-class redirect.

### Archive and restore

Archive and restore validate active/archive path types. `original_path` is untrusted metadata and must be revalidated.

## Target error model

Use stable machine-readable codes:

```text
CONFIG_INVALID
PATH_OUTSIDE_FUNDUS
PROJECT_NAME_INVALID
AREA_PATH_INVALID
NOTE_NOT_FOUND
NOTE_ALREADY_EXISTS
DUPLICATE_CANDIDATE
REVISION_CONFLICT
LOCK_TIMEOUT
FRONTMATTER_INVALID
INDEX_INVALID
MCP_PROTOCOL_VERSION_UNSUPPORTED
MCP_REQUEST_INVALID
MCP_TOOL_UNKNOWN
MUTATION_INCOMPLETE
BACKUP_INVALID
```

CLI output may include a human-readable message. MCP distinguishes:

- JSON-RPC protocol errors,
- tool execution errors with `isError: true`.

Unknown tools and malformed protocol messages are protocol errors.

## Target frontmatter implementation

P15 must make and document one choice:

### Preferred path

Use a pinned YAML implementation that can safely parse the supported corpus and preserve unknown keys. Prefer round-trip behavior when package provisioning is reliable.

### Allowed fallback

Retain a zero-dependency subset only when:

- the subset is documented,
- unsupported constructs fail explicitly,
- serializer quoting is correct,
- supported values round trip,
- type normalization is deliberate,
- property and fixture tests are comprehensive.

Silent pseudo-YAML is not an acceptable target.

## Target index implementation

Index version increases when its shape changes.

Recommended record:

```json
{
  "path": "Fundus/demo/note.md",
  "id": "project/demo/note",
  "scope": "project",
  "scope_path": "demo",
  "kind": "concept",
  "title": "Note",
  "description": "...",
  "aliases": [],
  "resource": null,
  "tags": [],
  "headings": [],
  "excerpt": "...",
  "tokens": [],
  "ticket_ids": [],
  "archived": false,
  "redirect_to": null,
  "revision": "sha256:...",
  "mtime_ns": 0,
  "size": 0
}
```

Freshness compares path, revision or a safe fast fingerprint, mtime, and size. Correctness must not depend solely on mtime.

All index updates occur under the corpus mutation lock.

## Target locking and transactions

Provide one lock abstraction. The implementation may use a small dependency or a tested lock-file strategy.

Requirements:

- bounded timeout,
- diagnostic owner metadata,
- stale-lock handling,
- process-safe behavior,
- no lock acquisition for pure read-only parsing,
- mutation lock covers note and index changes.

Multi-step operations use:

- atomic rename where possible,
- staged destination,
- explicit rollback,
- or a small journal.

Tests inject failures after each logical step.

## Target MCP implementation

The project may keep a custom adapter or adopt the official Python MCP SDK. The decision is based on packaging reliability and testability.

Regardless of implementation:

- stdio is newline-delimited JSON,
- stdout contains only MCP messages,
- supported versions are explicit,
- initialization state is tracked,
- advertised capabilities are accurate,
- tool arguments are validated,
- output schemas are honored,
- structured content is returned,
- behavior annotations are provided,
- the packaged command is integration-tested.

Supported protocol versions confirmed during P11:

```text
2025-11-25
2025-06-18
```

Codex host verification negotiated `2025-11-25`; integration coverage also retains `2025-06-18` compatibility.

## Target `.mcp.json`

Use a documented Codex shape, preferably a direct server map:

```json
{
  "fundus": {
    "command": "python3",
    "args": [
      "./skills/fundus/scripts/fundus_mcp.py"
    ],
    "cwd": "."
  }
}
```

If interpreter portability requires a launcher, package and test the launcher instead of assuming both `python` and `python3` exist.

The custom package validator validates the documented direct and `mcp_servers` shapes and rejects the old repository-specific camel-case wrapper.

## Target configuration

Configuration source precedence:

```text
explicit operation argument
OBSIDIAN_VAULT_PATH
FUNDUS_CONFIG_PATH
project .codex/fundus.json
user ~/.config/fundus/config.json
non-personal built-in defaults
```

`config.example.json` remains portable.

Package build must fail if a known personal path appears in distributable files.

## Tool-surface migration

During compatibility:

- keep existing MCP tool names as wrappers where practical,
- add new proposal/apply operations,
- mark old immediate mutation names deprecated in descriptions,
- remove one-time migration tools from the default surface only after CLI/admin access and docs are verified.

## Documentation rules during implementation

After a phase:

- current behavior moves from “target” to “current” only when tests pass,
- README changes describe only shipped behavior,
- SKILL instructions remain compact,
- examples use current tool names,
- external spec links use the tested protocol revision,
- tracker records evidence and remaining risks.

## External references

- https://learn.chatgpt.com/docs/build-plugins
- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- https://modelcontextprotocol.io/specification/2025-11-25/schema
