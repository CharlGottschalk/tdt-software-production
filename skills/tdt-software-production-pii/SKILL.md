---
name: tdt-software-production-pii
description: Review staged linked-project content and complete proposed commit messages for private information before authorized software-production commits, or on direct request.
---

Find the owning ThisDamnThing workspace via `.tdt/config.json`. Read the installed
`.tdt/stacks/tdt-software-production/docs/workflow.md`. Resolve the requested
project ID through core `tdt --workspace WORKSPACE project list` and
`project inspect ID`; use the canonical linked source path and its instructions.
When ID is absent or ambiguous, ask for selection; do not guess or scan another
project. Missing/moved source needs clarification, not silent relinking.

Read `.tdt/stacks/tdt-software-production/docs/privacy-review.md` and follow
its complete review/commit boundary. Run Python 3.11+ on the installed bundle's
`templates/privacy-review.py` with `--repo PROJECT` and, when available,
`--message-file MESSAGE`. Resolve both resources from the owning workspace,
never the provider bridge, `.dev/`, a source checkout or global skill directory.
The template is a standalone explicitly invoked read-only helper, not a hook;
do not copy it into the external project. Review alone does not authorize any
external source modification, staging, commit or push.
