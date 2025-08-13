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
    """Run the token-optimized scraper with intelligence levels"""
    print("🚀 Starting Token-Optimized AI Scraper with Intelligence Levels...")
    
    # Import directly without going through __init__.py
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent
    scraper_path = project_root / 'src' / 'scrapers'
    sys.path.insert(0, str(scraper_path))
    
    try:
        from token_optimized_scraper_v2 import TokenOptimizedAIScraper
    except ImportError as e:
        print(f"❌ Could not import intelligence levels scraper: {e}")
        print("💡 Trying alternative approach...")
        
        # Alternative: use the working scraper from earlier test
        from pathlib import Path
        import subprocess
        
        print("\n🧠 Select Intelligence Level:")
        print("1. 🔸 Basic - Simple extraction (~$0.0008/page)")
        print("2. 🔹 Standard - Business insights (~$0.0015/page)")
        print("3. 🔷 Comprehensive - Full analysis (~$0.0035/page)")
        
        intelligence_choice = input("Enter intelligence level (1-3): ").strip()
        intelligence_levels = {"1": "basic", "2": "standard", "3": "comprehensive"}
        intelligence_level = intelligence_levels.get(intelligence_choice, "standard")
        
        print(f"\n🎯 Selected: {intelligence_level.title()} Intelligence")
        print("🚀 Running intelligence levels scraper directly...")
        
        # Run the standalone scraper
        scraper_file = project_root / 'src' / 'scrapers' / 'token_optimized_scraper_v2.py'
        result = subprocess.run([sys.executable, str(scraper_file)], 
                              capture_output=False, text=True, cwd=str(project_root))
        
        if result.returncode == 0:
            print("✅ Scraping completed successfully!")
        else:
            print("❌ Scraping failed. Check the logs for details.")
        return
    
    scraper = TokenOptimizedAIScraper()
    
    # Intelligence level selection
    print("\n🧠 Select Intelligence Level:")
    print("1. 🔸 Basic - Simple extraction (~$0.0008/page)")
    print("   • Merchant name and cashback rate")
    print("   • Confidence score")
    print("   • Fastest processing")
    print()
    print("2. 🔹 Standard - Business insights (~$0.0015/page)")
    print("   • Basic extraction PLUS:")
    print("   • Market position analysis")
    print("   • Revenue opportunity assessment") 
    print("   • User experience evaluation")
    print("   • Actionable recommendations")
    print()
    print("3. 🔷 Comprehensive - Full analysis (~$0.0035/page)")
    print("   • Standard insights PLUS:")
    print("   • Competitive analysis")
    print("   • Detailed business intelligence")
    print("   • Strategic recommendations")
    print("   • Data quality metrics")
    print()
    
    intelligence_choice = input("Enter intelligence level (1-3): ").strip()
    intelligence_levels = {"1": "basic", "2": "standard", "3": "comprehensive"}
    intelligence_level = intelligence_levels.get(intelligence_choice, "standard")
    
    print(f"\n🎯 Selected: {intelligence_level.title()} Intelligence")
    
    # Interactive budget selection based on intelligence level
    level_config = scraper.intelligence_levels[intelligence_level]
    cost_per_page = level_config["estimated_cost_per_call"]
    
    print(f"\n💰 Select budget (at ~${cost_per_page:.4f} per page):")
    print(f"1. Small (10 pages - ~${cost_per_page * 10:.3f})")
    print(f"2. Medium (25 pages - ~${cost_per_page * 25:.3f})")
    print(f"3. Large (50 pages - ~${cost_per_page * 50:.3f})")
    print("4. Custom budget")
    print("5. No limit")
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == "1":
        budget = int(cost_per_page * 10 * 1000)  # Convert to tokens
        max_pages = 10
    elif choice == "2":
        budget = int(cost_per_page * 25 * 1000)
        max_pages = 25
    elif choice == "3":
        budget = int(cost_per_page * 50 * 1000)
        max_pages = 50
    elif choice == "4":
        try:
            pages = int(input("Enter number of pages: "))
            budget = int(cost_per_page * pages * 1000)
            max_pages = pages
        except ValueError:
            budget = 2000
            max_pages = 15
    else:
        budget = None
        max_pages = 30
    
    if budget:
        print(f"📊 Budget set to {budget} tokens (~${budget * cost_per_page / 1000:.3f})")
    else:
        print("📊 No budget limit set")
    
    print(f"🎯 Intelligence Level: {intelligence_level.title()}")
    print(f"📄 Maximum Pages: {max_pages}")
    
    # Site selection
    print("\n🌐 Select site to scrape:")
    print("1. ShopBack only")
    print("2. CashRewards only") 
    print("3. Both sites")
    
    site_choice = input("Enter choice (1-3): ").strip()
    
    results = []
    
    if site_choice in ["1", "3"]:
        print(f"\n📊 Scraping ShopBack with {intelligence_level} intelligence...")
        shopback_results = scraper.scrape_with_intelligence_level(
            site_name="shopback", 
            intelligence_level=intelligence_level,
            max_pages=max_pages,
            token_budget=budget//2 if budget and site_choice == "3" else budget
        )
        if shopback_results:
            scraper.save_intelligence_results(shopback_results, "shopback", intelligence_level)
            results.extend(shopback_results)
    
    if site_choice in ["2", "3"]:
        # Reset token tracking if doing both sites
        if site_choice == "3":
            scraper.total_tokens_used = 0
            scraper.token_costs = 0.0
        
        print(f"\n📊 Scraping CashRewards with {intelligence_level} intelligence...")
        cashrewards_results = scraper.scrape_with_intelligence_level(
            site_name="cashrewards",
            intelligence_level=intelligence_level, 
            max_pages=max_pages,
            token_budget=budget//2 if budget and site_choice == "3" else budget
        )
        if cashrewards_results:
            scraper.save_intelligence_results(cashrewards_results, "cashrewards", intelligence_level)
            results.extend(cashrewards_results)
    
    # Summary
    print(f"\n✅ Intelligent scraping complete!")
    print(f"🧠 Intelligence Level: {intelligence_level.title()}")
    print(f"📊 Total results: {len(results)}")
    print(f"💰 Total cost: ${scraper.token_costs:.4f} ({scraper.total_tokens_used} tokens)")
    
    if intelligence_level == "basic":
        print(f"📄 Results saved as CSV files")
    elif intelligence_level == "standard": 
        print(f"📄 Results saved as enhanced CSV files")
    else:
        print(f"📄 Results saved as comprehensive JSON files")
    
    # Show sample insights based on intelligence level
    if results:
        sample = results[0]
        print(f"\n💡 Sample insights for {sample.get('merchant', sample.get('basic_info', {}).get('merchant_name', 'merchant'))}):")
        
        if intelligence_level == "basic":
            print(f"   💰 Cashback: {sample.get('cashback_offer', 'N/A')}")
            print(f"   🎯 Confidence: {sample.get('confidence', 'N/A')}")
        elif intelligence_level == "standard":
            print(f"   💰 Cashback: {sample.get('cashback_offer', 'N/A')}")
            print(f"   � Market Position: {sample.get('market_position', 'N/A')}")
            print(f"   💼 Revenue Opportunity: {sample.get('revenue_opportunity', 'N/A')}")
            print(f"   📱 Mobile Optimized: {sample.get('mobile_optimized', 'N/A')}")
        else:  # comprehensive
            basic_info = sample.get('basic_info', {})
            competitive = sample.get('competitive_analysis', {})
            insights = sample.get('business_insights', {})
            print(f"   � Cashback: {basic_info.get('cashback_offer', 'N/A')}")
            print(f"   🏆 Market Position: {competitive.get('market_position', 'N/A')}")
            print(f"   🎯 Revenue Opportunity: {insights.get('revenue_opportunity', 'N/A')}")
            print(f"   💡 Recommendations: {len(sample.get('actionable_recommendations', []))} strategic insights")

