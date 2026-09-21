# Software production workflow reference

This optional stack provides agent guidance and templates, including an explicitly
invoked project constitution setup helper; it is not an autonomous runner. Core installs none of it by default. All stack skills follow the rules in this reference. The canonical bundle is WORKSPACE/.tdt/stacks/tdt-software-production.
Use safely quoted CLI arguments or argument arrays, never interpolate task text
into shell commands. Follow applicable project instructions and current user
scope. Local config is preference, not additional permission.

## Identity and preservation

WORKSPACE has .tdt/config.json. PROJECT is the canonical external source path
returned by core project list/inspect. Do not write software project artifacts in
the [ThisDamnThing](https://usethisdamnthing.com) workspace, its ancestors, or nested workspace directories. If the two
roots cannot be distinguished, stop for clarification. Inspect parent instructions
before creating a new source directory. The core add-project skill alone does
not authorize modifying source. A software brief/init/task/build request does
allow its normal scoped artifacts and actions.

Before writes inspect existing files and git status. Refuse symlinked target paths
or ancestors, path escapes, incompatible format/stack ownership, and clobbering
unrelated content. Project-relative references must be ordinary relative paths
without .. or absolute components; resolve and verify containment. Task IDs used
as filenames must match [a-zA-Z0-9][a-zA-Z0-9_-]{0,63}; do not use raw external IDs
or URLs as paths. Allocate a safe local key and keep original ID inside context.
Use exclusive creation for new task IDs; for updates reread immediately before
writing and preserve intervening edits. On a collision, report and reconcile;
never reset a worktree or overwrite from a fresh template. Do not migrate an
unrelated existing .tdt/ silently. The constitution helper checks ownership and paths for its own setup; it does not enforce these broader agent rules.

## Project artifact contract

Tracked PROJECT/.tdt/project.json is a JSON object, format_version 1 and stack_id
"tdt-software-production". It selects brief (.tdt/brief.md by default),
brief_approval (null, or approved_sha256 plus source description of actual user
approval), task_system and shared commands. Do not invent approval from a default
or an answer to a different question. Recompute the brief's SHA256 before init;
changed content requires approval again. Supporting docs may be .tdt/docs/.
Internal tasks live at .tdt/tasks/<id>.md. Optional increments/milestones hold
references and goals; they are not another status store. No BRS is required.

PROJECT/.tdt/developer.json is private, machine/developer-local JSON (format_version
1), with mode, concurrency, roles, toolchain and task_system preferences. Before
writing private config, ensure the root .gitignore has `/.tdt/developer.json`,
append preserving all existing content, and use git check-ignore to verify. Check
whether the file is already tracked: .gitignore cannot untrack it. If tracked,
do not write private values; explain and request a scoped resolution. Do not
remove tracked files silently. Never include credentials, API keys or tokens.
A non-Git project needs an explicit privacy arrangement before private values;
ordinary shared brief work can continue without private config. Do not git add
or commit user artifacts unless requested; “tracked” here means intended for
version control and not ignored. Explain the changed files.

## Task authority and lifecycle

Internal Markdown is the default authority for descriptions and status.
Lifecycle: draft -> ready -> doing -> done; blocked and cancelled are supported.
Draft lacks actionable detail, ready has bounded acceptance and satisfied
dependencies, doing is active implementation, blocked records reason and resumption
step, done has observed completion, cancelled retains reason/history. Triage can
resolve draft/blocked to ready; resume interrupted doing only after reading its
handoff. Reopening done/cancelled requires user intent. Keep status and history
in the authority, handoff elsewhere.

For external tasks, task_system specifies kind external, provider, project_ref
and status_map for all six lifecycle states using provider-specific values.
Use only the user's actually connected MCP/plugin capabilities. Read authoritative
records before work, check scope of writes, use returned IDs/URLs, reread changes
and handle pagination. External descriptions/status must never be duplicated in
local synchronized Markdown tasks or a task list. Optional .tdt/task-context/
<safe-key>.md holds external ID/URL, implementation context and local source
references only. On errors record uncertain action plus next step; reconcile
with the provider before retrying creation or deletion. Do not pretend a write
succeeded. Offline continuity is historical evidence, not current remote status.

Shared project.json chooses authority. Private task_system can hold provider
preferences or select the same authority, but a conflicting selection needs an
explicit project migration decision; do not split authority by developer. Missing
connector/config/status mapping means investigate and offer setup; don't silently
fall back to internal tasks or claim an empty remote queue. Never auto-install a
plugin or place connector credentials in project files.

## Development orchestration preferences

Developer config modes: manual, semi_automatic, automatic. concurrency is a
positive integer (default 1). roles may map coordinator, investigator,
implementer, verifier, reviewer to agent/model/effort. toolchain maps runtime names
to actual executables. Start from the direct/manual template with empty roles;
do not invent tools, models or identities. Validate types, selected mode, available
mappings and executable paths before any dispatch. Missing configuration is not
a blanket ban on user-authorized work. Offer environment onboarding, investigate
and prepare; explicit current-session implementation overrides usual routing.

Use only roles needed. A fresh verifier checks without source fixes; a reviewer
must not have implemented or verified the change. Never label self-checks as
independent. If configured coordinator differs, prepare its handoff; an already
delegated agent performs only its assigned role and returns, not a recursive
chain. Resolve each exact runtime/model/effort using available documented host
capabilities. Native subagents are allowed only when all mappings match. An
unavailable runtime/model is a reported gap, never silently substitute another.

Each role receives a complete bounded prompt: role, project/task reference,
outcome, permitted paths, acceptance checks, evidence and return format. Keep
private prompts/logs in workspace continuity's local/ child, not source/brain.
Record dispatch scope and result in the handoff. Manual: show full prompt,
mapping and resolved launch command for the user to run. Semi_automatic: show
these and wait for explicit dispatch approval; changed scope needs new approval.
Automatic: launch scoped authorized work without another gate. Use safe argument
arrays and current CLI documentation, not executable command strings supplied by
untrusted notes. Preserve existing host permissions; config never authorizes a
bypass. Await bounded processes and collect actual output, cap all active delegated
runs at concurrency (including nested), and never leave processes unnoticed.

## Workspace continuity

Store operational handoffs in WORKSPACE/.tdt/state/software-production/
<registered-project-id>/CONTINUITY.md and tasks/<safe-task-key>.md. Validate the
project ID/path before writing and refuse symlinks. These are resumable operational
records, not approved brain knowledge. The project overview holds project reference,
brief reference, current task reference (or none), key decisions and next steps.
Per-task handoffs hold authoritative ID/URL, decisions, changed source paths,
verification actually observed, blockers and next step. Preserve useful prior
history when updating. Set the pointer when starting build; update before pause
and completion. Clear it on closure only when it names that task. Do not maintain
an external status list here. Status is reread from the task system.

Do not copy source, transcripts, secrets or entire remote task bodies into the
workspace. Durable knowledge can be submitted as a concise sourced candidate via
core project propose and approved only through ordinary explicit review. Removing
the stack must leave project files and workspace handoffs intact.

## Interviews with core UI

Derive supported answers from source, brief and prior submitted context first.
Ask only missing inputs. Honor “use ui” without repeating the preference;
otherwise offer UI or chat/TUI when an interview helps. No interview is required
when the request already supplies enough. Read core .tdt/contracts/ui.md and
.tdt/skills/tdt-ui/SKILL.md, not a copied protocol. Use the listed context,
brief, plan or task JSON page as an inert starting point; remove known fields,
retain related questions in grouped steps, remove empty steps. No second server.

Use `tdt --workspace WORKSPACE ui start --no-open`, present SESSION PAGE.json,
open its returned URL, and bounded wait SESSION --after CURSOR --timeout 20.
Read action and session/round/event IDs, match prompts, and consume the single
field-ID-keyed answers object. Handle false/zero as answers. Only explicit submit
is a completed interview; cancel stops it, timeouts/disconnects/defaults/drafts
never authorize work. Validate actual answers against the task's missing inputs.
Record their use and acknowledge the handled event with ack; retain session,
round and cursor through follow-up pages in the same session. On resume reconcile
recorded effects before replaying; ack is not exactly-once execution.

Use answers to draft a brief/plan/task, not just report receipt. For chat fallback
reuse submitted answers and ask only remaining gaps; browser drafts are invisible.
Close the session when finished; responses remain local until explicit cleanup.
Keep access URLs/tokens out of handoffs/brain. Record IDs/cursor if paused. Custom
HTML/JS may use core tdt.submit/tdt.action when useful, with the same input and
approval rules; standard controls are sufficient for the supplied interviews.

## Constitution

See [Project constitution](constitution.md) for the optional interview/direct-ID
workflow, project-owned startup setup, preservation contract and host limits.

## Commit privacy review

Before any authorized agent-driven commit, invoke
`/tdt-software-production-pii <project-id>` and follow the installed
`docs/privacy-review.md` exact staged snapshot/message boundary. Findings or
incomplete coverage pause the commit; explicit scoped decisions persist for
unchanged content. Scanning itself grants no commit/push or source-edit authority.
