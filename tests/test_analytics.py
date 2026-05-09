"""Tests for OPTIMIZER Agent analytics."""

import pytest
from optimizer.analytics import PerformanceTracker
import os


class TestPerformanceTracker:
    """Test cases for PerformanceTracker class."""

    def test_tracker_initialization(self, tmp_path):
        """Test PerformanceTracker initializes correctly."""
        tracker = PerformanceTracker(str(tmp_path))
        assert tracker.history_file.parent == tmp_path
        assert tracker.config_dir.name == ".claude"

    def test_tracker_creates_data_dir(self, tmp_path):
        """Test tracker creates data directory if it doesn't exist."""
        new_dir = tmp_path / "new_analytics"
        tracker = PerformanceTracker(str(new_dir))
        assert new_dir.exists()

    def test_log_listing(self, tmp_path):
        """Test logging listing metrics."""
        tracker = PerformanceTracker(str(tmp_path))
        tracker.log_listing("test123", {"views": 100, "sales": 5})

        assert tracker.history_file.exists()
        with open(tracker.history_file) as f:
            content = f.read()
            assert "test123" in content
            assert "100" in content

    def test_log_multiple_listings(self, tmp_path):
        """Test logging multiple listings."""
        tracker = PerformanceTracker(str(tmp_path))
        tracker.log_listing("listing1", {"views": 100})
        tracker.log_listing("listing2", {"views": 200})

        with open(tracker.history_file) as f:
            lines = f.readlines()
            assert len(lines) == 2

    def test_get_listing_trend(self, tmp_path):
        """Test calculating listing trends."""
        tracker = PerformanceTracker(str(tmp_path))
        tracker.log_listing("test123", {"views": 100, "sales": 5})
        tracker.log_listing("test123", {"views": 120, "sales": 7})

        trends = tracker.get_listing_trend("test123")
        assert "views" in trends

    def test_get_listing_trend_no_data(self, tmp_path):
        """Test trend with no data for listing."""
        tracker = PerformanceTracker(str(tmp_path))
        tracker.log_listing("other", {"views": 100})

        trends = tracker.get_listing_trend("nonexistent")
        assert trends == {}

    def test_decline_detection(self, tmp_path):
        """Test tracker detects declining performance."""
        tracker = PerformanceTracker(str(tmp_path))
        tracker.log_listing("declining", {"views": 200, "favorites": 20})
        tracker.log_listing("declining", {"views": 100, "favorites": 8})

        trends = tracker.get_listing_trend("declining")
        assert trends.get("views", 0) < 0
        assert trends.get("favorites", 0) < 0

    def test_growth_detection(self, tmp_path):
        """Test tracker detects growing performance."""
        tracker = PerformanceTracker(str(tmp_path))
        tracker.log_listing("growing", {"views": 50})
        tracker.log_listing("growing", {"views": 150})

        trends = tracker.get_listing_trend("growing")
        assert trends.get("views", 0) > 0
