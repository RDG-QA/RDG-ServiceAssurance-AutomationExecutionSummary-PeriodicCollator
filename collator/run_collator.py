"""
run_collator.py
---------------
Main entry point for the RDG Service Assurance Automation Collator.

Usage:
    python collator/run_collator.py [--input data/input] [--output data/output]

Steps:
  1. Parses all HTML files in the input directory
  2. Merges manually entered screenshot data (ReadyAPI PNGs)
  3. Builds and saves the Excel workbook to the output directory
"""

import argparse
import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

from collator.parse_reports import parse_directory
from collator.parse_screenshots import get_screenshot_data
from collator.build_workbook import build_workbook


def main():
    parser = argparse.ArgumentParser(
        description="RDG Service Assurance – Automation Execution Summary Collator"
    )
    parser.add_argument(
        "--input", default="data/input",
        help="Directory containing HTML report files (default: data/input)"
    )
    parser.add_argument(
        "--output", default="data/output",
        help="Directory to save the output Excel workbook (default: data/output)"
    )
    parser.add_argument(
        "--no-screenshots", action="store_true",
        help="Skip loading manually entered screenshot data"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("RDG Service Assurance – Automation Collator v1.0")
    print("=" * 60)

    # 1. Parse HTML reports
    print(f"\n📂  Scanning input directory: {args.input}")
    html_data = parse_directory(args.input)
    print(f"    → Found {len(html_data)} HTML report(s)")

    # 2. Merge screenshot data
    screenshot_data = []
    if not args.no_screenshots:
        screenshot_data = get_screenshot_data()
        print(f"    → Loaded {len(screenshot_data)} manually entered screenshot record(s)")

    all_data = html_data + screenshot_data
    print(f"\n📊  Total records to process: {len(all_data)}")

    if not all_data:
        print("\n⚠️   No data found. Check your input directory and screenshot data.")
        sys.exit(1)

    # 3. Build workbook
    print(f"\n📝  Building workbook...")
    output_path = build_workbook(all_data, output_path=None)

    print(f"\n✅  Done! Output saved to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
