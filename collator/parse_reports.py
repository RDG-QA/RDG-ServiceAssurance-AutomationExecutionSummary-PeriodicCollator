"""
parse_reports.py
----------------
Parses HTML test report files into structured dicts.

Supports:
  - Playwright Dashboard (RQA-555 Railcard, PA Systems, NR Website)
  - Robot Framework HTML reports (NR App iOS/Android)
  - Allure / JUnit HTML reports (RDM)

Returns a list of dicts with keys:
  system, release, run_date, tool, total, passed, failed, other, notes
"""

import re
from pathlib import Path


def parse_playwright_dashboard(filepath: Path) -> dict:
    """Parse a Playwright Dashboard HTML file (RQA-555 / PA systems)."""
    content = filepath.read_text(encoding="utf-8", errors="ignore")

    subtitle_m = re.search(
        r"Issue:\s*(RQA-\d+)\s*·\s*Flows:\s*(.*?)\s*·\s*Sheet:\s*([^<\n]+)",
        content, re.DOTALL
    )
    issue  = subtitle_m.group(1).strip() if subtitle_m else "Unknown"
    flows  = subtitle_m.group(2).replace("\n", "").strip() if subtitle_m else ""
    sheet  = subtitle_m.group(3).strip().rstrip("</div>").strip() if subtitle_m else "Unknown"

    passed_m  = re.search(r"Passed:</strong>\s*([\d,]+)", content)
    failed_m  = re.search(r"Failed:</strong>\s*([\d,]+)", content)
    flaky_m   = re.search(r"Flaky:</strong>\s*([\d,]+)", content)
    total_m   = re.search(r"Passed:</strong>\s*[\d,]+\s*<span[^>]*>of\s*([\d,]+)", content)

    passed = int(passed_m.group(1).replace(",", "")) if passed_m else 0
    failed = int(failed_m.group(1).replace(",", "")) if failed_m else 0
    flaky  = int(flaky_m.group(1).replace(",", ""))  if flaky_m  else 0
    total  = int(total_m.group(1).replace(",", ""))  if total_m  else passed + failed

    dates    = re.findall(r"\d{4}-\d{2}-\d{2}", content)
    run_date = dates[0] if dates else "Unknown"

    system_name = f"Railcard (RQA-555) – {sheet}" if issue.startswith("RQA") else "PA - Retail TOC Portal"

    return {
        "system":   system_name,
        "release":  f"{filepath.stem} ({run_date})",
        "run_date": run_date,
        "tool":     "Playwright Dashboard",
        "total":    total,
        "passed":   passed,
        "failed":   failed,
        "other":    flaky,
        "notes":    f"Sheet: {sheet}. Flows: {flows}. flaky={flaky}.",
    }


def parse_playwright_html(filepath: Path, system: str) -> dict:
    """Parse a standard Playwright HTML test report (PA / NR Website)."""
    content = filepath.read_text(encoding="utf-8", errors="ignore")

    passed_m  = re.search(r"(\d+)\s+passed", content)
    failed_m  = re.search(r"(\d+)\s+failed", content)
    flaky_m   = re.search(r"(\d+)\s+flaky",  content)
    skipped_m = re.search(r"(\d+)\s+skipped", content)

    passed  = int(passed_m.group(1))  if passed_m  else 0
    failed  = int(failed_m.group(1))  if failed_m  else 0
    flaky   = int(flaky_m.group(1))   if flaky_m   else 0
    skipped = int(skipped_m.group(1)) if skipped_m else 0
    total   = passed + failed + flaky + skipped

    dates    = re.findall(r"\d{4}-\d{2}-\d{2}", content)
    run_date = dates[0] if dates else "Unknown"

    return {
        "system":   system,
        "release":  f"{filepath.name} ({run_date})",
        "run_date": run_date,
        "tool":     "Playwright",
        "total":    total,
        "passed":   passed,
        "failed":   failed,
        "other":    flaky + skipped,
        "notes":    f"expected={passed}, unexpected={failed}, flaky={flaky}, skipped={skipped}.",
    }


def parse_robot_framework(filepath: Path, system: str) -> dict:
    """Parse a Robot Framework HTML report (NR App iOS/Android)."""
    content = filepath.read_text(encoding="utf-8", errors="ignore")

    passed_m = re.search(r"(\d+)\s+tests?,\s+(\d+)\s+passed,\s+(\d+)\s+failed", content)
    if passed_m:
        total  = int(passed_m.group(1))
        passed = int(passed_m.group(2))
        failed = int(passed_m.group(3))
    else:
        passed = failed = total = 0

    dates    = re.findall(r"\d{8}\s+\d{2}:\d{2}:\d{2}", content)
    run_date = dates[0][:8] if dates else "Unknown"
    if run_date != "Unknown":
        run_date = f"{run_date[:4]}-{run_date[4:6]}-{run_date[6:]}"

    return {
        "system":   system,
        "release":  f"{filepath.stem} ({run_date})",
        "run_date": run_date,
        "tool":     "Robot Framework",
        "total":    total,
        "passed":   passed,
        "failed":   failed,
        "other":    0,
        "notes":    f"Robot Framework report.",
    }


def auto_parse(filepath: Path) -> dict | None:
    """
    Attempt to auto-detect the report type from the HTML content
    and parse accordingly. Returns None if unrecognised.
    """
    content = filepath.read_text(encoding="utf-8", errors="ignore")[:2000]

    if "Playwright Dashboard" in content and "RQA-" in content:
        return parse_playwright_dashboard(filepath)
    if "Playwright Dashboard" in content:
        return parse_playwright_html(filepath, system="PA - Retail TOC Portal")
    if "Robot Framework" in content or "robot-framework" in content.lower():
        system = "National Rail App - iOS" if "ios" in filepath.name.lower() else "National Rail App - Android"
        return parse_robot_framework(filepath, system)
    if "allure" in content.lower() or "junit" in content.lower():
        return parse_playwright_html(filepath, system="RDM (Reference Data Management)")

    return None


def parse_directory(input_dir: str) -> list[dict]:
    """
    Parse all HTML files in the given directory.
    Returns a list of parsed report dicts.
    """
    results = []
    for path in sorted(Path(input_dir).glob("*.html")):
        result = auto_parse(path)
        if result:
            results.append(result)
        else:
            print(f"  [WARN] Could not auto-detect format for: {path.name}")
    return results
