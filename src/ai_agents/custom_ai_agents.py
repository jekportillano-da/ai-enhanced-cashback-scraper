"""
Custom AI Agents for specific scraping scenarios
"""

from ai_agents import BaseAIAgent, ScrapingContext, ExtractionResult
from typing import Optional, Dict, List
import re
from bs4 import BeautifulSoup, Tag
try:
    import requests
    from transformers import pipeline
    import spacy
except ImportError:
    requests = None
    pipeline = None
    spacy = None


class VisionBasedAgent(BaseAIAgent):
    """AI agent that uses computer vision to analyze page screenshots"""
    
    def __init__(self, use_gpt4_vision: bool = False):
        super().__init__("Vision_Agent")
        self.use_gpt4_vision = use_gpt4_vision
        
    def process(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Use vision AI to analyze page layout and extract data"""
        if not self.use_gpt4_vision:
            self.logger.warning("GPT-4 Vision not enabled, skipping vision-based extraction")
            return None
            
        try:
            # Take screenshot of the page (would need selenium/playwright)
            screenshot_path = self._take_screenshot(context.url)
            
            # Use GPT-4 Vision to analyze the screenshot
            result = self._analyze_with_vision(screenshot_path, context)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Vision-based extraction failed: {e}")
            return None
    
    def _take_screenshot(self, url: str) -> str:
        """Take screenshot of the webpage"""
        # This would require selenium/playwright implementation
        # Placeholder for now
        self.logger.info(f"Would take screenshot of {url}")
        return "screenshot.png"
    
    def _analyze_with_vision(self, screenshot_path: str, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Analyze screenshot with GPT-4 Vision"""
        # This would integrate with GPT-4 Vision API
        # Placeholder for now
        self.logger.info("Would analyze screenshot with GPT-4 Vision")
        return None


class NLPEnhancedAgent(BaseAIAgent):
    """AI agent that uses NLP to understand content semantics"""
    
    def __init__(self):
        super().__init__("NLP_Agent")
        try:
            # Load spaCy model for NLP
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
            
        try:
            # Load Hugging Face sentiment analysis pipeline
            self.sentiment_analyzer = pipeline("sentiment-analysis")
        except Exception:
            self.logger.warning("Could not load sentiment analyzer")
            self.sentiment_analyzer = None
    
    def process(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Use NLP to understand content and extract relevant information"""
        if not self.nlp:
            return None
            
        try:
            # Extract clean text
            text = self._extract_clean_text(context.soup)
            
            # Process with spaCy
            doc = self.nlp(text)
            
            # Find potential merchant names (organizations, proper nouns)
            merchant_candidates = self._find_merchant_candidates(doc)
            
            # Find cashback information using semantic understanding
            cashback_info = self._find_cashback_semantic(doc, text)
            
            if merchant_candidates and cashback_info:
                # Choose the best merchant candidate
                best_merchant = self._select_best_merchant(merchant_candidates, context)
                
                result = ExtractionResult(
                    merchant_name=best_merchant,
                    cashback_offer=cashback_info,
                    confidence_score=0.75,
                    extraction_method="NLP_Semantic"
                )
                
                self.log_attempt(context, result, "NLP_Semantic")
                return result
                
        except Exception as e:
            self.logger.error(f"NLP extraction failed: {e}")
        
        self.log_attempt(context, None, "NLP_Semantic")
        return None
    
    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text for NLP processing"""
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "aside", "header"]):
            element.decompose()
        
        return soup.get_text()
    
    def _find_merchant_candidates(self, doc) -> List[str]:
        """Find potential merchant names using NLP"""
        candidates = []
        
        # Look for organizations
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON", "GPE"]:
                candidates.append(ent.text.strip())
        
        # Look for proper nouns that might be brand names
        for token in doc:
            if (token.pos_ == "PROPN" and 
                len(token.text) > 2 and 
                token.text.isalpha()):
                candidates.append(token.text)
        
        # Remove duplicates and filter
        return list(set([c for c in candidates if self._is_valid_merchant_candidate(c)]))
    
    def _is_valid_merchant_candidate(self, candidate: str) -> bool:
        """Check if a candidate is a valid merchant name"""
        if len(candidate) < 2 or len(candidate) > 50:
            return False
        
        # Skip common words that aren't merchant names
        skip_words = {
            "home", "shop", "store", "buy", "sale", "offer", "deal",
            "cashback", "reward", "earn", "save", "discount"
        }
        
        return candidate.lower() not in skip_words
    
    def _find_cashback_semantic(self, doc, text: str) -> Optional[str]:
        """Find cashback information using semantic understanding"""
        # Look for sentences containing cashback-related terms
        cashback_sentences = []
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            if any(term in sent_text for term in ["cashback", "cash back", "earn", "reward", "%"]):
                cashback_sentences.append(sent.text.strip())
        
        # Find the most relevant cashback sentence
        for sentence in cashback_sentences:
            # Look for percentage or dollar amounts
            percentage_match = re.search(r'\d+\.?\d*%', sentence)
            dollar_match = re.search(r'\$\d+\.?\d*', sentence)
            
            if percentage_match or dollar_match:
                return sentence
        
        # Fallback: return the first cashback sentence
        if cashback_sentences:
            return cashback_sentences[0]
        
        return None
    
    def _select_best_merchant(self, candidates: List[str], context: ScrapingContext) -> str:
        """Select the best merchant candidate"""
        if not candidates:
            return "Unknown"
        
        # Score candidates based on various factors
        scored_candidates = []
        
        for candidate in candidates:
            score = 0
            
            # Prefer candidates that appear in the URL
            if candidate.lower() in context.url.lower():
                score += 3
            
            # Prefer candidates that appear in title tags
            title_elements = context.soup.find_all(["title", "h1", "h2"])
            for element in title_elements:
                if candidate.lower() in element.get_text().lower():
                    score += 2
            
            # Prefer longer, more specific names
            score += len(candidate) * 0.1
            
            scored_candidates.append((candidate, score))
        
        # Return the highest-scoring candidate
        best_candidate = max(scored_candidates, key=lambda x: x[1])
        return best_candidate[0]


