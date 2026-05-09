"""CREATOR Agent — Content generation with llm-council."""

import subprocess
import json
import re
from pathlib import Path
from typing import Optional


class ContentGenerator:
    """Generate product content using llm-council deliberation."""

    def __init__(self, config_dir: str = ".claude"):
        self.config_dir = Path(config_dir)

    def generate_listing_title(self, product_type: str, tags: list[str], niche: str = "") -> str:
        """Generate SEO-optimized listing title via council."""
        prompt = f"""Generate an Etsy listing title for: {product_type}

Target niche: {niche or "general"}
Target tags: {', '.join(tags[:5])}

Requirements:
- Max 140 characters (Etsy limit)
- Front-load most important keywords
- Include 2-3 emotional/benefit words
- No special characters except hyphens

Return ONLY the title."""

        return self._run_council("creator-council", prompt)

    def generate_description(self, product_type: str, features: list[str], use_case: str) -> str:
        """Generate product description via council."""
        prompt = f"""Write an Etsy product description for: {product_type}

Key features:
{chr(10).join(f'- {f}' for f in features)}

Primary use case: {use_case}

Structure:
- Hook (1 sentence that grabs attention)
- Features (5-7 bullet points)
- What you get (file formats, sizes, quantities)
- How to use (step-by-step)
- FAQ (address 1-2 common concerns)

Tone: Friendly, professional, helpful. Return the description only."""

        return self._run_council("creator-council", prompt)

    def generate_tags(self, product_type: str, target_audience: str) -> list[str]:
        """Generate 13 Etsy tags via council (max 20 chars each)."""
        prompt = f"""Generate exactly 13 Etsy tags for: {product_type}
Target audience: {target_audience}

Rules:
- Max 20 characters per tag (Etsy hard limit)
- Use multi-word phrases buyers search for
- Mix: 4 broad + 6 specific + 3 long-tail
- No special characters, spaces only

Return as JSON array of exactly 13 strings."""

        result = self._run_council("creator-council", prompt)
        try:
            json_match = re.search(r'\[(.+?)\]', result, re.DOTALL)
            if json_match:
                tags = json.loads(f"[{json_match.group(1)}]")
                return [t.strip()[:20] for t in tags if t][:13]
        except:
            pass
        return ["digital planner", "printable", "productivity", "organization"][:13]

    def _run_council(self, council_name: str, prompt: str) -> str:
        """Run llm-council and return synthesis."""
        config_path = self.config_dir / f"{council_name}.json"
        result = subprocess.run(
            ["uv", "run", "llm-council", "--config", str(config_path), prompt],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return result.stdout
