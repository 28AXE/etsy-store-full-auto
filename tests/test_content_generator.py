"""Tests for CREATOR Agent content and PDF generators."""

import pytest
import os
from pathlib import Path
from creator.content_generator import ContentGenerator
from creator.pdf_generator import PDFGenerator


class TestContentGenerator:
    """Test cases for ContentGenerator class."""

    def test_generator_class_exists(self):
        """Test ContentGenerator class is defined."""
        gen = ContentGenerator()
        assert gen is not None

    def test_generator_initialization(self):
        """Test ContentGenerator initializes with default config_dir."""
        gen = ContentGenerator()
        assert gen.config_dir.name == ".claude"

    def test_generator_custom_config_dir(self):
        """Test ContentGenerator accepts custom config_dir."""
        gen = ContentGenerator(config_dir="custom_config")
        assert gen.config_dir.name == "custom_config"


class TestPDFGenerator:
    """Test cases for PDFGenerator class."""

    def test_pdf_generator_class_exists(self):
        """Test PDFGenerator class is defined."""
        gen = PDFGenerator()
        assert gen is not None

    def test_pdf_generator_creates_output_dir(self, tmp_path):
        """Test PDFGenerator creates output directory."""
        output_dir = tmp_path / "output"
        gen = PDFGenerator(output_dir=str(output_dir))
        assert output_dir.exists()

    def test_planner_creates_file(self, tmp_path):
        """Test create_planner creates a valid PDF file."""
        gen = PDFGenerator(output_dir=str(tmp_path))
        sections = [{"title": "Morning", "items": ["Wake up", "Exercise"]}]
        filepath = gen.create_planner("Daily Planner", sections, "test.pdf")
        assert os.path.exists(filepath)
        assert Path(filepath).stat().st_size > 0

    def test_wall_art_creates_file(self, tmp_path):
        """Test create_wall_art creates a valid PDF file."""
        gen = PDFGenerator(output_dir=str(tmp_path))
        filepath = gen.create_wall_art("Breathe", "test_art.pdf")
        assert os.path.exists(filepath)
        assert Path(filepath).stat().st_size > 0

    def test_planner_multiple_sections(self, tmp_path):
        """Test create_planner with multiple sections."""
        gen = PDFGenerator(output_dir=str(tmp_path))
        sections = [
            {"title": "Morning", "items": ["Wake up", "Exercise"]},
            {"title": "Evening", "items": ["Read", "Sleep"]}
        ]
        filepath = gen.create_planner("Daily Planner", sections, "multi.pdf")
        assert os.path.exists(filepath)
        assert Path(filepath).stat().st_size > 0