def run_interactive_mode():
    """Run interactive mode to choose scraper type"""
    print("🤖 AI-Enhanced Cashback Scraper")
    print("=" * 40)
    print()
    print("Choose your scraper:")
    print("1. 🚀 Production Scraper (basic AI integration)")
    print("2. 🧠 Intelligence Levels Scraper (NEW! - advanced AI analysis)")
    print("3. 🎯 Legacy Token-Optimized Scraper (cost control)")
    print("4. 📖 View Examples")
    print("5. 🧪 Run Tests")
    print("6. ❌ Exit")
    print()
    print("💡 Recommended: Option 2 (Intelligence Levels) for best insights!")
    print()
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == "1":
        run_production_scraper()
    elif choice == "2":
        run_optimized_scraper()
    elif choice == "3":
        run_legacy_optimized_scraper()
    elif choice == "4":
        run_examples()
    elif choice == "5":
        run_tests()
    elif choice == "6":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice. Please try again.")
        run_interactive_mode()

def run_legacy_optimized_scraper():
    """Run the legacy token-optimized scraper"""
    print("🚀 Starting Legacy Token-Optimized AI Scraper...")
    try:
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
        scraper.save_results(shopback_results, "legacy_shopback")
        
        print("\n📊 Scraping CashRewards...")
        cashrewards_results = scraper.scrape_site("cashrewards", max_pages=15, token_budget=budget//2 if budget else None)
        scraper.save_results(cashrewards_results, "legacy_cashrewards")
        
        # Combined results
        all_results = shopback_results + cashrewards_results
        scraper.save_results(all_results, "legacy_combined")
        
        print(f"\n✅ Legacy scraping complete! Found {len(all_results)} offers")
        print(f"💰 Total cost: ${scraper.token_costs:.4f} ({scraper.total_tokens_used} tokens)")
        print(f"📁 Results saved to legacy_*.csv and legacy_*.json")
        
    except ImportError:
        print("❌ Legacy scraper not available. Use the Intelligence Levels scraper instead!")

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
