#!/usr/bin/env python3
"""Read-only compatibility check for the DFIR-IRIS IrisMISP hotfix."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence


DEFAULT_COMPOSE_DIR = Path("/opt/ir/iris-web")
DEFAULT_SERVICE = "app"

NAV_PATH = Path(
    "/iriswebapp/app/templates/modals/modal_attributes_nav.html"
)
TABS_PATH = Path(
    "/iriswebapp/app/templates/modals/modal_attributes_tabs.html"
)

CA_EXPR = (
    r"\{\{\s*ca\.lower\(\)\s*\|\s*"
    r"replace\(\s*' '\s*,\s*'_'\s*\)\s*\}\}"
)
PAGE_UID_EXPR = r"\{\{\s*page_uid\s*\}\}"
LOOP_EXPR = r"\{\{\s*loop\.index\s*\}\}"
OUTER_LOOP_EXPR = r"\{\{\s*outer_loop\.index\s*\}\}"

NAV_TARGET = (
    "attr_{{page_uid}}{{ loop.index }}_"
    "{{ ca.lower() | replace(' ', '_' ) }}"
)
PANE_TARGET = (
    "attr_{{page_uid}}{{ outer_loop.index }}_"
    "{{ ca.lower() | replace(' ', '_' ) }}"
)


class CheckError(RuntimeError):
    pass


def run(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            list(command),
            cwd=str(cwd) if cwd else None,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise CheckError(
            f"Command not found: {command[0]}"
        ) from exc

    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        raise CheckError(
            f"Command failed ({result.returncode}): "
            f"{' '.join(command)}"
            + (f"\n{details}" if details else "")
        )
    return result


def get_container(compose_dir: Path, service: str) -> str:
    container = run(
        ["docker", "compose", "ps", "-q", service],
        cwd=compose_dir,
    ).stdout.strip()

    if not container:
        raise CheckError(
            f"No running container found for service '{service}'."
        )
    if "\n" in container:
        raise CheckError(
            f"Multiple containers found for service '{service}'."
        )
    return container


def read_file(container: str, path: Path) -> str:
    return run(
        ["docker", "exec", container, "cat", str(path)]
    ).stdout


def is_patched(nav_text: str, tabs_text: str) -> bool:
    return (
        f'href="#{NAV_TARGET}"' in nav_text
        and f'aria-controls="{NAV_TARGET}"' in nav_text
        and f'id="{PANE_TARGET}"' in tabs_text
        and f'aria-labelledby="{PANE_TARGET}-tab"' in tabs_text
    )


def has_numeric_first_layout(
    nav_text: str,
    tabs_text: str,
) -> bool:
    numeric_nav = re.search(
        r'href="#(?:'
        + PAGE_UID_EXPR
        + r")?"
        + LOOP_EXPR
        + r"\s*_\s*"
        + CA_EXPR
        + r'"',
        nav_text,
    )
    intermediate_nav = re.search(
        r'href="#'
        + CA_EXPR
        + r"\s*_\s*"
        + LOOP_EXPR
        + r'"',
        nav_text,
    )
    numeric_pane = re.search(
        r'id="(?:'
        r"\{%\s*if\s+is_case_page\s*%\}\s*"
        r"itab_\s*"
        r"\{%\s*endif\s*%\}\s*"
        r")?(?:"
        + PAGE_UID_EXPR
        + r")?"
        + OUTER_LOOP_EXPR
        + r"\s*_\s*"
        + CA_EXPR
        + r'"',
        tabs_text,
    )
    return bool(
        (numeric_nav or intermediate_nav)
        and numeric_pane
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Perform a read-only compatibility check for the "
            "DFIR-IRIS IrisMISP custom-tab hotfix."
        )
    )
    parser.add_argument(
        "--compose-dir",
        type=Path,
        default=DEFAULT_COMPOSE_DIR,
    )
    parser.add_argument(
        "--service",
        default=DEFAULT_SERVICE,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if shutil.which("docker") is None:
        raise CheckError("The docker command is not installed.")

    compose_dir = args.compose_dir.expanduser().resolve()
    if not compose_dir.is_dir():
        raise CheckError(
            f"Compose directory does not exist: {compose_dir}"
        )

    container = get_container(compose_dir, args.service)
    nav_text = read_file(container, NAV_PATH)
    tabs_text = read_file(container, TABS_PATH)

    print(f"Container: {container}")
    print(f"Navigation template: {NAV_PATH}")
    print(f"Content template: {TABS_PATH}")

    if is_patched(nav_text, tabs_text):
        print("Status: PATCHED")
        print("Next action: run verify.py")
        return 0

    if has_numeric_first_layout(nav_text, tabs_text):
        print("Status: VULNERABLE_NUMERIC_FIRST_ID")
        print("Next action: run apply.py")
        return 10

    print("Status: UNSUPPORTED_TEMPLATE_LAYOUT")
    print(
        "Next action: stop and inspect the two templates manually."
    )
    return 20


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
