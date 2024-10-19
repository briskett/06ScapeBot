import requests
import pandas as pd
import time

# Function to fetch items from a specific category
def fetch_items_from_category(category):
    items = []
    for alpha in 'abcdefghijklmnopqrstuvwxyz':
        page = 1
        while True:
            url = f"https://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={category}&alpha={alpha}&page={page}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                if response.text.strip() == "":
                    print(f"Empty response for URL: {url}")
                    break
                data = response.json()
                if not data['items']:
                    break
                items.extend(data['items'])
                page += 1
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                break
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")
                break
            except ValueError as val_err:
                print(f"JSON decode error: {val_err}")
                break
            time.sleep(1)  # Adding a delay to avoid hitting rate limits
    return items

# Fetching items from broader categories
broad_categories = [17]  # Example categories (usually general equipment, armor, etc.)
all_items = []

for category in broad_categories:
    category_items = fetch_items_from_category(category)
    all_items.extend(category_items)
    print(f"Fetched {len(category_items)} items from category {category}")

print(f"Total items fetched from all categories: {len(all_items)}")

# Keywords to identify mage armor
mage_armor_keywords = ['robe', 'wizard', 'mage', 'battle-mage', 'vestment', 'magic']

# Filter items for mage armor using keywords
mage_armor_items = [item for item in all_items if any(keyword in item['name'].lower() for keyword in mage_armor_keywords)]
print(f"Total mage armor items filtered: {len(mage_armor_items)}")

# Function to fetch item details
def get_item_details(item_id, retries=5):
    url = f"https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={item_id}"
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.text.strip() == "":
                print(f"Empty response for URL: {url}")
                continue
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError as val_err:
            print(f"JSON decode error: {val_err}")
        if attempt < retries - 1:
            wait_time = 2 ** attempt
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    return None

# Function to calculate margin
def calculate_margin(item_details):
    try:
        buy_price = item_details['item']['buy_average']
        sell_price = item_details['item']['sell_average']
        if buy_price is not None and sell_price is not None:
            margin = sell_price - buy_price
            return margin
        else:
            return None
    except KeyError:
        return None

# Function to collect margins for mage armor items
def get_mage_armor_margins(items):
    margins = []
    for item in items:
        details = get_item_details(item['id'])
        if details:
            margin = calculate_margin(details)
            if margin is not None:
                margins.append({'id': item['id'], 'name': item['name'], 'margin': margin})
                print(f"Item: {item['name']}, Margin: {margin}")  # Debugging line to see each item's margin
            else:
                print(f"Item: {item['name']} has no valid margin")  # Debugging line for items without valid margin
        else:
            print(f"Failed to fetch details for item ID: {item['id']}")  # Debugging line for failed details fetch
    return margins

# Main script to get mage armor item margins
mage_armor_margins = get_mage_armor_margins(mage_armor_items)

# Check if any items with margins were found
if mage_armor_margins:
    # Using pandas to create a DataFrame and sort by margin
    df_mage_margins = pd.DataFrame(mage_armor_margins)

    if 'margin' in df_mage_margins.columns:
        df_mage_margins = df_mage_margins.sort_values(by='margin', ascending=False)

        # Displaying top 10 mage armor items with the greatest margin
        print("Top 10 Mage Armor Items with Greatest Margins:")
        print(df_mage_margins.head(10))

        # Save the results to a CSV file for further analysis
        df_mage_margins.to_csv('mage_armor_margins.csv', index=False)
        print("Data saved to mage_armor_margins.csv")
    else:
        print("No 'margin' column found in the DataFrame. The margin calculation might have failed.")
else:
    print("No mage armor items with valid margins found.")
