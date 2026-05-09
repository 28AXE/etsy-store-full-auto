"""SCOUT Agent — Data extractors for Etsy listings."""

from typing import Optional
from playwright.async_api import Page


class ListingExtractor:
    """Extract structured data from Etsy listing pages."""

    def __init__(self, page: Page):
        self.page = page

    async def extract_listing(self, listing_url: str) -> Optional[dict]:
        """Extract full listing data including price, sales, reviews, and tags."""
        try:
            await self.page.goto(listing_url, wait_until="domcontentloaded", timeout=30000)
            title = await self.page.text_content("h1")
            price = await self._extract_price()
            sales = await self._extract_sales_count()
            reviews = await self._extract_review_data()
            tags = await self._extract_tags()
            description = await self._extract_description()

            return {
                "url": listing_url,
                "title": title.strip() if title else "",
                "price": price,
                "sales_count": sales,
                "review_count": reviews.get("count"),
                "average_rating": reviews.get("rating"),
                "tags": tags,
                "description": description,
            }
        except Exception as e:
            print(f"Error extracting listing: {e}")
            return None

    async def _extract_price(self) -> Optional[float]:
        """Extract price from listing page."""
        price_el = await self.page.query_selector("[data-testid='listing-price']")
        if price_el:
            text = await price_el.text_content()
            try:
                return float(text.replace("$", "").replace("€", "").replace(",", ""))
            except ValueError:
                return None
        return None

    async def _extract_sales_count(self) -> Optional[int]:
        """Extract number of sales from listing page."""
        sales_el = await self.page.query_selector("[data-testid='sales-count']")
        if sales_el:
            text = await sales_el.text_content()
            try:
                return int("".join(filter(str.isdigit, text)))
            except ValueError:
                return None
        return None

    async def _extract_review_data(self) -> dict:
        """Extract review count and average rating."""
        reviews = {"count": None, "rating": None}

        rating_el = await self.page.query_selector("[data-testid='reviews-rating']")
        if rating_el:
            text = await rating_el.text_content()
            try:
                reviews["rating"] = float(text.split()[0])
            except (ValueError, IndexError):
                pass

        count_el = await self.page.query_selector("[data-testid='reviews-count']")
        if count_el:
            text = await count_el.text_content()
            try:
                reviews["count"] = int("".join(filter(str.isdigit, text)))
            except ValueError:
                pass

        return reviews

    async def _extract_tags(self) -> list[str]:
        """Extract Etsy tags (max 13) from listing page."""
        tags = []
        tag_elements = await self.page.query_selector_all("[data-testid='listing-tag']")
        for tag in tag_elements[:13]:
            text = await tag.text_content()
            if text:
                tags.append(text.strip())
        return tags

    async def _extract_description(self) -> Optional[str]:
        """Extract product description from listing page."""
        desc_el = await self.page.query_selector("[data-testid='item-description']")
        if desc_el:
            return await desc_el.text_content()

        # Fallback: look for description in main content area
        main_el = await self.page.query_selector("main")
        if main_el:
            text = await main_el.text_content()
            if text:
                return text[:2000]  # Limit description length
        return None
