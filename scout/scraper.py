"""SCOUT Agent — Etsy scraper with Playwright and rate limiting."""

import asyncio
import random
from playwright.async_api import async_playwright, Page
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class EtsyScraper:
    """Etsy scraper with rate limiting and anti-detection."""

    BASE_URL = "https://www.etsy.com"

    def __init__(self, rate_limit_seconds: float = 5.0):
        self.rate_limit_seconds = rate_limit_seconds
        self.ua = UserAgent()
        self._browser = None
        self._page = None
        self._last_request_time = 0.0

    async def __aenter__(self):
        playwright = await async_playwright().start()
        self._browser = await playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        self._page = await self._browser.new_page()
        await self._page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            await self._browser.close()

    async def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = asyncio.get_event_loop().time() - self._last_request_time
        if elapsed < self.rate_limit_seconds:
            await asyncio.sleep(self.rate_limit_seconds - elapsed + random.uniform(0.5, 2.0))
        self._last_request_time = asyncio.get_event_loop().time()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=5, max=60),
        retry=retry_if_exception_type(TimeoutError)
    )
    async def fetch_shop(self, shop_name: str) -> dict:
        """Fetch shop data including listings count."""
        if self._page is None:
            raise RuntimeError("Scraper not initialized. Use 'async with EtsyScraper()'")

        await self._rate_limit()

        url = f"{self.BASE_URL}/shop/{shop_name}"
        await self._page.goto(url, wait_until="domcontentloaded", timeout=30000)

        try:
            await self._page.wait_for_selector("[data-testid='listing-link']", timeout=10000)
        except Exception:
            pass

        listings = await self._page.query_selector_all("[data-testid='listing-link']")

        return {
            "shop_name": shop_name,
            "listing_count": len(listings),
            "url": url,
        }

    async def fetch_listing_details(self, listing_url: str) -> dict | None:
        """Fetch detailed data from a single listing page."""
        if self._page is None:
            raise RuntimeError("Scraper not initialized")

        await self._rate_limit()

        try:
            await self._page.goto(listing_url, wait_until="domcontentloaded", timeout=30000)

            title = await self._page.text_content("h1")
            price = await self._extract_price()
            sales = await self._extract_sales_count()

            return {
                "url": listing_url,
                "title": title.strip() if title else "",
                "price": price,
                "sales_count": sales,
            }
        except Exception as e:
            print(f"Error fetching listing: {e}")
            return None

    async def _extract_price(self) -> float | None:
        price_el = await self._page.query_selector("[data-testid='listing-price']")
        if price_el:
            text = await price_el.text_content()
            try:
                return float(text.replace("$", "").replace("€", "").replace(",", ""))
            except ValueError:
                return None
        return None

    async def _extract_sales_count(self) -> int | None:
        sales_el = await self._page.query_selector("[data-testid='sales-count']")
        if sales_el:
            text = await sales_el.text_content()
            try:
                return int("".join(filter(str.isdigit, text)))
            except ValueError:
                return None
        return None
