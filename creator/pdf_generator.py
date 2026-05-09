"""CREATOR Agent — PDF generation for digital products."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from pathlib import Path


class PDFGenerator:
    """Generate PDF products (printables, planners, worksheets)."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()

    def create_planner(self, title: str, sections: list[dict], filename: str) -> str:
        """Create a planner PDF with given sections."""
        doc = SimpleDocTemplate(
            str(self.output_dir / filename),
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        story = []
        title_style = ParagraphStyle(
            'CustomTitle', parent=self.styles['Heading1'],
            fontSize=24, spaceAfter=30, alignment=1
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.2*inch))

        for section in sections:
            section_style = ParagraphStyle(
                'Section', parent=self.styles['Heading2'],
                fontSize=16, spaceAfter=12, spaceBefore=20
            )
            story.append(Paragraph(section.get("title", ""), section_style))
            for item in section.get("items", []):
                story.append(Paragraph(f"• {item}", self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            story.append(Spacer(1, 0.5*inch))

        doc.build(story)
        return str(self.output_dir / filename)

    def create_wall_art(self, quote: str, filename: str = "wall_art.pdf") -> str:
        """Create wall art PDF with quote."""
        doc = SimpleDocTemplate(str(self.output_dir / filename), pagesize=A4)
        quote_style = ParagraphStyle(
            'Quote', parent=self.styles['Normal'],
            fontSize=36, alignment=1, spaceAfter=20, textColor=colors.darkgrey
        )
        story = [Spacer(1, 2*inch), Paragraph(quote, quote_style), Spacer(1, 2*inch)]
        doc.build(story)
        return str(self.output_dir / filename)
