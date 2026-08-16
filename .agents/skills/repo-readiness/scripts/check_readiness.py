#!/usr/bin/env python3
"""Deterministically audit repository signals that support AI-assisted work."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    "coverage",
}

CHECKS = (
    {
        "id": "agent-context",
        "label": "Agent context files",
        "points": 3,
        "priority": 1,
        "patterns": ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules"),
        "recommendation": "Add a concise AGENTS.md or equivalent with the repository map, conventions, and validation commands.",
    },
    {
        "id": "agent-instructions",
        "label": "Agent instruction and rule files",
        "points": 3,
        "priority": 2,
        "patterns": ("copilot-instructions.md", "*.instructions.md", "*.mdc", ".windsurfrules"),
        "recommendation": "Add scoped agent instructions for the coding tool your team uses, including boundaries and required checks.",
    },
    {
        "id": "repeatable-workflows",
        "label": "Repeatable AI workflows",
        "points": 2,
        "priority": 3,
        "patterns": ("SKILL.md", "*.prompt.md"),
        "recommendation": "Package a recurring workflow as a focused SKILL.md or prompt file with clear inputs, steps, and outputs.",
    },
    {
        "id": "project-documentation",
        "label": "Project documentation",
        "points": 1,
        "priority": 4,
        "patterns": ("README.md", "CONTRIBUTING.md"),
        "recommendation": "Document setup, repository structure, common commands, and the expected verification path.",
    },
    {
        "id": "development-automation",
        "label": "Development automation",
        "points": 1,
        "priority": 5,
        "patterns": ("Makefile", "package.json", "pyproject.toml", "Cargo.toml", "go.mod", ".github/workflows/*.yml", ".github/workflows/*.yaml"),
        "recommendation": "Expose a repeatable test, lint, build, or CI command so an agent can verify changes consistently.",
    },
)


def iter_files(root: Path) -> Iterable[Path]:
    for current_root, directories, filenames in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in IGNORED_DIRS)
        for filename in sorted(filenames):
            yield Path(current_root) / filename


def matches(relative_path: Path, pattern: str) -> bool:
    if "/" in pattern:
        return relative_path.match(pattern)
    return relative_path.name == pattern or relative_path.match(pattern)


def audit(root: Path) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Repository path is not a directory: {root}")

    relative_files = sorted(path.relative_to(root) for path in iter_files(root))
    checks = []
    total = 0
    for definition in CHECKS:
        found = sorted(
            {path.as_posix() for path in relative_files if any(matches(path, pattern) for pattern in definition["patterns"])}
        )
        present = bool(found)
        awarded = definition["points"] if present else 0
        total += awarded
        checks.append(
            {
                "id": definition["id"],
                "label": definition["label"],
                "status": "present" if present else "missing",
                "points": awarded,
                "max_points": definition["points"],
                "paths": found,
                "priority": definition["priority"],
                "recommendation": None if present else definition["recommendation"],
            }
        )

    max_score = sum(definition["points"] for definition in CHECKS)
    rating = (
        "not-ready" if total <= 2 else
        "developing" if total <= 5 else
        "ready" if total <= 8 else
        "strong"
    )
    return {
        "schema_version": 1,
        "repository": str(root),
        "score": total,
        "max_score": max_score,
        "percentage": round(total / max_score * 100),
        "rating": rating,
        "checks": checks,
        "next_steps": [
            {"priority": check["priority"], "check_id": check["id"], "text": check["recommendation"]}
            for check in checks
            if check["recommendation"]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", help="Repository directory to audit")
    parser.add_argument("--pretty", action="store_true", help="Indent the JSON output")
    args = parser.parse_args()
    try:
        result = audit(Path(args.repository))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
