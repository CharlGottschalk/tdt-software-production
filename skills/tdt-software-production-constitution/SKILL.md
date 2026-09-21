---
name: tdt-software-production-constitution
description: Create or reuse a linked project's concise constitution and configure project-local Claude or Codex startup, using its registered project ID.
---

Use the installed workspace and its canonical
`.tdt/stacks/tdt-software-production/` bundle, never a host bridge directory.
Read bundle `docs/workflow.md` and `docs/constitution.md`. Accept the project ID
argument; if absent, run core `project list`, show IDs and names (source directory
names), and ask for selection. Resolve the ID through `project inspect`; unknown
IDs or missing/moved directories stop without project writes. Never guess a path,
initialize a workspace in the project, or create project `.tdt/config.json`.

Read applicable project/parent instructions, existing `.tdt/CONSTITUTION.md`,
`.tdt/project.json`, the referenced brief, and bounded relevant conventions.
Check the brief hash against its approval record before treating it as approved.
Keep existing instructions applicable throughout. Existing constitutions are
project-owned: summarize and offer reuse or an explicit scoped update; do not
replace from the starter or introduce competing rules. Retain local edits.

Direct invocation authorizes constitution/setup work. An offer in another
interview does not: first explain the location and SessionStart behavior and obtain
acceptance. Decline/cancel means no constitution, hooks or setup files and continuation
of the original workflow. Do not ask again for authorization already given.

Use `templates/constitution.md` as a portable design aid, not prescribed rules.
Derive concrete rules from approved requirements and conventions, with evidence
references. Group only unresolved choices: scope, architecture/complexity, source
and artifact layout, verification, dependency/security practices, collaboration
and preservation as relevant. Distinguish selected rules from suggestions; resolve
policy choices with the user rather than silently making suggestions binding.
No imported ThisDamnThing development rules, no blanket ban on tests, machine paths, role
mappings or secrets. Aim for a short document, at most 32 KiB. Honor core UI when
requested, chat otherwise: reuse prior answers and shared UI session/round/cursor
handling, omit known questions, and never repeat the brief interview. On missing
answers pause with a handoff, without installing speculative policy.

Use selected/configured host(s), asking claude/codex/both only when unknown.
Read `docs/constitution.md` for the helper preview/apply commands and limitations.
Stage grounded content outside the project, preview the complete change list,
and apply within existing authorization. Existing content updates require the
reviewed original SHA256. Without a content change, reuse the file as-is. A helper
conflict stops setup; explain the conflict and preserve files, never delete
ownership records or force an overwrite to bypass it. Private developer config
and existing instructions/permissions remain untouched.

Report actual changed files, content decisions and remaining choices. Verify
loader boundaries and fresh host delivery separately; configuration alone does
not prove execution. Do not change host trust or permissions. No global hooks,
workspace hook/skill copies, or dependency on the removable bundle in generated
project artifacts. Record outcome and real verification limits in workspace
project continuity. Uninstall preserves this setup; removal needs a separate
explicit project action.

If a project commit is separately authorized, use the shared workflow's privacy
review before committing generated setup. Review actual staged configuration and
message, including machine-specific hook paths; setup approval is not approval
to publish those paths. Do not copy this stack workflow into the constitution as
a new user rule.
