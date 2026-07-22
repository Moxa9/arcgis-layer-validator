"""
validate.py

Main entry point for the ArcGIS Validator.
"""

from pathlib import Path

from browser import BrowserManager
from config import (
    SAVE_EVERY,
    SCREENSHOT_DIR,
)
from excel_handler import ExcelHandler
from logger import logger
from validator import ArcGISValidator


def main():

    logger.info("=" * 60)
    logger.info("ArcGIS Validator Started")
    logger.info("=" * 60)

    browser = BrowserManager()
    browser.start()

    excel = ExcelHandler()

    validator = ArcGISValidator(browser)

    processed = 0

    try:

        for row, url in excel.iter_rows():

            screenshot = SCREENSHOT_DIR / f"row_{row}.png"

            result = validator.validate(
                mapviewer_url=url,
                screenshot_path=str(screenshot),
            )

            excel.write_result(row, result)

            processed += 1

            logger.info(
    f"Row {row} | {result.status} | {result.error}"
)
            

            if processed % SAVE_EVERY == 0:

                excel.save()

                logger.info(
                    f"Checkpoint saved after {processed} rows."
                )

        excel.save()

        logger.info("Validation completed successfully.")

    finally:

        browser.close()


if __name__ == "__main__":
    main()