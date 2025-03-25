from scrapy.http import HtmlResponse
from scrapy import signals
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging

class SeleniumMiddleware:
    def __init__(self):
        # Configure Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")  # Use new headless mode

        # Use a real browser User-Agent
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )

        # Prevent detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Initialize WebDriver once and reuse it
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        # Remove detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def process_request(self, request, spider):
        logging.info(f"Processing request with Selenium: {request.url}")
        self.driver.get(request.url)

        try:
            # Wait for Cloudflare or dynamic content
            WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located((By.ID, "cf-spinner-please-wait"))
            )
        except TimeoutException:
            logging.warning(f"Timeout waiting for Cloudflare verification on {request.url}")

        body = self.driver.page_source

        return HtmlResponse(
            url=self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self, spider):
        """Properly close the WebDriver when Scrapy stops."""
        logging.info("Closing Selenium WebDriver")
        self.driver.quit()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware
