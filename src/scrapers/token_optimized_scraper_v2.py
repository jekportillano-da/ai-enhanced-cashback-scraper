#!/usr/bin/env python3
"""
Token-Optimized AI Scraper with Intelligence Levels
===================================================

Enhanced version with multiple intelligence levels:
- Basic: Simple cashback extraction (GPT-3.5-turbo)
- Standard: Business insights and recommendations (GPT-3.5-turbo)
- Comprehensive: Full business intelligence analysis (GPT-4o)

The comprehensive level automatically uses GPT-4o for superior analysis quality.
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
        
        # Error tracking for monitoring
        self.error_stats = {
            'skipped_urls': 0,
            'filtered_urls': 0,
            '404_errors': 0,
            '403_errors': 0,
            '500_errors': 0,
            'timeout_errors': 0,
            'connection_errors': 0,
            'successful_extractions': 0,
            'failed_extractions': 0
        }
        
        # Intelligence levels configuration with model flexibility
        self.intelligence_levels = {
            "basic": {
                "max_tokens": 150,
                "temperature": 0.1,
                "analysis_depth": "simple"
            },
            "standard": {
                "max_tokens": 500,
                "temperature": 0.2,
                "analysis_depth": "moderate"
            },
            "comprehensive": {
                "max_tokens": 2000,
                "temperature": 0.15,
                "analysis_depth": "detailed"
            }
        }
        
        # Model pricing configuration
        self.model_pricing = {
            "gpt-3.5-turbo": {
                "input_cost_per_1k": 0.0015,
                "output_cost_per_1k": 0.002,
                "name": "GPT-3.5 Turbo"
            },
            "gpt-4o": {
                "input_cost_per_1k": 0.005,
                "output_cost_per_1k": 0.015,
                "name": "GPT-4o"
            }
        }
        
        # Combined cost estimates (level + model combinations)
        self.cost_estimates = {
            ("basic", "gpt-3.5-turbo"): 0.0008,
            ("basic", "gpt-4o"): 0.008,
            ("standard", "gpt-3.5-turbo"): 0.0015,
            ("standard", "gpt-4o"): 0.012,
            ("comprehensive", "gpt-3.5-turbo"): 0.0035,
            ("comprehensive", "gpt-4o"): 0.015
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
    
    def get_cost_estimate(self, intelligence_level, model_name):
        """Get cost estimate for intelligence level + model combination"""
        return self.cost_estimates.get((intelligence_level, model_name), 0.001)
    
    def get_available_models(self):
        """Get list of available AI models"""
        return list(self.model_pricing.keys())
    
    def get_model_info(self, model_name):
        """Get model information including pricing"""
        return self.model_pricing.get(model_name, self.model_pricing["gpt-3.5-turbo"])
    
    def calculate_dynamic_cost(self, intelligence_level, model_name, input_tokens, output_tokens):
        """Calculate actual cost based on token usage"""
        model_info = self.get_model_info(model_name)
        input_cost = (input_tokens * model_info["input_cost_per_1k"]) / 1000
        output_cost = (output_tokens * model_info["output_cost_per_1k"]) / 1000
        return input_cost + output_cost
    
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
    
    def ai_extract(self, html_content, url, intelligence_level="standard", model_name="gpt-3.5-turbo"):
        """Use AI to extract merchant data with intelligence levels and model selection"""
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
            
            # Use the selected model
            model_info = self.get_model_info(model_name)
            self.logger.info(f"AI extraction ({intelligence_level}) - Using {model_info['name']} - Input tokens: {total_input_tokens}")
            
            # Make API call with selected model and intelligence level settings
            response = self.openai_client.chat.completions.create(
                model=model_name,
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
            
            # Calculate cost using dynamic pricing
            cost = self.calculate_dynamic_cost(intelligence_level, model_name, usage.prompt_tokens, usage.completion_tokens)
            
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
    
    def validate_url_batch(self, urls, max_workers=10):
        """Quickly validate URLs in parallel to filter out broken ones before scraping"""
        valid_urls = []
        
        def check_url(url):
            """Quick check if URL is accessible"""
            try:
                # Use HEAD request for faster checking
                response = self.session.head(url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    return url
            except:
                pass
            return None
        
        self.logger.info(f"🔍 Pre-validating {len(urls)} URLs to filter out broken ones...")
        
        # Use ThreadPoolExecutor for parallel validation
        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(check_url, url): url for url in urls}
            
            for i, future in enumerate(as_completed(future_to_url), 1):
                if i % 50 == 0 or i == len(urls):
                    self.logger.info(f"   Validated {i}/{len(urls)} URLs...")
                    
                result = future.result()
                if result:
                    valid_urls.append(result)
        
        self.logger.info(f"✅ Found {len(valid_urls)}/{len(urls)} valid URLs ({(len(valid_urls)/len(urls)*100):.1f}% success rate)")
        return valid_urls

    def should_skip_url(self, url):
        """Check if URL should be skipped based on patterns that commonly fail"""
        skip_patterns = [
            '/notfound',
            '/error',
            '/404',
            '/maintenance',
            '.xml',
            '.css',
            '.js',
            '.pdf',
            '.jpg',
            '.png',
            '.gif',
            '/api/',
            '/admin/',
            '/login',
            '/logout',
            '/search?',
            '/category/',
            '/tag/',
            '/page/',
            'javascript:',
            'mailto:',
            'tel:',
            '#'
        ]
        
        url_lower = url.lower()
        
        # Check for skip patterns
        for pattern in skip_patterns:
            if pattern in url_lower:
                return True
        
        # Skip URLs that are too long (often dynamic/problematic)
        if len(url) > 200:
            return True
            
        # Skip URLs with too many query parameters
        if url.count('?') > 1 or url.count('&') > 5:
            return True
            
        return False
    
    def scrape_page(self, url, intelligence_level="standard", model_name="gpt-3.5-turbo", max_retries=2):
        """Scrape a single page with specified intelligence level and model"""
        
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    self.logger.info(f"Retry {attempt}/{max_retries} for {url}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.info(f"Scraping ({intelligence_level}): {url}")
                
                # Get the response but don't raise on HTTP errors yet
                response = self.session.get(url, timeout=30)
                
                # Check for common errors that should skip AI processing
                if response.status_code == 404:
                    self.logger.warning(f"⚠️ Page not found (404): {url} - Skipping AI analysis")
                    self.error_stats['404_errors'] += 1
                    return None
                elif response.status_code == 403:
                    self.logger.warning(f"⚠️ Access forbidden (403): {url} - Skipping AI analysis")
                    self.error_stats['403_errors'] += 1
                    return None
                elif response.status_code == 500:
                    self.logger.warning(f"⚠️ Server error (500): {url} - Retrying..." if attempt < max_retries else f"⚠️ Server error (500): {url} - Skipping after retries")
                    self.error_stats['500_errors'] += 1
                    if attempt < max_retries:
                        continue
                    return None
                elif response.status_code == 429:
                    self.logger.warning(f"⚠️ Rate limited (429): {url} - Retrying..." if attempt < max_retries else f"⚠️ Rate limited (429): {url} - Skipping after retries")
                    if attempt < max_retries:
                        time.sleep(5)  # Extra delay for rate limiting
                        continue
                    return None
                elif response.status_code != 200:
                    self.logger.warning(f"⚠️ HTTP {response.status_code}: {url} - Skipping AI analysis")
                    return None
                
                # Check if response has meaningful content
                if len(response.text.strip()) < 100:
                    self.logger.warning(f"⚠️ Response too short ({len(response.text)} chars): {url} - Skipping AI analysis")
                    return None
                
                # Check for common error pages in content
                    error_indicators = [
                        '404', 'not found', 'page not found', 'error occurred', 'access denied',
                        'store unavailable', 'not available', 'no longer available', 'currently unavailable',
                        'this store is not available', 'store not found', 'shop unavailable', 'shop not found',
                        'no longer exists', 'no longer active', 'inactive store', 'inactive shop', 'closed store', 'closed shop'
                    ]
                    content_lower = response.text.lower()
                    if any(indicator in content_lower for indicator in error_indicators):
                        self.logger.warning(f"⚠️ Error page detected: {url} - Skipping AI analysis")
                        return None
                
                # Only call AI if we have valid content
                result = self.ai_extract(response.text, url, intelligence_level, model_name)
                
                if result:
                    merchant = result.get('merchant') or result.get('basic_info', {}).get('merchant_name', 'Unknown')
                    tokens = result.get('tokens_used') or result.get('extraction_metadata', {}).get('tokens_used', 0)
                    cost = result.get('cost') or result.get('extraction_metadata', {}).get('cost', 0)
                    
                    self.error_stats['successful_extractions'] += 1
                    self.logger.info(f"✅ {intelligence_level.title()}: {merchant} [{tokens} tokens, ${cost:.4f}]")
                    return result
                else:
                    self.error_stats['failed_extractions'] += 1
                    self.logger.warning(f"⚠️ No data extracted from {url}")
                    return None
                    
            except requests.exceptions.Timeout:
                self.error_stats['timeout_errors'] += 1
                self.logger.warning(f"⚠️ Timeout accessing {url}" + (" - Retrying..." if attempt < max_retries else " - Skipping after retries"))
                if attempt >= max_retries:
                    return None
                continue
            except requests.exceptions.ConnectionError:
                self.error_stats['connection_errors'] += 1
                self.logger.warning(f"⚠️ Connection error accessing {url}" + (" - Retrying..." if attempt < max_retries else " - Skipping after retries"))
                if attempt >= max_retries:
                    return None
                continue
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"⚠️ Request error accessing {url}: {e}" + (" - Retrying..." if attempt < max_retries else " - Skipping after retries"))
                if attempt >= max_retries:
                    return None
                continue
            except Exception as e:
                self.logger.error(f"❌ Unexpected error scraping {url}: {e}")
                return None
        
        return None
    
    def scrape_with_intelligence_level(self, site_name, intelligence_level="standard", model_name="gpt-3.5-turbo", max_pages=10, token_budget=None, retailer_list=None):
        """Scrape with specified intelligence level, model, and budget control"""
        
        # Get cost estimate for the level+model combination
        estimated_cost_per_page = self.get_cost_estimate(intelligence_level, model_name)
        
        if token_budget:
            estimated_pages = int(token_budget / (estimated_cost_per_page * 1000))  # Convert to token count
            max_pages = min(max_pages, estimated_pages)
            model_info = self.get_model_info(model_name)
            self.logger.info(f"🎯 Intelligence Level: {intelligence_level.title()}")
            self.logger.info(f"🤖 AI Model: {model_info['name']}")
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

            # If retailer_list is provided, filter store_urls to only those matching retailer names
            if retailer_list:
                print(f"[DEBUG] Target retailer_list: {retailer_list}")
                from services.retailer_matcher import match_retailer
                url_retailer_names = [url.split('/store/')[-1].replace('-', ' ').replace('_', ' ').split('/')[0] for url in store_urls]
                print(f"[DEBUG] Extracted url_retailer_names: {url_retailer_names}")
                matches = match_retailer(retailer_list, url_retailer_names, cutoff=0.6)
                print(f"[DEBUG] Fuzzy matches: {matches}")
                matched_urls = [url for url, name in zip(store_urls, url_retailer_names) if name in matches.values()]
                self.logger.info(f"Filtered to {len(matched_urls)} URLs matching top retailers")
                if not matched_urls:
                    print("[DEBUG] No matched URLs found for top retailers. Falling back to all store URLs.")
                    all_candidate_urls = store_urls
                else:
                    all_candidate_urls = matched_urls
            else:
                # Use all available URLs - prioritize store URLs but include all for backup
                all_candidate_urls = store_urls + [url for url in urls if url not in store_urls]

            # First pass: filter out obviously bad URLs
            filtered_urls = [url for url in all_candidate_urls if not self.should_skip_url(url)]
            self.logger.info(f"📋 After pattern filtering: {len(filtered_urls)} candidate URLs")

            # Second pass: validate URLs are actually accessible
            selected_urls = self.validate_url_batch(filtered_urls)

            self.logger.info(f"🎯 Ready to scrape {len(selected_urls)} validated URLs (will continue until {max_pages} successful results)")

        except Exception as e:
            self.logger.error(f"Error fetching sitemap: {e}")
            return []
        
        # Scrape pages until we get target number of results
        results = []
        tokens_used_session = 0
        processed_urls = 0
        target_results = max_pages
        
        self.logger.info(f"🎯 Target: {target_results} successful extractions with {intelligence_level} intelligence...")
        self.logger.info(f"📝 Will process up to {len(selected_urls)} URLs until target is reached")
        
        for url in selected_urls:
            # Check if we've reached our target
            if len(results) >= target_results:
                self.logger.info(f"🎯 Target reached! Got {len(results)}/{target_results} successful extractions")
                break
            
            # Check budget
            if token_budget and tokens_used_session >= token_budget:
                self.logger.warning(f"⚠️ Token budget reached ({tokens_used_session}/{token_budget}). Stopping with {len(results)}/{target_results} results.")
                break
            
            processed_urls += 1
            
            self.logger.info(f"Scraping ({len(results)}/{target_results}): {url}")
            result = self.scrape_page(url, intelligence_level, model_name)
            
            if result:
                results.append(result)
                
                # Track tokens for budget
                page_tokens = result.get('tokens_used') or result.get('extraction_metadata', {}).get('tokens_used', 0)
                tokens_used_session += page_tokens
                
                # Brief pause between requests
                time.sleep(1)
        
        # Check if we reached target or ran out of URLs
        if len(results) >= target_results:
            self.logger.info(f"✅ {site_name} scraping complete! Successfully reached target: {len(results)}/{target_results} results")
        elif processed_urls >= len(selected_urls):
            self.logger.warning(f"⚠️ {site_name} scraping complete but target not reached. Got {len(results)}/{target_results} results after processing all {processed_urls} available URLs")
        else:
            self.logger.info(f"🎉 {site_name} scraping stopped. Found {len(results)}/{target_results} results after processing {processed_urls} URLs")
            
        # Show efficiency stats
        if processed_urls > 0:
            success_rate = (len(results) / processed_urls) * 100
            self.logger.info(f"📈 Processing efficiency: {success_rate:.1f}% ({len(results)} successes out of {processed_urls} attempts)")
        
        self.logger.info(f"💰 Session tokens used: {tokens_used_session}")
        
        # Display error statistics
        self.display_error_stats(target_results, processed_urls)
        
        return results
    
    def display_error_stats(self, target_results=None, processed_urls=None):
        """Display error statistics for monitoring"""
        stats = self.error_stats
        total_errors = sum([stats['filtered_urls'], stats['404_errors'], stats['403_errors'], 
                           stats['500_errors'], stats['timeout_errors'], stats['connection_errors']])
        
        if processed_urls and processed_urls > 0:
            self.logger.info("📊 Scraping Efficiency:")
            self.logger.info(f"   🎯 Target results: {target_results}")
            self.logger.info(f"   ✅ Successful extractions: {stats['successful_extractions']}")
            self.logger.info(f"   📄 URLs processed: {processed_urls}")
            self.logger.info(f"   ⚠️ Total errors skipped: {total_errors}")
            
            if target_results:
                completion_rate = (stats['successful_extractions'] / target_results) * 100
                self.logger.info(f"   📈 Target completion: {completion_rate:.1f}%")
            
            if processed_urls > 0:
                efficiency = (stats['successful_extractions'] / processed_urls) * 100
                self.logger.info(f"   ⚡ Processing efficiency: {efficiency:.1f}%")
            
            self.logger.info("📊 Error Breakdown:")
            if stats['filtered_urls'] > 0:
                self.logger.info(f"   ⏭️ Filtered URLs: {stats['filtered_urls']}")
            if stats['404_errors'] > 0:
                self.logger.info(f"   🚫 404 errors: {stats['404_errors']}")
            if stats['403_errors'] > 0:
                self.logger.info(f"   🔒 403 errors: {stats['403_errors']}")
            if stats['500_errors'] > 0:
                self.logger.info(f"   ⚠️ 500 errors: {stats['500_errors']}")
            if stats['timeout_errors'] > 0:
                self.logger.info(f"   ⏰ Timeout errors: {stats['timeout_errors']}")
            if stats['connection_errors'] > 0:
                self.logger.info(f"   🔌 Connection errors: {stats['connection_errors']}")
            if stats['failed_extractions'] > 0:
                self.logger.info(f"   ❌ Failed extractions: {stats['failed_extractions']}")
    
    def save_intelligence_results(self, results, site_name, intelligence_level, retailer_scores=None):
        """Save results to CSV or JSON based on intelligence level"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        if intelligence_level == "comprehensive":
            csv_file = os.path.join(data_dir, f"{site_name}_comprehensive_{timestamp}.csv")
            json_file = os.path.join(data_dir, f"{site_name}_comprehensive_{timestamp}.json")
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
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
                    writer.writerow(self.flatten_comprehensive_competitive_data(result))
        
        else:  # comprehensive - NOW SAVES AS CSV TOO!
            # Create comprehensive CSV with flattened competitive intelligence data
            data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
            os.makedirs(data_dir, exist_ok=True)
            csv_file = os.path.join(data_dir, f"{site_name}_{intelligence_level}_{timestamp}.csv")
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
        summary_file = os.path.join(data_dir, f"{site_name}_{intelligence_level}_summary_{timestamp}.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(cost_summary, f, indent=2)

        self.logger.info(f"💾 Results saved:")
        if intelligence_level == "comprehensive":
            self.logger.info(f"   📊 CSV Data: {csv_file}")
            self.logger.info(f"   📄 JSON Backup: {json_file}")
        else:
            csv_file = os.path.join(data_dir, f"{site_name}_{intelligence_level}_{timestamp}.csv")
            json_file = os.path.join(data_dir, f"{site_name}_{intelligence_level}_{timestamp}.json")
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
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
                    writer.writerow(self.flatten_comprehensive_competitive_data(result))
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
