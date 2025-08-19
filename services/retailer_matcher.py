import difflib

def match_retailer(trends_list, cashback_list, cutoff=0.7):
    """
    For each retailer in trends_list, find the closest match in cashback_list.
    Returns a dict: {trends_retailer: matched_cashback_retailer or None}
    """
    matches = {}
    cashback_names = [name.lower().strip() for name in cashback_list]
    for retailer in trends_list:
        retailer_norm = retailer.lower().strip()
        found = difflib.get_close_matches(retailer_norm, cashback_names, n=1, cutoff=cutoff)
        if found:
            # Return the original cashback name (not normalized)
            idx = cashback_names.index(found[0])
            matches[retailer] = cashback_list[idx]
        else:
            matches[retailer] = None
    return matches

# Example usage:
if __name__ == "__main__":
    # Simulate Google Trends output
    trends = ['Woolworths', 'Kmart', 'Amazon', 'Chemist Warehouse', 'Big W']
    # Simulate cashback site retailer list
    cashback = ['Woolworths Group', 'Kmart Australia', 'Amazon AU', 'Chemist Warehouse', 'BIG W']
    result = match_retailer(trends, cashback)
    for k, v in result.items():
        print(f"{k} -> {v if v else 'No match'}")
