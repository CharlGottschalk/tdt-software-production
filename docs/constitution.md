# Project constitution

`/tdt-software-production-constitution <project-id>` creates a short,
project-specific `.tdt/CONSTITUTION.md` and local SessionStart setup. Missing ID
prompts with registered IDs/names; unknown or unavailable projects stop. Add,
brief and init offer this only when absent; accepting authorizes separate project
setup, declining continues the original workflow without constitution writes.
A direct request already authorizes setup. Unresolved rules still need answers.
The constitution is project-owned and normally version controlled. Existing
instructions apply; reuse or explicitly review updates to an existing document.

## Setup helper

From the installed bundle, use a Python 3.11+ interpreter that will remain
available to project sessions. This helper uses only the standard library.
BUNDLE means WORKSPACE/.tdt/stacks/tdt-software-production. Use safely quoted
arguments or subprocess arrays, including paths with spaces.

```sh
python3 BUNDLE/templates/constitution-setup.py --workspace WORKSPACE
python3 BUNDLE/templates/constitution-setup.py --workspace WORKSPACE --project-id ID --host both --content DRAFT
python3 BUNDLE/templates/constitution-setup.py --workspace WORKSPACE --project-id ID --host both --content DRAFT --apply
```

DRAFT holds only the grounded constitution content the interview resolved.
Omit `--content` to reuse an existing constitution byte-for-byte. To apply an
authorized content update, add `--expected-sha256 HASH`, the full SHA256 of the
reviewed previous constitution. Intervening document edits invalidate this value.
The default previews without writes; `--apply` performs already authorized work.
Do not infer authorization from the flag or invent an extra approval ceremony.
Read project instructions and project.json before using the helper.

Generated files: `.tdt/CONSTITUTION.md`, `.tdt/constitution-loader.py`,
`.tdt/constitution-setup.json`, and the selected `.claude/settings.json` and/or
`.codex/hooks.json`. The ownership record covers only the loader and exact hook
entries, never the constitution contents or unrelated provider keys. Existing
hooks and permissions survive. Edited/missing owned entries, duplicate hooks,
unowned loader names, symlinks, incompatible project config and malformed provider
JSON cause refusal before writes. Repeated setup is unchanged. Reconcile a
collision explicitly; this version has no force/migration/removal command.
Normal exceptions attempt rollback; this is not a crash-atomic multi-file transaction.
Avoid concurrent project setup processes.

The loader is copied into the project and needs no [ThisDamnThing](https://usetdt.com) import, workspace bundle
or stack source. Commands use the selected interpreter and absolute project
loader path, POSIX-quoted. Moving a project or removing that interpreter requires
explicitly reviewing/reconfiguring its hook entries. Native Windows setup is
not supported by this helper. It generates POSIX shell commands and requires a
compatible host environment.

## Check startup loading

The loader requires a SessionStart JSON payload with absolute `cwd`; it reads at
most 64 KiB of input and 32 KiB of constitution. Outside-project events and nested
Git projects/workspaces emit nothing. Missing/unsafe/oversize constitution files
produce stderr and a nonzero exit, not substitute policy. Normal project
subdirectories are supported. A project with no detectable nested boundary is
considered part of its containing project.

Check the configured command directly with representative event JSON, then start
fresh Claude and Codex sessions in the selected project and confirm the actual
additional context. Confirm an outside-project event emits none. Host project
trust, hook feature availability and runtime rules still apply; do not change
trust or permissions. Confirm that the host actually loads the rules; a configuration entry alone is
not sufficient. No AGENTS.md
or CLAUDE.md fallback is added by this helper, so fallback reads cannot be confused
with hook delivery. A separately useful fallback must be clearly owned, preserve
existing text, and be reported separately from execution evidence.

Core registration alone remains read-only toward linked source. Stack removal
only removes workspace-owned stack files and preserves this project-owned setup.
Removing project setup is a separate explicitly requested action: preserve the
constitution unless its deletion was also requested, remove only verified owned
entries, and retain unrelated provider configuration.

## Review before committing project setup

Constitution setup does not authorize a Git commit. For an otherwise authorized
commit, follow the stack's [privacy review](privacy-review.md) boundary for the
exact staged content and complete message. Generated provider configuration and
ownership records contain project/interpreter paths: inspect them before staging
and follow the project's local-configuration policy. Do not silently ignore files,
remove attribution or treat setup approval as approval to publish personal paths.
This review does not change the user's constitution or add project policy rules.
