#!/usr/bin/env python3
"""Test enhanced model selection system"""

from src.scrapers.token_optimized_scraper_v2 import TokenOptimizedAIScraper

def test_enhanced_model_selection():
    scraper = TokenOptimizedAIScraper()
    
    print("🧪 Testing Enhanced Model Selection System")
    print("=" * 50)
    
    print("Available models:", scraper.get_available_models())
    print()
    
    print("Cost Matrix (Intelligence Level + Model):")
    levels = ['basic', 'standard', 'comprehensive']
    models = ['gpt-3.5-turbo', 'gpt-4o']
    
    for level in levels:
        print(f"{level.upper()}:")
        for model in models:
            cost = scraper.get_cost_estimate(level, model)
            model_info = scraper.get_model_info(model)
            print(f"  {model_info['name']}: ${cost:.4f}/page")
        print()
    
    print("✅ Enhanced model selection system working!")
    print()
    
    # Test dynamic cost calculation
    print("Test Dynamic Cost Calculation:")
    test_cost = scraper.calculate_dynamic_cost('comprehensive', 'gpt-4o', 500, 1000)
    print(f"Comprehensive + GPT-4o (500 input, 1000 output tokens): ${test_cost:.4f}")
    
    test_cost = scraper.calculate_dynamic_cost('basic', 'gpt-3.5-turbo', 200, 100)
    print(f"Basic + GPT-3.5 (200 input, 100 output tokens): ${test_cost:.4f}")

if __name__ == "__main__":
    test_enhanced_model_selection()
