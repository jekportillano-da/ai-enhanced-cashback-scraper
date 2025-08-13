#!/usr/bin/env python3
"""
Pokitpal Competitive Intelligence Scraper Demo
==============================================

Simple demo showing competitive intelligence capabilities.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

def demo_competitive_intelligence():
    """Demo competitive intelligence features"""
    
    print("🔍 Pokitpal Competitive Intelligence Demo")
    print("=" * 50)
    
    try:
        # Import the main scraper
        scraper_path = project_root / 'src' / 'scrapers'
        sys.path.insert(0, str(scraper_path))
        
        from token_optimized_scraper_v2 import TokenOptimizedAIScraper
        
        # Initialize scraper
        scraper = TokenOptimizedAIScraper()
        
        print("🎯 Running Standard Intelligence Level Analysis...")
        print("📊 Analyzing competitors with competitive intelligence for Pokitpal")
        
        # Demo with a small budget
        results = scraper.scrape_with_intelligence_level(
            site_name="shopback",
            intelligence_level="standard", 
            max_pages=2,
            token_budget=1000  # Small budget for demo
        )
        
        if results:
            print(f"\n✅ Competitive Analysis Complete!")
            print(f"📊 Competitors analyzed: {len(results)}")
            print(f"💰 Analysis cost: ${scraper.token_costs:.4f}")
            
            # Show competitive insights
            for i, result in enumerate(results, 1):
                merchant = result.get('merchant', 'Unknown')
                threat = result.get('competitive_threat_level', 'Unknown')
                opportunity = result.get('pokitpal_opportunity', 'Unknown')
                cashback = result.get('cashback_offer', 'Unknown')
                
                print(f"\n🏪 Competitor {i}: {merchant}")
                print(f"   💰 Cashback Rate: {cashback}")
                print(f"   ⚠️ Threat to Pokitpal: {threat}")
                print(f"   🎯 Opportunity Level: {opportunity}")
                
                # Show strategic recommendations
                recs = result.get('pokitpal_strategic_recommendations', [])
                if recs:
                    print(f"   💡 Strategic Recommendation: {recs[0]}")
            
            # Save results
            scraper.save_intelligence_results(results, "competitive_demo", "standard")
            print(f"\n💾 Results saved as CSV file for Excel analysis")
            
        else:
            print("❌ No competitive intelligence obtained")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure the scraper modules are properly installed")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def show_intelligence_levels():
    """Show available intelligence levels"""
    
    print("\n🧠 Available Intelligence Levels:")
    print("-" * 35)
    print("🔸 Basic ($0.0008/page)")
    print("   • Merchant name and cashback rate")
    print("   • Competitive threat assessment")
    print()
    print("🔹 Standard ($0.0015/page)")
    print("   • Business insights with competitive context")
    print("   • Pokitpal-specific opportunities")
    print("   • Strategic recommendations")
    print()
    print("🔷 Comprehensive ($0.0035/page)")
    print("   • Full competitive intelligence analysis")
    print("   • Market positioning insights")
    print("   • Detailed strategic recommendations")
    print("   • Partnership vs competition assessment")

def main():
    """Run the demo"""
    
    show_intelligence_levels()
    
    print("\n" + "=" * 50)
    print("Starting Demo...")
    print("=" * 50)
    
    demo_competitive_intelligence()
    
    print("\n🎉 Demo Complete!")
    print("\n💡 Next Steps:")
    print("   • Check the data/ folder for CSV results")
    print("   • Open CSV files in Excel for analysis")
    print("   • Run main.py for full scraping capabilities")

if __name__ == "__main__":
    main()
