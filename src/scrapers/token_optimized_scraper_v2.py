#!/usr/bin/env python3
"""
Token-Optimized AI Scraper with Intelligence Levels
===================================================

Enhanced version with multiple intelligence levels:
- Basic: Simple cashback extraction
- Standard: Business insights and recommendations  
- Comprehensive: Full business intelligence analysis
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
from datetime import datetime

# Load environment variables
load_dotenv()

class TokenOptimizedAIScraper:
    """AI-enhanced scraper with intelligent token management and multiple intelligence levels"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.setup_logging()
        self.model_name = "gpt-3.5-turbo"
        self.openai_client = None
        self.tokenizer = None
        self.setup_ai()
        
        # Token tracking
        self.total_tokens_used = 0
        self.total_api_calls = 0
        self.token_costs = 0.0
        self.max_input_tokens = 3000
        
        # Intelligence levels configuration
        self.intelligence_levels = {
            "basic": {
                "max_tokens": 150,
                "temperature": 0.1,
                "analysis_depth": "simple",
                "estimated_cost_per_call": 0.0008
            },
            "standard": {
                "max_tokens": 500,
                "temperature": 0.2,
                "analysis_depth": "moderate",
                "estimated_cost_per_call": 0.0015
            },
            "comprehensive": {
                "max_tokens": 1500,
                "temperature": 0.2,
                "analysis_depth": "detailed",
                "estimated_cost_per_call": 0.0035
            }
        }
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/token_scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_ai(self):
        """Initialize AI components"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                self.logger.warning("No OpenAI API key found. AI features disabled.")
                return
            
            self.openai_client = openai.OpenAI(api_key=api_key)
            self.tokenizer = tiktoken.encoding_for_model(self.model_name)
            self.logger.info("AI components initialized successfully")
            
        except Exception as e:
            self.logger.warning(f"AI setup failed: {e}")
    
    def count_tokens(self, text):
        """Count tokens in text"""
        if not self.tokenizer:
            return len(text.split()) * 1.3
        return len(self.tokenizer.encode(text))
    
    def optimize_content_for_tokens(self, html_content, url):
        """Optimize HTML content to minimize tokens while preserving important info"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unnecessary elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        relevant_sections = []
        
        # 1. Look for cashback-related keywords in various elements
        cashback_keywords = ['cashback', 'cash back', 'reward', 'earn', '%', 'discount', 'offer', 'deal']
        
        for keyword in cashback_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements[:2]:  # Limit to first 2 matches per keyword
                parent = element.parent
                if parent and parent.name not in ['script', 'style']:
                    text = parent.get_text().strip()
                    if text and len(text) < 200:  # Keep sections under 200 chars
                        relevant_sections.append(text)
        
        # 2. Get title and main content
        title = soup.find('title')
        if title:
            relevant_sections.insert(0, f"TITLE: {title.get_text().strip()}")
        
        # 3. Look for percentage and dollar amounts
        all_text = soup.get_text()
        percentage_matches = re.findall(r'[^.]*\d+\.?\d*%[^.]*', all_text)
        for match in percentage_matches[:3]:
            relevant_sections.append(f"RATE: {match.strip()}")
        
        # Combine and optimize
        optimized_content = "\n".join(relevant_sections[:12])  # Limit sections
        
        # Trim if too long
        token_count = self.count_tokens(optimized_content)
        if token_count > self.max_input_tokens:
            words = optimized_content.split()
            max_words = int(self.max_input_tokens * 0.75)
            optimized_content = " ".join(words[:max_words])
        
        return optimized_content, self.count_tokens(optimized_content)
    
    def create_optimized_prompt(self, content, url, intelligence_level="standard"):
        """Create a token-optimized prompt based on intelligence level with competitive analysis context"""
        
        # Add competitive context for Pokitpal
        competitive_context = """
CONTEXT: This analysis is for Pokitpal, a cashback/rewards platform. Analyze these competitor cashback merchants to understand:
- How they position their offers vs Pokitpal's potential offerings
- Market gaps Pokitpal could exploit
- Competitive threats and opportunities
- Strategic recommendations for Pokitpal's competitive positioning
"""
        
        if intelligence_level == "basic":
            prompt = f"""{competitive_context}

Extract competitor cashback data from this webpage content.

URL: {url}
Content: {content}

Return only JSON:
{{"merchant_name": "name or null", "cashback_offer": "offer or null", "confidence": 0.9, "competitive_threat": "high|medium|low"}}"""
        
        elif intelligence_level == "standard":
            prompt = f"""{competitive_context}

Analyze this competitor cashback merchant page for Pokitpal's strategic planning.

URL: {url}
Content: {content}

Return JSON with competitive intelligence:
{{"basic_info": {{"merchant_name": "name", "cashback_offer": "rate", "offer_type": "percentage|fixed"}}, 
"competitive_intelligence": {{"threat_level": "high|medium|low", "market_position": "premium|mid_market|budget", "pokitpal_opportunity": "high|medium|low"}},
"user_experience": {{"ease_of_use": "excellent|good|average|poor", "mobile_optimized": true|false}},
"pokitpal_recommendations": ["competitive_rec1", "competitive_rec2"],
"confidence": 0.9}}"""
        
        else:  # comprehensive
            prompt = f"""{competitive_context}

Provide comprehensive competitive intelligence analysis of this cashback merchant for Pokitpal's strategic advantage.

URL: {url}
Content: {content}

Return detailed competitive analysis JSON:
{{"basic_info": {{"merchant_name": "name", "cashback_offer": "rate", "offer_type": "type"}},
"competitive_positioning": {{"market_position": "position", "unique_selling_points": ["point1"], "competitive_advantages": ["adv1"], "weaknesses_pokitpal_can_exploit": ["weakness1"]}},
"offer_intelligence": {{"offer_attractiveness": "level", "offer_complexity": "level", "pokitpal_differentiation_opportunity": "high|medium|low", "special_conditions": ["cond1"], "exclusions": ["excl1"]}},
"user_experience": {{"ease_of_use": "level", "signup_process": "complexity", "payment_methods": ["method1"], "mobile_optimized": true|false, "pokitpal_ux_advantages": ["advantage1"]}},
"strategic_insights": {{"threat_to_pokitpal": "level", "partnership_opportunity": "level", "market_share_vulnerability": "level", "customer_acquisition_difficulty": "level"}},
"pokitpal_strategic_recommendations": ["detailed_competitive_rec1", "detailed_market_entry_rec2", "detailed_differentiation_rec3"],
"competitive_summary": {{"overall_threat_level": "high|medium|low", "pokitpal_response_priority": "urgent|high|medium|low", "recommended_pokitpal_strategy": "compete_directly|differentiate|avoid|partner"}},
"data_quality": {{"extraction_confidence": 0.9, "data_completeness": 0.8, "analysis_reliability": 0.85}}}}"""
        
        return prompt
    
    def ai_extract(self, html_content, url, intelligence_level="standard"):
        """Use AI to extract merchant data with intelligence levels"""
        if not self.openai_client:
            return None
        
        try:
            # Get intelligence level config
            level_config = self.intelligence_levels.get(intelligence_level, self.intelligence_levels["standard"])
            
            # Optimize content for token efficiency
            optimized_content, input_tokens = self.optimize_content_for_tokens(html_content, url)
            
            # Create prompt based on intelligence level
            prompt = self.create_optimized_prompt(optimized_content, url, intelligence_level)
            
            # Create system message based on intelligence level
            if intelligence_level == "basic":
                system_message = "You are a competitive intelligence analyst for Pokitpal (a cashback platform). Extract competitor data and assess competitive threats. Return only valid JSON."
            elif intelligence_level == "standard":
                system_message = "You are a competitive intelligence analyst for Pokitpal. Analyze competitor cashback platforms to identify threats, opportunities, and strategic recommendations for Pokitpal's competitive advantage."
            else:  # comprehensive
                system_message = "You are a senior competitive intelligence analyst for Pokitpal, a cashback/rewards platform. Provide detailed competitive analysis to help Pokitpal strategically position against competitors, identify market gaps, and develop winning strategies."
            
            # Count total input tokens
            total_input_tokens = self.count_tokens(system_message + prompt)
            
            self.logger.info(f"AI extraction ({intelligence_level}) - Input tokens: {total_input_tokens}")
            
            # Make API call with intelligence level settings
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=level_config["temperature"],
                max_tokens=level_config["max_tokens"]
            )
            
            # Track usage
            usage = response.usage
            total_tokens = usage.total_tokens
            cost = (usage.prompt_tokens * 0.0015 + usage.completion_tokens * 0.002) / 1000
            
            self.total_tokens_used += total_tokens
            self.total_api_calls += 1
            self.token_costs += cost
            
            # Parse response based on intelligence level
            ai_content = response.choices[0].message.content.strip()
            
            if intelligence_level == "basic":
                result = self.parse_basic_response(ai_content, url, total_tokens, cost)
            elif intelligence_level == "standard":
                result = self.parse_standard_response(ai_content, url, total_tokens, cost)
            else:  # comprehensive
                result = self.parse_comprehensive_response(ai_content, url, total_tokens, cost)
            
            return result
            
        except Exception as e:
            self.logger.error(f"AI extraction failed: {e}")
            return None
    
    def parse_basic_response(self, ai_content, url, tokens_used, cost):
        """Parse basic AI response with competitive context"""
        try:
            json_start = ai_content.find('{')
            json_end = ai_content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = ai_content[json_start:json_end]
                data = json.loads(json_str)
                
                return {
                    "merchant": data.get("merchant_name", "Unknown"),
                    "cashback_offer": data.get("cashback_offer", "Not found"),
                    "competitive_threat": data.get("competitive_threat", "unknown"),
                    "confidence": data.get("confidence", 0.5),
                    "method": "AI_Basic_Competitive",
                    "tokens_used": tokens_used,
                    "cost": cost,
                    "url": url,
                    "scraped_at": datetime.now().isoformat()
                }
        except:
            pass
        
        return {
            "merchant": "Parsing Error",
            "cashback_offer": "Could not extract",
            "competitive_threat": "unknown",
            "confidence": 0.1,
            "method": "AI_Basic_Competitive_Error",
            "tokens_used": tokens_used,
            "cost": cost,
            "url": url,
            "scraped_at": datetime.now().isoformat()
        }
    
    def parse_standard_response(self, ai_content, url, tokens_used, cost):
        """Parse standard intelligence AI response with competitive context"""
        try:
            json_start = ai_content.find('{')
            json_end = ai_content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = ai_content[json_start:json_end]
                data = json.loads(json_str)
                
                basic_info = data.get("basic_info", {})
                competitive_intel = data.get("competitive_intelligence", {})
                user_experience = data.get("user_experience", {})
                recommendations = data.get("pokitpal_recommendations", [])
                
                return {
                    "merchant": basic_info.get("merchant_name", "Unknown"),
                    "cashback_offer": basic_info.get("cashback_offer", "Not found"),
                    "offer_type": basic_info.get("offer_type", "unknown"),
                    "competitive_threat_level": competitive_intel.get("threat_level", "unknown"),
                    "market_position": competitive_intel.get("market_position", "unknown"),
                    "pokitpal_opportunity": competitive_intel.get("pokitpal_opportunity", "unknown"),
                    "ease_of_use": user_experience.get("ease_of_use", "unknown"),
                    "mobile_optimized": user_experience.get("mobile_optimized", None),
                    "pokitpal_strategic_recommendations": recommendations[:2],
                    "confidence": data.get("confidence", 0.7),
                    "method": "AI_Standard_Competitive",
                    "tokens_used": tokens_used,
                    "cost": cost,
                    "url": url,
                    "scraped_at": datetime.now().isoformat()
                }
        except Exception as e:
            self.logger.warning(f"Standard competitive response parsing failed: {e}")
        
        return self.parse_basic_response(ai_content, url, tokens_used, cost)
    
    def parse_comprehensive_response(self, ai_content, url, tokens_used, cost):
        """Parse comprehensive intelligence AI response"""
        try:
            json_start = ai_content.find('{')
            json_end = ai_content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = ai_content[json_start:json_end]
                data = json.loads(json_str)
                
                # Add metadata to the comprehensive analysis
                data['extraction_metadata'] = {
                    'method': 'AI_Comprehensive',
                    'tokens_used': tokens_used,
                    'cost': cost,
                    'url': url,
                    'scraped_at': datetime.now().isoformat(),
                    'intelligence_level': 'comprehensive'
                }
                
                return data
        except Exception as e:
            self.logger.warning(f"Comprehensive response parsing failed: {e}")
        
        return self.parse_standard_response(ai_content, url, tokens_used, cost)
    
    def scrape_page(self, url, intelligence_level="standard"):
        """Scrape a single page with specified intelligence level"""
        try:
            self.logger.info(f"Scraping ({intelligence_level}): {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            result = self.ai_extract(response.text, url, intelligence_level)
            
            if result:
                merchant = result.get('merchant') or result.get('basic_info', {}).get('merchant_name', 'Unknown')
                tokens = result.get('tokens_used') or result.get('extraction_metadata', {}).get('tokens_used', 0)
                cost = result.get('cost') or result.get('extraction_metadata', {}).get('cost', 0)
                
                self.logger.info(f"✅ {intelligence_level.title()}: {merchant} [{tokens} tokens, ${cost:.4f}]")
                return result
            else:
                self.logger.warning(f"No data extracted from {url}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return None
    
    def scrape_with_intelligence_level(self, site_name, intelligence_level="standard", max_pages=10, token_budget=None):
        """Scrape with specified intelligence level and budget control"""
        
        level_config = self.intelligence_levels.get(intelligence_level, self.intelligence_levels["standard"])
        estimated_cost_per_page = level_config["estimated_cost_per_call"]
        
        if token_budget:
            estimated_pages = int(token_budget / (estimated_cost_per_page * 1000))  # Convert to token count
            max_pages = min(max_pages, estimated_pages)
            self.logger.info(f"🎯 Intelligence Level: {intelligence_level.title()}")
            self.logger.info(f"💰 Budget: {token_budget} tokens (~${estimated_cost_per_page * max_pages:.3f})")
            self.logger.info(f"📊 Estimated pages: {max_pages}")
        
        # Get sitemap URLs
        if site_name.lower() == "shopback":
            sitemap_url = "https://www.shopback.com.au/sitemap.xml"
            base_url = "https://www.shopback.com.au"
        elif site_name.lower() == "cashrewards":
            sitemap_url = "https://www.cashrewards.com.au/en/sitemap.xml"
            base_url = "https://www.cashrewards.com.au"
        else:
            self.logger.error(f"Unknown site: {site_name}")
            return []
        
        # Fetch and parse sitemap
        try:
            self.logger.info(f"Fetching sitemap: {sitemap_url}")
            response = self.session.get(sitemap_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            urls = [loc.get_text() for loc in soup.find_all('loc')]
            
            # Filter for store/merchant pages
            store_urls = [url for url in urls if '/store/' in url or any(keyword in url.lower() for keyword in ['shop', 'merchant', 'brand'])]
            
            self.logger.info(f"Found {len(urls)} URLs, {len(store_urls)} store URLs")
            
            # Limit URLs
            selected_urls = store_urls[:max_pages] if store_urls else urls[:max_pages]
            
        except Exception as e:
            self.logger.error(f"Error fetching sitemap: {e}")
            return []
        
        # Scrape pages
        results = []
        tokens_used_session = 0
        
        self.logger.info(f"Scraping {len(selected_urls)} pages with {intelligence_level} intelligence...")
        
        for i, url in enumerate(selected_urls, 1):
            # Check budget
            if token_budget and tokens_used_session >= token_budget:
                self.logger.warning(f"⚠️ Token budget reached ({tokens_used_session}/{token_budget}). Stopping.")
                break
            
            self.logger.info(f"Scraping {i}/{len(selected_urls)}: {url}")
            result = self.scrape_page(url, intelligence_level)
            
            if result:
                results.append(result)
                
                # Track tokens for budget
                page_tokens = result.get('tokens_used') or result.get('extraction_metadata', {}).get('tokens_used', 0)
                tokens_used_session += page_tokens
                
                # Brief pause between requests
                time.sleep(1)
        
        self.logger.info(f"🎉 {site_name} scraping complete! Found {len(results)} offers")
        self.logger.info(f"💰 Session tokens used: {tokens_used_session}")
        
        return results
    
    def save_intelligence_results(self, results, filename_base, intelligence_level):
        """Save results with intelligence level information in appropriate formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if intelligence_level == "basic":
            # Simple CSV for basic results
            csv_file = f"data/{filename_base}_{intelligence_level}_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if results:
                    fieldnames = ['merchant', 'cashback_offer', 'competitive_threat', 'confidence', 'method', 'tokens_used', 'cost', 'url', 'scraped_at']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
        
        elif intelligence_level == "standard":
            # Enhanced CSV for standard results
            csv_file = f"data/{filename_base}_{intelligence_level}_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if results:
                    fieldnames = ['merchant', 'cashback_offer', 'offer_type', 'competitive_threat_level', 'market_position', 'pokitpal_opportunity', 
                                'ease_of_use', 'mobile_optimized', 'pokitpal_strategic_recommendations', 
                                'confidence', 'method', 'tokens_used', 'cost', 'url', 'scraped_at']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in results:
                        # Convert recommendations list to string
                        result_copy = result.copy()
                        if 'pokitpal_strategic_recommendations' in result_copy and isinstance(result_copy['pokitpal_strategic_recommendations'], list):
                            result_copy['pokitpal_strategic_recommendations'] = '; '.join(result_copy['pokitpal_strategic_recommendations'])
                        writer.writerow(result_copy)
        
        else:  # comprehensive - NOW SAVES AS CSV TOO!
            # Create comprehensive CSV with flattened competitive intelligence data
            csv_file = f"data/{filename_base}_{intelligence_level}_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if results:
                    # Define comprehensive fieldnames for competitive intelligence
                    fieldnames = [
                        'merchant_name', 'cashback_offer', 'offer_type',
                        'market_position', 'unique_selling_points', 'competitive_advantages', 'weaknesses_pokitpal_can_exploit',
                        'offer_attractiveness', 'offer_complexity', 'pokitpal_differentiation_opportunity',
                        'special_conditions', 'exclusions',
                        'ease_of_use', 'signup_process', 'payment_methods', 'mobile_optimized', 'pokitpal_ux_advantages',
                        'threat_to_pokitpal', 'partnership_opportunity', 'market_share_vulnerability', 'customer_acquisition_difficulty',
                        'pokitpal_recommendation_1', 'pokitpal_recommendation_2', 'pokitpal_recommendation_3',
                        'overall_threat_level', 'pokitpal_response_priority', 'recommended_pokitpal_strategy',
                        'extraction_confidence', 'data_completeness', 'analysis_reliability',
                        'tokens_used', 'cost', 'url', 'scraped_at'
                    ]
                    
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for result in results:
                        flattened = self.flatten_comprehensive_competitive_data(result)
                        writer.writerow(flattened)
            
            # Also save JSON for backup/detailed analysis
            json_file = f"data/{filename_base}_{intelligence_level}_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Always create a summary
        cost_summary = {
            "analysis_summary": {
                "intelligence_level": intelligence_level,
                "total_results": len(results),
                "total_tokens_used": self.total_tokens_used,
                "total_api_calls": self.total_api_calls,
                "total_cost": round(self.token_costs, 4),
                "average_cost_per_result": round(self.token_costs / len(results), 4) if results else 0,
                "timestamp": timestamp,
                "competitive_analysis_for": "Pokitpal"
            }
        }
        
        summary_file = f"data/{filename_base}_{intelligence_level}_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(cost_summary, f, indent=2)
        
        self.logger.info(f"💾 Results saved:")
        if intelligence_level == "comprehensive":
            self.logger.info(f"   📊 CSV Data: {csv_file}")
            self.logger.info(f"   📄 JSON Backup: {json_file}")
        else:
            self.logger.info(f"   📊 Data: {csv_file}")
        self.logger.info(f"   📈 Summary: {summary_file}")
        self.logger.info(f"   💰 Total cost: ${self.token_costs:.4f}")
    
    def flatten_comprehensive_competitive_data(self, result):
        """Flatten comprehensive competitive intelligence data for CSV export"""
        
        basic_info = result.get('basic_info', {})
        competitive = result.get('competitive_positioning', {})
        offer_intel = result.get('offer_intelligence', {})
        user_exp = result.get('user_experience', {})
        strategic = result.get('strategic_insights', {})
        recommendations = result.get('pokitpal_strategic_recommendations', [])
        summary = result.get('competitive_summary', {})
        data_quality = result.get('data_quality', {})
        metadata = result.get('extraction_metadata', {})
        
        return {
            'merchant_name': basic_info.get('merchant_name', ''),
            'cashback_offer': basic_info.get('cashback_offer', ''),
            'offer_type': basic_info.get('offer_type', ''),
            
            'market_position': competitive.get('market_position', ''),
            'unique_selling_points': '; '.join(competitive.get('unique_selling_points', [])),
            'competitive_advantages': '; '.join(competitive.get('competitive_advantages', [])),
            'weaknesses_pokitpal_can_exploit': '; '.join(competitive.get('weaknesses_pokitpal_can_exploit', [])),
            
            'offer_attractiveness': offer_intel.get('offer_attractiveness', ''),
            'offer_complexity': offer_intel.get('offer_complexity', ''),
            'pokitpal_differentiation_opportunity': offer_intel.get('pokitpal_differentiation_opportunity', ''),
            'special_conditions': '; '.join(offer_intel.get('special_conditions', [])),
            'exclusions': '; '.join(offer_intel.get('exclusions', [])),
            
            'ease_of_use': user_exp.get('ease_of_use', ''),
            'signup_process': user_exp.get('signup_process', ''),
            'payment_methods': '; '.join(user_exp.get('payment_methods', [])),
            'mobile_optimized': user_exp.get('mobile_optimized', ''),
            'pokitpal_ux_advantages': '; '.join(user_exp.get('pokitpal_ux_advantages', [])),
            
            'threat_to_pokitpal': strategic.get('threat_to_pokitpal', ''),
            'partnership_opportunity': strategic.get('partnership_opportunity', ''),
            'market_share_vulnerability': strategic.get('market_share_vulnerability', ''),
            'customer_acquisition_difficulty': strategic.get('customer_acquisition_difficulty', ''),
            
            'pokitpal_recommendation_1': recommendations[0] if len(recommendations) > 0 else '',
            'pokitpal_recommendation_2': recommendations[1] if len(recommendations) > 1 else '',
            'pokitpal_recommendation_3': recommendations[2] if len(recommendations) > 2 else '',
            
            'overall_threat_level': summary.get('overall_threat_level', ''),
            'pokitpal_response_priority': summary.get('pokitpal_response_priority', ''),
            'recommended_pokitpal_strategy': summary.get('recommended_pokitpal_strategy', ''),
            
            'extraction_confidence': data_quality.get('extraction_confidence', ''),
            'data_completeness': data_quality.get('data_completeness', ''),
            'analysis_reliability': data_quality.get('analysis_reliability', ''),
            
            'tokens_used': metadata.get('tokens_used', ''),
            'cost': metadata.get('cost', ''),
            'url': metadata.get('url', ''),
            'scraped_at': metadata.get('scraped_at', '')
        }

def main():
    """Demo function showing intelligence levels"""
    print("🚀 Token-Optimized AI Scraper with Intelligence Levels")
    print("=" * 60)
    
    scraper = TokenOptimizedAIScraper()
    
    print("\n🧠 Choose Intelligence Level:")
    print("1. 🔸 Basic - Simple extraction (~$0.0008/page)")
    print("2. 🔹 Standard - Business insights (~$0.0015/page)")  
    print("3. 🔷 Comprehensive - Full analysis (~$0.0035/page)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    levels = {"1": "basic", "2": "standard", "3": "comprehensive"}
    intelligence_level = levels.get(choice, "standard")
    
    print(f"\n🎯 Selected: {intelligence_level.title()} Intelligence")
    
    # Demo with ShopBack
    results = scraper.scrape_with_intelligence_level(
        site_name="shopback",
        intelligence_level=intelligence_level,
        max_pages=3,
        token_budget=2000
    )
    
    if results:
        scraper.save_intelligence_results(results, f"demo_{intelligence_level}", intelligence_level)
        print(f"\n✅ Demo complete! {len(results)} results saved")
        print(f"💰 Total cost: ${scraper.token_costs:.4f}")
    else:
        print("\n❌ No results obtained")

if __name__ == "__main__":
    main()
