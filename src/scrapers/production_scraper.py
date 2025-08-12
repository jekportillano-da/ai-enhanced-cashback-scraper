"""
Production-Ready AI-Enhanced Scraper - Ready to Run!
"""

import requests
import csv
import json
import time
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()

class SimpleAIScraper:
    """Simple AI-enhanced scraper ready for production use"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.setup_logging()
        self.openai_client = None
        self.setup_ai()
        
        # Statistics
        self.total_attempts = 0
        self.ai_successes = 0
        self.traditional_successes = 0
        
        # Token tracking (approximate)
        self.estimated_tokens_used = 0
        self.api_calls_made = 0
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AIScraper')
    
    def setup_ai(self):
        """Setup OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
                self.logger.info("✅ OpenAI client initialized")
            except Exception as e:
                self.logger.warning(f"⚠️ OpenAI setup failed: {e}")
        else:
            self.logger.info("ℹ️ No OpenAI API key - using traditional methods only")
    
    def fetch_sitemap_urls(self, sitemap_url):
        """Fetch URLs from sitemap"""
        try:
            self.logger.info(f"Fetching sitemap: {sitemap_url}")
            response = self.session.get(sitemap_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "xml")
            urls = [loc.text for loc in soup.find_all("loc")]
            
            self.logger.info(f"Found {len(urls)} URLs in sitemap")
            return urls
            
        except Exception as e:
            self.logger.error(f"Failed to fetch sitemap: {e}")
            return []
    
    def ai_extract(self, html_content, url):
        """Use AI to extract merchant data"""
        if not self.openai_client:
            return None
            
        try:
            # Clean HTML for AI processing with token optimization
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements that consume tokens but don't help
            for element in soup(["script", "style", "nav", "footer", "aside", "header", 
                               "meta", "link", "noscript", "iframe", "svg"]):
                element.decompose()
            
            # Extract key content sections to minimize tokens
            key_content = []
            
            # 1. Page title
            title = soup.find('title')
            if title:
                key_content.append(f"TITLE: {title.get_text().strip()}")
            
            # 2. Main headers
            headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])[:5]  # Limit to 5 headers
            for header in headers:
                text = header.get_text().strip()
                if text and len(text) < 150:
                    key_content.append(f"HEADER: {text}")
            
            # 3. Cashback-related elements
            cashback_elements = soup.find_all(attrs={'class': lambda x: x and any(
                keyword in ' '.join(x).lower() for keyword in ['cashback', 'rate', 'offer', 'reward']
            )})[:3]  # Limit to 3 elements
            
            for element in cashback_elements:
                text = element.get_text().strip()
                if text and len(text) < 200:
                    key_content.append(f"CASHBACK: {text}")
            
            # 4. Text with percentages or dollar signs
            all_text = soup.get_text()
            import re
            percentage_matches = re.findall(r'[^.]*\d+\.?\d*%[^.]*', all_text)[:2]
            for match in percentage_matches:
                key_content.append(f"PERCENT: {match.strip()}")
            
            # Combine and limit content (roughly 1500 characters = ~400 tokens)
            clean_text = "\n".join(key_content)[:1500]
            
            prompt = f"""
Extract cashback information from this webpage content.

URL: {url}
Content: {clean_text}

Return JSON format:
{{
    "merchant_name": "exact merchant name or null",
    "cashback_offer": "exact cashback offer or null",
    "confidence": 0.95
}}

Only return valid JSON, no other text.
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract cashback data. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,  # Limit output tokens to control cost
                temperature=0.1
            )
            
            # Track approximate token usage
            self.api_calls_made += 1
            # Rough estimate: input ~400 tokens + output ~100 tokens
            estimated_tokens = len(prompt.split()) * 1.3 + 100
            self.estimated_tokens_used += estimated_tokens
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_text = result_text[start:end]
                result = json.loads(json_text)
                
                if result.get('merchant_name') and result.get('cashback_offer'):
                    return {
                        'merchant': result['merchant_name'],
                        'cashback_offer': result['cashback_offer'],
                        'confidence': result.get('confidence', 0.8),
                        'method': 'AI_LLM'
                    }
            
        except Exception as e:
            self.logger.debug(f"AI extraction failed for {url}: {e}")
        
        return None
    
    def traditional_extract(self, soup, url):
        """Traditional CSS selector extraction"""
        try:
            # Try to find merchant name
            merchant = None
            for selector in ['h1', 'h2', '.merchant-name', '.store-name', 'title']:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text and len(text) > 2 and len(text) < 100:
                        merchant = text
                        break
            
            if not merchant:
                return None
            
            # Try to find cashback offer
            cashback = "No Cashback Info"
            cashback_selectors = [
                'h4.fs_sbds-global-font-size-7',  # ShopBack
                'h3[data-test-id="cashback-rate"]',  # CashRewards
                '.cashback-rate',
                '.rate',
                'h3', 'h4', 'h5'
            ]
            
            for selector in cashback_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if any(keyword in text.lower() for keyword in ['%', 'cashback', 'cash back', 'earn', '$']):
                        cashback = text
                        break
            
            return {
                'merchant': merchant,
                'cashback_offer': cashback,
                'confidence': 0.7,
                'method': 'Traditional_CSS'
            }
            
        except Exception as e:
            self.logger.debug(f"Traditional extraction failed for {url}: {e}")
            return None
    
    def scrape_page(self, url):
        """Scrape a single page with AI + traditional fallback"""
        self.total_attempts += 1
        
        try:
            # Fetch page
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try AI extraction first
            ai_result = self.ai_extract(response.text, url)
            if ai_result:
                self.ai_successes += 1
                return {
                    **ai_result,
                    'url': url,
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Fallback to traditional extraction
            traditional_result = self.traditional_extract(soup, url)
            if traditional_result:
                self.traditional_successes += 1
                return {
                    **traditional_result,
                    'url': url,
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            
        except Exception as e:
            self.logger.debug(f"Error scraping {url}: {e}")
        
        return None
    
    def scrape_site(self, sitemap_url, site_name, max_pages=50):
        """Scrape a cashback site"""
        self.logger.info(f"🚀 Starting {site_name} scraper...")
        
        # Get URLs
        urls = self.fetch_sitemap_urls(sitemap_url)
        if not urls:
            return []
        
        # Filter URLs if needed
        if 'cashrewards' in site_name.lower():
            urls = [url for url in urls if '/store/' in url]
        
        # Limit number of pages for demo
        urls = urls[:max_pages]
        
        offers = []
        
        self.logger.info(f"Scraping {len(urls)} pages...")
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Scraping {i}/{len(urls)}: {url}")
            
            result = self.scrape_page(url)
            if result:
                offers.append(result)
                self.logger.info(f"✅ {result['method']}: {result['merchant']} - {result['cashback_offer']}")
            
            # Rate limiting
            time.sleep(1)
            
            # Show progress every 10 pages
            if i % 10 == 0:
                self.logger.info(f"Progress: {i}/{len(urls)} pages, {len(offers)} offers found")
        
        self.logger.info(f"🎉 {site_name} scraping complete! Found {len(offers)} offers")
        return offers
    
    def save_results(self, offers, filename_prefix):
        """Save results to CSV and JSON"""
        if not offers:
            self.logger.warning("No offers to save")
            return
        
        # Save CSV
        csv_file = f"{filename_prefix}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=offers[0].keys())
            writer.writeheader()
            writer.writerows(offers)
        
        # Save JSON
        json_file = f"{filename_prefix}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(offers, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"💾 Results saved to {csv_file} and {json_file}")
    
    def get_stats(self):
        """Get scraping statistics including token estimates"""
        if self.total_attempts == 0:
            return "No scraping attempts yet"
        
        ai_rate = (self.ai_successes / self.total_attempts) * 100
        traditional_rate = (self.traditional_successes / self.total_attempts) * 100
        overall_rate = ((self.ai_successes + self.traditional_successes) / self.total_attempts) * 100
        
        # Estimate cost (GPT-3.5-turbo: ~$0.0035 per 1K tokens)
        estimated_cost = (self.estimated_tokens_used / 1000) * 0.0035
        
        return {
            'total_attempts': self.total_attempts,
            'ai_successes': self.ai_successes,
            'traditional_successes': self.traditional_successes,
            'ai_success_rate': f"{ai_rate:.1f}%",
            'traditional_success_rate': f"{traditional_rate:.1f}%",
            'overall_success_rate': f"{overall_rate:.1f}%",
            'api_calls_made': self.api_calls_made,
            'estimated_tokens_used': self.estimated_tokens_used,
            'estimated_cost': f"${estimated_cost:.4f}"
        }

def main():
    """Main scraping function"""
    print("🚀 AI-Enhanced Cashback Scraper - Production Run")
    print("=" * 50)
    
    # Create scraper
    scraper = SimpleAIScraper()
    
    # Choose what to scrape
    print("\n🎯 Choose scraping target:")
    print("1. ShopBack Australia (fast demo - 10 pages)")
    print("2. CashRewards Australia (fast demo - 10 pages)")
    print("3. Both sites (comprehensive)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        offers = scraper.scrape_site(
            "https://www.shopback.com.au/sitemap.xml",
            "ShopBack",
            max_pages=10
        )
        scraper.save_results(offers, "shopback_offers")
        
    elif choice == "2":
        offers = scraper.scrape_site(
            "https://www.cashrewards.com.au/en/sitemap.xml",
            "CashRewards",
            max_pages=10
        )
        scraper.save_results(offers, "cashrewards_offers")
        
    elif choice == "3":
        # Scrape both sites
        shopback_offers = scraper.scrape_site(
            "https://www.shopback.com.au/sitemap.xml",
            "ShopBack",
            max_pages=25
        )
        
        cashrewards_offers = scraper.scrape_site(
            "https://www.cashrewards.com.au/en/sitemap.xml", 
            "CashRewards",
            max_pages=25
        )
        
        # Save individual results
        scraper.save_results(shopback_offers, "shopback_offers")
        scraper.save_results(cashrewards_offers, "cashrewards_offers")
        
        # Combine and save
        all_offers = shopback_offers + cashrewards_offers
        scraper.save_results(all_offers, "combined_offers")
        
    elif choice == "4":
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice")
        return
    
    # Show statistics
    stats = scraper.get_stats()
    print(f"\n📊 Scraping Statistics:")
    print(f"   Total attempts: {stats['total_attempts']}")
    print(f"   AI success rate: {stats['ai_success_rate']}")
    print(f"   Traditional success rate: {stats['traditional_success_rate']}")
    print(f"   Overall success rate: {stats['overall_success_rate']}")
    print(f"   API calls made: {stats['api_calls_made']}")
    print(f"   Estimated tokens used: {stats['estimated_tokens_used']}")
    print(f"   Estimated cost: {stats['estimated_cost']}")
    
    print(f"\n🎉 Scraping complete! Check the output files in this folder.")

if __name__ == "__main__":
    main()
