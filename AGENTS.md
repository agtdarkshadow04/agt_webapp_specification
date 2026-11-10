# Agent guide — AGT Web Application Specification

This repository holds one normative document, [`agt-webapp-spec.md`](agt-webapp-spec.md): the standard every AGT
web app follows. There is no code. Apps keep pinned copies of tagged releases (SPEC-2), so a change here reaches
an app only when that app upgrades (SPEC-3).

## Branches

- `main` holds the latest spec, including unreleased changes. Releases are annotated tags `vX.Y.Z` on `main`.
- Work on a feature branch and open a PR into `main`. Never move or delete a tag.

## Commands

```bash
python3 scripts/check_spec.py   # links, requirement IDs, header version vs CHANGELOG — run before every commit
```

## Where things live

| Path | Purpose |
| --- | --- |
| `agt-webapp-spec.md` | The spec. Sections `## N.`, rules `**PREFIX-N**` |
| `CHANGELOG.md` | One section per spec version (Keep a Changelog); newest first |
| `README.md` | How apps use the spec and how to change it |
| `scripts/check_spec.py` | Consistency checks; no dependencies |

## Conventions and gotchas

- **Version bump in every PR that changes the spec** (SPEC-4): major for a new or stricter MUST, minor for a new
  SHOULD/MAY or section, patch for clarifications. Update the `Spec version` row and add a `## [X.Y.Z] - Unreleased`
  section to `CHANGELOG.md`. When the maintainer asks for a release, the release PR replaces `Unreleased` with the
  date; then create the annotated tag `vX.Y.Z` on `main`.
- **Requirement IDs are stable.** Never reuse or renumber an ID. Add new rules with the next free number of their
  prefix. Mark removed rules as removed instead of deleting them silently. Section numbers may change; when they
  do, fix every `§N` reference and `(#anchor)` link (the check script catches broken links).
- **Upgrade notes** go in every major version's CHANGELOG section: what an app must change to comply.
- **Readers are agents:** say exactly what to do, with names, paths, values and rule IDs. Use MUST/SHOULD/MAY
  (RFC 2119). Prefer tables and short rules to prose.
- **The reference implementation** is `agtdarkshadow04/agt_event_calendar`. Rules should match what it does, or
  its `AGENTS.md` should list the gap. New rules usually mean a follow-up issue there.
- Commit messages: short imperative sentence.
