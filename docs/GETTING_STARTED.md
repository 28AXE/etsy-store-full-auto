# Getting Started with Etsy Digital Products Store

## Prerequisites

- Python 3.10+
- uv (package manager)
- Playwright browsers

## Installation

```bash
git clone <repo>
cd etsy-store
uv sync
uv run playwright install chromium
```

## Quick Start

### 1. Scrape competitor shops

```bash
# Scrape a successful shop
uv run etsy-store scrape "SuccessfulShopName" -o data/competitor.json

# Rate limit: 1 request per 5 seconds (configurable)
```

### 2. Analyze market data

```bash
uv run etsy-store analyze data/competitor.json
```

Output shows:
- Best sellers (high sales volume)
- Top tags (most common)
- Market gaps (opportunities)

### 3. Generate products

```bash
# Generate a planner PDF
uv run etsy-store generate "Daily Planner" -o output

# Output: PDF ready for Etsy upload
```

### 4. Track performance

Use the `optimizer` module to track your own shop performance after uploading.

## Configuration

Edit `config/niches.json` to target different product categories.

## Next Steps

1. Scrape 10-20 competitor shops
2. Identify 3-5 high-opportunity niches
3. Generate 5-10 products per niche
4. Upload to Etsy with optimized titles/tags
5. Track performance and iterate
