#!/usr/bin/env python3
"""
AI-Enhanced Cashback Scraper - Main Entry Point
============================================

This is the main entry point for the AI-enhanced cashback scraper.
Run this script to start scraping with intelligent data extraction.

Usage:
    python main.py              # Interactive mode
    python main.py --production  # Run production scraper
    python main.py --optimized   # Run token-optimized scraper
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

def main():
    """Main entry point"""
    try:
        # Check command line arguments
        if len(sys.argv) > 1:
            if '--production' in sys.argv:
                run_production_scraper()
            elif '--optimized' in sys.argv:
                run_optimized_scraper()
            else:
                print("Unknown option. Use --production or --optimized")
                sys.exit(1)
        else:
            # Interactive mode
            run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\n🛑 Scraping cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def run_production_scraper():
    """Run the production scraper"""
    print("🚀 Starting Production AI Scraper...")
    from scrapers.production_scraper import SimpleAIScraper
    
    scraper = SimpleAIScraper()
    
    # Run both sites
    print("\n📊 Scraping ShopBack...")
    shopback_results = scraper.scrape_site("shopback", max_pages=10)
    scraper.save_results(shopback_results, "production_shopback")
    
    print("\n📊 Scraping CashRewards...")
    cashrewards_results = scraper.scrape_site("cashrewards", max_pages=10)
    scraper.save_results(cashrewards_results, "production_cashrewards")
    
    # Combined results
    all_results = shopback_results + cashrewards_results
    scraper.save_results(all_results, "production_combined")
    
    print(f"\n✅ Production scraping complete! Found {len(all_results)} offers")
    print(f"📁 Results saved to production_*.csv and production_*.json")

def run_optimized_scraper():
    """Run the token-optimized scraper"""
    print("🚀 Starting Token-Optimized AI Scraper...")
    from scrapers.token_optimized_scraper import TokenOptimizedAIScraper
    
    scraper = TokenOptimizedAIScraper()
    
    # Interactive budget selection
    print("\n💰 Select token budget:")
    print("1. Small (1,000 tokens - ~$0.004)")
    print("2. Medium (5,000 tokens - ~$0.018)")
    print("3. Large (10,000 tokens - ~$0.035)")
    print("4. No limit")
    
    choice = input("Enter choice (1-4): ").strip()
    budgets = {"1": 1000, "2": 5000, "3": 10000, "4": None}
    budget = budgets.get(choice, 1000)
    
    if budget:
        print(f"📊 Budget set to {budget} tokens")
    else:
        print("📊 No budget limit set")
    
    # Run both sites with budget
    print("\n📊 Scraping ShopBack...")
    shopback_results = scraper.scrape_site("shopback", max_pages=15, token_budget=budget//2 if budget else None)
    scraper.save_results(shopback_results, "optimized_shopback")
    
    print("\n📊 Scraping CashRewards...")
    cashrewards_results = scraper.scrape_site("cashrewards", max_pages=15, token_budget=budget//2 if budget else None)
    scraper.save_results(cashrewards_results, "optimized_cashrewards")
    
    # Combined results
    all_results = shopback_results + cashrewards_results
    scraper.save_results(all_results, "optimized_combined")
    
    print(f"\n✅ Optimized scraping complete! Found {len(all_results)} offers")
    print(f"💰 Total cost: ${scraper.token_costs:.4f} ({scraper.total_tokens_used} tokens)")
    print(f"📁 Results saved to optimized_*.csv and optimized_*.json")

def run_interactive_mode():
    """Run interactive mode to choose scraper type"""
    print("🤖 AI-Enhanced Cashback Scraper")
    print("=" * 40)
    print()
    print("Choose your scraper:")
    print("1. 🚀 Production Scraper (basic AI integration)")
    print("2. 🎯 Token-Optimized Scraper (advanced cost control)")
    print("3. 📖 View Examples")
    print("4. 🧪 Run Tests")
    print("5. ❌ Exit")
    print()
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        run_production_scraper()
    elif choice == "2":
        run_optimized_scraper()
    elif choice == "3":
        run_examples()
    elif choice == "4":
        run_tests()
    elif choice == "5":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice. Please try again.")
        run_interactive_mode()

def run_examples():
    """Run example demonstrations"""
    print("\n📖 Running Examples...")
    print("=" * 30)
    
    try:
        from examples.simple_demo import main as simple_demo
        simple_demo()
    except ImportError:
        print("❌ Examples not available. Make sure all files are in place.")

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running Tests...")
    print("=" * 20)
    
    try:
        from tests.test_api_key import main as test_main
        test_main()
    except ImportError:
        print("❌ Tests not available. Make sure all files are in place.")

if __name__ == "__main__":
    main()
