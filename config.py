"""
config.py

Central configuration for the ArcGIS Validator.
"""

from pathlib import Path

# ---------------------------------------------------------------------
# Project directories
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = BASE_DIR / "reports"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
LOG_DIR = BASE_DIR / "logs"

for directory in [
    OUTPUT_DIR,
    REPORT_DIR,
    SCREENSHOT_DIR,
    LOG_DIR,
]:
    directory.mkdir(exist_ok=True)

# ---------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------

INPUT_EXCEL = INPUT_DIR / "input.xlsx"
OUTPUT_EXCEL = OUTPUT_DIR / "validated.xlsx"
FAILED_CSV = REPORT_DIR / "failed_links.csv"
SUMMARY_FILE = REPORT_DIR / "summary.txt"

LOG_FILE = LOG_DIR / "validator.log"

# ---------------------------------------------------------------------
# Browser
# ---------------------------------------------------------------------

HEADLESS = True

VIEWPORT = {
    "width": 1600,
    "height": 900,
}

PAGE_TIMEOUT = 30000          # milliseconds
WAIT_AFTER_LOAD = 5000        # milliseconds

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

MAX_WORKERS = 8

SAVE_EVERY = 25

MAX_RETRIES = 2

HTTP_TIMEOUT = 20  # seconds

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/138.0 Safari/537.36"
)

# ---------------------------------------------------------------------
# ArcGIS REST
# ---------------------------------------------------------------------

REST_SUFFIX = "?f=pjson"

COUNT_QUERY = (
    "/query?"
    "where=1%3D1"
    "&returnCountOnly=true"
    "&f=json"
)

# ---------------------------------------------------------------------
# Status values
# ---------------------------------------------------------------------

STATUS_WORKING = "Working"
STATUS_EMPTY = "Empty Layer"
STATUS_BROKEN = "Broken Service"
STATUS_UNSUPPORTED = "Unsupported Layer"
STATUS_AUTH = "Authentication Required"
STATUS_TIMEOUT = "Timeout"
STATUS_HTTP = "HTTP Error"
STATUS_UNKNOWN = "Unknown Error"

# ---------------------------------------------------------------------
# UI Error Patterns
# ---------------------------------------------------------------------

ERROR_PATTERNS = [
    "Unable to add layer",
    "Support for adding this layer type",
    "Layer failed to load",
    "Authentication required",
    "Token Required",
    "Service unavailable",
    "Access denied",
    "Layer is not available",
]