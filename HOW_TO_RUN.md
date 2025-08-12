# How to Run the AI-Enhanced Cashback Scraper 🚀

This guide will walk you through setting up and running the AI-enhanced cashback scraper.

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (required for AI features)
- Internet connection

## 🛠️ Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Running the Scraper

### Option 1: Interactive Mode (Recommended)

```bash
python main.py
```

This will present you with a menu to choose from:
- Production Scraper (basic AI integration)
- Token-Optimized Scraper (advanced cost control)
- Examples and Demos
- Tests

### Option 2: Command Line Options

**Production Scraper:**
```bash
python main.py --production
```

**Token-Optimized Scraper:**
```bash
python main.py --optimized
```

### Option 3: Direct Scraper Execution

**Production Scraper (Basic AI):**
```bash
python src/scrapers/production_scraper.py
```

**Token-Optimized Scraper (Advanced):**
```bash
python src/scrapers/token_optimized_scraper.py
```

## 📊 Understanding the Output

### Files Created

The scraper creates several output files:

1. **CSV Files** (in `data/` directory):
   - `production_*.csv` or `optimized_*.csv`
   - Contains merchant names, cashback offers, confidence scores

2. **JSON Files** (in `data/` directory):
   - `production_*.json` or `optimized_*.json`
   - Structured data with metadata

3. **Token Summary Files** (for optimized scraper):
   - `*_token_summary.json`
   - Cost analysis and token usage statistics

4. **Log Files** (in `logs/` directory):
   - Detailed execution logs for debugging

### Output Format

**CSV Format:**
```csv
merchant,cashback_offer,confidence,method,tokens_used,cost,url,scraped_at
Hotels.com,3%,0.9,AI_LLM,318,0.0005,https://...,2025-08-12 14:03:01
```

**JSON Format:**
```json
{
  "merchant": "Hotels.com",
  "cashback_offer": "3%",
  "confidence": 0.9,
  "method": "AI_LLM",
  "tokens_used": 318,
  "cost": 0.0005,
  "url": "https://...",
  "scraped_at": "2025-08-12 14:03:01"
}
```

## ⚙️ Configuration Options

### Token Budget (Optimized Scraper)

When running the token-optimized scraper, you can set budgets:
- Small: 1,000 tokens (~$0.004)
- Medium: 5,000 tokens (~$0.018)
- Large: 10,000 tokens (~$0.035)
- No limit

### Site Selection

Choose which sites to scrape:
1. ShopBack Australia only
2. CashRewards Australia only
3. Both sites
4. Custom configuration

## 🔍 Monitoring and Debugging

### Real-time Monitoring

The scraper provides real-time feedback:
- Progress indicators
- Success/failure rates
- Token usage and costs
- Performance metrics

### Log Files

Check the `logs/` directory for detailed information:
- Execution traces
- Error messages
- Performance data
- AI extraction details

### Performance Metrics

The scraper reports:
- **Success Rate**: Percentage of successful extractions
- **Cost per Extraction**: Average cost per successful result
- **Token Efficiency**: Tokens used per API call
- **Processing Speed**: Pages processed per minute

## 🧪 Testing Your Setup

### Validate API Key

```bash
python tests/test_api_key.py
```

### Run Examples

```bash
python main.py
# Choose option 3 (View Examples)
```

### Simple Demo

```bash
python examples/simple_demo.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**
   - Ensure `.env` file exists with valid `OPENAI_API_KEY`

2. **Import Errors**
   - Check that all dependencies are installed: `pip install -r requirements.txt`

3. **Network Issues**
   - Verify internet connection
   - Check if target websites are accessible

4. **Token Limit Exceeded**
   - Reduce the number of pages or set a smaller token budget

### Getting Help

1. Check the log files in `logs/` directory
2. Run with verbose output: `python main.py` (interactive mode shows more details)
3. Validate your setup with `python tests/test_api_key.py`

## 📈 Expected Performance

### Typical Results

- **Success Rate**: 50-70% for AI extractions
- **Cost**: $0.0005-0.001 per successful extraction
- **Speed**: 15-20 pages per minute
- **Token Usage**: 250-350 tokens per AI call

### Optimization Tips

1. **Use Token Budget**: Set reasonable limits to control costs
2. **Select Specific Sites**: Don't scrape everything if you only need specific data
3. **Monitor Logs**: Check success rates and adjust parameters
4. **Batch Processing**: Let the scraper handle multiple pages efficiently

## 🎯 Next Steps

After successfully running the scraper:

1. **Analyze Results**: Open CSV files in Excel or Google Sheets
2. **Customize Configuration**: Modify settings in `config/` directory  
3. **Extend Functionality**: Add new sites or AI agents
4. **Schedule Runs**: Set up automated scraping with cron jobs or task scheduler

Happy scraping! 🤖💰
