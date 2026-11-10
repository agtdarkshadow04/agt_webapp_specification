# Changelog

All notable changes to the AGT Web Application Specification. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and the spec is versioned as SPEC-4 describes:
major for a new or stricter MUST, minor for a new SHOULD/MAY or section, patch for clarifications.

Versions before 4.0.0 were developed in the reference implementation's repository
(`agtdarkshadow04/agt_event_calendar`, `docs/agt-webapp-spec.md`); the PR numbers below refer to that repository.

## [4.0.0] - 2026-11-10

### Upgrade notes

- Copy `agt-webapp-spec.md` from the `v4.0.0` tag to `docs/agt-webapp-spec.md` in your app, unmodified, and name
  the version and tag in `AGENTS.md` (SPEC-2, DOC-2).
- Move any deviations your app listed in the spec itself into the deviations table of its `AGENTS.md`. The spec
  no longer has an Appendix A.

### Added

- §0.1 *Where the spec lives*: this repository is the source of truth, and spec releases are `vX.Y.Z` tags
  (SPEC-1). Apps keep a pinned, unmodified copy (SPEC-2) and move to a new spec version in a PR of their own
  (SPEC-3). Changes to the spec go to this repository with a version bump and a CHANGELOG entry, keeping
  requirement IDs stable (SPEC-4).
- `docs/agt-webapp-spec.md` in the repository layout (REPO-1), and a checklist item for the pinned copy.
- A **Source** row in the header.

### Changed

- DOC-2: `AGENTS.md` links to the pinned copy and names its version and source tag.
- WF-4: proposed spec changes are PRs to this repository.
- The reference implementation and the app registry now point to `agtdarkshadow04/agt_event_calendar`.

### Removed

- Appendix A (the reference implementation's deviations). They are listed in the calendar's `AGENTS.md`. The
  note that the calendar's app-specific features are examples, not templates, moved to §0.

## [3.0.0] - 2026-11-09

### Added

- §21 *Versioning and releases* (VER-1..13): Semantic Versioning for apps, what counts as major, minor and patch,
  a bump in each PR, `CHANGELOG.md` with upgrade notes, deprecation before removal, `vX.Y.Z` tags with GitHub
  Releases, and installations that check out release tags (calendar PR #53).

### Changed

- API-12, DEP-5, DEP-6, DEP-9, DOC-1, TEST-4, WF-5 and the checklist refer to §21. Agent workflow and the
  checklist became §22 and §23.

## [2.0.0] - 2026-11-09

### Added

- §13 *Logging* (LOG-1..23): a server log and an audit log in a separate log store, shown in the admin dashboard,
  with an audit hook, IP pseudonymization, retention settings and exports, and kept out of backups (calendar
  PR #50).

### Changed

- Sections 13–21 became 14–22. STACK-1, REPO-1, SRV-6, DATA-10, CFG-5, BAK-2, BAK-4, FE-2, UI-8, TEST-4 and DOC-1
  were updated for logging.

## [1.0.1] - 2026-11-09

### Changed

- Appendix A lists only the reference implementation's remaining deviations, after the calendar was brought into
  compliance (calendar PR #49).

## [1.0.0] - 2026-11-09

### Added

- First release: stack, layout, REST API and OpenAPI, data storage, configuration, single-admin first run,
  security, ALTCHA, backups, frontend, visual design system (including UI-14 portal glyphs), accessibility,
  internationalization, Docker Compose and systemd deployment, testing, documentation and agent workflow
  (calendar PR #48).
