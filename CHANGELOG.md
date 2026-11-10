# Changelog

All notable changes to the AGT Web Application Specification. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and the spec is versioned as SPEC-4 describes:
major for a new or stricter MUST, minor for a new SHOULD/MAY or section, patch for clarifications.

Versions before 4.0.0 were developed in the reference implementation's repository
(`agtdarkshadow04/agt_event_calendar`, `docs/agt-webapp-spec.md`); the PR numbers below refer to that repository.

## [5.2.0] - Unreleased

### Added

- `assets/`: the AGT logo and the fonts apps bundle (NMS Futura, NMS Glyphs Mono, Twemoji Country Flags and the
  optional NMS Alphabet), with SHA-256, source, copyright and licence for each in `assets/README.md`, and the licence
  texts in `assets/licenses/` (#7). `scripts/check_spec.py` checks the hashes.
- UI-15: apps copy these assets unmodified from the spec repository at their spec tag, SHOULD ship the licence files
  and credit the fonts in their README; the licences' own terms (the logo is all rights reserved, NMS Glyphs Mono is
  non-commercial) apply (#7).
- Header rows **Reference version** (AGT Event Calendar 2.2.0, pinned to a commit until it is tagged) and **Assets**
  (#7).
- UI-3: the optional `NMS Alphabet` font for text in the Expedition alphabet.

### Changed

- §0: "when the spec is silent" refers to the reference implementation at the pinned **Reference version**, not its
  latest commit (#7).
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
