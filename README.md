![ThisDamnThing Software Production](docs/assets/banner.png)

# Software Production

A [ThisDamnThing](https://usethisdamnthing.com) stack for taking software projects from a brief to working code. It
provides skills and templates for project onboarding, planning, implementation
and handoffs, plus optional project rules and pre-commit privacy review. Work
stays in your linked source repository, with questions handled in chat or [ThisDamnThing](https://usethisdamnthing.com) UI.

## Release status

Candidate version: **0.2.0**. Canonical source: [CharlGottschalk/tdt-software-production](https://github.com/CharlGottschalk/tdt-software-production).
The registry commands below are the planned public installation path; production
listing and installation are still awaiting release verification.

Local acceptance is on Linux x86_64 with Python 3.12 and Claude/Codex. macOS
and native Windows are unverified. The constitution setup helper currently requires POSIX.
Agent-directed work follows the linked project instructions and user authorization;
source edits, Git operations and external services are disclosed in the usage guide.

## Install

With [ThisDamnThing](https://usethisdamnthing.com) installed and a workspace initialized, ask your agent to install
`tdt-software-production` using `/tdt-install-stack` (Claude) or
`$tdt-install-stack` (Codex). The skill finds the stack in the marketplace,
shows the selected release for review and installs it from the registry.

Or use the CLI, replacing the workspace path with your own:

Run the path-based examples from a parent directory containing `workspace` and
the stack source directories. Paths are relative to that directory; adjust them
to your layout. Commands without `--workspace` run from the workspace root.

```sh
tdt stack install tdt-software-production --inspect
tdt --workspace ./workspace stack install tdt-software-production
```

Review the inspected release and any prerequisites before running the install command.
Restart Claude or Codex in your
[ThisDamnThing](https://usethisdamnthing.com) workspace to load the skills, then start with
`/tdt-software-production-add` for existing source or
`/tdt-software-production-brief` for a new project. In Codex, use `$` instead
of `/`, or select the skill from the picker.

See the [usage guide](docs/usage.md) for the full workflow and available skills.

## License

Licensed under the [Apache License 2.0](LICENSE). Copyright Charl Gottschalk.
