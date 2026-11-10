#!/usr/bin/env python3
"""Checks agt-webapp-spec.md: internal links resolve, requirement IDs are unique and every cited ID is defined,
and the version in the header matches the newest CHANGELOG.md release. Exits 1 on any problem.

Usage: python3 scripts/check_spec.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = (ROOT / 'agt-webapp-spec.md').read_text(encoding='utf-8')
changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
problems: list[str] = []


def slug(heading: str) -> str:
    """GitHub's heading anchor."""
    text = re.sub(r'[^\w\- ]', '', heading.strip().lower())
    return text.replace(' ', '-')


anchors = {slug(m.group(1)) for m in re.finditer(r'^#{1,6} (.+)$', spec, re.M)}
for link in sorted(set(re.findall(r'\]\(#([^)]+)\)', spec))):
    if link not in anchors:
        problems.append(f'broken internal link: #{link}')

# Requirement IDs are defined as **PREFIX-N**, optionally with a label: **DATA-5 (SQLite)**.
# Every ID is defined exactly once (SPEC-4).
defined = re.findall(r'\*\*([A-Z0-9]+-\d+)(?: \([^)*]*\))?\*\*', spec)
for rule_id in sorted(set(defined)):
    if defined.count(rule_id) > 1:
        problems.append(f'requirement ID defined more than once: {rule_id}')
prefixes = {rule_id.split('-')[0] for rule_id in defined}
cited = set(re.findall(r'\b(' + '|'.join(sorted(prefixes)) + r')-(\d+)\b', spec))
for prefix, number in sorted(cited):
    if f'{prefix}-{number}' not in defined:
        problems.append(f'cited but never defined: {prefix}-{number}')

version = re.search(r'\| \*\*Spec version\*\* \| (\d+\.\d+\.\d+) \|', spec)
newest = re.search(r'^## \[(\d+\.\d+\.\d+)\]', changelog, re.M)
if not version:
    problems.append('no "Spec version" row in the header')
elif not newest or newest.group(1) != version.group(1):
    problems.append(f'spec version {version.group(1)} is not the newest CHANGELOG.md heading')

for problem in problems:
    print(problem)
print(f'{len(defined)} requirement IDs, {len(anchors)} headings: ' + ('FAILED' if problems else 'OK'))
sys.exit(1 if problems else 0)
