# Cashback Scraper Configuration
# Add your custom configurations here

SCRAPER_SETTINGS = {
    "default_delay": 1,  # Delay between requests in seconds
    "max_workers": 5,    # Maximum concurrent workers
    "timeout": 10,       # Request timeout in seconds
    "retry_attempts": 3, # Number of retry attempts for failed requests
}

# Custom user agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Output formats
OUTPUT_FORMATS = ["csv", "json", "excel"]

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_enabled": True,
    "console_enabled": True
}
