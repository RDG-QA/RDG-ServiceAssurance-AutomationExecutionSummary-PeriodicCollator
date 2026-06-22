"""
parse_screenshots.py
--------------------
Helper for manually entering ReadyAPI screenshot data.

ReadyAPI results are presented as screenshots (PNG) and cannot be
machine-parsed. This module provides a structured template for
entering screenshot data manually.

Usage:
    Edit the SCREENSHOT_DATA list below with your screenshot data,
    then import this module in run_collator.py.
"""

# ── Manual screenshot data ──────────────────────────────────────────────────
# Add one dict per screenshot. Fields:
#   system    : exact system name (must match system_map.py)
#   release   : descriptive label e.g. "Full Suite (30-Apr-2026)"
#   run_date  : "DD-Mon-YYYY" or "YYYY-MM-DD"
#   tool      : always "ReadyAPI"
#   total     : total test cases executed
#   passed    : passed test cases
#   failed    : failed test cases
#   other     : skipped / not run (usually 0 for ReadyAPI)
#   notes     : free text — suite names, observations

SCREENSHOT_DATA = [
    # ── AWS Gateway API ──
    {
        "system":   "AWS Gateway API",
        "release":  "Full Suite (31-Mar-2026)",
        "run_date": "31-Mar-2026",
        "tool":     "ReadyAPI",
        "total":    168,
        "passed":   168,
        "failed":   0,
        "other":    0,
        "notes":    "5 suites: Experience-Availability, v2 Bookings, RefData, Coaches, Passenger Reports. All passed.",
    },
    # ── Railcard API (Final) ──
    {
        "system":   "Railcard API (Final)",
        "release":  "Full Suite (01-Apr-2026)",
        "run_date": "01-Apr-2026",
        "tool":     "ReadyAPI",
        "total":    51,
        "passed":   51,
        "failed":   0,
        "other":    0,
        "notes":    "4 Suites: Accounts, Orders, Railcards, Manual. All passed.",
    },
    # Add more entries here...
]


def get_screenshot_data() -> list[dict]:
    """Return the manually entered screenshot data."""
    return SCREENSHOT_DATA
