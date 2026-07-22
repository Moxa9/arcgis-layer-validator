# ArcGIS Layer Validator

A Python-based automation tool that validates ArcGIS Map Viewer links in bulk.

The validator reads ArcGIS Map Viewer URLs from an Excel workbook, validates the underlying ArcGIS REST service, checks whether the layer loads successfully, and generates an annotated Excel report with validation results.

---

## Features

- Validate thousands of ArcGIS Map Viewer links automatically
- Extract ArcGIS REST service URLs from Map Viewer links
- Verify ArcGIS REST endpoints
- Detect unavailable or broken services
- Detect authentication-required services
- Identify empty layers
- Capture screenshots for failed validations
- Export validation results to Excel
- Generate logs for troubleshooting

---

## Project Structure

```text
validator/
│
├── browser.py
├── config.py
├── excel_handler.py
├── logger.py
├── validator.py
├── validate.py
│
├── input.xlsx
│
├── output/
│   └── validated.xlsx
│
├── screenshots/
│
├── logs/
│
├── reports/
│
├── requirements.txt
└── README.md
```

---

## Validation Workflow

```text
Excel Workbook
        │
        ▼
Read ArcGIS MapViewer URL
        │
        ▼
Extract ArcGIS REST URL
        │
        ▼
Validate REST Service
        │
        ▼
Open ArcGIS Map Viewer
        │
        ▼
Check for UI Errors
        │
        ▼
Write Results to Excel
```

---

## Validation Status

The validator classifies each URL into one of the following categories:

| Status | Description |
|---------|-------------|
| Working | Layer loaded successfully |
| Empty Layer | Layer exists but contains no features |
| Broken Service | REST service unavailable |
| Authentication Required | Layer requires login/token |
| Unsupported Layer | Layer type not supported |
| HTTP Error | HTTP request failed |
| Timeout | Request exceeded timeout |
| Unknown Error | Unexpected validation error |

---

## Requirements

- Python 3.11+
- Playwright
- Chromium Browser

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browser:

```bash
playwright install chromium
```

---

## Input

The validator expects an Excel workbook named:

```text
input.xlsx
```

The workbook must contain a worksheet named:

```text
Layer_Servers
```

The worksheet should include an `arcgis_link` column containing ArcGIS Map Viewer URLs.

Example:

```
https://www.arcgis.com/apps/mapviewer/index.html?url=https://server/rest/services/Layer/MapServer/0
```

---

## Run

```bash
py validate.py
```

---

## Output

After execution the validator generates:

```text
output/
    validated.xlsx
```

Additional folders:

```text
screenshots/
```

Contains screenshots of failed validations.

```text
logs/
```

Contains execution logs.

---

## Technologies Used

- Python
- Playwright
- Requests
- OpenPyXL
- ArcGIS REST API

---

## Future Improvements

- Parallel browser workers
- Resume interrupted executions
- Progress bar with ETA
- Validation summary report
- Duplicate URL caching
- Multi-sheet workbook support

---

## License

MIT License