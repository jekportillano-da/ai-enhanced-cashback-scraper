"""
Quick API Key Test - Verify OpenAI integration works
"""

import os
from dotenv import load_dotenv

def test_openai_connection():
    """Test if OpenAI API key works"""
    
    print("🔑 Testing OpenAI API Key...")
    print("=" * 30)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    if api_key == 'your_openai_api_key_here':
        print("❌ API key not updated in .env file")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...{api_key[-10:]}")
    
    # Test OpenAI connection
    try:
        import openai
        
        # Set up client (new OpenAI library format)
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple completion
        print("🧪 Testing API connection...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello from AI scraper!' in exactly 5 words."}
            ],
            max_tokens=20,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API Response: {result}")
        print("🎉 OpenAI connection successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

def test_ai_scraper_integration():
    """Test if AI scraper integration works"""
    
    print("\n🤖 Testing AI Scraper Integration...")
    print("=" * 35)
    
    try:
        from ai_enhanced_scraper import AIScraperFactory
        
        # Create AI scraper
        scraper = AIScraperFactory.create_ai_scraper("shopback_ai")
        
        print("✅ AI scraper created successfully!")
        print(f"🧠 AI agents available: {len(scraper.ai_orchestrator.agents)}")
        
        # List available agents
        for i, agent in enumerate(scraper.ai_orchestrator.agents, 1):
            print(f"   {i}. {agent.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI scraper integration failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🧪 AI-Enhanced Scraper Test Suite")
    print("=" * 40)
    
    # Test API key
    api_success = test_openai_connection()
    
    # Test scraper integration
    scraper_success = test_ai_scraper_integration()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 25)
    print(f"OpenAI API: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"AI Scraper: {'✅ PASS' if scraper_success else '❌ FAIL'}")
    
    if api_success and scraper_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Your AI-enhanced scraper is ready to use!")
        print("\n💡 Next steps:")
        print("   1. Run: python run_scraper.py")
        print("   2. Choose option 2 (AI-Enhanced Scraper)")
        print("   3. Watch the AI agents work their magic!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        if not api_success:
            print("   • Verify your OpenAI API key is correct")
            print("   • Check your internet connection")
            print("   • Ensure you have API credits available")

if __name__ == "__main__":
    main()
