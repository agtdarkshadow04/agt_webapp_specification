#!/usr/bin/env python3
"""Checks agt-webapp-spec.md: internal links resolve, requirement IDs are unique and every cited ID is defined,
the version in the header matches the newest CHANGELOG.md release, and every file in assets/ matches the SHA-256
listed in assets/README.md (and every listed file exists). Exits 1 on any problem.

Usage: python3 scripts/check_spec.py
"""
import hashlib
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

# assets/README.md lists each asset as | `path` | purpose | `sha256` |, paths relative to assets/.
assets_dir = ROOT / 'assets'
listed = dict(re.findall(r'^\| `([^`]+)` \| [^|]+ \| `([0-9a-f]{64})` \|$',
                         (assets_dir / 'README.md').read_text(encoding='utf-8'), re.M))
for path, digest in sorted(listed.items()):
    file = assets_dir / path
    if not file.is_file():
        problems.append(f'assets/README.md lists a missing file: assets/{path}')
    elif hashlib.sha256(file.read_bytes()).hexdigest() != digest:
        problems.append(f'SHA-256 of assets/{path} does not match assets/README.md')
for file in sorted(assets_dir.rglob('*')):
    rel = file.relative_to(assets_dir).as_posix()
    if file.is_file() and rel != 'README.md' and rel not in listed:
        problems.append(f'assets/{rel} is not listed in assets/README.md')

# The base stylesheet's :root rule must be the UI-1 token block, byte for byte (after removing the indent).
ui1 = re.search(r'\*\*UI-1\*\*.*?```css\n(.*?)```', spec, re.S)
base_css = assets_dir / 'css' / 'agt-base.css'
if ui1 and base_css.is_file():
    block = '\n'.join(line[2:] if line.startswith('  ') else line for line in ui1.group(1).splitlines())
    if block.strip() not in base_css.read_text(encoding='utf-8'):
        problems.append('assets/css/agt-base.css does not contain the UI-1 :root block verbatim')

for problem in problems:
    print(problem)
print(f'{len(defined)} requirement IDs, {len(anchors)} headings, {len(listed)} assets: ' + ('FAILED' if problems else 'OK'))
sys.exit(1 if problems else 0)
