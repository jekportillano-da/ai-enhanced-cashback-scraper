"""
Quick Demo Script - Actually runs and produces output files
"""

import csv
import json
import time
from pathlib import Path

def create_sample_output():
    """Create sample output files to show what the scraper produces"""
    
    print("🔄 Creating sample scraper output...")
    
    # Sample data that would be scraped
    sample_offers = [
        {
            "merchant": "Amazon Australia",
            "cashback_offer": "5% cashback",
            "url": "https://www.shopback.com.au/amazon-australia",
            "scraped_at": "2024-08-12 14:30:00",
            "extraction_method": "AI_LLM",
            "confidence_score": 0.95
        },
        {
            "merchant": "Nike",
            "cashback_offer": "3% cashback + $20 bonus",
            "url": "https://www.shopback.com.au/nike",
            "scraped_at": "2024-08-12 14:30:15", 
            "extraction_method": "Pattern_Learning",
            "confidence_score": 0.88
        },
        {
            "merchant": "eBay",
            "cashback_offer": "2% cashback",
            "url": "https://www.shopback.com.au/ebay",
            "scraped_at": "2024-08-12 14:30:30",
            "extraction_method": "Adaptive_Selector",
            "confidence_score": 0.82
        },
        {
            "merchant": "Booking.com",
            "cashback_offer": "4% cashback",
            "url": "https://www.shopback.com.au/booking-com",
            "scraped_at": "2024-08-12 14:30:45",
            "extraction_method": "AI_LLM",
            "confidence_score": 0.93
        },
        {
            "merchant": "Woolworths",
            "cashback_offer": "2% cashback on groceries",
            "url": "https://www.shopback.com.au/woolworths",
            "scraped_at": "2024-08-12 14:31:00",
            "extraction_method": "Traditional_CSS",
            "confidence_score": 0.75
        }
    ]
    
    # Create CSV output
    csv_file = "sample_scraper_output.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Headers
        writer.writerow(["Merchant", "Cashback Offer", "URL", "Scraped At", "Extraction Method", "Confidence Score"])
        
        # Data rows
        for offer in sample_offers:
            writer.writerow([
                offer["merchant"],
                offer["cashback_offer"], 
                offer["url"],
                offer["scraped_at"],
                offer["extraction_method"],
                offer["confidence_score"]
            ])
    
    print(f"✅ Created CSV output: {csv_file}")
    
    # Create JSON output
    json_file = "sample_scraper_output.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(sample_offers, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created JSON output: {json_file}")
    
    # Create AI learning patterns file
    ai_patterns = {
        "learned_patterns": {
            "shopback": {
                "merchant_selectors": [
                    {"selector": "h1.merchant-title", "confidence": 0.92, "success_count": 18},
                    {"selector": ".store-name", "confidence": 0.87, "success_count": 15}
                ],
                "cashback_selectors": [
                    {"selector": "h4.cashback-rate", "confidence": 0.95, "success_count": 22},
                    {"selector": ".offer-percentage", "confidence": 0.89, "success_count": 16}
                ]
            }
        },
        "performance_stats": {
            "total_pages_scraped": len(sample_offers),
            "ai_extraction_success": 2,
            "pattern_learning_success": 1, 
            "adaptive_selector_success": 1,
            "traditional_fallback_success": 1,
            "overall_success_rate": "100%",
            "ai_success_rate": "80%",
            "average_confidence": 0.87
        },
        "last_updated": "2024-08-12 14:31:00"
    }
    
    patterns_file = "ai_learning_data.json"
    with open(patterns_file, "w", encoding="utf-8") as f:
        json.dump(ai_patterns, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created AI learning data: {patterns_file}")
    
    # Create log file
    log_file = "scraper_activity.log"
    log_entries = [
        "2024-08-12 14:30:00 - INFO - Starting AI-enhanced scraping session",
        "2024-08-12 14:30:00 - INFO - Loaded 3 AI agents: LLM, Pattern_Learning, Adaptive_Selector",
        "2024-08-12 14:30:00 - INFO - Fetching sitemap from https://www.shopback.com.au/sitemap.xml",
        "2024-08-12 14:30:05 - INFO - Found 1,247 URLs in sitemap",
        "2024-08-12 14:30:05 - INFO - Starting extraction with 3 concurrent workers",
        "2024-08-12 14:30:15 - INFO - AI_LLM extracted: Amazon Australia - 5% cashback (confidence: 0.95)",
        "2024-08-12 14:30:30 - INFO - Pattern_Learning extracted: Nike - 3% cashback + $20 bonus (confidence: 0.88)",
        "2024-08-12 14:30:45 - INFO - Adaptive_Selector extracted: eBay - 2% cashback (confidence: 0.82)",
        "2024-08-12 14:31:00 - INFO - AI_LLM extracted: Booking.com - 4% cashback (confidence: 0.93)",
        "2024-08-12 14:31:15 - INFO - Traditional_CSS extracted: Woolworths - 2% cashback on groceries (confidence: 0.75)",
        "2024-08-12 14:31:30 - INFO - Scraping completed. Total offers: 5, Success rate: 100%",
        "2024-08-12 14:31:30 - INFO - AI performance: 80% success rate, 0.87 average confidence",
        "2024-08-12 14:31:35 - INFO - Saved results to CSV and JSON files",
        "2024-08-12 14:31:35 - INFO - Updated AI learning patterns with 2 new successful extractions"
    ]
    
    with open(log_file, "w", encoding="utf-8") as f:
        for entry in log_entries:
            f.write(entry + "\n")
    
    print(f"✅ Created activity log: {log_file}")
    
    return len(sample_offers)

def show_output_summary():
    """Show summary of created output files"""
    
    print("\n📁 OUTPUT FILES CREATED:")
    print("=" * 30)
    
    # Check file sizes and show details
    files_info = [
        ("sample_scraper_output.csv", "Cashback offers in CSV format"),
        ("sample_scraper_output.json", "Cashback offers in JSON format"), 
        ("ai_learning_data.json", "AI learning patterns and performance stats"),
        ("scraper_activity.log", "Detailed scraping activity log")
    ]
    
    for filename, description in files_info:
        file_path = Path(filename)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"📄 {filename}")
            print(f"   📝 {description}")
            print(f"   📊 Size: {size} bytes")
            print()
    
    print("💡 You can open these files to see the scraper output!")

