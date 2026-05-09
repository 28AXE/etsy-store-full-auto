"""Tests for ANALYST Agent analyzer."""

import pytest
import pandas as pd
from analyst.analyzer import MarketAnalyzer


class TestMarketAnalyzer:
    """Test cases for MarketAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test MarketAnalyzer initializes with default data_dir."""
        analyzer = MarketAnalyzer()
        assert analyzer.data_dir.name == "data"
        assert analyzer.df is None

    def test_analyzer_custom_data_dir(self):
        """Test MarketAnalyzer accepts custom data_dir."""
        analyzer = MarketAnalyzer(data_dir="custom_data")
        assert analyzer.data_dir.name == "custom_data"

    def test_load_csv(self, tmp_path):
        """Test analyzer loads CSV files."""
        analyzer = MarketAnalyzer(str(tmp_path))
        test_df = pd.DataFrame({"title": ["Test"], "price": [10.0], "sales_count": [5]})
        test_df.to_csv(tmp_path / "test.csv", index=False)

        result = analyzer.load_listings("test.csv")
        assert len(result) == 1
        assert analyzer.df is not None

    def test_load_json(self, tmp_path):
        """Test analyzer loads JSON files."""
        analyzer = MarketAnalyzer(str(tmp_path))
        test_df = pd.DataFrame({"title": ["Test"], "price": [10.0]})
        test_df.to_json(tmp_path / "test.json", orient="records")

        result = analyzer.load_listings("test.json")
        assert len(result) == 1

    def test_load_unsupported_format(self, tmp_path):
        """Test analyzer rejects unsupported formats."""
        analyzer = MarketAnalyzer(str(tmp_path))
        (tmp_path / "test.txt").write_text("data")

        with pytest.raises(ValueError, match="Unsupported file format"):
            analyzer.load_listings("test.txt")

    def test_prepare_data_for_council(self):
        """Test data preparation for llm-council."""
        analyzer = MarketAnalyzer()
        test_df = pd.DataFrame({
            "title": ["A", "B", "C"],
            "price": [5.0, 10.0, 15.0],
            "sales_count": [100, 50, 10]
        })
        analyzer.df = test_df

        data = analyzer.prepare_data_for_council()
        assert "total_listings" in data
        assert "top_listings" in data
        assert analyzer.df["title"].iloc[0] == "A"

    def test_prepare_data_no_dataframe(self):
        """Test prepare_data_for_council with no data."""
        analyzer = MarketAnalyzer()
        assert analyzer.df is None
        data = analyzer.prepare_data_for_council()
        assert data == "No data loaded"

    def test_find_best_sellers(self):
        """Test finding best-selling listings."""
        analyzer = MarketAnalyzer()
        test_df = pd.DataFrame({
            "title": ["A", "B", "C"],
            "price": [5.0, 10.0, 15.0],
            "sales_count": [100, 50, 10]
        })
        analyzer.df = test_df

        bestsellers = analyzer.find_best_sellers(min_sales=50)
        assert len(bestsellers) == 2

        bestsellers = analyzer.find_best_sellers(min_sales=100)
        assert len(bestsellers) == 1

    def test_find_best_sellers_no_data(self):
        """Test find_best_sellers with no data."""
        analyzer = MarketAnalyzer()
        result = analyzer.find_best_sellers()
        assert len(result) == 0

    def test_extract_top_tags(self):
        """Test extracting top tags."""
        analyzer = MarketAnalyzer()
        test_df = pd.DataFrame({
            "title": ["A", "B", "C"],
            "tags": [["planner", "productivity"], ["planner", "daily"], ["tracker", "productivity"]]
        })
        analyzer.df = test_df

        top_tags = analyzer.extract_top_tags(n=3)
        assert len(top_tags) == 3
        assert top_tags[0][0] == "planner"  # Most common

    def test_extract_top_tags_no_data(self):
        """Test extract_top_tags with no data."""
        analyzer = MarketAnalyzer()
        result = analyzer.extract_top_tags()
        assert result == []

    def test_identify_gaps(self):
        """Test identifying market gaps."""
        analyzer = MarketAnalyzer()
        test_df = pd.DataFrame({
            "title": ["A", "B"],
            "sales_count": [100, 10],
            "tags": [["rare_tag"], ["common_tag"]]
        })
        analyzer.df = test_df

        gaps = analyzer.identify_gaps()
        assert "rare_tag" in gaps
        assert gaps["rare_tag"]["avg_sales"] == 100

    def test_identify_gaps_no_data(self):
        """Test identify_gaps with no data."""
        analyzer = MarketAnalyzer()
        result = analyzer.identify_gaps()
        assert result == {}
