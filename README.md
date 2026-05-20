# Obsidian Wiki Skill

This repository is the source of truth for the local `obsidian-wiki` Agent Skill.

The skill persists codebase knowledge into an Obsidian vault as per-repository wiki documents. The same skill package can be installed for Codex, Claude Code, and ForgeCode.

Existing wiki documents can be updated by appending content, replacing a named heading section, or rewriting the full article body with `update --mode rewrite`.
Created documents keep one generated top-level title heading; duplicate matching H1 headings in supplied content are removed automatically.

## Layout

- `SKILL.md`: agent-agnostic skill manifest and operating instructions.
- `commands/`: slash-command wrappers that invoke the skill from supported agents.
- `scripts/obsidian_wiki.py`: deterministic scan/read/create/update tool for wiki documents.
- `config.json`: local default configuration used by the installed skill.
- `config.example.json`: portable configuration template.
- `docs/`: project documentation for maintainers.
- `Taskfile.yml`: local development tasks.

## Build

Run:

```bash
task build
```

The build task creates:

```text
dist/obsidian-wiki
```

Only runtime files are copied into the package.

## Install

Install for all supported agents:

```bash
task install
```

Or install one target:

```bash
task install:codex
task install:claude
task install:forge
```

The install targets copy the same built package into:

```text
~/.codex/skills/obsidian-wiki
~/.claude/skills/obsidian-wiki
~/.forge/skills/obsidian-wiki
```

They also install the `document` command into each agent's command location:

```text
~/.codex/prompts/document.md
~/.claude/commands/document.md
~/.agents/commands/document.md
```

Use it as `/document ...` in Codex and Claude Code. In ForgeCode, use the native command form `:document ...`.

Restart the target agent after installing or changing the skill so the skill manifest is reloaded.

## Codex Permissions

For fast documentation runs in Codex, approve this command prefix when prompted:

```text
python /Users/christian/.codex/skills/obsidian-wiki/scripts/obsidian_wiki.py
```

The skill instructions prefer inline `--content` for create and update operations, which avoids a separate temporary-file creation step. Use `--content-file` only for notes that are too large or awkward to quote inline.

## Verify

Run:

```bash
task verify
```

This builds the package, checks the script entrypoint, and runs the unit tests.

After installing, verify agent-specific installs with:

```bash
task verify:codex
task verify:claude
task verify:forge
```

You can also run the built or installed script directly:

```bash
python dist/obsidian-wiki/scripts/obsidian_wiki.py --help
```

## Configuration

Configuration resolves in this order:

1. `OBSIDIAN_VAULT_PATH`
2. project-local `.agents/obsidian-wiki.json`
3. project-local `.codex/obsidian-wiki.json` for backward compatibility
4. project-local `.claude/obsidian-wiki.json` for backward compatibility
5. installed skill-local `config.json`

Default configuration targets:

```text
/Users/christian/vault/Hypatos/Wiki
```

## Update Workflow

1. Edit the source files in this repository.
2. Run `task verify`.
3. Run `task install`.
4. Start a new agent session.

The installed skill is a copied directory, so repository changes are not reflected globally until the install task runs again.
