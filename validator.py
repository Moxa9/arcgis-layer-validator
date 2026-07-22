"""
validator.py

Core validation logic for ArcGIS Map Viewer links.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs, urlparse

import requests
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from browser import BrowserManager
from config import (
    COUNT_QUERY,
    ERROR_PATTERNS,
    HTTP_TIMEOUT,
    PAGE_TIMEOUT,
    REST_SUFFIX,
    STATUS_AUTH,
    STATUS_BROKEN,
    STATUS_EMPTY,
    STATUS_HTTP,
    STATUS_TIMEOUT,
    STATUS_UNKNOWN,
    STATUS_UNSUPPORTED,
    STATUS_WORKING,
    WAIT_AFTER_LOAD,
)
from logger import logger


# ---------------------------------------------------------------------
# Validation Result
# ---------------------------------------------------------------------

@dataclass
class ValidationResult:
    status: str
    http_status: Optional[int] = None
    feature_count: Optional[int] = None
    error: str = ""
    screenshot: str = ""


class ArcGISValidator:

    def __init__(self, browser: BrowserManager):
        self.browser = browser
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        })

    # ------------------------------------------------------------
    # Extract REST URL
    # ------------------------------------------------------------

    @staticmethod
    def extract_rest_url(mapviewer_url: str) -> Optional[str]:
        """
        Extract the ArcGIS REST URL from:

        https://www.arcgis.com/apps/mapviewer/index.html?url=<REST_URL>
        """

        try:
            parsed = urlparse(mapviewer_url)

            params = parse_qs(parsed.query)

            if "url" not in params:
                return None

            return params["url"][0]

        except Exception:
            return None

    # ------------------------------------------------------------
    # REST JSON URL
    # ------------------------------------------------------------

    @staticmethod
    def build_rest_json_url(rest_url: str) -> str:

        if "?" in rest_url:
            return rest_url + "&f=pjson"

        return rest_url + REST_SUFFIX

    # ------------------------------------------------------------
    # Count Query URL
    # ------------------------------------------------------------

    @staticmethod
    def build_count_url(rest_url: str) -> str:

        rest_url = rest_url.rstrip("/")

        return rest_url + COUNT_QUERY

    # ------------------------------------------------------------
    # HTTP GET helper
    # ------------------------------------------------------------

    def get_json(self, url: str):

        response = self.session.get(
            url,
            timeout=HTTP_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()
        # ------------------------------------------------------------
    # REST Validation
    # ------------------------------------------------------------

    def validate_rest(self, rest_url: str) -> ValidationResult:
        """
        Validate the ArcGIS REST service.
        """

        try:
            json_url = self.build_rest_json_url(rest_url)

            data = self.get_json(json_url)

        except requests.exceptions.Timeout:
            return ValidationResult(
                status=STATUS_TIMEOUT,
                error="REST request timed out",
            )

        except requests.exceptions.HTTPError as exc:

            code = exc.response.status_code

            return ValidationResult(
                status=STATUS_HTTP,
                http_status=code,
                error=f"HTTP {code}",
            )

        except Exception as exc:

            return ValidationResult(
                status=STATUS_UNKNOWN,
                error=str(exc),
            )

        # -----------------------------------------
        # ArcGIS returned an error object
        # -----------------------------------------

        if "error" in data:

            message = data["error"].get("message", "Unknown ArcGIS error")

            code = data["error"].get("code")

            if code in (498, 499):
                return ValidationResult(
                    status=STATUS_AUTH,
                    error=message,
                )

            return ValidationResult(
                status=STATUS_BROKEN,
                error=message,
            )

        # -----------------------------------------
        # Count query
        # -----------------------------------------

        feature_count = None

        try:

            count_json = self.get_json(
                self.build_count_url(rest_url)
            )

            feature_count = count_json.get("count")

        except Exception:
            feature_count = None

        if feature_count == 0:

            return ValidationResult(
                status=STATUS_EMPTY,
                feature_count=0,
            )

        return ValidationResult(
            status=STATUS_WORKING,
            feature_count=feature_count,
        )
        # ------------------------------------------------------------
    # UI Validation (Playwright)
    # ------------------------------------------------------------

    def validate_ui(self, mapviewer_url: str, screenshot_path: str = "") -> ValidationResult:
        """
        Validate the ArcGIS Map Viewer UI.
        Assumes the REST validation has already passed.
        """

        page = self.browser.new_page()

        try:
            page.goto(
                mapviewer_url,
                timeout=PAGE_TIMEOUT,
                wait_until="networkidle",
            )

            page.wait_for_timeout(WAIT_AFTER_LOAD)

            page_text = page.locator("body").inner_text()

            for pattern in ERROR_PATTERNS:
                if pattern.lower() in page_text.lower():

                    if screenshot_path:
                        page.screenshot(
                            path=screenshot_path,
                            full_page=True,
                        )

                    status = STATUS_UNSUPPORTED

                    if "authentication" in pattern.lower():
                        status = STATUS_AUTH

                    return ValidationResult(
                        status=status,
                        error=pattern,
                        screenshot=screenshot_path,
                    )

            return ValidationResult(
                status=STATUS_WORKING,
            )

        except PlaywrightTimeoutError:

            if screenshot_path:
                page.screenshot(
                    path=screenshot_path,
                    full_page=True,
                )

            return ValidationResult(
                status=STATUS_TIMEOUT,
                error="Playwright timeout",
                screenshot=screenshot_path,
            )

        except Exception as exc:

            if screenshot_path:
                page.screenshot(
                    path=screenshot_path,
                    full_page=True,
                )

            return ValidationResult(
                status=STATUS_UNKNOWN,
                error=str(exc),
                screenshot=screenshot_path,
            )

        finally:
            page.close()
        # ------------------------------------------------------------
    # Complete Validation
    # ------------------------------------------------------------

    def validate(
        self,
        mapviewer_url: str,
        screenshot_path: str = "",
    ) -> ValidationResult:
        """
        Complete validation pipeline.

        1. Extract REST URL
        2. Validate REST service
        3. Validate Map Viewer UI
        4. Return one combined result
        """

        logger.info(f"Validating: {mapviewer_url}")

        rest_url = self.extract_rest_url(mapviewer_url)

        if not rest_url:
            return ValidationResult(
                status=STATUS_UNKNOWN,
                error="Unable to extract REST URL",
            )

        # Stage 1: REST Validation
        rest_result = self.validate_rest(rest_url)

        if rest_result.status != STATUS_WORKING:
            return rest_result

        # Stage 2: UI Validation
        ui_result = self.validate_ui(
            mapviewer_url,
            screenshot_path,
        )

        # Preserve REST information
        ui_result.feature_count = rest_result.feature_count
        ui_result.http_status = rest_result.http_status

        return ui_result