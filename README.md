## AI-Enhanced Cashback Scraper

### Project Structure

```
├── archive/                # Old docs, legacy files
├── config/                 # Configuration files
├── data/                   # All output CSV/JSON files
├── examples/               # Example scripts and demos
├── logs/                   # Log files
├── services/               # Retailer scraping and Google Trends logic
├── src/
│   ├── ai_agents/          # AI agent logic
│   └── scrapers/           # Scraper modules
├── tests/                  # Unit tests
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
├── main.py                 # Main entry point
├── run_scraper.py          # Run script
├── README.md               # Project documentation
├── CHANGELOG.md            # Changelog
├── HOW_TO_RUN.md           # How to run instructions
├── LICENSE                 # License
```



# AI-Enhanced Competitive Intelligence Scraper

AI-powered competitive intelligence analysis for cashback platforms. Dynamically scrapes, ranks, and analyzes competitors like ShopBack and Cashrewards using Google Trends and advanced business logic.

---
**Author:** John Jerick Portillano
---

## 🎯 Features

- **AI-Powered Analysis**: Three intelligence levels (Basic, Standard, Comprehensive)
- **Competitive Intelligence**: Pokitpal-focused competitor analysis
- **Cost Control**: Token budget management and optimization
- **Excel-Ready Output**: CSV and Excel files for business analysis
- **Smart Content Optimization**: Minimizes API costs while maximizing insights


## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env file
   ```

3. **Run Competitive Analysis**
   ```bash
   python main.py
   ```

4. **Choose Intelligence Level**
   - Basic: Simple extraction with threat assessment
   - Standard: Business insights + competitive recommendations
   - Comprehensive: Full competitive intelligence analysis

## Intelligence Levels

### Basic Intelligence
- Merchant name and cashback rates
- Competitive threat assessment (High/Medium/Low)
- Simple CSV output

### Standard Intelligence (Recommended)
- All Basic features PLUS:
- Market position analysis
- Pokitpal-specific opportunities
- Strategic recommendations
- Enhanced CSV with business metrics

### Comprehensive Intelligence
- All Standard features PLUS:
- Full competitive positioning analysis
- Market gaps Pokitpal can exploit
- Partnership vs competition strategies
- Excel file with multiple analysis sheets


## Project Structure

See above for the latest folder layout. All output files are now saved in the `data/` folder. Legacy and unused files are archived in `archive/`.

## Competitive Intelligence Output

### Key Analysis Fields:
- Threat Assessment: How dangerous each competitor is to Pokitpal
- Market Opportunities: Weaknesses Pokitpal can exploit
- Strategic Recommendations: Pokitpal-specific action items
- Differentiation Opportunities: Ways to stand out from competitors
- Response Priority: Urgency level for competitive response

### Sample Output:
```
Competitor: Hotels.com
├── Cashback Rate: 3%
├── Threat Level: Medium
├── Market Position: Direct competitor in hotel bookings
├── Pokitpal Opportunity: Limited cashback offer
└── Strategy: Differentiate with higher rates
```

## Cost Management

- Token Budget Control: Set spending limits upfront
- Real-time Cost Tracking: Monitor expenses during scraping
- Optimized Prompts: Minimize tokens while maximizing insights
- Intelligent Content Parsing: Extract only relevant information

## Business Intelligence Features

### Competitive Analysis:
- Market positioning assessment
- Competitive advantages identification
- Weakness exploitation opportunities
- Partnership vs competition recommendations

### Strategic Insights:
- Revenue opportunity analysis
- Customer acquisition difficulty assessment
- Market share vulnerability evaluation
- Recommended response strategies

## Development Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd project-root
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1     # Windows
   source .venv/bin/activate       # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test Environment**
   ```bash
   python tests/test_environment.py
   ```

## Usage Examples

### Basic Competitive Analysis
```python
from src.scrapers.token_optimized_scraper_v2 import TokenOptimizedAIScraper



# Analyze competitors with Standard intelligence
results = scraper.scrape_with_intelligence_level(
    site_name="shopback",
    intelligence_level="standard",
    max_pages=10,
    token_budget=2000  # ~$3 budget
)

# Save as Excel and CSV
scraper.save_intelligence_results(results, "competitors", "standard")
```

### Quick Demo
```bash
python examples/competitive_intelligence_demo.py
```

## Configuration

### Environment Variables (.env)
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Intelligence Level Settings
- Adjust token budgets in `main.py`
- Modify analysis depth in scraper configuration
- Customize competitive analysis prompts


## Output Files

### CSV Files (Excel-ready)
- `data/competitors_standard_YYYYMMDD_HHMMSS.csv`
- `data/top_retailers.csv` (Google Trends)
- Clean columns for business analysis
- Strategic recommendations included

### Excel Files (Comprehensive only)
- Multiple sheets: Intelligence, Full Data, Summary
- Professional formatting for presentations
- Advanced competitive metrics

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add competitive feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.


## Support

- Environment Issues: Run `python tests/test_environment.py`
- API Problems: Check OpenAI API key in `.env` file
- Output Questions: See `data/README.md` for file format details

---

Built for competitive intelligence and business analysis.
