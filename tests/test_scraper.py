"""Tests for SCOUT Agent scraper."""

import pytest
from scout.scraper import EtsyScraper


class TestEtsyScraper:
    """Test cases for EtsyScraper class."""

    def test_scraper_initialization(self):
        """Test scraper can be initialized with rate limit."""
        scraper = EtsyScraper(rate_limit_seconds=5)
        assert scraper.rate_limit_seconds == 5
        assert scraper.ua is not None
        assert scraper._browser is None  # Not initialized until context manager

    def test_scraper_default_rate_limit(self):
        """Test scraper default rate limit is 5 seconds."""
        scraper = EtsyScraper()
        assert scraper.rate_limit_seconds == 5.0

    def test_scraper_base_url(self):
        """Test scraper has correct Etsy base URL."""
        assert EtsyScraper.BASE_URL == "https://www.etsy.com"

    @pytest.mark.asyncio
    async def test_scraper_context_manager(self):
        """Test scraper initializes and cleans up browser."""
        async with EtsyScraper() as scraper:
            assert scraper._browser is not None
            assert scraper._page is not None
        # After exit, browser should still exist but we can't test cleanup easily

    def test_scraper_user_agent(self):
        """Test scraper has user agent generator."""
        scraper = EtsyScraper()
        ua_string = scraper.ua.random
        assert isinstance(ua_string, str)
        assert len(ua_string) > 0
