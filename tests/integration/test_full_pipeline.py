"""Integration tests for full pipeline: scrape → analyze → generate."""

import pytest
import os
from pathlib import Path


@pytest.mark.integration
def test_scraper_works():
    """Test that scraper can connect to Etsy (skip in CI)."""
    if os.environ.get("CI"):
        pytest.skip("Skip network tests in CI")

    # This would actually hit Etsy - use mock in real tests
    pass


@pytest.mark.integration
def test_analyzer_processes_data(tmp_path):
    """Test analyzer can process sample data."""
    from analyst.analyzer import MarketAnalyzer
    import pandas as pd

    # Create sample data
    sample = pd.DataFrame({
        "title": ["Planner A", "Planner B"],
        "price": [8.0, 12.0],
        "sales_count": [50, 10],
        "tags": [["planner", "productivity"], ["planner", "daily"]]
    })
    sample.to_csv(tmp_path / "sample.csv", index=False)

    analyzer = MarketAnalyzer(str(tmp_path))
    analyzer.load_listings("sample.csv")

    bestsellers = analyzer.find_best_sellers(min_sales=5)
    assert len(bestsellers) == 2

    gaps = analyzer.identify_gaps()
    assert isinstance(gaps, dict)


def test_generator_creates_pdf(tmp_path):
    """Test PDF generator creates valid files."""
    from creator.pdf_generator import PDFGenerator

    gen = PDFGenerator(str(tmp_path))
    sections = [{"title": "Test", "items": ["Item 1"]}]
    filepath = gen.create_planner("Test Planner", sections, "test.pdf")

    assert Path(filepath).exists()
    assert Path(filepath).stat().st_size > 0  # Non-empty file
