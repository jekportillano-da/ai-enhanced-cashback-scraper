"""
AI-Enhanced Cashback Scraper with Intelligent Agents
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
import openai
from abc import ABC, abstractmethod
import logging
from pathlib import Path
import time
import requests


@dataclass
class ScrapingContext:
    """Context information for AI agents"""
    url: str
    html_content: str
    soup: BeautifulSoup
    previous_attempts: List[Dict] = None
    site_type: str = None
    
    def __post_init__(self):
        if self.previous_attempts is None:
            self.previous_attempts = []


@dataclass
class ExtractionResult:
    """Result from AI extraction"""
    merchant_name: str
    cashback_offer: str
    confidence_score: float
    extraction_method: str
    additional_data: Dict = None
    
    def __post_init__(self):
        if self.additional_data is None:
            self.additional_data = {}


class BaseAIAgent(ABC):
    """Base class for AI agents"""
    
    def __init__(self, name: str, config: Dict = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"AI_Agent_{name}")
        
    @abstractmethod
    def process(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Process the scraping context and return extraction result"""
        pass
    
    def log_attempt(self, context: ScrapingContext, result: Optional[ExtractionResult], method: str):
        """Log extraction attempt for learning"""
        attempt = {
            "timestamp": time.time(),
            "method": method,
            "success": result is not None,
            "confidence": result.confidence_score if result else 0.0,
            "url": context.url
        }
        context.previous_attempts.append(attempt)


class LLMExtractionAgent(BaseAIAgent):
    """AI agent that uses LLM for intelligent data extraction"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        super().__init__("LLM_Extractor")
        self.api_key = api_key
        self.model = model
        if api_key:
            openai.api_key = api_key
    
    def create_extraction_prompt(self, context: ScrapingContext) -> str:
        """Create a prompt for LLM extraction"""
        # Get clean text content from HTML
        clean_text = self._extract_clean_text(context.soup)
        
        prompt = f"""
You are an expert web scraper. Extract cashback/rewards information from this webpage content.

URL: {context.url}

HTML Content (cleaned):
{clean_text[:3000]}  # Limit to avoid token limits

Please extract the following information:
1. Merchant/Store Name
2. Cashback Rate/Offer (percentage, dollar amount, or description)

Return your response as JSON with this exact format:
{{
    "merchant_name": "exact merchant name",
    "cashback_offer": "exact cashback offer text",
    "confidence": 0.95,
    "reasoning": "brief explanation of how you found this information"
}}