class ContextAwareAgent(BaseAIAgent):
    """AI agent that uses context from previous scraping attempts"""
    
    def __init__(self):
        super().__init__("Context_Aware")
        self.site_patterns = {}
        self.success_history = []
    
    def process(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Use context from previous attempts to improve extraction"""
        
        # Determine site type from URL
        site_type = self._determine_site_type(context.url)
        
        # Get patterns specific to this site type
        site_patterns = self.site_patterns.get(site_type, {})
        
        # Try extraction using site-specific patterns
        result = self._extract_with_patterns(context, site_patterns)
        
        if result:
            # Update success history
            self._update_success_history(site_type, result, context)
            
        return result
    
    def _determine_site_type(self, url: str) -> str:
        """Determine the type of site from URL"""
        if "shopback" in url:
            return "shopback"
        elif "cashrewards" in url:
            return "cashrewards"
        elif "rakuten" in url:
            return "rakuten"
        else:
            return "generic"
    
    def _extract_with_patterns(self, context: ScrapingContext, patterns: Dict) -> Optional[ExtractionResult]:
        """Extract data using site-specific patterns"""
        
        # Use learned patterns if available
        if patterns:
            merchant = self._extract_with_pattern(context.soup, patterns.get("merchant_pattern"))
            cashback = self._extract_with_pattern(context.soup, patterns.get("cashback_pattern"))
            
            if merchant:
                result = ExtractionResult(
                    merchant_name=merchant,
                    cashback_offer=cashback or "No Cashback Info",
                    confidence_score=0.8,
                    extraction_method="Context_Aware"
                )
                
                self.log_attempt(context, result, "Context_Aware")
                return result
        
        # Fallback to generic extraction
        return self._generic_extraction(context)
    
    def _extract_with_pattern(self, soup: BeautifulSoup, pattern: Optional[Dict]) -> Optional[str]:
        """Extract text using a specific pattern"""
        if not pattern:
            return None
            
        try:
            element = soup.select_one(pattern["selector"])
            if element:
                return element.get_text().strip()
        except:
            pass
        
        return None
    
    def _generic_extraction(self, context: ScrapingContext) -> Optional[ExtractionResult]:
        """Generic extraction when no specific patterns are available"""
        
        # Simple fallback extraction
        h1 = context.soup.find("h1")
        merchant = h1.get_text().strip() if h1 else "Unknown"
        
        # Look for any element containing percentage
        cashback_element = context.soup.find(text=re.compile(r'\d+\.?\d*%'))
        cashback = cashback_element.strip() if cashback_element else "No Cashback Info"
        
        if merchant != "Unknown":
            result = ExtractionResult(
                merchant_name=merchant,
                cashback_offer=cashback,
                confidence_score=0.5,
                extraction_method="Context_Aware_Generic"
            )
            
            self.log_attempt(context, result, "Context_Aware_Generic")
            return result
        
        self.log_attempt(context, None, "Context_Aware_Generic")
        return None
    
    def _update_success_history(self, site_type: str, result: ExtractionResult, context: ScrapingContext):
        """Update success history and learn patterns"""
        
        # Store successful extraction for learning
        success_record = {
            "site_type": site_type,
            "merchant": result.merchant_name,
            "cashback": result.cashback_offer,
            "url": context.url,
            "confidence": result.confidence_score
        }
        
        self.success_history.append(success_record)
        
        # Learn patterns from successful extractions
        if result.confidence_score > 0.7:
            self._learn_pattern(site_type, context, result)
    
    def _learn_pattern(self, site_type: str, context: ScrapingContext, result: ExtractionResult):
        """Learn extraction patterns from successful attempts"""
        
        # Try to identify the elements that contained the extracted data
        merchant_element = self._find_element_containing_text(context.soup, result.merchant_name)
        cashback_element = self._find_element_containing_text(context.soup, result.cashback_offer)
        
        if merchant_element:
            merchant_pattern = self._create_selector_pattern(merchant_element)
            if site_type not in self.site_patterns:
                self.site_patterns[site_type] = {}
            self.site_patterns[site_type]["merchant_pattern"] = merchant_pattern
        
        if cashback_element:
            cashback_pattern = self._create_selector_pattern(cashback_element)
            if site_type not in self.site_patterns:
                self.site_patterns[site_type] = {}
            self.site_patterns[site_type]["cashback_pattern"] = cashback_pattern
    
    def _find_element_containing_text(self, soup: BeautifulSoup, text: str) -> Optional[Tag]:
        """Find the element that contains specific text"""
        if not text or text == "No Cashback Info":
            return None
            
        # Look for exact text match
        element = soup.find(text=text)
        if element and hasattr(element, 'parent'):
            return element.parent
        
        # Look for partial text match
        elements = soup.find_all(text=re.compile(re.escape(text)))
        if elements and hasattr(elements[0], 'parent'):
            return elements[0].parent
        
        return None
    
    def _create_selector_pattern(self, element: Tag) -> Dict:
        """Create a CSS selector pattern from an element"""
        pattern = {
            "tag": element.name,
            "selector": element.name
        }
        
        # Add class if available
        if element.get("class"):
            classes = " ".join(element["class"])
            pattern["selector"] = f"{element.name}.{classes.replace(' ', '.')}"
        
        # Add ID if available
        if element.get("id"):
            pattern["selector"] = f"#{element['id']}"
        
        return pattern
