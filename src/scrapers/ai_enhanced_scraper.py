"""
AI-Enhanced Cashback Scraper - Integration with existing scraper system
"""

from cashback_scraper import BaseCashbackScraper, CashbackOffer
from ai_agents import AIAgentOrchestrator, ExtractionResult
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIEnhancedCashbackScraper(BaseCashbackScraper):
    """Enhanced scraper that uses AI agents for flexible data extraction"""
    
    def __init__(self, config: dict, openai_api_key: str = None):
        super().__init__(config)
        
        # Initialize AI orchestrator
        api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.ai_orchestrator = AIAgentOrchestrator(api_key)
        
        # Track AI performance
        self.ai_success_count = 0
        self.fallback_success_count = 0
        self.total_attempts = 0
        
    def extract_merchant_data(self, soup, url: str) -> Optional[CashbackOffer]:
        """Enhanced extraction using AI agents with fallback to traditional methods"""
        self.total_attempts += 1
        
        # First, try AI-powered extraction
        ai_result = self._try_ai_extraction(soup, url)
        if ai_result:
            self.ai_success_count += 1
            return self._convert_ai_result_to_cashback_offer(ai_result, url)
        
        # Fallback to traditional extraction methods
        traditional_result = self._try_traditional_extraction(soup, url)
        if traditional_result:
            self.fallback_success_count += 1
            return traditional_result
        
        self.logger.warning(f"Both AI and traditional extraction failed for {url}")
        return None
    
    def _try_ai_extraction(self, soup, url: str) -> Optional[ExtractionResult]:
        """Try AI-powered extraction"""
        try:
            html_content = str(soup)
            return self.ai_orchestrator.extract_data(url, html_content, soup)
        except Exception as e:
            self.logger.error(f"AI extraction failed for {url}: {e}")
            return None
    
    def _try_traditional_extraction(self, soup, url: str) -> Optional[CashbackOffer]:
        """Fallback to traditional CSS selector-based extraction"""
        try:
            # Extract merchant name using traditional selectors
            merchant_name = self._extract_merchant_traditional(soup)
            if not merchant_name:
                return None
            
            # Extract cashback offer using traditional selectors
            cashback_offer = self._extract_cashback_traditional(soup)
            
            return CashbackOffer(
                merchant=merchant_name,
                cashback_offer=cashback_offer or "No Cashback Info",
                url=url
            )
            
        except Exception as e:
            self.logger.error(f"Traditional extraction failed for {url}: {e}")
            return None
    
    def _extract_merchant_traditional(self, soup) -> Optional[str]:
        """Traditional merchant name extraction"""
        selectors = self.config.get('merchant_selectors', [
            "h1", 
            "h2", 
            ".merchant-name", 
            ".store-name",
            "[data-test*='name']"
        ])
        
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text and len(text) > 2:
                        return text
            except:
                continue
        return None
    
    def _extract_cashback_traditional(self, soup) -> Optional[str]:
        """Traditional cashback extraction"""
        selectors = self.config.get('cashback_selectors', [
            "[data-test-id='cashback-rate']",
            ".cashback-rate",
            ".rate",
            "h3", "h4", "h5"
        ])
        
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if self._is_cashback_text(text):
                        return text
            except:
                continue
        return None
    
    def _is_cashback_text(self, text: str) -> bool:
        """Check if text contains cashback information"""
        if not text:
            return False
        
        import re
        cashback_patterns = [
            r'\d+\.?\d*%',
            r'\$\d+',
            r'cashback',
            r'points',
            r'earn'
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in cashback_patterns)
    
    def _convert_ai_result_to_cashback_offer(self, ai_result: ExtractionResult, url: str) -> CashbackOffer:
        """Convert AI extraction result to CashbackOffer"""
        return CashbackOffer(
            merchant=ai_result.merchant_name,
            cashback_offer=ai_result.cashback_offer,
            url=url
        )
    
    def get_ai_performance_stats(self) -> dict:
        """Get AI performance statistics"""
        if self.total_attempts == 0:
            return {"message": "No scraping attempts yet"}
        
        return {
            "total_attempts": self.total_attempts,
            "ai_success_count": self.ai_success_count,
            "traditional_success_count": self.fallback_success_count,
            "ai_success_rate": self.ai_success_count / self.total_attempts * 100,
            "traditional_success_rate": self.fallback_success_count / self.total_attempts * 100,
            "overall_success_rate": (self.ai_success_count + self.fallback_success_count) / self.total_attempts * 100
        }


class AIShopBackScraper(AIEnhancedCashbackScraper):
    """AI-enhanced ShopBack scraper"""
    
    def __init__(self, openai_api_key: str = None):
        config = {
            "name": "shopback_ai",
            "sitemap_url": "https://www.shopback.com.au/sitemap.xml",
            "delay": 1,
            "merchant_selectors": ["h1", ".merchant-name"],
            "cashback_selectors": ["h4.fs_sbds-global-font-size-7", ".cashback-rate"]
        }
        super().__init__(config, openai_api_key)


class AICashRewardsScraper(AIEnhancedCashbackScraper):
    """AI-enhanced CashRewards scraper"""
    
    def __init__(self, openai_api_key: str = None):
        config = {
            "name": "cashrewards_ai",
            "sitemap_url": "https://www.cashrewards.com.au/en/sitemap.xml",
            "url_filter": "https://www.cashrewards.com.au/store",
            "delay": 1,
            "merchant_selectors": ["h1", ".merchant-name"],
            "cashback_selectors": ["h3[data-test-id='cashback-rate']", ".cashback-rate"]
        }
        super().__init__(config, openai_api_key)


class AIScraperFactory:
    """Factory for creating AI-enhanced scrapers"""
    
    SCRAPER_CONFIGS = {
        "shopback_ai": AIShopBackScraper,
        "cashrewards_ai": AICashRewardsScraper
    }
    
    @classmethod
    def create_ai_scraper(cls, scraper_type: str, openai_api_key: str = None) -> AIEnhancedCashbackScraper:
        """Create an AI-enhanced scraper"""
        if scraper_type not in cls.SCRAPER_CONFIGS:
            raise ValueError(f"Unknown AI scraper type: {scraper_type}")
        
        scraper_class = cls.SCRAPER_CONFIGS[scraper_type]
        return scraper_class(openai_api_key)
    
    @classmethod
    def get_available_ai_scrapers(cls) -> list:
        """Get list of available AI scraper types"""
        return list(cls.SCRAPER_CONFIGS.keys())


# Example usage and testing
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Test AI-enhanced scraping
    print("Testing AI-Enhanced Cashback Scraping")
    print("=" * 40)
    
    # Get OpenAI API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Warning: No OpenAI API key found. AI features will be limited.")
    
    # Create AI-enhanced scraper
    scraper = AIScraperFactory.create_ai_scraper("shopback_ai", api_key)
    
    # Test on a few URLs (you would normally scrape all)
    test_urls = [
        "https://www.shopback.com.au/store/example-store-1",
        "https://www.shopback.com.au/store/example-store-2"
    ]
    
    print(f"Testing AI extraction on {len(test_urls)} URLs...")
    
    for url in test_urls:
        try:
            # This would normally be called by scrape_all()
            print(f"\nTesting: {url}")
            
            # In real usage, this would fetch the page
            # result = scraper.scrape_page(url)
            # print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error testing {url}: {e}")
    
    # Show performance stats
    stats = scraper.get_ai_performance_stats()
    print(f"\nAI Performance Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
