"""
Simple usage examples for the cashback scraper system
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scrapers.cashback_scraper import CashbackScraperFactory, CashbackAggregator


def example_single_scraper():
    """Example: Run a single scraper"""
    print("Running ShopBack scraper only...")
    
    # Create scraper instance
    scraper = CashbackScraperFactory.create_scraper("shopback")
    
    # Scrape data
    offers = scraper.scrape_all(max_workers=3)
    
    # Save results
    scraper.save_to_csv(offers, "shopback_results.csv")
    scraper.save_to_json(offers, "shopback_results.json")
    
    print(f"Found {len(offers)} offers from ShopBack")


def example_multiple_scrapers():
    """Example: Run multiple scrapers and combine results"""
    print("Running all scrapers...")
    
    # Create aggregator
    aggregator = CashbackAggregator()
    
    # Run all scrapers
    all_results = aggregator.run_all_scrapers(max_workers=3)
    
    # Combine and save results
    combined_offers = aggregator.combine_and_save("all_cashback_offers")
    
    # Print summary
    summary = aggregator.get_summary()
    print("\nResults Summary:")
    for scraper, stats in summary.items():
        print(f"{scraper}: {stats['total_offers']} offers, {stats['unique_merchants']} unique merchants")


def example_custom_scraper():
    """Example: How to add a new scraper"""
    # To add a new scraper, you would:
    # 1. Create a new class inheriting from BaseCashbackScraper
    # 2. Implement the extract_merchant_data method
    # 3. Add configuration to CashbackScraperFactory.SCRAPER_CONFIGS
    
    print("See cashback_scraper.py for examples of custom scraper implementation")


if __name__ == "__main__":
    print("Cashback Scraper Examples")
    print("=" * 30)
    
    # Choose which example to run
    choice = input("\nChoose example:\n1. Single scraper\n2. Multiple scrapers\n3. Show custom scraper info\nEnter choice (1-3): ")
    
    if choice == "1":
        example_single_scraper()
    elif choice == "2":
        example_multiple_scrapers()
    elif choice == "3":
        example_custom_scraper()
    else:
        print("Invalid choice. Running multiple scrapers example...")
        example_multiple_scrapers()
