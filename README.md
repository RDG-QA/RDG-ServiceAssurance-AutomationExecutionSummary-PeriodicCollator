# RDG Service Assurance – Automation Execution Summary – Periodic Collator

![RDG Service Assurance](https://img.shields.io/badge/RDG-Service%20Assurance-blue) ![Version](https://img.shields.io/badge/version-1.0-green) ![Python](https://img.shields.io/badge/python-3.9%2B-yellow)

## Overview

This repository contains the tooling and documentation for the **RDG Service Assurance Automation Execution Summary Periodic Collator** — a system for collecting, parsing, and consolidating automated test execution reports across multiple RDG systems into a single formatted Excel workbook.

The collator ingests test reports from a variety of tools and formats (Playwright HTML dashboards, ReadyAPI project screenshots, Robot Framework reports, Allure/JUnit outputs) and produces a consolidated Excel workbook with:

- 📋 **Executive Summary** — KPI tiles, per-system pass rates, grand totals
- 📊 **Raw Data** — one row per test run, grouped by system with batch dividers
- 📈 **Pivot Chart** — clustered bar chart grouped by core system

---

## Supported Systems (as of Jun 2026)

| System | Tool / Framework | Report Format |
|---|---|---|
| AWS Gateway API Test Suite | ReadyAPI | Screenshot (PNG) |
| MuleSoft API Test Suite | ReadyAPI | Screenshot (PNG) |
| RDM (Reference Data Management) | Allure / Java | HTML Report |
| PA Systems (Retail TOC Portal, EEH, Request Assistance, Manage Booking) | Playwright / SoapUI | HTML Report |
| National Rail Website (Live Trains) | Playwright | HTML Report |
| National Rail App – iOS & Android | Robot Framework | HTML Report |
| Railcard (RQA-555) – BAU / Checks / Comprehensive | Playwright Dashboard | HTML Dashboard |
| Railcard API (Final) | ReadyAPI | Screenshot (PNG) |

---

## Repository Structure

```
RDG-ServiceAssurance-AutomationExecutionSummary-PeriodicCollator/
│
├── README.md                    # This file
├── USER_MANUAL.pdf              # Full user manual with instructions
│
├── collator/
│   ├── parse_reports.py         # Core HTML parser for Playwright/Robot/Allure reports
│   ├── parse_screenshots.py     # Manual data entry helper for ReadyAPI screenshots
│   ├── build_workbook.py        # Excel workbook builder (openpyxl)
│   ├── system_map.py            # System name → consolidated label mapping
│   └── run_collator.py          # Main entry point — runs full pipeline
│
├── data/
│   ├── input/                   # Drop report HTML files and PNGs here
│   └── output/                  # Generated Excel workbooks saved here
│
├── requirements.txt             # Python dependencies
└── .gitignore
```

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_ORG/RDG-ServiceAssurance-AutomationExecutionSummary-PeriodicCollator.git
cd RDG-ServiceAssurance-AutomationExecutionSummary-PeriodicCollator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your report files

Copy your HTML report files and/or PNG screenshots into:

```
data/input/
```

### 4. Run the collator

```bash
python collator/run_collator.py
```

The output Excel workbook will be saved to `data/output/` with a timestamped filename:

```
RDG - Service Assurance - Automation Summary - v1.0 - YYYYMMDD-HHMM.xlsx
```

---

## Input File Types

| Type | Extension | Systems |
|---|---|---|
| Playwright HTML Dashboard | `.html` | Railcard RQA-555, PA Systems, NR Website |
| Robot Framework HTML | `.html` | National Rail App iOS & Android |
| Allure/JUnit HTML | `.html` | RDM |
| ReadyAPI screenshots | `.png` / `.PNG` | AWS Gateway API, MuleSoft API, Railcard API |

> **Note:** ReadyAPI screenshots require manual data entry via `parse_screenshots.py` as they cannot be machine-parsed. See the User Manual for instructions.

---

## Output Workbook

The generated Excel file contains three worksheets:

1. **Executive Summary** — High-level KPI tiles + consolidated table (one row per core system)
2. **Raw Data** — Full detail, one row per report run, grouped by system
3. **Pivot Chart** — Clustered bar chart of Total / Passed / Failed / Other by core system

---

## System Consolidation Map

Multiple sub-system report names are merged into single consolidated rows in the pivot:

| Raw System Name | Consolidated Label |
|---|---|
| PA - Retail TOC Portal, EEH, PA - Request Assistance, PA - Manage Booking, Staff Account Management | PA Systems (combined) |
| National Rail App - iOS, National Rail App - Android | National Rail App (iOS & Android) |
| Railcard (RQA-555) – BAU, Railcard (RQA-555) – Checks, Railcard (RQA-555) – Comprehensive | Railcard (RQA-555) |

---

## Dependencies

```
openpyxl>=3.1.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
fpdf2>=2.7.0
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-change`
3. Commit your changes: `git commit -m "Add my change"`
4. Push to the branch: `git push origin feature/my-change`
5. Open a Pull Request

---

## Version History

| Version | Date | Notes |
|---|---|---|
| 1.0 | Jun 2026 | Initial release — 138 report rows, 8 core systems, Mar–Jun 2026 data |

---

## Contact

RDG Quality Assurance – Service Assurance Team
