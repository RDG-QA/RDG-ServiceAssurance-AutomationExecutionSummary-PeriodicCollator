"""
system_map.py
-------------
Maps granular system names (as they appear in raw report data) to
consolidated core system labels used in the Pivot Chart and Executive Summary.

Also defines the canonical display order for the pivot table.
"""

SYSTEM_MAP = {
    "AWS Gateway API":                      "AWS Gateway API",
    "MuleSoft API Test Suite":              "MuleSoft API Test Suite",
    "RDM (Reference Data Management)":      "RDM (Reference Data Management)",
    "PA - Retail TOC Portal":               "PA Systems (combined)",
    "Enhanced Electronic Handover (EEH)":   "PA Systems (combined)",
    "PA - Request Assistance via Retail":   "PA Systems (combined)",
    "PA - Manage Booking":                  "PA Systems (combined)",
    "Staff Account Management":             "PA Systems (combined)",
    "National Rail Website (Live Trains)":  "National Rail Website (Live Trains)",
    "National Rail App - iOS":              "National Rail App (iOS & Android)",
    "National Rail App - Android":          "National Rail App (iOS & Android)",
    "Railcard (RQA-555) – BAU":             "Railcard (RQA-555)",
    "Railcard (RQA-555) – Checks":          "Railcard (RQA-555)",
    "Railcard (RQA-555) – Comprehensive":   "Railcard (RQA-555)",
    "Railcard API (Final)":                 "Railcard API (Final)",
}

# Canonical display order in pivot / summary tables
SYSTEM_ORDER = [
    "AWS Gateway API",
    "MuleSoft API Test Suite",
    "RDM (Reference Data Management)",
    "PA Systems (combined)",
    "National Rail Website (Live Trains)",
    "National Rail App (iOS & Android)",
    "Railcard (RQA-555)",
    "Railcard API (Final)",
]
