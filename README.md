# AGT Web Application Specification

> **AI Disclosure:** This specification was created using generative AI.

The normative standard for every Alliance of Galactic Travellers (AGT) web application: stack, repository
layout, API, data storage, configuration, authentication, security, logging, backups, UI design,
internationalization, deployment, testing, documentation and versioning. Its readers are mainly the AI coding
agents that build and maintain AGT apps.

**The spec:** [`agt-webapp-spec.md`](agt-webapp-spec.md). **What changed:** [`CHANGELOG.md`](CHANGELOG.md).

**Reference implementation:** [AGT Event Calendar](https://github.com/agtdarkshadow04/agt_event_calendar).

## Using the spec in an app

Each app keeps a pinned copy of the spec version it follows (SPEC-2):

1. Pick a release tag (`vX.Y.Z`; the newest is the default for new apps). `v6.0.0` is the first production-ready
   version; earlier tags are development releases.
2. Copy `agt-webapp-spec.md` from that tag to `docs/agt-webapp-spec.md` in the app, unmodified:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/agtdarkshadow04/agt_webapp_specification/vX.Y.Z/agt-webapp-spec.md \
     -o docs/agt-webapp-spec.md
   ```

3. In the app's `AGENTS.md`, link to the copy and name the version and tag, for example "follows the AGT Web
   Application Specification v4.0.0 (`agt_webapp_specification@v4.0.0`)" (DOC-2).
4. Copy the logo and fonts from `assets/` at the same tag into `public/`, unmodified, with the licence files
   (UI-15), and `assets/css/agt-base.css` to `src/agt-base.css`, imported first by `src/styles.css` (UI-16). [`assets/README.md`](assets/README.md) lists each file's SHA-256, source and licence.
5. List every rule the app doesn't meet in the deviations table of its `AGENTS.md`, never by editing the copy.

To move an app to a newer spec version, follow SPEC-3: one PR that replaces the copy, updates `AGENTS.md`, and
implements the new rules or lists them as deviations "to fix". `CHANGELOG.md` lists what changed in each version,
with upgrade notes for major versions.

## Changing the spec

Follow SPEC-4: open a PR here that changes only the spec, this README and `CHANGELOG.md`, bumps the version in
the spec's header, and adds a `CHANGELOG.md` entry. Requirement IDs are stable: never reuse or renumber one.
Before opening the PR, run:

```bash
python3 scripts/check_spec.py
```

It checks that internal links resolve, that requirement IDs are unique and defined, and that the header version
matches the newest `CHANGELOG.md` entry.

Releases are annotated tags `vX.Y.Z` on `main`, created when the maintainer asks, plus a GitHub Release with the
version's `CHANGELOG.md` section. Tags are never moved.
