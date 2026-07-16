#!/usr/bin/env python3
"""Back up and patch the DFIR-IRIS IrisMISP custom-tab templates."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


DEFAULT_COMPOSE_DIR = Path("/opt/ir/iris-web")
DEFAULT_SERVICE = "app"
DEFAULT_BACKUP_ROOT = (
    Path.home() / "iris-hotfix-backups" / "iris-misp-report"
)

NAV_PATH = Path(
    "/iriswebapp/app/templates/modals/modal_attributes_nav.html"
)
TABS_PATH = Path(
    "/iriswebapp/app/templates/modals/modal_attributes_tabs.html"
)


class HotfixError(RuntimeError):
    """Expected hotfix failure with a user-facing message."""


@dataclass(frozen=True)
class PatchResult:
    href: int
    aria_controls: int
    pane_id: int
    pane_aria_labelledby: int

    @property
    def total(self) -> int:
        return (
            self.href
            + self.aria_controls
            + self.pane_id
            + self.pane_aria_labelledby
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


def run(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command without using a shell."""
    try:
        result = subprocess.run(
            list(command),
            cwd=str(cwd) if cwd else None,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise HotfixError(f"Command not found: {command[0]}") from exc

    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        raise HotfixError(
            f"Command failed ({result.returncode}): "
            f"{' '.join(command)}"
            + (f"\n{details}" if details else "")
        )
    return result


def get_container(compose_dir: Path, service: str) -> str:
    """Return the single running container ID for the compose service."""
    result = run(
        ["docker", "compose", "ps", "-q", service],
        cwd=compose_dir,
    )
    container = result.stdout.strip()

    if not container:
        raise HotfixError(
            f"No running container found for service '{service}'."
        )
    if "\n" in container:
        raise HotfixError(
            f"Multiple containers found for service '{service}'."
        )
    return container


def docker_read(container: str, path: Path) -> str:
    """Read a UTF-8 file from the running container."""
    return run(
        ["docker", "exec", container, "cat", str(path)]
    ).stdout


def docker_write(container: str, path: Path, content: str) -> None:
    """Write a UTF-8 file to the running container via base64."""
    encoded = base64.b64encode(
        content.encode("utf-8")
    ).decode("ascii")

    python_code = (
        "from pathlib import Path;"
        "import base64;"
        f"Path({str(path)!r}).write_bytes("
        f"base64.b64decode({encoded!r}))"
    )

    run(
        [
            "docker",
            "exec",
            container,
            "python3",
            "-c",
            python_code,
        ]
    )


def expected_fragments() -> tuple[str, str, str, str]:
    return (
        f'href="#{NAV_TARGET}"',
        f'aria-controls="{NAV_TARGET}"',
        f'id="{PANE_TARGET}"',
        f'aria-labelledby="{PANE_TARGET}-tab"',
    )


def is_patched(nav_text: str, tabs_text: str) -> bool:
    """Return True when all four safe identifiers are present."""
    href, aria, pane_id, pane_aria = expected_fragments()
    return (
        href in nav_text
        and aria in nav_text
        and pane_id in tabs_text
        and pane_aria in tabs_text
    )


def build_nav_current_id_pattern() -> str:
    """Match known numeric-first or previous intermediate nav IDs."""
    numeric_first = (
        r"(?:"
        + PAGE_UID_EXPR
        + r")?"
        + LOOP_EXPR
        + r"\s*_\s*"
        + CA_EXPR
    )
    name_first = (
        CA_EXPR
        + r"\s*_\s*"
        + LOOP_EXPR
    )
    return r"(?:" + numeric_first + r"|" + name_first + r")"


def build_pane_current_id_pattern() -> str:
    """Match known numeric-first or previous intermediate pane IDs."""
    optional_itab = (
        r"(?:"
        r"\{%\s*if\s+is_case_page\s*%\}\s*"
        r"itab_\s*"
        r"\{%\s*endif\s*%\}\s*"
        r")?"
    )
    numeric_first = (
        optional_itab
        + r"(?:"
        + PAGE_UID_EXPR
        + r")?"
        + OUTER_LOOP_EXPR
        + r"\s*_\s*"
        + CA_EXPR
    )
    name_first = (
        CA_EXPR
        + r"\s*_\s*"
        + OUTER_LOOP_EXPR
    )
    return r"(?:" + numeric_first + r"|" + name_first + r")"


def patch_templates(
    nav_text: str,
    tabs_text: str,
) -> tuple[str, str, PatchResult]:
    """Patch exactly four attributes and refuse ambiguous layouts."""
    if is_patched(nav_text, tabs_text):
        return nav_text, tabs_text, PatchResult(0, 0, 0, 0)

    nav_id = build_nav_current_id_pattern()
    pane_id = build_pane_current_id_pattern()

    href_pattern = re.compile(
        r'href="#' + nav_id + r'"'
    )
    aria_pattern = re.compile(
        r'aria-controls="' + nav_id + r'"'
    )
    pane_id_pattern = re.compile(
        r'id="' + pane_id + r'"'
    )
    pane_aria_pattern = re.compile(
        r'aria-labelledby="' + pane_id + r'-tab"'
    )

    nav_updated, href_count = href_pattern.subn(
        f'href="#{NAV_TARGET}"',
        nav_text,
        count=1,
    )
    nav_updated, aria_count = aria_pattern.subn(
        f'aria-controls="{NAV_TARGET}"',
        nav_updated,
        count=1,
    )
    tabs_updated, pane_id_count = pane_id_pattern.subn(
        f'id="{PANE_TARGET}"',
        tabs_text,
        count=1,
    )
    tabs_updated, pane_aria_count = pane_aria_pattern.subn(
        f'aria-labelledby="{PANE_TARGET}-tab"',
        tabs_updated,
        count=1,
    )

    result = PatchResult(
        href=href_count,
        aria_controls=aria_count,
        pane_id=pane_id_count,
        pane_aria_labelledby=pane_aria_count,
    )

    expected = PatchResult(1, 1, 1, 1)
    if result != expected:
        raise HotfixError(
            "Refusing to write because the template structure was "
            "not matched exactly.\n"
            f"Replacement counts: {result}"
        )

    verify_content(nav_updated, tabs_updated)
    return nav_updated, tabs_updated, result


def verify_content(nav_text: str, tabs_text: str) -> None:
    """Raise an error unless all four expected fragments exist."""
    href, aria, pane_id, pane_aria = expected_fragments()
    missing: list[str] = []

    if href not in nav_text:
        missing.append("navigation href")
    if aria not in nav_text:
        missing.append("navigation aria-controls")
    if pane_id not in tabs_text:
        missing.append("content pane id")
    if pane_aria not in tabs_text:
        missing.append("content pane aria-labelledby")

    if missing:
        raise HotfixError(
            "Verification failed: " + ", ".join(missing)
        )


def backup_files(
    *,
    container: str,
    compose_dir: Path,
    service: str,
    backup_root: Path,
) -> Path:
    """Copy both original templates to a timestamped host directory."""
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )
    backup_dir = backup_root / timestamp
    backup_dir.mkdir(parents=True, exist_ok=False)

    mapping = {
        "modal_attributes_nav.html.original": NAV_PATH,
        "modal_attributes_tabs.html.original": TABS_PATH,
    }
    manifest_files: dict[str, dict[str, object]] = {}

    for output_name, container_path in mapping.items():
        output_path = backup_dir / output_name

        run(
            [
                "docker",
                "cp",
                f"{container}:{container_path}",
                str(output_path),
            ]
        )

        if not output_path.is_file():
            raise HotfixError(
                f"Backup file was not created: {output_path}"
            )
        raw = output_path.read_bytes()
        if not raw:
            raise HotfixError(
                f"Backup file is empty: {output_path}"
            )

        manifest_files[output_name] = {
            "container_path": str(container_path),
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }

    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "compose_dir": str(compose_dir),
        "service": service,
        "container": container,
        "files": manifest_files,
    }
    (backup_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return backup_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Back up and patch the DFIR-IRIS IrisMISP custom-tab "
            "identifier templates."
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
        "--backup-root",
        type=Path,
        default=DEFAULT_BACKUP_ROOT,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the patch without writing or restarting.",
    )
    parser.add_argument(
        "--no-restart",
        action="store_true",
        help="Write the patch without restarting the app service.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if shutil.which("docker") is None:
        raise HotfixError("The docker command is not installed.")

    compose_dir = args.compose_dir.expanduser().resolve()
    if not compose_dir.is_dir():
        raise HotfixError(
            f"Compose directory does not exist: {compose_dir}"
        )

    container = get_container(compose_dir, args.service)
    nav_text = docker_read(container, NAV_PATH)
    tabs_text = docker_read(container, TABS_PATH)

    if is_patched(nav_text, tabs_text):
        print("Status: PATCHED")
        print("No files were modified.")
        return 0

    nav_updated, tabs_updated, result = patch_templates(
        nav_text,
        tabs_text,
    )

    print("Planned replacements:")
    print(f"  href: {result.href}")
    print(f"  aria-controls: {result.aria_controls}")
    print(f"  pane id: {result.pane_id}")
    print(
        "  pane aria-labelledby: "
        f"{result.pane_aria_labelledby}"
    )

    if args.dry_run:
        print("DRY RUN PASS")
        print("No files were modified.")
        return 0

    backup_root = args.backup_root.expanduser().resolve()
    backup_root.mkdir(parents=True, exist_ok=True)

    backup_dir = backup_files(
        container=container,
        compose_dir=compose_dir,
        service=args.service,
        backup_root=backup_root,
    )
    print(f"BACKUP PASS: {backup_dir}")

    # Both patches are validated in memory before either file is written.
    docker_write(container, NAV_PATH, nav_updated)
    docker_write(container, TABS_PATH, tabs_updated)

    current_nav = docker_read(container, NAV_PATH)
    current_tabs = docker_read(container, TABS_PATH)
    verify_content(current_nav, current_tabs)
    print("PATCH VERIFICATION PASS")

    if not args.no_restart:
        run(
            ["docker", "compose", "restart", args.service],
            cwd=compose_dir,
        )
        print("APP SERVICE RESTARTED")

    print("HOTFIX APPLIED SUCCESSFULLY")
    print(f"Rollback backup: {backup_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except HotfixError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
