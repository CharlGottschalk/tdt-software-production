# Pre-commit privacy review

Invoke `/tdt-software-production-pii <project-id>` to review staged changes and
the complete proposed commit message. In Codex, use
`$tdt-software-production-pii <project-id>` or the skill picker. The review
combines a local pattern scan with semantic inspection and reports masked findings.

## Review procedure

Direct invocation authorizes read-only review of the selected worktree/index and
proposed message. It does not authorize fixes, staging, commit, push, identity
changes, history rewriting or source removal. Preserve the scope of the user’s request.

1. Resolve the intended Git worktree, including linked worktrees and any explicit
   GIT_INDEX_FILE environment. Ask if the target is ambiguous. Use the companion
   helper with direct subprocess argument arrays, never shell interpolation of
   paths or messages. The helper resolves Git's actual index and uses NUL-delimited
   paths/object IDs. Do not replace index bytes with working-tree reads.
2. Obtain the complete proposed message (subject, body, trailers). For already
   authorized commit work, prepare a safe Conventional Commit message in a private
   literal file outside tracked content; otherwise request it. Without it, return
   incomplete/message pending. Never put detected values in the proposal.
3. Read the helper's sanitized JSON. Status pass means bounded pattern coverage
   only. Complete a semantic review of the full staged versions, staged paths and
   message: names, personal identifiers, private emails, phones, physical addresses,
   account/user IDs, internal organizations/customers, credentials/tokens and
   machine paths, including custom Unix roots, Windows profiles and UNC shares.
   For safe local inspection, use object IDs from Git's raw NUL-delimited staged
   diff with cat-file; never follow symlinks or external textconv/diff commands.
   Inspect only changed staged blobs (1 MiB each, 8 MiB total), not history or
   untracked/ignored files. Do not dump raw source/message into terminal logs or
   agent transcripts: use a private local viewer with the user where sensitive
   context is not already safely available. If semantic inspection is unavailable,
   return incomplete and request that bounded local review; do not invent a pass.
4. Return pass, findings, or incomplete with snapshot, coverage/gaps and masked
   findings. A file reference is SHA256 of its raw repository-relative path,
   first 12 hex digits; line numbers are one-based and location `path` refers to
   the filename. Message line 1 is the subject; later lines cover body/trailers.
   Keep entire excerpts `[redacted]`, since adjacent text may also be private.
   Use these references for local resolution; never log raw names/paths/secrets.
   Existing-context means an identical line exists in the immediate prior version
   (rename/copy source where Git detects it), not proof of prior public exposure.
   Duplicated/moved lines can be classified as existing; inspect that distinction
   semantically. A missing prior version is incomplete, not evidence of newness.
5. Explain heuristics: author/contact attribution may be intentionally public;
   example domains, generic placeholders and ordinary source/URL paths can be
   legitimate. Do not automatically delete or broadly exclude them. Suggest
   relative paths/placeholders, reserved example emails or a scoped untracking/
   ignore correction. Never print a credential as an example fix. Publication of
   author/committer identity is a separate optional concern; never change it silently.
6. Findings pause the agent commit until corrected or explicitly accepted by the
   user for the identified finding IDs and unchanged bytes. Preserve those exact
   decisions in the current conversation; do not ask again for unchanged IDs.
   Semantic findings need an equivalent digest of path/blob or complete message,
   category and location. Never accept on the user's behalf. Declined, unresolved
   findings and coverage gaps keep the commit paused. Unsupported files require
   bounded manual inspection; acceptance alone must not disguise missing coverage.
   If resuming without reliable decisions, report what is missing. Any retained
   decision file must be local, verified ignored, minimal (digests and decisions,
   no raw evidence), and never promoted to brain notes or tracked reports.
7. Fix only within existing authorization, preserving unrelated edits and partial
   staging. Show a sanitized scoped proposal if authorization is missing. Never
   broad `git add`, discard/rebuild the index, auto-remove files or rewrite history.
   A prior leak needs separate handling. Re-run review after fixes/staging/message
   changes. Reuse only unchanged finding decisions; review all new findings.
8. Immediately before an authorized agent commit, rerun the helper with the same
   complete message and require the snapshot to match the semantically reviewed
   snapshot. A mismatch requires renewed review. Pattern exit zero alone does not
   authorize a commit; only full coverage and resolved/accepted findings do.
   Use an argument array such as `['git', '-C', repo, 'commit', '--cleanup=verbatim',
   '-F', message_file]`; no `-a`, path-limited commit or extra message/trailer flags
   that change the reviewed selection. Honor existing Git safeguards. Editor/hooks
   and concurrent writers can still change bytes after review: do not claim final
   coverage unless the resulting commit tree/message are verified against the
   reviewed index entries/message. Otherwise explicitly report final-byte coverage
   unverified. On discrepancies pause further publication and report masked
   locations; do not undo the commit automatically.

## Non-interactive runs

An orchestrator may run build or close headless and mark the request
non-interactive. That mark changes only how findings are returned, never what
is authorized. When findings or gaps remain, the skill must not ask and must
not commit:

- Leave the reviewed change staged exactly as reviewed.
- Write the complete proposed message, byte for byte, to the private file the
  request supplies. It must resolve inside workspace continuity's `local/` child
  (`WORKSPACE/.tdt/state/software-production/<registered-project-id>/local/`),
  with no symlinks or path escapes; otherwise report incomplete and write nothing.
- Report sanitized JSON only: `snapshot`, `message_sha256`, `status`, `gaps`,
  and per finding `id`, `category`, `path_ref` (the 12-hex path reference) or
  `message`, and `line`. No excerpts, raw paths or values.
- Keep the task `doing` (close does not advance status) and record "paused on
  privacy findings" with the snapshot in the per-task handoff.

Without the mark, behaviour is the interactive procedure above.

## Commit-only resume

A follow-up request may carry the user's decisions to commit an already reviewed,
still staged snapshot. It must name the message file, the `snapshot` and
`message_sha256` the decisions were made for, and each accepted finding `id`.
The run commits nothing else and makes no source or staging changes:

1. Rerun the helper with the same `--repo` and `--message-file`.
2. Commit only if `snapshot` and `message_sha256` match the request, there are
   no gaps, every reported finding ID is accepted in the request, and no
   accepted ID is missing from the report. Semantic findings recorded in the
   handoff must be likewise accepted and unchanged.
3. Commit with `['git', '-C', repo, 'commit', '--cleanup=verbatim', '-F',
   message_file]`, then verify as in step 8.
4. On any difference, do not commit; report the new findings non-interactively.

The helper's `snapshot` already binds the staged index entries (the tree that
would be committed), HEAD and the message bytes.

## Decisions relayed by a tool

Decisions passed in the request count as the user's explicit acceptance, and as
the "current conversation" for step 6, only when the user made them
interactively for those exact finding IDs and bytes and the tool only passes
them on. The tool does not accept on the user's behalf. There are still no
standing, category-wide or inferred approvals; a decision the tool generated or
defaulted is no decision.

This is agent workflow guidance, not guaranteed manual-commit interception. No
scan proves absence of private information. Project constitutions should
reference this boundary. A release needs a separate review of its complete contents;
a staged-change review does not cover an entire repository or authorize publication.
