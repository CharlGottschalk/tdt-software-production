# Registry submission draft

Draft only; submit the verified release through https://stacks.usethisdamnthing.com.
The production submission flow still needs acceptance.
This file is not part of stack.json and does not claim a published listing.

- ID: tdt-software-production
- Description: Briefs, tasks and software delivery in linked projects, with optional core UI.
- Version: 0.2.1
- Author: ThisDamnThing
- License: Apache-2.0
- Copyright: Charl Gottschalk
- Skills: all ten skills explicitly listed in stack.json; start with
  /tdt-software-production-add or /tdt-software-production-brief
- Source repository: https://github.com/CharlGottschalk/tdt-software-production

Before submission, supply the actual GitHub repository and a release reference
resolvable to a committed revision. Record only verified commits/digests. Local
selected-content SHA256 and downloaded archive SHA256 are different values.

Project constitution: `/tdt-software-production-constitution <project-id>`;
see [guide](docs/constitution.md) for interview offers and project-local startup setup.

- Supported agents: Claude and Codex; recorded local acceptance on Linux x86_64
  with Python 3.12. macOS/native Windows remain unverified; constitution setup
  currently requires POSIX.
- Prerequisites: ThisDamnThing CLI and the chosen host agent; Git for staged privacy
  review. Project-specific tools/services are determined from the linked project.
- Data and effects: reads registered project files and writes authorized project
  artifacts/source; runs approved project commands. Optional constitution setup
  installs project-local startup hooks only after authorization. The bundle itself
  declares no automatically activated hooks/providers. Host-agent services and
  separately authorized tools may send data; no independent stack telemetry.
- Publication: review source/license/version/commit and both archive and selected
  content digests. A website submission is pending review, not an approved listing.
