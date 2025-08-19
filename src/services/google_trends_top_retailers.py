import csv
from datetime import datetime
from pytrends.request import TrendReq
from services.retailer_scraper import scrape_shopback_retailers, scrape_cashrewards_retailers

def fetch_top_retailers(region='AU', top_n=20, filename='top_retailers.csv'):
    # Get dynamic retailer names
    shopback = scrape_shopback_retailers()
    cashrewards = scrape_cashrewards_retailers()
    print(f"ShopBack retailers found: {shopback}")
    print(f"Cashrewards retailers found: {cashrewards}")
    all_retailers = list(set(shopback + cashrewards))
    print(f"Total unique retailers: {len(all_retailers)}")

    if not all_retailers:
        print("No retailers found from scraping. Exiting.")
        return []

    # Batch into groups of 5 for pytrends
    batch_size = 5
    interest_scores = {}
    pytrends = TrendReq(hl='en-US', tz=360)
    for i in range(0, len(all_retailers), batch_size):
        batch = all_retailers[i:i+batch_size]
        print(f"Processing batch: {batch}")
        try:
            pytrends.build_payload(batch, cat=0, timeframe='now 7-d', geo=region, gprop='')
            trends = pytrends.interest_over_time()
            print(f"Pytrends result for batch: {trends}")
            if not trends.empty:
                for retailer in batch:
                    if retailer in trends:
                        avg_score = trends[retailer].mean()
                        interest_scores[retailer] = avg_score
            else:
                print(f"No trend data for batch: {batch}")
        except Exception as e:
            print(f"Batch {batch} failed: {e}")
            continue

    if not interest_scores:
        print("No interest scores found for any retailer. Exiting.")
        return []

    # Rank by interest score
    ranked = sorted(interest_scores.items(), key=lambda x: x[1], reverse=True)
    top_retailers = [r[0] for r in ranked[:top_n]]

    # Save to CSV (overwrite) in data folder
    import os
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, filename)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['retailer', 'score', 'timestamp'])
        for retailer in top_retailers:
            writer.writerow([retailer, interest_scores.get(retailer, 0), datetime.now().isoformat()])
    print(f"Saved top {top_n} retailers to {csv_path}")
    return top_retailers

if __name__ == "__main__":
    import sys
    # Allow user to specify top_n from command line, default to 5
    top_n = 5
    if len(sys.argv) > 1:
        try:
            top_n = int(sys.argv[1])
        except:
            pass
    fetch_top_retailers(top_n=top_n)
