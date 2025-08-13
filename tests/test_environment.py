#!/usr/bin/env python3
"""
Test API Key Configuration for Pokitpal Competitive Intelligence Scraper
=======================================================================

Simple test to verify OpenAI API key is properly configured.
"""

import os
from dotenv import load_dotenv
import openai

def test_api_key():
    """Test if OpenAI API key is properly configured"""
    
    print("🔑 Testing API Key Configuration")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key exists
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("💡 Please add your OpenAI API key to .env file")
        return False
    
    print(f"✅ API key found (ends with: ...{api_key[-8:]})")
    
    # Test API connection
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=5
        )
        
        print("✅ API connection successful")
        print(f"💰 Test cost: ~$0.0001")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        print("💡 Please check your API key and internet connection")
        return False

def test_environment_setup():
    """Test overall environment setup"""
    
    print("\n🧪 Testing Environment Setup")
    print("=" * 35)
    
    try:
        # Test imports
        import requests
        import tiktoken
        import pandas
        import openpyxl
        
        print("✅ All required packages installed")
        
        # Test directories
        import pathlib
        project_root = pathlib.Path(__file__).parent.parent
        
        required_dirs = ['src', 'data', 'logs', 'config']
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            if dir_path.exists():
                print(f"✅ {dir_name}/ directory exists")
            else:
                print(f"❌ {dir_name}/ directory missing")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def main():
    """Run all tests"""
    
    print("🧪 Pokitpal Scraper Environment Tests")
    print("=" * 45)
    
    # Test environment
    env_ok = test_environment_setup()
    
    # Test API key
    api_ok = test_api_key()
    
    print("\n📊 Test Results:")
    print(f"   Environment Setup: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"   API Configuration: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if env_ok and api_ok:
        print("\n🎉 All tests passed! Ready for competitive intelligence scraping.")
    else:
        print("\n⚠️ Some tests failed. Please fix issues before running scraper.")

if __name__ == "__main__":
    main()
