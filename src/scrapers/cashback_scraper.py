import requests
import csv
import json
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pathlib import Path
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


@dataclass
class CashbackOffer:
    """Data class for cashback offer information"""
    merchant: str
    cashback_offer: str
    url: str
    scraped_at: str = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = time.strftime('%Y-%m-%d %H:%M:%S')


class BaseCashbackScraper(ABC):
    """Abstract base class for cashback scrapers"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{self.config["name"]}_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.config["name"])
    
    def fetch_sitemap_urls(self) -> List[str]:
        """Fetch URLs from sitemap"""
        try:
            response = self.session.get(self.config["sitemap_url"], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "xml")
            urls = [loc.text for loc in soup.find_all("loc")]
            
            self.logger.info(f"Found {len(urls)} URLs in sitemap")
            return urls
            
        except Exception as e:
            self.logger.error(f"Failed to fetch sitemap: {e}")
            return []
    
    def filter_urls(self, urls: List[str]) -> List[str]:
        """Filter URLs based on configuration"""
        if "url_filter" in self.config:
            filtered_urls = [url for url in urls if self.config["url_filter"] in url]
            self.logger.info(f"Filtered to {len(filtered_urls)} relevant URLs")
            return filtered_urls
        return urls
    
    @abstractmethod
    def extract_merchant_data(self, soup: BeautifulSoup, url: str) -> Optional[CashbackOffer]:
        """Extract merchant data from page soup - must be implemented by subclasses"""
        pass
    
    def scrape_page(self, url: str) -> Optional[CashbackOffer]:
        """Scrape a single page"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                self.logger.warning(f"Failed to load {url} - Status: {response.status_code}")
                return None
                
            soup = BeautifulSoup(response.text, "html.parser")
            return self.extract_merchant_data(soup, url)
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return None
    
    def scrape_all(self, max_workers: int = 5) -> List[CashbackOffer]:
        """Scrape all URLs with concurrent processing"""
        urls = self.fetch_sitemap_urls()
        if not urls:
            return []
            
        filtered_urls = self.filter_urls(urls)
        offers = []
        
        self.logger.info(f"Starting to scrape {len(filtered_urls)} URLs with {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self.scrape_page, filtered_urls)
            
            for result in results:
                if result:
                    offers.append(result)
                    self.logger.info(f"Scraped: {result.merchant} - {result.cashback_offer}")
                
                # Rate limiting
                time.sleep(self.config.get("delay", 1))
        
        self.logger.info(f"Scraping complete! Found {len(offers)} valid offers")
        return offers
    
    def save_to_csv(self, offers: List[CashbackOffer], filename: str = None):
        """Save offers to CSV file"""
        if not filename:
            filename = f"{self.config['name']}_offers.csv"
            
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Merchant", "Cashback Offer", "URL", "Scraped At"])
            
            for offer in offers:
                writer.writerow([offer.merchant, offer.cashback_offer, offer.url, offer.scraped_at])
        
        self.logger.info(f"Data saved to {filename}")
    
    def save_to_json(self, offers: List[CashbackOffer], filename: str = None):
        """Save offers to JSON file"""
        if not filename:
            filename = f"{self.config['name']}_offers.json"
            
        data = [
            {
                "merchant": offer.merchant,
                "cashback_offer": offer.cashback_offer,
                "url": offer.url,
                "scraped_at": offer.scraped_at
            }
            for offer in offers
        ]
        
        with open(filename, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Data saved to {filename}")


class ShopBackScraper(BaseCashbackScraper):
    """Scraper for ShopBack website"""
    
    def extract_merchant_data(self, soup: BeautifulSoup, url: str) -> Optional[CashbackOffer]:
        """Extract merchant data from ShopBack page"""
        try:
            # Extract merchant name
            merchant_element = soup.find("h1")
            if not merchant_element:
                return None
            merchant_name = merchant_element.text.strip()
            
            # Extract cashback offer
            cashback_offer = "No Cashback Info"
            cashback_element = soup.find("h4", class_="fs_sbds-global-font-size-7")
            if cashback_element:
                cashback_offer = cashback_element.text.strip()
            
            # Additional selectors to try if primary fails
            if cashback_offer == "No Cashback Info":
                alternative_selectors = [
                    {"tag": "span", "class": "cashback-rate"},
                    {"tag": "div", "class": "rate"},
                    {"tag": "p", "class": "cashback-percentage"}
                ]
                
                for selector in alternative_selectors:
                    element = soup.find(selector["tag"], class_=selector["class"])
                    if element:
                        cashback_offer = element.text.strip()
                        break
            
            return CashbackOffer(
                merchant=merchant_name,
                cashback_offer=cashback_offer,
                url=url
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting data from {url}: {e}")
            return None


class CashRewardsScraper(BaseCashbackScraper):
    """Scraper for CashRewards website"""
    
    def extract_merchant_data(self, soup: BeautifulSoup, url: str) -> Optional[CashbackOffer]:
        """Extract merchant data from CashRewards page"""
        try:
            # Extract merchant name
            merchant_element = soup.find("h1")
            if not merchant_element:
                return None
            merchant_name = merchant_element.text.strip()
            
            # Skip if merchant name is unknown
            if merchant_name.lower() in ["unknown", ""]:
                return None
            
            # Extract cashback offer
            cashback_offer = "No Cashback Info"
            cashback_element = soup.find("h3", {"data-test-id": "cashback-rate"})
            if cashback_element:
                cashback_offer = cashback_element.text.strip()
            
            # Additional selectors to try if primary fails
            if cashback_offer == "No Cashback Info":
                alternative_selectors = [
                    {"tag": "span", "attrs": {"class": "cashback-rate"}},
                    {"tag": "div", "attrs": {"class": "rate-display"}},
                    {"tag": "p", "attrs": {"data-test": "rate"}}
                ]
                
                for selector in alternative_selectors:
                    element = soup.find(selector["tag"], selector["attrs"])
                    if element:
                        cashback_offer = element.text.strip()
                        break
            
            return CashbackOffer(
                merchant=merchant_name,
                cashback_offer=cashback_offer,
                url=url
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting data from {url}: {e}")
            return None


class CashbackScraperFactory:
    """Factory class to create appropriate scraper instances"""
    
    SCRAPER_CONFIGS = {
        "shopback": {
            "name": "shopback",
            "sitemap_url": "https://www.shopback.com.au/sitemap.xml",
            "delay": 1,
            "scraper_class": ShopBackScraper
        },
        "cashrewards": {
            "name": "cashrewards",
            "sitemap_url": "https://www.cashrewards.com.au/en/sitemap.xml",
            "url_filter": "https://www.cashrewards.com.au/store",
            "delay": 1,
            "scraper_class": CashRewardsScraper
        }
    }
    
    @classmethod
    def create_scraper(cls, scraper_type: str) -> BaseCashbackScraper:
        """Create a scraper instance based on type"""
        if scraper_type not in cls.SCRAPER_CONFIGS:
            raise ValueError(f"Unknown scraper type: {scraper_type}")
        
        config = cls.SCRAPER_CONFIGS[scraper_type]
        scraper_class = config.pop("scraper_class")
        return scraper_class(config)
    
    @classmethod
    def get_available_scrapers(cls) -> List[str]:
        """Get list of available scraper types"""
        return list(cls.SCRAPER_CONFIGS.keys())


class CashbackAggregator:
    """Aggregator to run multiple scrapers and combine results"""
    
    def __init__(self):
        self.results = {}
    
    def run_scraper(self, scraper_type: str, max_workers: int = 5) -> List[CashbackOffer]:
        """Run a specific scraper"""
        scraper = CashbackScraperFactory.create_scraper(scraper_type)
        offers = scraper.scrape_all(max_workers=max_workers)
        self.results[scraper_type] = offers
        return offers
    
    def run_all_scrapers(self, max_workers: int = 5) -> Dict[str, List[CashbackOffer]]:
        """Run all available scrapers"""
        available_scrapers = CashbackScraperFactory.get_available_scrapers()
        
        for scraper_type in available_scrapers:
            print(f"\n{'='*50}")
            print(f"Running {scraper_type} scraper...")
            print(f"{'='*50}")
            self.run_scraper(scraper_type, max_workers)
        
        return self.results
    
    def combine_and_save(self, filename: str = "combined_cashback_offers"):
        """Combine all results and save to files"""
        all_offers = []
        
        for scraper_type, offers in self.results.items():
            for offer in offers:
                offer_dict = {
                    "source": scraper_type,
                    "merchant": offer.merchant,
                    "cashback_offer": offer.cashback_offer,
                    "url": offer.url,
                    "scraped_at": offer.scraped_at
                }
                all_offers.append(offer_dict)
        
        # Save to CSV
        df = pd.DataFrame(all_offers)
        df.to_csv(f"{filename}.csv", index=False)
        
        # Save to JSON
        with open(f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(all_offers, f, indent=2, ensure_ascii=False)
        
        print(f"\nCombined {len(all_offers)} offers from {len(self.results)} sources")
        print(f"Results saved to {filename}.csv and {filename}.json")
        
        return all_offers
    
    def get_summary(self) -> Dict:
        """Get summary statistics of scraped data"""
        summary = {}
        
        for scraper_type, offers in self.results.items():
            summary[scraper_type] = {
                "total_offers": len(offers),
                "merchants_with_cashback": len([o for o in offers if o.cashback_offer != "No Cashback Info"]),
                "unique_merchants": len(set(o.merchant for o in offers))
            }
        
        return summary


if __name__ == "__main__":
    # Example usage
    print("Cashback Scraper System")
    print("=" * 30)
    
    # Option 1: Run individual scraper
    # scraper = CashbackScraperFactory.create_scraper("shopback")
    # offers = scraper.scrape_all(max_workers=3)
    # scraper.save_to_csv(offers)
    # scraper.save_to_json(offers)
    
    # Option 2: Run all scrapers
    aggregator = CashbackAggregator()
    all_results = aggregator.run_all_scrapers(max_workers=3)
    
    # Save combined results
    aggregator.combine_and_save("combined_cashback_offers")
    
    # Print summary
    summary = aggregator.get_summary()
    print("\nScraping Summary:")
    print("=" * 20)
    for scraper, stats in summary.items():
        print(f"\n{scraper.title()}:")
        print(f"  Total offers: {stats['total_offers']}")
        print(f"  Merchants with cashback: {stats['merchants_with_cashback']}")
        print(f"  Unique merchants: {stats['unique_merchants']}")
