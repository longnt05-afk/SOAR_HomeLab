#!/usr/bin/env python3
"""Offline tests for the patch logic implemented in apply.py."""

from __future__ import annotations

import sys

from apply import (
    HotfixError,
    PatchResult,
    is_patched,
    patch_templates,
)


ORIGINAL_NAV = """\
<a class="nav-link" data-toggle="pill"
href="#{{page_uid}}{{ loop.index }}_{{  ca.lower() | replace(' ', '_' ) }}"
role="tab"
aria-controls="{{page_uid}}{{ loop.index }}_{{  ca.lower() | replace(' ', '_' ) }}"
aria-selected="false">{{ca}}</a>
"""

ORIGINAL_TABS = """\
<div class="tab-pane"
id="{% if is_case_page %}itab_{% endif %}{{page_uid}}{{ outer_loop.index }}_{{ ca.lower() | replace(' ', '_' ) }}"
aria-labelledby="{% if is_case_page %}itab_{% endif %}{{page_uid}}{{ outer_loop.index }}_{{ ca.lower() | replace(' ', '_' ) }}-tab">
</div>
"""

INTERMEDIATE_NAV = """\
<a class="nav-link" data-toggle="pill"
href="#{{ loop.index }}_{{ ca.lower() | replace(' ', '_' ) }}"
role="tab"
aria-controls="{{ loop.index }}_{{ ca.lower() | replace(' ', '_' ) }}"
aria-selected="false">{{ca}}</a>
"""

INTERMEDIATE_TABS = """\
<div class="tab-pane"
id="{{page_uid}}{{ outer_loop.index }}_{{ ca.lower() | replace(' ', '_' ) }}"
aria-labelledby="{{page_uid}}{{ outer_loop.index }}_{{ ca.lower() | replace(' ', '_' ) }}-tab">
</div>
"""


def run_case(
    name: str,
    nav_text: str,
    tabs_text: str,
) -> tuple[str, str]:
    nav_out, tabs_out, result = patch_templates(
        nav_text,
        tabs_text,
    )

    expected = PatchResult(1, 1, 1, 1)
    if result != expected:
        raise AssertionError(
            f"{name}: unexpected replacement count: {result}"
        )
    if not is_patched(nav_out, tabs_out):
        raise AssertionError(
            f"{name}: patched output was not recognized"
        )

    print(f"[PASS] {name}")
    return nav_out, tabs_out


def main() -> int:
    first_nav, first_tabs = run_case(
        "Original v2.4.29-style sample",
        ORIGINAL_NAV,
        ORIGINAL_TABS,
    )

    run_case(
        "Intermediate numeric-first sample",
        INTERMEDIATE_NAV,
        INTERMEDIATE_TABS,
    )

    second_nav, second_tabs, result = patch_templates(
        first_nav,
        first_tabs,
    )
    if result.total != 0:
        raise AssertionError(
            "Already-patched sample was modified again"
        )
    if second_nav != first_nav or second_tabs != first_tabs:
        raise AssertionError(
            "Already-patched sample changed unexpectedly"
        )

    print("[PASS] Already-patched sample")
    print("SELF-TEST PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, HotfixError) as exc:
        print(f"SELF-TEST FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
