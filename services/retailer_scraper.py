import requests
from bs4 import BeautifulSoup

def scrape_shopback_retailers():
    url = "https://www.shopback.com.au"
    response = requests.get(url, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")
    retailers = set()
    # Find Popular Stores section by heading
    popular_heading = soup.find(lambda tag: tag.name == "h3" and "Popular Stores" in tag.text)
    if popular_heading:
        # Get all links after the heading until the next heading
        for sib in popular_heading.find_all_next("a", href=True):
            href = sib["href"]
            # Only take links that look like retailer pages
            if href.startswith("/") or "shopback.com.au/" in href:
                name = sib.text.strip()
                if name and len(name) > 2:
                    retailers.add(name)
            # Stop if we hit another section
            if sib.find_previous_sibling(lambda t: t.name == "h3" and t != popular_heading):
                break
    return list(retailers)

def scrape_cashrewards_retailers():
    url = "https://www.cashrewards.com.au/all-stores"
    response = requests.get(url, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")
    retailers = set()
    # Find all <a> tags where href contains /store/
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/store/" in href:
            name = a.text.strip()
            if name and len(name) > 2:
                retailers.add(name)
    return list(retailers)

if __name__ == "__main__":
    shopback = scrape_shopback_retailers()
    cashrewards = scrape_cashrewards_retailers()
    print(f"ShopBack retailers: {shopback[:10]}")
    print(f"Cashrewards retailers: {cashrewards[:10]}")