def display_sample_content():
    """Display sample content from the output files"""
    
    print("\n📋 SAMPLE OUTPUT CONTENT:")
    print("=" * 35)
    
    # Show CSV content
    print("\n📄 CSV Output (sample_scraper_output.csv):")
    print("-" * 45)
    try:
        with open("sample_scraper_output.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()[:4]  # Show first 4 lines
            for line in lines:
                print(f"   {line.strip()}")
        print("   ... (and more rows)")
    except FileNotFoundError:
        print("   File not found")
    
    # Show JSON content
    print("\n📄 JSON Output (first entry):")
    print("-" * 30)
    try:
        with open("sample_scraper_output.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if data:
                print(json.dumps(data[0], indent=4))
    except FileNotFoundError:
        print("   File not found")
    
    # Show AI stats
    print("\n🤖 AI Performance Stats:")
    print("-" * 25)
    try:
        with open("ai_learning_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            stats = data.get("performance_stats", {})
            for key, value in stats.items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
    except FileNotFoundError:
        print("   File not found")

def main():
    """Main demo function"""
    
    print("🎯 CASHBACK SCRAPER OUTPUT DEMO")
    print("=" * 40)
    print("This demo creates sample output files to show")
    print("what the AI-enhanced scraper produces.\n")
    
    # Create sample outputs
    offers_count = create_sample_output()
    
    print(f"\n🎉 Demo completed!")
    print(f"📊 Simulated scraping of {offers_count} cashback offers")
    
    # Show file summary
    show_output_summary()
    
    # Show sample content
    display_sample_content()
    
    print("\n" + "=" * 50)
    print("🚀 READY TO RUN REAL SCRAPER!")
    print("=" * 50)
    print("\n💡 To run the actual scraper:")
    print("   1. Set up OpenAI API key in .env file")
    print("   2. Run: python run_scraper.py")
    print("   3. Choose option 1 (Traditional) or 2 (AI-Enhanced)")
    print("\n📁 Output files will be created in this folder")
    print("📊 Check the CSV/JSON files for scraped data")
    print("🤖 Check the learning data for AI improvements")

if __name__ == "__main__":
    main()
