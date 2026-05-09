"""Tests for SCOUT Agent extractors."""

import pytest
from scout.extractors import ListingExtractor


class TestListingExtractor:
    """Test cases for ListingExtractor class."""

    def test_extractor_class_exists(self):
        """Test ListingExtractor class is defined."""
        assert ListingExtractor is not None

    def test_extractor_requires_page(self):
        """Test extractor requires a Page argument."""
        with pytest.raises(TypeError):
            ListingExtractor()  # Missing required page argument

    def test_extractor_stores_page(self, mocker):
        """Test extractor stores the page reference."""
        mock_page = mocker.MagicMock()
        extractor = ListingExtractor(mock_page)
        assert extractor.page == mock_page

    @pytest.mark.asyncio
    async def test_extract_listing_structure(self, mocker):
        """Test extract_listing returns correct structure."""
        mock_page = mocker.AsyncMock()
        mock_page.text_content = mocker.AsyncMock(return_value="Test Title")
        mock_page.query_selector = mocker.AsyncMock(return_value=None)
        mock_page.query_selector_all = mocker.AsyncMock(return_value=[])
        mock_page.goto = mocker.AsyncMock()

        extractor = ListingExtractor(mock_page)
        result = await extractor.extract_listing("https://etsy.com/listing/123")

        assert result is not None
        assert "url" in result
        assert "title" in result
        assert "price" in result
        assert "sales_count" in result
        assert "tags" in result
        assert result["url"] == "https://etsy.com/listing/123"
        assert result["title"] == "Test Title"

    @pytest.mark.asyncio
    async def test_extract_listing_handles_errors(self, mocker):
        """Test extract_listing handles exceptions gracefully."""
        mock_page = mocker.AsyncMock()
        mock_page.goto = mocker.AsyncMock(side_effect=TimeoutError("Timeout"))

        extractor = ListingExtractor(mock_page)
        result = await extractor.extract_listing("https://etsy.com/listing/123")

        assert result is None
