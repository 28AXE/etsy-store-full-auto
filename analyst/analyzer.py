"""ANALYST Agent — Market data analysis with llm-council."""

import pandas as pd
import subprocess
import json
import re
from pathlib import Path
from typing import Optional


class MarketAnalyzer:
    """Analyze Etsy market data with llm-council deliberation."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.df: Optional[pd.DataFrame] = None
        self.config_dir = Path(".claude")

    def load_listings(self, filepath: str) -> pd.DataFrame:
        """Load listings data from JSON/CSV."""
        path = self.data_dir / filepath

        if path.suffix == ".json":
            self.df = pd.read_json(path)
        elif path.suffix == ".csv":
            self.df = pd.read_csv(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        return self.df

    def run_council_analysis(self, data_sample: str) -> dict:
        """Run llm-council deliberation on market data."""
        prompt = f"""Analyse these Etsy market data and identify opportunities:

{data_sample}

Provide:
1. Top 5 best-selling product types (by sales count)
2. Optimal price ranges for each category
3. Top 10 most common tags in successful listings
4. Market gaps (high demand, low competition niches)
5. Recommended 3 niches to target

Return as JSON with keys: best_sellers, price_ranges, top_tags, gaps, recommendations"""

        config_path = self.config_dir / "analyst-council.json"
        result = subprocess.run(
            ["uv", "run", "llm-council", "--config", str(config_path), prompt],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )

        output = result.stdout
        try:
            json_match = re.search(r'```json\s*(.+?)\s*```', output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            return {"raw_analysis": output}
        except json.JSONDecodeError:
            return {"raw_analysis": output, "error": "Failed to parse JSON"}

    def prepare_data_for_council(self) -> str:
        """Prepare DataFrame as text for llm-council."""
        if self.df is None:
            return "No data loaded"

        summary = {
            "total_listings": len(self.df),
            "avg_price": float(self.df["price"].mean()) if "price" in self.df.columns else 0,
            "avg_sales": float(self.df["sales_count"].mean()) if "sales_count" in self.df.columns else 0,
            "top_listings": self.df.nlargest(10, "sales_count")[["title", "price", "sales_count"]].to_dict("records")
            if "sales_count" in self.df.columns and len(self.df) > 0 else []
        }
        return json.dumps(summary, indent=2)

    def find_best_sellers(self, min_sales: int = 10) -> pd.DataFrame:
        """Find listings with sales above threshold."""
        if self.df is None or "sales_count" not in self.df.columns:
            return pd.DataFrame()

        return self.df[self.df["sales_count"] >= min_sales]

    def extract_top_tags(self, n: int = 10) -> list[tuple[str, int]]:
        """Extract most common tags from listings."""
        if self.df is None or "tags" not in self.df.columns:
            return []

        from collections import Counter
        all_tags = []
        for tags in self.df["tags"]:
            if isinstance(tags, list):
                all_tags.extend(tags)

        return Counter(all_tags).most_common(n)

    def identify_gaps(self) -> dict:
        """Identify market gaps based on tag frequency and sales correlation."""
        if self.df is None or "tags" not in self.df.columns or "sales_count" not in self.df.columns:
            return {}

        from collections import defaultdict
        tag_sales = defaultdict(list)

        for _, row in self.df.iterrows():
            if isinstance(row["tags"], list):
                for tag in row["tags"]:
                    tag_sales[tag].append(row["sales_count"])

        gaps = {}
        for tag, sales in tag_sales.items():
            avg_sales = sum(sales) / len(sales)
            frequency = len(sales)
            opportunity_score = avg_sales * (1 / (frequency + 1))
            gaps[tag] = {
                "avg_sales": avg_sales,
                "frequency": frequency,
                "opportunity_score": opportunity_score
            }

        return gaps
