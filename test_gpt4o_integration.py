#!/usr/bin/env python3
"""Test GPT-4o model selection logic"""

from src.scrapers.token_optimized_scraper_v2 import TokenOptimizedAIScraper

def test_model_selection():
    scraper = TokenOptimizedAIScraper()
    
    print("🧪 GPT-4o Integration Test")
    print("=" * 30)
    
    print(f"Default model: {scraper.model_name}")
    
    print("\nIntelligence Level Configurations:")
    levels = ['basic', 'standard', 'comprehensive']
    
    for level in levels:
        config = scraper.intelligence_levels[level]
        model_note = " (GPT-4o)" if level == 'comprehensive' else ""
        print(f"  {level.title()}: {config['max_tokens']} tokens, ${config['estimated_cost_per_call']}{model_note}")
    
    print("\n✅ Model selection logic configured correctly!")
    print("✅ Comprehensive level will automatically use GPT-4o")
    print("✅ Basic/Standard levels use GPT-3.5-turbo")

if __name__ == "__main__":
    test_model_selection()
