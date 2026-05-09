"""CLI for Etsy Digital Products Store."""

import argparse
import asyncio
import json
from pathlib import Path


async def scrape_shop(shop_name: str, output_file: str):
    """Scrape a single Etsy shop."""
    from scout.scraper import EtsyScraper
    from scout.extractors import ListingExtractor

    async with EtsyScraper() as scraper:
        shop_data = await scraper.fetch_shop(shop_name)
        print(f"Scraped {shop_data['listing_count']} listings from {shop_name}")

        with open(output_file, "w") as f:
            json.dump(shop_data, f, indent=2)

    return shop_data


async def analyze_market(data_file: str):
    """Analyze market data."""
    from analyst.analyzer import MarketAnalyzer

    analyzer = MarketAnalyzer()
    analyzer.load_listings(data_file)

    print("\n=== Market Analysis ===")
    print(f"\nBest sellers (10+ sales):")
    bestsellers = analyzer.find_best_sellers(min_sales=10)
    if len(bestsellers) > 0:
        print(bestsellers[["title", "price", "sales_count"]].to_string())
    else:
        print("No listings with 10+ sales found")

    print(f"\nTop tags:")
    for tag, count in analyzer.extract_top_tags(10):
        print(f"  {tag}: {count} listings")

    print(f"\nMarket gaps:")
    gaps = analyzer.identify_gaps()
    for tag, data in list(gaps.items())[:5]:
        print(f"  {tag}: score {data['opportunity_score']:.2f}")


async def generate_product(product_type: str, output_dir: str):
    """Generate a digital product."""
    from creator.content_generator import ContentGenerator
    from creator.pdf_generator import PDFGenerator

    gen = ContentGenerator()
    pdf = PDFGenerator(output_dir)

    # Generate content
    title = gen.generate_listing_title(product_type, ["digital", "printable"], "seo")
    tags = gen.generate_tags(product_type, "productivity enthusiasts")

    print(f"\nGenerated product:")
    print(f"  Title: {title[:80]}...")
    print(f"  Tags: {tags[:5]}...")

    # Create PDF
    sections = [
        {"title": "Getting Started", "items": ["Download files", "Print at home or professional print"]},
        {"title": "Features", "items": ["Instant download", "High quality PDF", "Reusable"]},
    ]
    filepath = pdf.create_planner(title[:30].replace(' ', '_'), sections, f"{product_type.replace(' ', '_')}.pdf")
    print(f"  PDF: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Etsy Digital Products Store")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape Etsy shops")
    scrape_parser.add_argument("shop", help="Shop name to scrape")
    scrape_parser.add_argument("-o", "--output", default="data/shop.json")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze market data")
    analyze_parser.add_argument("data_file", help="JSON file with listings data")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate digital product")
    generate_parser.add_argument("type", help="Product type (planner, tracker, wall_art)")
    generate_parser.add_argument("-o", "--output", default="output")

    args = parser.parse_args()

    if args.command == "scrape":
        asyncio.run(scrape_shop(args.shop, args.output))
    elif args.command == "analyze":
        asyncio.run(analyze_market(args.data_file))
    elif args.command == "generate":
        asyncio.run(generate_product(args.type, args.output))


if __name__ == "__main__":
    main()
