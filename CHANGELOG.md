# Changelog

All notable changes to the AGT Web Application Specification. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and the spec is versioned as SPEC-4 describes:
major for a new or stricter MUST, minor for a new SHOULD/MAY or section, patch for clarifications.

Versions before 4.0.0 were developed in the reference implementation's repository
(`agtdarkshadow04/agt_event_calendar`, `docs/agt-webapp-spec.md`); the PR numbers below refer to that repository.

## [6.0.0] - Unreleased

### Upgrade notes

- **Manifest (BAK-2, BAK-7):** write exactly the listed manifest fields, with `formatVersion` as the integer `1`;
  list every archive entry except `manifest.json`; reject archives with unlisted or missing entries, unsafe paths, or
  a newer `formatVersion` (`422 archive_rejected`). Keep restoring every older `formatVersion`.
- **Restore (BAK-3):** `action=restore` re-runs the whole preview validation on its own upload; remove any preview
  token or cached preview state.
- **Operation lock (BAK-8):** add one in-process lock with the states `idle`, `backup`, `restore`. A second backup or
  restore gets `409 conflict`. During a backup, data writes wait up to 30 s, then get `503 maintenance` with
  `Retry-After: 10`. During a restore, every `/api/` route except `GET /api/health` returns `503 maintenance`, health
  returns `{ "status": "maintenance" }`, and background jobs pause. Add `maintenance` to the error codes (API-6) and
  show it in the UI as a notice that retries once (FE-5).
- **Snapshot (BAK-9):** take the database snapshot and copy the uploads inside the `backup` lock.
- **Restore steps (BAK-4, BAK-10, BAK-11):** drain in-flight requests (30 s, else `409 conflict`), close and reopen the
  database or `pg.Pool`, run the post-restore health check, roll back on failure (Postgres: from the pre-restore
  backup), and on a failed rollback stay in maintenance with `<dataDir>/restore-failed.json` and refuse to start while
  that file exists. Sessions are ended only by a successful restore.
- **Tests and docs:** add the TEST-4 backup format, concurrency and failure tests, and the README Troubleshooting
  entries for "maintenance in progress" and recovering from a failed restore.
