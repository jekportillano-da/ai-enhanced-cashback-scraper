# How to Run the Pokitpal Competitive Intelligence Scraper

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.8+ installed
- OpenAI API key
- Internet connection

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd pokitpal-competitive-scraper

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Test Environment

```bash
python tests/test_environment.py
```

## 🎯 Running Competitive Analysis

### Interactive Mode (Recommended)
```bash
python main.py
```

Follow the prompts to:
1. Choose intelligence level (Basic/Standard/Comprehensive)
2. Set budget
3. Select competitors to analyze
4. Get Excel-ready results

### Quick Demo
```bash
python examples/competitive_intelligence_demo.py
```

## 🧠 Intelligence Levels

### 🔸 Basic Intelligence (~$0.0008/page)
- **What**: Simple merchant and cashback data
- **Output**: CSV file
- **Use Case**: Quick competitor overview
- **Budget**: $5-10 for 50-100 pages

### 🔹 Standard Intelligence (~$0.0015/page) ⭐ **Recommended**
- **What**: Business insights + competitive analysis
- **Output**: Enhanced CSV with business metrics
- **Use Case**: Strategic planning and competitive positioning
- **Budget**: $10-20 for 50-100 pages

### 🔷 Comprehensive Intelligence (~$0.0035/page)
- **What**: Full competitive intelligence analysis
- **Output**: Excel file with multiple sheets + CSV
- **Use Case**: Deep competitive research and strategic planning
- **Budget**: $20-50 for 50-100 pages

## 📊 Understanding the Output

### CSV Files (All Levels)
- Open directly in Excel
- Clean column names for business analysis
- Strategic recommendations included

### Excel Files (Comprehensive Only)
- **Sheet 1**: Competitive Intelligence Summary
- **Sheet 2**: Full Detailed Data
- **Sheet 3**: Analysis Summary & Metrics

### Key Data Fields
- **Threat Level**: How dangerous competitor is to Pokitpal
- **Market Opportunities**: Weaknesses Pokitpal can exploit
- **Strategic Recommendations**: Pokitpal-specific action items
- **Response Priority**: Urgency level for competitive response

## 💰 Budget Planning

### Sample Budgets:
- **Small Analysis**: $5-10 (20-30 competitors)
- **Medium Analysis**: $15-25 (50-75 competitors)
- **Large Analysis**: $30-50 (100+ competitors)

### Cost Control:
- Set token budget upfront
- Real-time cost monitoring
- Automatic stopping when budget reached

## 🔧 Advanced Usage

### Programmatic Usage
```python
from src.scrapers.token_optimized_scraper_v2 import TokenOptimizedAIScraper

scraper = TokenOptimizedAIScraper()

# Analyze ShopBack competitors
results = scraper.scrape_with_intelligence_level(
    site_name="shopback",
    intelligence_level="standard",
    max_pages=25,
    token_budget=2000  # ~$3 budget
)

# Save results
scraper.save_intelligence_results(results, "shopback_analysis", "standard")
```

### Analyzing Specific Sites
- **ShopBack**: `site_name="shopback"`
- **CashRewards**: `site_name="cashrewards"`

## 🛠️ Troubleshooting

### Common Issues:

1. **"No module named..." errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **API key not working**
   - Check `.env` file has correct key
   - Verify key has sufficient credits

3. **No results obtained**
   - Check internet connection
   - Verify target sites are accessible
   - Try smaller budget/pages first

### Getting Help:
```bash
# Test your environment
python tests/test_environment.py

# Run simple demo
python examples/competitive_intelligence_demo.py
```

## 📁 File Locations

### Input:
- **Configuration**: `.env` file
- **Settings**: `main.py` for budget/page limits


### Output:
- **CSV Results**: `data/competitors_standard_YYYYMMDD_HHMMSS.csv`
- **Excel Results**: `data/competitors_comprehensive_YYYYMMDD_HHMMSS.xlsx`
- **Google Trends**: `data/top_retailers.csv`
- **Logs**: `logs/token_scraper.log`

## 🎯 Best Practices

### For Business Analysis:
1. **Start with Standard Intelligence** - best value for insights
2. **Set reasonable budgets** - $10-20 covers most analysis needs
3. **Use Excel files** - better for presentations and sharing
4. **Review logs** - check for any scraping issues

### For Development:
1. **Test with small budgets** first
2. **Monitor token usage** in real-time
3. **Use version control** for configuration changes
4. **Document customizations** for your team

## 🚀 Production Deployment

### Server Requirements:
- Python 3.8+
- 2GB+ RAM
- Stable internet connection
- OpenAI API access

### Automation:
- Schedule regular competitive analysis
- Set up monitoring and alerting
- Implement result processing pipelines
- Create dashboards from CSV/Excel output

---


Need help? Check the logs in `logs/` directory or run the test suite!
