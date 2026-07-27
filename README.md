# ArcGIS Layer Validation Automation Tool

## Overview

The **ArcGIS Layer Validation Automation Tool** is an end-to-end automation solution that validates ArcGIS Map Viewer links at scale. The tool extracts ArcGIS REST service URLs, validates service availability, checks the corresponding Map Viewer UI using Playwright, captures feature counts, generates Excel reports, stores results in SQLite, and uploads reports to AWS S3.

Designed to process thousands of records efficiently, the validator also supports automatic resume capability, allowing interrupted runs to continue from the last successfully processed record.

---

## Features

- Validate 7,800+ ArcGIS Map Viewer links
- ArcGIS REST API validation
- Playwright UI validation
- HTTP status verification
- Feature count extraction
- Automatic detection of broken and unsupported layers
- Authentication error detection
- Screenshot capture for failed validations
- Automatic resume after interruption
- Excel report generation
- SQLite database storage
- AWS S3 report upload
- Detailed logging

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Browser Automation | Playwright |
| API | ArcGIS REST API |
| HTTP Requests | Requests |
| Excel Processing | OpenPyXL |
| Database | SQLite, SQLAlchemy |
| Cloud Storage | AWS S3, Boto3 |
| Logging | Python Logging |

---

## Project Structure

```text
arcgis-layer-validator/
│
├── browser.py              # Playwright browser manager
├── config.py               # Configuration settings
├── db_loader.py            # SQLite loader
├── excel_handler.py        # Excel read/write operations
├── logger.py               # Logging configuration
├── s3_upload.py            # AWS S3 upload
├── validate.py             # Main application
├── validator.py            # Validation logic
├── requirements.txt
├── README.md
│
├── input/
│   └── input.xlsx
│
├── output/
│   └── validated.xlsx
│
├── screenshots/
│
├── logs/
│   └── validator.log
│
└── arcgis_validation.db
```

---

## Validation Workflow

```text
Input Excel
      │
      ▼
Extract ArcGIS REST URL
      │
      ▼
REST API Validation
      │
      ▼
Playwright UI Validation
      │
      ▼
Generate Validation Report
      │
      ├────────► SQLite Database
      │
      └────────► AWS S3 Upload
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/<your-github-username>/arcgis-layer-validator.git
cd arcgis-layer-validator
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python validate.py
```

---

## Output

The validator generates:

- ✅ Excel validation report
- ✅ HTTP status codes
- ✅ Feature counts
- ✅ Screenshot evidence for failed validations
- ✅ Validation logs
- ✅ SQLite database
- ✅ AWS S3 uploads

---

## Key Highlights

- Processed over **7,800 ArcGIS Map Viewer links**
- Automatic resume support for interrupted executions
- Robust error handling for REST and UI validation
- Cloud integration using AWS S3
- Structured logging and reporting
- Designed for future orchestration using Apache Airflow

---

## Future Enhancements

- Apache Airflow scheduling
- Parallel validation
- Email notifications
- Interactive dashboard
- Retry mechanism for failed validations
- Validation metrics dashboard

---

## Author

**Moksha Rathod**

GitHub: https://github.com/Moxa9