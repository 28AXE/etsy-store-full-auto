# Etsy Digital Products Store

[![Stars](https://img.shields.io/github/stars/28AXE/etsy-store-full-auto?style=flat)](https://github.com/28AXE/etsy-store-full-auto)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[![GitHub Topics](https://img.shields.io/badge/topics-etsy%20%7C%20digital--products%20%7C%20multi--agent%20%7C%20ai-blue)](https://github.com/28AXE/etsy-store-full-auto)

<p align="center">
  <strong>🤖 Autonomous multi-agent AI system for Etsy digital products</strong><br>
  Scrape competitors → Analyze gaps → Generate PDFs → Track performance
</p>

## Architecture

4 agents, each with its own llm-council for multi-LLM deliberation:

- **Scout** — Scrapes Etsy shops, extracts listing data (Playwright)
- **Analyst** — Identifies market opportunities and gaps (pandas + council)
- **Creator** — Generates product content and PDFs (council + reportlab)
- **Optimizer** — Tracks performance and recommends improvements (council)

## Quick Start

```bash
# Install dependencies
uv sync
uv run playwright install chromium

# Scrape a competitor shop
uv run etsy-store scrape "ShopName" -o data/shop.json

# Analyze market data
uv run etsy-store analyze data/shop.json

# Generate a digital product
uv run etsy-store generate "Daily Planner" -o output
```

## Project Structure

```
etsy-store/
├── scout/          # Scraping agent (Playwright + BeautifulSoup)
├── analyst/        # Market analysis agent (pandas + llm-council)
├── creator/        # Content generation agent (llm-council + PDF)
├── optimizer/      # Performance tracking agent (analytics + council)
├── config/         # Configuration files (niches, pricing)
├── data/           # Scraped data and analytics
├── docs/           # Documentation
├── tests/          # Test suite
└── .claude/        # llm-council configs per agent
```

## Requirements

- Python 3.10+
- uv (package manager)
- Ollama (for local LLMs)
- Playwright browsers

## License

MIT
