# Etsy Digital Products Store

Multi-agent system for creating and selling digital products on Etsy, powered by llm-council deliberation.

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
