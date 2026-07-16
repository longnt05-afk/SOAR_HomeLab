#!/usr/bin/env python3
"""Verify the DFIR-IRIS IrisMISP custom-tab hotfix."""

from __future__ import annotations

import argparse
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

NAV_TARGET = (
    "attr_{{page_uid}}{{ loop.index }}_"
    "{{ ca.lower() | replace(' ', '_' ) }}"
)
PANE_TARGET = (
    "attr_{{page_uid}}{{ outer_loop.index }}_"
    "{{ ca.lower() | replace(' ', '_' ) }}"
)


class VerifyError(RuntimeError):
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
        raise VerifyError(
            f"Command not found: {command[0]}"
        ) from exc

    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        raise VerifyError(
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
        raise VerifyError(
            f"No running container found for service '{service}'."
        )
    if "\n" in container:
        raise VerifyError(
            f"Multiple containers found for service '{service}'."
        )
    return container


def read_file(container: str, path: Path) -> str:
    return run(
        ["docker", "exec", container, "cat", str(path)]
    ).stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the four safe custom-tab identifiers after "
            "applying the DFIR-IRIS IrisMISP hotfix."
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
    parser.add_argument(
        "--show-lines",
        action="store_true",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if shutil.which("docker") is None:
        raise VerifyError("The docker command is not installed.")

    compose_dir = args.compose_dir.expanduser().resolve()
    if not compose_dir.is_dir():
        raise VerifyError(
            f"Compose directory does not exist: {compose_dir}"
        )

    container = get_container(compose_dir, args.service)
    nav_text = read_file(container, NAV_PATH)
    tabs_text = read_file(container, TABS_PATH)

    checks = {
        "navigation href": f'href="#{NAV_TARGET}"' in nav_text,
        "navigation aria-controls": (
            f'aria-controls="{NAV_TARGET}"' in nav_text
        ),
        "content pane id": (
            f'id="{PANE_TARGET}"' in tabs_text
        ),
        "content pane aria-labelledby": (
            f'aria-labelledby="{PANE_TARGET}-tab"' in tabs_text
        ),
    }

    failed = [
        name for name, passed in checks.items() if not passed
    ]

    for name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        print(f"[{result}] {name}")

    if failed:
        raise VerifyError(
            "Verification failed: " + ", ".join(failed)
        )

    print("VERIFICATION PASS")
    print(
        "Expected rendered pattern: "
        "attr_<number>_misp_report"
    )

    if args.show_lines:
        print("\nMatching navigation lines:")
        for line in nav_text.splitlines():
            if "attr_" in line and (
                "href=" in line or "aria-controls=" in line
            ):
                print(line.strip())

        print("\nMatching content-pane lines:")
        for line in tabs_text.splitlines():
            if "attr_" in line and (
                'id="' in line
                or "aria-labelledby=" in line
            ):
                print(line.strip())

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerifyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
