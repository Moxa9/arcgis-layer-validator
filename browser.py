"""
browser.py

Creates and manages a single Playwright browser instance.
"""

from playwright.sync_api import sync_playwright

from config import (
    HEADLESS,
    VIEWPORT,
    USER_AGENT,
)


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS
        )

        self.context = self.browser.new_context(
            viewport=VIEWPORT,
            user_agent=USER_AGENT,
            ignore_https_errors=True,
        )

    def new_page(self):
        return self.context.new_page()

    def close(self):
        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()