Rules:
- If you cannot find clear information, return null for that field
- Confidence should be 0.0 to 1.0 based on how certain you are
- Look for text like "cashback", "cash back", "rewards", "earn", "%", "points"
- Merchant name is usually in headers, titles, or prominent text
- Be precise and extract exact text, don't paraphrase
"""
        return prompt
    
    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """Extract clean, readable text from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def process(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Use LLM to extract data"""
        if not self.api_key:
            self.logger.warning("No OpenAI API key provided, skipping LLM extraction")
            return None
        
        try:
            prompt = self.create_extraction_prompt(context)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert web scraper that extracts cashback information."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                result_data = json.loads(result_text)
                
                if result_data.get("merchant_name") and result_data.get("cashback_offer"):
                    result = ExtractionResult(
                        merchant_name=result_data["merchant_name"],
                        cashback_offer=result_data["cashback_offer"],
                        confidence_score=result_data.get("confidence", 0.8),
                        extraction_method="LLM",
                        additional_data={"reasoning": result_data.get("reasoning", "")}
                    )
                    
                    self.log_attempt(context, result, "LLM")
                    return result
                    
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse LLM response as JSON: {result_text}")
                
        except Exception as e:
            self.logger.error(f"LLM extraction failed: {e}")
        
        self.log_attempt(context, None, "LLM")
        return None


class PatternLearningAgent(BaseAIAgent):
    """AI agent that learns patterns from successful extractions"""
    
    def __init__(self):
        super().__init__("Pattern_Learner")
        self.learned_patterns = self._load_patterns()
        self.success_patterns = []
        
    def _load_patterns(self) -> Dict:
        """Load previously learned patterns"""
        try:
            with open("learned_patterns.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "merchant_selectors": [],
                "cashback_selectors": [],
                "url_patterns": {}
            }
    
    def save_patterns(self):
        """Save learned patterns to file"""
        with open("learned_patterns.json", "w") as f:
            json.dump(self.learned_patterns, f, indent=2)
    
    def learn_from_success(self, context: ScrapingContext, result: ExtractionResult):
        """Learn patterns from successful extraction"""
        if result.confidence_score < 0.7:
            return
        
        # Extract patterns from successful extraction
        patterns = self._extract_patterns(context, result)
        
        # Add to learned patterns
        for pattern in patterns:
            if pattern not in self.learned_patterns["merchant_selectors"]:
                self.learned_patterns["merchant_selectors"].append(pattern)
        
        self.save_patterns()
    
    def _extract_patterns(self, context: ScrapingContext, result: ExtractionResult) -> List[Dict]:
        """Extract CSS/XPath patterns from successful extraction"""
        patterns = []
        
        # Try to find the element containing the merchant name
        merchant_elements = context.soup.find_all(text=re.compile(re.escape(result.merchant_name)))
        
        for element in merchant_elements[:3]:  # Limit to first 3 matches
            if hasattr(element, 'parent'):
                parent = element.parent
                pattern = {
                    "tag": parent.name,
                    "class": parent.get("class", []),
                    "id": parent.get("id", ""),
                    "text_pattern": result.merchant_name
                }
                patterns.append(pattern)
        
        return patterns
    
    def process(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Try extraction using learned patterns"""
        for pattern in self.learned_patterns["merchant_selectors"]:
            try:
                # Try to match the pattern
                elements = self._find_by_pattern(context.soup, pattern)
                
                for element in elements:
                    # Extract potential merchant name and cashback info
                    merchant = self._extract_merchant_from_element(element)
                    cashback = self._find_nearby_cashback(element)
                    
                    if merchant and cashback:
                        result = ExtractionResult(
                            merchant_name=merchant,
                            cashback_offer=cashback,
                            confidence_score=0.7,
                            extraction_method="Pattern_Learning"
                        )
                        
                        self.log_attempt(context, result, "Pattern_Learning")
                        return result
                        
            except Exception as e:
                self.logger.debug(f"Pattern matching failed: {e}")
                continue
        
        self.log_attempt(context, None, "Pattern_Learning")
        return None
    
    def _find_by_pattern(self, soup: BeautifulSoup, pattern: Dict) -> List[Tag]:
        """Find elements matching a learned pattern"""
        kwargs = {}
        
        if pattern.get("class"):
            kwargs["class_"] = pattern["class"]
        if pattern.get("id"):
            kwargs["id"] = pattern["id"]
            
        return soup.find_all(pattern["tag"], **kwargs)
    
    def _extract_merchant_from_element(self, element: Tag) -> Optional[str]:
        """Extract merchant name from element"""
        text = element.get_text().strip()
        if len(text) > 5 and len(text) < 100:  # Reasonable merchant name length
            return text
        return None
    
    def _find_nearby_cashback(self, element: Tag) -> Optional[str]:
        """Find cashback information near the merchant element"""
        # Look in siblings and parent elements
        search_elements = []
        
        if element.parent:
            search_elements.extend(element.parent.find_all())
        
        cashback_patterns = [
            r'\d+\.?\d*%',  # Percentage
            r'\$\d+\.?\d*',  # Dollar amount
            r'\d+\.?\d*\s*points',  # Points
            r'up to \d+',  # Up to X
        ]
        
        for search_element in search_elements[:10]:  # Limit search
            text = search_element.get_text()
            for pattern in cashback_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group()
        
        return None


class AdaptiveSelectorAgent(BaseAIAgent):
    """AI agent that adaptively finds selectors based on content analysis"""
    
    def __init__(self):
        super().__init__("Adaptive_Selector")
        
    def process(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Adaptively find selectors for merchant and cashback data"""
        
        # Find potential merchant name (usually in headers)
        merchant = self._find_merchant_name(context.soup)
        if not merchant:
            return None
            
        # Find potential cashback offer
        cashback = self._find_cashback_offer(context.soup)
        if not cashback:
            cashback = "No Cashback Info"
        
        result = ExtractionResult(
            merchant_name=merchant,
            cashback_offer=cashback,
            confidence_score=0.6,
            extraction_method="Adaptive_Selector"
        )
        
        self.log_attempt(context, result, "Adaptive_Selector")
        return result
    
    def _find_merchant_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Intelligently find merchant name"""
        # Priority order for merchant name search
        selectors = [
            "h1",
            "h2",
            "[data-test*='name']",
            "[data-test*='title']",
            ".merchant-name",
            ".store-name",
            ".title",
            "title"
        ]
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip()
                    if self._is_valid_merchant_name(text):
                        return text
            except:
                continue
                
        return None
    
    def _find_cashback_offer(self, soup: BeautifulSoup) -> Optional[str]:
        """Intelligently find cashback offer"""
        # Look for elements containing cashback keywords
        cashback_keywords = [
            "cashback", "cash back", "earn", "reward", "points", 
            "%", "percentage", "rate", "offer"
        ]
        
        # Find elements with cashback-related classes or data attributes
        selectors = [
            "[class*='cashback']",
            "[class*='rate']",
            "[class*='offer']",
            "[class*='reward']",
            "[data-test*='rate']",
            "[data-test*='cashback']",
            "h2, h3, h4, h5",
            ".percentage",
            ".rate"
        ]
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip()
                    if self._contains_cashback_info(text):
                        return text
            except:
                continue
        
        # Fallback: search all text for cashback patterns
        all_text = soup.get_text()
        patterns = [
            r'\d+\.?\d*%\s*cashback',
            r'earn\s+\d+\.?\d*%',
            r'up\s+to\s+\d+\.?\d*%',
            r'\$\d+\.?\d*\s*cashback'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, all_text, re.IGNORECASE)
            if match:
                return match.group()
        
        return None
    
    def _is_valid_merchant_name(self, text: str) -> bool:
        """Check if text is a valid merchant name"""
        if not text or len(text) < 2 or len(text) > 100:
            return False
        
        # Skip common non-merchant text
        skip_keywords = [
            "home", "shop", "browse", "search", "menu", "cart",
            "login", "sign up", "about", "contact", "help"
        ]
        
        return not any(keyword in text.lower() for keyword in skip_keywords)
    
    def _contains_cashback_info(self, text: str) -> bool:
        """Check if text contains cashback information"""
        if not text:
            return False
        
        cashback_patterns = [
            r'\d+\.?\d*%',
            r'\$\d+',
            r'points',
            r'cashback',
            r'cash back',
            r'earn',
            r'reward'
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in cashback_patterns)


class AIAgentOrchestrator:
    """Orchestrates multiple AI agents for intelligent scraping"""
    
    def __init__(self, openai_api_key: str = None):
        self.agents = [
            LLMExtractionAgent(openai_api_key),
            PatternLearningAgent(),
            AdaptiveSelectorAgent()
        ]
        self.logger = logging.getLogger("AI_Orchestrator")
        
    def extract_data(self, url: str, html_content: str, soup: BeautifulSoup) -> Optional[ExtractionResult]:
        """Use multiple AI agents to extract data"""
        context = ScrapingContext(
            url=url,
            html_content=html_content,
            soup=soup
        )
        
        best_result = None
        best_confidence = 0.0
        
        # Try each agent in order of preference
        for agent in self.agents:
            try:
                result = agent.process(context)
                
                if result and result.confidence_score > best_confidence:
                    best_result = result
                    best_confidence = result.confidence_score
                    
                    # If we get high confidence result, we can stop
                    if best_confidence > 0.9:
                        break
                        
            except Exception as e:
                self.logger.error(f"Agent {agent.name} failed: {e}")
                continue
        
        # Learn from successful extraction
        if best_result and best_result.confidence_score > 0.7:
            pattern_agent = next((a for a in self.agents if isinstance(a, PatternLearningAgent)), None)
            if pattern_agent:
                pattern_agent.learn_from_success(context, best_result)
        
        return best_result
    
    def add_agent(self, agent: BaseAIAgent):
        """Add a custom agent to the orchestrator"""
        self.agents.append(agent)
    
    def get_agent_stats(self) -> Dict:
        """Get statistics about agent performance"""
        stats = {}
        for agent in self.agents:
            # This would be enhanced with actual performance tracking
            stats[agent.name] = {
                "total_attempts": 0,
                "successful_extractions": 0,
                "average_confidence": 0.0
            }
        return stats
