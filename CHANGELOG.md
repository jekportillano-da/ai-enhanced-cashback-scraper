## [2025-08-19] Cleanup & Documentation Update

- Moved all output files to `data/` folder
- Removed legacy and unused files from main folder
- Deleted redundant README files from subfolders
- Cleaned up __pycache__ folders
- Updated main README.md for GitHub readiness
- Updated requirements.txt for dependencies
- Ensured all scripts and modules are in correct folders

# Changelog

All notable changes to the AI-Enhanced Cashback Scraper will be documented in this file.

## [1.0.2] - 2025-08-12

### Added
- Professional project structure with organized directories
- Comprehensive README.md with detailed documentation
- Main entry point (`main.py`) with interactive and CLI modes
- Token optimization with tiktoken integration
- Budget controls and cost tracking
- MIT License file
- .gitignore for proper version control
- HOW_TO_RUN.md with step-by-step instructions

### Changed
- Reorganized code into logical directories (src/, examples/, tests/, config/, data/, logs/)
- Updated all import statements to use new package structure
- Simplified requirements.txt with core dependencies
- Improved error handling and logging

### Removed
- Duplicate and unnecessary files
- Old run_scraper.py (replaced with main.py)
- Python cache files

### Project Structure
```
Project Scraper/
├── src/                    # Source code
│   ├── scrapers/          # Scraper implementations
│   └── ai_agents/         # AI agent modules
├── examples/              # Example scripts and demos
├── tests/                 # Test modules  
├── config/                # Configuration files
├── data/                  # Output data files
├── logs/                  # Log files
├── main.py                # Main entry point
└── documentation files
```

## [1.0.1] - 2025-08-12

### Added
- Token-optimized scraper with advanced cost control
- Real-time token usage tracking and cost estimation
- Content optimization to minimize token consumption
- Budget enforcement to prevent overspending
- Detailed token usage analytics and reporting

### Enhanced
- AI extraction success rate improved to ~57%
- Cost efficiency optimized to ~$0.0005 per extraction
- Performance metrics and monitoring
- Comprehensive error handling

## [1.0.0] - 2025-08-12

### Added
- Initial release of AI-Enhanced Cashback Scraper
- Core scraping framework for ShopBack and CashRewards
- AI agent system with multiple specialized agents:
  - LLM Extraction Agent (OpenAI GPT integration)
  - Pattern Learning Agent (adaptive learning)
  - Adaptive Selector Agent (CSS selector optimization)
- Multi-threaded concurrent processing
- CSV and JSON output formats
- Comprehensive logging system
- Configuration management
- Environment variable support

### Features
- Traditional web scraping with BeautifulSoup
- AI-powered data extraction using OpenAI GPT models
- Extensible architecture for adding new sites
- Performance tracking and analytics
- Error recovery and graceful degradation
