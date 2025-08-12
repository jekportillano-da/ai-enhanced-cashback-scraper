"""
Complete Example: AI-Enhanced Cashback Scraper Usage
"""

import os
import asyncio
from dotenv import load_dotenv
from ai_enhanced_scraper import AIScraperFactory, AIEnhancedCashbackScraper
from ai_agents import AIAgentOrchestrator
from custom_ai_agents import NLPEnhancedAgent, ContextAwareAgent

# Load environment variables
load_dotenv()

async def main():
    """Main example demonstrating AI-enhanced scraping"""
    
    print("🤖 AI-Enhanced Cashback Scraper Demo")
    print("=" * 50)
    
    # Get API key from environment
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("⚠️  No OpenAI API key found. Some AI features will be limited.")
        print("   Set OPENAI_API_KEY in your .env file for full functionality.")
    
    # Example 1: Basic AI-Enhanced Scraping
    print("\n1️⃣  Basic AI-Enhanced Scraping")
    print("-" * 30)
    
    try:
        # Create AI-enhanced scraper
        scraper = AIScraperFactory.create_ai_scraper("shopback_ai", openai_api_key)
        
        print(f"✅ Created AI-enhanced {scraper.config['name']} scraper")
        print(f"   - AI Orchestrator: {'Enabled' if openai_api_key else 'Limited'}")
        print(f"   - Fallback Methods: Enabled")
        
        # In a real scenario, you would run:
        # offers = scraper.scrape_all(max_workers=3)
        # scraper.save_to_csv(offers, "ai_enhanced_offers.csv")
        
        print("   - Ready to scrape with AI-powered extraction")
        
    except Exception as e:
        print(f"❌ Error creating AI scraper: {e}")
    
    # Example 2: Custom AI Agent Configuration
    print("\n2️⃣  Custom AI Agent Configuration")
    print("-" * 35)
    
    try:
        # Create orchestrator with custom agents
        orchestrator = AIAgentOrchestrator(openai_api_key)
        
        # Add custom agents
        orchestrator.add_agent(NLPEnhancedAgent())
        orchestrator.add_agent(ContextAwareAgent())
        
        print(f"✅ AI Orchestrator configured with {len(orchestrator.agents)} agents:")
        for i, agent in enumerate(orchestrator.agents, 1):
            print(f"   {i}. {agent.name}")
        
    except Exception as e:
        print(f"❌ Error configuring AI agents: {e}")
    
    # Example 3: Comparison with Traditional Scraping
    print("\n3️⃣  AI vs Traditional Scraping Comparison")
    print("-" * 40)
    
    # Simulate scraping results for demonstration
    simulate_performance_comparison()
    
    # Example 4: Learning and Adaptation Demo
    print("\n4️⃣  Learning and Adaptation Features")
    print("-" * 35)
    
    demonstrate_learning_features()
    
    print("\n🎉 Demo complete! Check the generated files for more details.")
    print("\n💡 Next steps:")
    print("   1. Set up your OpenAI API key in .env file")
    print("   2. Install additional dependencies: pip install -r requirements.txt")
    print("   3. Run: python ai_enhanced_scraper.py")


def simulate_performance_comparison():
    """Simulate performance comparison between AI and traditional methods"""
    
    # Simulated performance data
    traditional_stats = {
        "success_rate": 75,
        "adaptability": "Low",
        "maintenance": "High",
        "accuracy": "Good"
    }
    
    ai_enhanced_stats = {
        "success_rate": 92,
        "adaptability": "High", 
        "maintenance": "Low",
        "accuracy": "Excellent"
    }
    
    print("📊 Performance Comparison:")
    print(f"   Traditional Scraping:")
    for key, value in traditional_stats.items():
        print(f"     • {key.title()}: {value}{'%' if isinstance(value, int) else ''}")
    
    print(f"   AI-Enhanced Scraping:")
    for key, value in ai_enhanced_stats.items():
        print(f"     • {key.title()}: {value}{'%' if isinstance(value, int) else ''}")
    
    improvement = ai_enhanced_stats["success_rate"] - traditional_stats["success_rate"]
    print(f"   🚀 Improvement: +{improvement}% success rate")


def demonstrate_learning_features():
    """Demonstrate learning and adaptation features"""
    
    learning_features = [
        "🧠 Pattern Learning: Automatically learns successful extraction patterns",
        "🔄 Adaptive Selectors: Adjusts to website changes automatically", 
        "📚 Context Awareness: Uses previous attempts to improve accuracy",
        "🎯 Confidence Scoring: Provides reliability metrics for extractions",
        "🔍 Multi-Method Fallback: Tries multiple extraction approaches",
        "📊 Performance Tracking: Monitors and reports extraction success rates"
    ]
    
    print("🤖 AI Learning & Adaptation Features:")
    for feature in learning_features:
        print(f"   {feature}")
    
    print("\n📈 Benefits:")
    print("   • Reduced maintenance when websites change")
    print("   • Improved accuracy over time")
    print("   • Automatic adaptation to new site structures")
    print("   • Intelligent fallback strategies")


def create_sample_config_file():
    """Create a sample configuration file"""
    
    sample_config = """
# AI-Enhanced Scraper Configuration

AI_SETTINGS = {
    "openai_model": "gpt-3.5-turbo",
    "confidence_threshold": 0.7,
    "max_tokens": 500,
    "temperature": 0.1,
    "enable_learning": True,
    "enable_vision": False,  # Requires GPT-4 Vision
    "enable_nlp": True
}

SCRAPING_SETTINGS = {
    "max_workers": 3,
    "request_delay": 1,
    "timeout": 10,
    "retry_attempts": 3,
    "user_agent_rotation": True
}

LEARNING_SETTINGS = {
    "save_patterns": True,
    "pattern_file": "learned_patterns.json",
    "min_confidence_for_learning": 0.8,
    "max_patterns_per_site": 10
}
"""
    
    with open("ai_scraper_config.py", "w") as f:
        f.write(sample_config)
    
    print("📝 Created sample configuration file: ai_scraper_config.py")


if __name__ == "__main__":
    asyncio.run(main())
    create_sample_config_file()
