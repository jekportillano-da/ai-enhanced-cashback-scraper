"""
Token-Optimized AI-Enhanced Scraper with Cost Control
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
import re
import tiktoken

# Load environment variables
load_dotenv()

class TokenOptimizedAIScraper:
    """AI-enhanced scraper with intelligent token management"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.setup_logging()
        self.model_name = "gpt-3.5-turbo"  # Add model name
        self.openai_client = None
        self.tokenizer = None
        self.setup_ai()
        
        # Token tracking
        self.total_tokens_used = 0
        self.total_api_calls = 0
        self.token_costs = 0.0
        
        # Statistics
        self.total_attempts = 0
        self.ai_successes = 0
        self.traditional_successes = 0
        
        # Token limits
        self.max_input_tokens = 3000  # Conservative limit for input
        self.max_output_tokens = 150  # Limit output tokens
        self.model_name = "gpt-3.5-turbo"
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('token_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('TokenAIScraper')
    
    def setup_ai(self):
        """Setup OpenAI client and tokenizer"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
                # Initialize tokenizer for token counting
                self.tokenizer = tiktoken.encoding_for_model(self.model_name)
                self.logger.info("✅ OpenAI client and tokenizer initialized")
            except Exception as e:
                self.logger.warning(f"⚠️ OpenAI setup failed: {e}")
        else:
            self.logger.info("ℹ️ No OpenAI API key - using traditional methods only")
    
    def count_tokens(self, text):
        """Count tokens in text"""
        if not self.tokenizer:
            return len(text.split()) * 1.3  # Rough estimate
        
        try:
            return len(self.tokenizer.encode(text))
        except:
            return len(text.split()) * 1.3
    
    def optimize_content_for_tokens(self, html_content, url):
        """Optimize HTML content to minimize tokens while preserving important info"""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements that don't contain cashback info
        for element in soup(["script", "style", "nav", "footer", "aside", "header", 
                           "meta", "link", "noscript", "iframe", "svg", "path"]):
            element.decompose()
        
        # Extract potentially relevant sections
        relevant_sections = []
        
        # 1. Headers (likely to contain merchant names)
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for header in headers:
            text = header.get_text().strip()
            if text and len(text) < 200:
                relevant_sections.append(f"HEADER: {text}")
        
        # 2. Elements with cashback-related classes or IDs
        cashback_keywords = ['cashback', 'cash-back', 'rate', 'offer', 'reward', 'earn', 'percentage']
        for keyword in cashback_keywords:
            elements = soup.find_all(attrs={'class': re.compile(keyword, re.I)})
            elements.extend(soup.find_all(attrs={'id': re.compile(keyword, re.I)}))
            elements.extend(soup.find_all(attrs={'data-test': re.compile(keyword, re.I)}))
            elements.extend(soup.find_all(attrs={'data-test-id': re.compile(keyword, re.I)}))
            
            for element in elements:
                text = element.get_text().strip()
                if text and len(text) < 300:
                    relevant_sections.append(f"CASHBACK: {text}")
        
        # 3. Text containing percentage signs or dollar signs
        all_text = soup.get_text()
        percentage_matches = re.findall(r'[^.]*\d+\.?\d*%[^.]*', all_text)
        dollar_matches = re.findall(r'[^.]*\$\d+\.?\d*[^.]*', all_text)
        
        for match in percentage_matches[:3]:  # Limit to first 3 matches
            relevant_sections.append(f"PERCENT: {match.strip()}")
        
        for match in dollar_matches[:2]:  # Limit to first 2 matches
            relevant_sections.append(f"DOLLAR: {match.strip()}")
        
        # 4. Title and meta description
        title = soup.find('title')
        if title:
            relevant_sections.insert(0, f"TITLE: {title.get_text().strip()}")
        
        # Combine relevant sections
        optimized_content = "\n".join(relevant_sections[:15])  # Limit to 15 sections
        
        # Check token count and trim if necessary
        token_count = self.count_tokens(optimized_content)
        
        if token_count > self.max_input_tokens:
            # Trim content to fit within token limit
            words = optimized_content.split()
            # Estimate words per token (roughly 0.75)
            max_words = int(self.max_input_tokens * 0.75)
            optimized_content = " ".join(words[:max_words])
            
            self.logger.debug(f"Content trimmed from {token_count} to ~{self.count_tokens(optimized_content)} tokens")
        
        return optimized_content, self.count_tokens(optimized_content)
    
    def create_optimized_prompt(self, content, url):
        """Create a token-optimized prompt"""
        
        prompt = f"""Extract cashback data from this webpage content.

URL: {url}

Content:
{content}

Return only JSON:
{{"merchant_name": "name or null", "cashback_offer": "offer or null", "confidence": 0.9}}"""
        
        return prompt
    
    def ai_extract(self, html_content, url):
        """Use AI to extract merchant data with token optimization"""
        if not self.openai_client:
            return None
        
        try:
            # Optimize content for token efficiency
            optimized_content, input_tokens = self.optimize_content_for_tokens(html_content, url)
            
            # Create optimized prompt
            prompt = self.create_optimized_prompt(optimized_content, url)
            
            # Count total input tokens
            system_message = "Extract cashback data. Return only valid JSON."
            total_input_tokens = self.count_tokens(system_message + prompt)
            
            self.logger.debug(f"Input tokens: {total_input_tokens}, Content tokens: {input_tokens}")
            
            # Make API call with token limits
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_output_tokens,
                temperature=0.1
            )
            
            # Track token usage
            usage = response.usage
            self.total_tokens_used += usage.total_tokens
            self.total_api_calls += 1
            
            # Calculate cost (GPT-3.5-turbo pricing: $0.0015/1K input, $0.002/1K output)
            input_cost = (usage.prompt_tokens / 1000) * 0.0015
            output_cost = (usage.completion_tokens / 1000) * 0.002
            call_cost = input_cost + output_cost
            self.token_costs += call_cost
            
            self.logger.debug(f"API call: {usage.prompt_tokens} input + {usage.completion_tokens} output = {usage.total_tokens} total tokens, ${call_cost:.4f}")
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response
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
                        'method': 'AI_LLM',
                        'tokens_used': usage.total_tokens,
                        'cost': call_cost
                    }
            
        except json.JSONDecodeError as e:
            self.logger.debug(f"JSON parse error for {url}: {e}")
        except Exception as e:
            self.logger.debug(f"AI extraction failed for {url}: {e}")
        
        return None
    
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
    
    def traditional_extract(self, soup, url):
        """Traditional CSS selector extraction (no tokens used)"""
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
                'method': 'Traditional_CSS',
                'tokens_used': 0,
                'cost': 0.0
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
            
            # Try AI extraction first (uses tokens)
            ai_result = self.ai_extract(response.text, url)
            if ai_result:
                self.ai_successes += 1
                return {
                    **ai_result,
                    'url': url,
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Fallback to traditional extraction (no tokens)
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
    
    def scrape_site(self, sitemap_url, site_name, max_pages=50, token_budget=None):
        """Scrape a cashback site with token budget control"""
        self.logger.info(f"🚀 Starting {site_name} scraper...")
        if token_budget:
            estimated_cost = (token_budget / 1000) * 0.0035  # Rough estimate
            self.logger.info(f"💰 Token budget: {token_budget} tokens (~${estimated_cost:.3f})")
        
        # Get URLs
        urls = self.fetch_sitemap_urls(sitemap_url)
        if not urls:
            return []
        
        # Filter URLs if needed
        if 'cashrewards' in site_name.lower():
            urls = [url for url in urls if '/store/' in url]
        
        # Limit number of pages
        urls = urls[:max_pages]
        
        offers = []
        tokens_used_this_session = 0
        
        self.logger.info(f"Scraping {len(urls)} pages...")
        
        for i, url in enumerate(urls, 1):
            # Check token budget
            if token_budget and tokens_used_this_session >= token_budget:
                self.logger.warning(f"⚠️ Token budget reached ({tokens_used_this_session}/{token_budget}). Stopping.")
                break
            
            self.logger.info(f"Scraping {i}/{len(urls)}: {url}")
            
            result = self.scrape_page(url)
            if result:
                offers.append(result)
                tokens_used = result.get('tokens_used', 0)
                tokens_used_this_session += tokens_used
                cost = result.get('cost', 0)
                
                self.logger.info(f"✅ {result['method']}: {result['merchant']} - {result['cashback_offer']} "
                               f"[{tokens_used} tokens, ${cost:.4f}]")
            
            # Rate limiting
            time.sleep(1)
            
            # Show progress every 10 pages
            if i % 10 == 0:
                avg_tokens = tokens_used_this_session / i if i > 0 else 0
                self.logger.info(f"Progress: {i}/{len(urls)} pages, {len(offers)} offers, "
                               f"{tokens_used_this_session} tokens used (avg: {avg_tokens:.1f}/page)")
        
        self.logger.info(f"🎉 {site_name} scraping complete! Found {len(offers)} offers")
        self.logger.info(f"💰 Session tokens used: {tokens_used_this_session}")
        
        return offers
    
    def save_results(self, offers, filename_prefix):
        """Save results to CSV and JSON with token information"""
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
        
        # Save token usage summary
        token_summary = {
            'total_offers': len(offers),
            'total_tokens_used': self.total_tokens_used,
            'total_api_calls': self.total_api_calls,
            'total_cost': self.token_costs,
            'average_tokens_per_call': self.total_tokens_used / max(self.total_api_calls, 1),
            'average_cost_per_offer': self.token_costs / len(offers),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        summary_file = f"{filename_prefix}_token_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(token_summary, f, indent=2)
        
        self.logger.info(f"💾 Results saved to {csv_file}, {json_file}, and {summary_file}")
        self.logger.info(f"💰 Total cost: ${self.token_costs:.4f} ({self.total_tokens_used} tokens)")
    
    def get_stats(self):
        """Get scraping statistics including token usage"""
        if self.total_attempts == 0:
            return "No scraping attempts yet"
        
        ai_rate = (self.ai_successes / self.total_attempts) * 100
        traditional_rate = (self.traditional_successes / self.total_attempts) * 100
        overall_rate = ((self.ai_successes + self.traditional_successes) / self.total_attempts) * 100
        
        return {
            'total_attempts': self.total_attempts,
            'ai_successes': self.ai_successes,
            'traditional_successes': self.traditional_successes,
            'ai_success_rate': f"{ai_rate:.1f}%",
            'traditional_success_rate': f"{traditional_rate:.1f}%",
            'overall_success_rate': f"{overall_rate:.1f}%",
            'total_tokens_used': self.total_tokens_used,
            'total_api_calls': self.total_api_calls,
            'total_cost': f"${self.token_costs:.4f}",
            'average_tokens_per_call': f"{self.total_tokens_used / max(self.total_api_calls, 1):.1f}",
            'cost_per_successful_extraction': f"${self.token_costs / max(self.ai_successes, 1):.4f}"
        }

def main():
    """Main scraping function with token budget options"""
    print("🚀 Token-Optimized AI Scraper - Production Run")
    print("=" * 50)
    
    # Create scraper
    scraper = TokenOptimizedAIScraper()
    
    # Token budget options
    print("\n💰 Choose token budget:")
    print("1. Small budget (1,000 tokens - ~$0.004)")
    print("2. Medium budget (5,000 tokens - ~$0.018)")
    print("3. Large budget (10,000 tokens - ~$0.035)")
    print("4. No budget limit")
    
    budget_choice = input("\nEnter budget choice (1-4): ").strip()
    
    token_budgets = {
        "1": 1000,
        "2": 5000, 
        "3": 10000,
        "4": None
    }
    
    token_budget = token_budgets.get(budget_choice, 1000)
    
    if token_budget:
        estimated_cost = (token_budget / 1000) * 0.0035
        print(f"📊 Selected budget: {token_budget} tokens (~${estimated_cost:.4f})")
    else:
        print("📊 No token budget limit set")
    
    # Choose what to scrape
    print("\n🎯 Choose scraping target:")
    print("1. ShopBack Australia (demo)")
    print("2. CashRewards Australia (demo)")
    print("3. Both sites")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        offers = scraper.scrape_site(
            "https://www.shopback.com.au/sitemap.xml",
            "ShopBack",
            max_pages=20,
            token_budget=token_budget
        )
        scraper.save_results(offers, "token_shopback_offers")
        
    elif choice == "2":
        offers = scraper.scrape_site(
            "https://www.cashrewards.com.au/en/sitemap.xml",
            "CashRewards",
            max_pages=20,
            token_budget=token_budget
        )
        scraper.save_results(offers, "token_cashrewards_offers")
        
    elif choice == "3":
        # Split budget between both sites
        site_budget = token_budget // 2 if token_budget else None
        
        shopback_offers = scraper.scrape_site(
            "https://www.shopback.com.au/sitemap.xml",
            "ShopBack",
            max_pages=15,
            token_budget=site_budget
        )
        
        cashrewards_offers = scraper.scrape_site(
            "https://www.cashrewards.com.au/en/sitemap.xml",
            "CashRewards", 
            max_pages=15,
            token_budget=site_budget
        )
        
        # Save individual results
        scraper.save_results(shopback_offers, "token_shopback_offers")
        scraper.save_results(cashrewards_offers, "token_cashrewards_offers")
        
        # Combine and save
        all_offers = shopback_offers + cashrewards_offers
        scraper.save_results(all_offers, "token_combined_offers")
        
    elif choice == "4":
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice")
        return
    
    # Show statistics
    stats = scraper.get_stats()
    print(f"\n📊 Final Statistics:")
    print(f"   Total attempts: {stats['total_attempts']}")
    print(f"   AI success rate: {stats['ai_success_rate']}")
    print(f"   Traditional success rate: {stats['traditional_success_rate']}")
    print(f"   Overall success rate: {stats['overall_success_rate']}")
    print(f"   Total tokens used: {stats['total_tokens_used']}")
    print(f"   Total API calls: {stats['total_api_calls']}")
    print(f"   Total cost: {stats['total_cost']}")
    print(f"   Average tokens per call: {stats['average_tokens_per_call']}")
    print(f"   Cost per successful AI extraction: {stats['cost_per_successful_extraction']}")
    
    print(f"\n🎉 Scraping complete! Check the output files for results and token usage details.")

if __name__ == "__main__":
    main()