- **Error bodies (API-6, #9):** add `code` (and `params` where the table lists them) to every `FieldError`, including
  `notices`, and `params` to the error codes that need values (`rate_limited`, `maintenance`, `file_too_large`,
  `field_too_large`, `defined_in_config`). The shared validators return the same codes. Update the `ErrorBody` and
  `FieldError` schemas. Existing fields keep their meaning, so older clients keep working.
- **AI disclosure (DOC-1, #10):** change the README's disclosure line to exactly
  `> **AI Disclosure:** This software was created using generative AI.` Remove "Its functionality has been verified
  by human review." and any other claim of review or verification.
- **Stack (STACK-1, #12):** move to Node.js 26 (`engines` `>=26.0.0`, `node:26-bookworm-slim` in both Dockerfile stages,
  NodeSource `setup_26.x`, `esbuild --target=node26`), TypeScript `~7.0`, Vite `^8.3` with `@vitejs/plugin-react`
  `^6.3`, and esbuild `^0.28` (Vite 8 needs esbuild 0.27 or newer, and `npm install` fails on the peer
  conflict otherwise). Run `npm run check` afterwards; the reference implementation needed no source changes.
- **Install scripts (STACK-7, #12):** record `allowScripts` in `package.json` (`npm install-scripts approve
  better-sqlite3 esbuild`) so that `npm install-scripts ls` lists nothing.
- **Translated errors (I18N-6, #9):** add a translation in every locale for every error code and field code, add
  `src/lib/errors.ts` with `errorText()` and `fieldErrorText()`, and show errors only through them (FE-5). Add the
  TEST-4 translation and error body checks.

### Added

- §12.1 *Archive format*: the full `manifest.json` schema with an example, path rules, and BAK-7 on format versions
  (#5).
- §12.2 *Consistency and concurrency*: BAK-8, the operation lock with `503 maintenance` and `409 conflict`, and BAK-9,
  consistent snapshots (#5).
- BAK-10 (rollback) and BAK-11 (failed rollback: maintenance, marker file, refusal to start) (#5).
- API-6: the error body's `params`, and `code` and `params` on every `FieldError`, with a standard table of field
  codes (#9).
- STACK-7: apps record an install-script decision for every dependency in `allowScripts`, because npm 11.20 and
  newer skips unapproved install scripts (#12).
- I18N-6: clients translate every error code and field code in all locales; the English `message` is only a fallback
  (#9).
- API-6: `503 maintenance`. TEST-4: backup format, concurrency and failure tests. This also covers #11's test of
  backups under concurrent writes.

### Changed

- BAK-3: `action=restore` re-validates its upload; there is no state between preview and restore (#5).
- BAK-4: restore is an ordered procedure with draining, a database or pool reopen, and a post-restore health check
  (#5).
- STACK-1: Node.js 26 LTS (was 24), TypeScript `~7.0` (was `~5.8`), Vite 8 with `@vitejs/plugin-react` 6 (was Vite 6),
  esbuild `^0.28`. DEP-1, DEP-6 and TEST-1 use Node.js 26 (#12).
- DOC-1: the AI disclosure line no longer claims human review, which the spec never required; it is now
  "This software was created using generative AI." (#10). The spec repository's README says the same of the spec.
- I18N-5, FE-5, FE-6: error text is translated by code, and the shared validators return field codes (#9).
- SRV-11: `GET /api/health` reports `maintenance` during a restore. FE-5: how clients show `503 maintenance`.
- DOC-1: Troubleshooting covers maintenance and failed restores.

## [5.2.0] - 2026-11-10

### Added

- `assets/`: the AGT logo and the fonts apps bundle (NMS Futura, NMS Glyphs Mono and Twemoji Country Flags), with SHA-256, source, copyright and licence for each in `assets/README.md`, and the licence
  texts in `assets/licenses/` (#7). `scripts/check_spec.py` checks the hashes.
- UI-15: apps copy these assets unmodified from the spec repository at their spec tag, SHOULD ship the licence files
  and credit the fonts in their README; the licences' own terms (the logo is all rights reserved, NMS Glyphs Mono is
  non-commercial) apply (#7). The two No Man's Sky fonts are credited to their embedded authors and to Hello
  Games.
- Header rows **Reference version** (AGT Event Calendar 2.2.0, pinned to a commit until it is tagged) and **Assets**
  (#7).
- STACK-5: which versions of Node.js, Vite and other dependencies count as supported, and that apps SHOULD only
  use supported versions within the STACK-1 lines (#12).
- STACK-6: a dependency review (lockfile changes and `npm audit`) in every release PR, and a support review at each
  Node.js LTS change and at least every six months (SHOULD) (#12).
- §19.1 *Acceptance tests*, all SHOULD, run before every release with the results in the release PR (#11):
  - TEST-6: a Playwright browser suite (`npm run test:e2e`) for both entries: setup and sign-in, dialogs and focus,
    accessible names with an automated WCAG 2.2 AA check, no horizontal scroll at each breakpoint and at 300 px,
    and live regions;
  - TEST-7: a manual accessibility checklist (keyboard, screen reader, contrast, zoom and font scale, reduced
    motion, every locale);
  - TEST-8: Docker Compose and local installation smoke tests, and a server test for `Secure` cookies behind a
    proxy;
  - TEST-9: an upgrade from the previous release and a rollback, following the README.
- STACK-1: `@playwright/test` (and optionally `@axe-core/playwright`) as development dependencies; TEST-1: the
  `test:e2e` script, outside `npm run check`.
- UI-3: the community `NMS Alphabet` font is not an AGT asset, because its FontStruct licence prohibits hosting
  it as a web font.

### Changed

- UI-1: `--agt-red-orange` is `#cb4c2b` instead of `#e25530` (#27). White text on it, as UI-9 requires for
  `.button-primary`, was 3.76:1 and failed A11Y-1's 4.5:1; it is now 4.56:1. Apps change the token in their UI-1
  block when they move to this version; nothing else changes.
- A11Y-1: a table of the approved text and background token pairs with their contrast ratios, replacing the claim
  that every token pair passes. `--agt-red` text is not used on `--surface-soft` (4.37:1) (#27).
- §0: "when the spec is silent" refers to the reference implementation at the pinned **Reference version**, not its
  latest commit (#7).
- VER-12: the release PR description SHOULD carry the dependency review (STACK-6) and the acceptance test results
  (TEST-6 to TEST-9).
- UI-5, UI-14: brand assets are copied from the spec repository's `assets/`, not from the reference implementation.

## [5.1.0] - 2026-11-10

### Added

- TEST-4: Postgres apps test that backups contain no `logs` objects and that a restore leaves the log store
  unchanged.
- API-13: the OpenAPI test SHOULD assert each operation's `security` value.
- CFG-2: `AGT_<APP>_TEST_DATABASE_URL`, the test database of Postgres apps (TEST-3).
- API-6: `400 unknown_setting` and `400 invalid_setting` (CFG-8) in the table of standard codes.
- Header rows for the owner, the release date and approval record, and the security contact (#15).
- CFG-6: allowed values of every standard dashboard-editable key (#15).

### Changed

- The PostgreSQL migration rule is now **DATA-11** (#14). It was the second definition of DATA-5, so a citation of
  "DATA-5" did not name one rule. DATA-5 stays the SQLite rule; the content of both rules is unchanged. Apps that
  cite DATA-5 for PostgreSQL migrations (in code comments or the deviations table of `AGENTS.md`) change the
  citation to DATA-11 when they move to this version. `scripts/check_spec.py` no longer exempts DATA-5 from the
  duplicate-ID check.
- Clarifications that keep implementations from diverging (#15):
  - AUTH-3: admin usernames are trimmed, 1–64 characters (SHOULD), and compared exactly; how to compare secrets of
    different lengths in constant time.
  - AUTH-5: length caps on the setup and login fields, and a `bodyLimit` of at most 2 MiB for JSON (SHOULD).
  - API-8: sort order and tie-breakers, cursor encoding, invalid and stale cursors, the default `limit`.
  - API-10: `additionalProperties: false` applies to `params` and `querystring`, and what Fastify's default
    `removeAdditional` does with unknown properties.
  - SEC-7: rate limits are keyed by `request.ip`, which honours `trustProxy`.
  - I18N-1: locale codes are BCP 47 tags; `pt` uses `pt-BR` where the region matters. Codes are never renamed.

### Fixed

- Postgres backups included the log store and a restore overwrote it (#6), contrary to LOG-17: `pg_dump` dumped the
  `logs` schema, and `pg_restore --clean` replaced the audit log and the IP-hash key (`log_meta`) with the backup's
  copies. BAK-2 now dumps with `--exclude-schema=logs`. BAK-4 restores from a filtered table of contents
  (`--use-list`) that leaves out the `logs` schema, so backups made before this fix still restore without
  touching the logs; BAK-3 warns about them. Apps that follow LOG-17 already must make these changes: dump with
  `--exclude-schema=logs` and restore with the filtered list.
- API-11 gave the wrong OpenAPI `security` for first-run setup and login (#8): setup fell under `[]`, hiding the
  CSRF header it needs (SEC-5), and login fell under the admin-write value, claiming a session it cannot need
  (AUTH-9). Both now use `[{ csrfHeader: [] }]`, and API-11 has a table of the four `security` values.
- The lists of environment variables and error codes were incomplete and contradicted themselves (#13). CFG-2 said
  the variables were "limited to this set" but did not list `AGT_<APP>_TEST_DATABASE_URL`, which TEST-3 uses,
  and then allowed other secrets anyway. It now lists that variable and has an explicit rule for app-specific
  secrets (operator-supplied secrets only, listed in `.env.example` and the README). API-6 now says its table is
  the standard set, not an exhaustive list: apps MAY add codes for other situations and SHOULD list every code in
  the `ErrorBody` schema's description.

## [5.0.0] - 2026-11-10

### Upgrade notes

- Pass `maxmem` to every scrypt call (AUTH-2): `64 * 1024 * 1024` when hashing, and at least
  `128 · r · (N + p + 2)` bytes (twice that recommended) computed from the stored hash's parameters when
  verifying. Without it, Node rejects the AUTH-2 parameters and first-run setup and login fail.
- Add a test that hashes and verifies a password with the production options (TEST-4).
- Stop reading `altcha.hmacKey` (ALT-2, CFG-5). Always generate the ALTCHA HMAC key into `app_secrets`. Because
  unknown config keys stop the server (CFG-3), an app that accepted the key MUST NOT reject it straight away:
  keep it in the config schema for one minor release as deprecated (VER-10), ignore its value, and write a
  `warn` server-log entry at startup telling the operator to delete it from `config.yaml`. Remove it from the
  schema in the app's next major release. Ignoring it changes the key, which only invalidates challenges that
  are open at the time of the upgrade.
- Default `server.host` to `127.0.0.1`, read `AGT_<APP>_SERVER_HOST` as the default when `server.host` is not
  set (CFG-2, CFG-5), set `AGT_<APP>_SERVER_HOST=0.0.0.0` in the Dockerfile (DEP-1), and publish the Compose port
  as `"127.0.0.1:<port>:<port>"` (DEP-2). This changes how existing installs behave, so it is a major version of
  the app (VER-3). Its upgrade notes MUST tell operators that the app is now reachable only from its own host and
  how to reach it through a TLS proxy (DEP-10); operators with a proxy on another machine set `server.host` or the
  published address explicitly.
- Optionally (SHOULD), warn in the server log the first time a login or setup request arrives over plain HTTP
  from a non-loopback address (SEC-4).

### Added

- TEST-4: password hashing and verification with the production scrypt options.
- CFG-2: `AGT_<APP>_SERVER_HOST`, the default listen address, set to `0.0.0.0` by the Dockerfile.
- SEC-4: a server-log warning when credentials arrive over plain HTTP from another machine (SHOULD).

### Changed

- CFG-5: `server.host` defaults to `127.0.0.1`; `altcha.hmacKey` is removed.
- ALT-2: the ALTCHA HMAC key is always generated and stored in `app_secrets`.
- SEC-8: table of allowed secret locations (`.env`, `app_secrets`, `log_meta`) and whether each is in backups.
- DEP-1: the Dockerfile sets `AGT_<APP>_SERVER_HOST=0.0.0.0`. DEP-2: Compose publishes `127.0.0.1:<port>:<port>`.
- DEP-10: which `trustProxy` address to use for Docker, and how to expose the app to a proxy on another machine.

### Fixed

- AUTH-2 could not be followed as written: `N = 2^15, r = 8, p = 1` need slightly more than Node's default
  32 MiB `maxmem`, so scrypt threw `ERR_CRYPTO_INVALID_SCRYPT_PARAMS`. AUTH-2 now requires `maxmem` for hashing
  and verification (#2).
- Secret storage rules contradicted each other (#3): SEC-8 allowed secrets only in `.env` and `app_secrets`, but
  CFG-5 and ALT-2 allowed the ALTCHA HMAC key in `config.yaml` (and so in every backup, BAK-2), and LOG-12 keeps
  the IP-hash key in `log_meta`. SEC-8 now lists every allowed location and whether it is in backups, and the
  key can no longer be configured.
- A default install exposed plaintext admin login on every interface (#4): `server.host` defaulted to `0.0.0.0`
  and Compose published the port on all interfaces, contradicting principle 3 (*Secure by default*). The app is
  now reachable only from its own host until the operator puts a TLS proxy in front (SEC-4, DEP-10).

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
