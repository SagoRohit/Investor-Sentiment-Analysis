import requests
import pandas as pd
import time
import json
from datetime import date, timedelta, datetime

# ==============================================================================
# 1. Configuration & Authentication
# ==============================================================================

# 🔑 ACTION: Replace with your actual API key!
API_KEY = "new1_7b60e436d2304ce8838ce460d0e61e56"

# 🌐 API Endpoint
BASE_URL = "https://api.twitterapi.io/twitter/tweet/advanced_search"

# 🗓️ Define the FULL research period
START_OF_RESEARCH = date(2025, 9, 29)
END_OF_RESEARCH = date(2025, 9, 30)

# ==============================================================================
# 2. *** NEW: COST CONTROL ***
# ==============================================================================
# This new variable limits how may pages of results we get for each day.
# Set to 2, it will fetch a maximum of ~200 tweets per day (if 100 per page).
# This prevents the script from running indefinitely and controls costs.
MAX_PAGES_PER_DAY = 2

# ==============================================================================
# 3. Keyword Grouping & Query Structure (Improved Logic)
# ==============================================================================

# G1: Tariff/Trade (Must be present)
TARIFF_TRADE_KEYWORDS = "(tariff OR tariffs OR \"trade war\" OR imports OR exports OR trade)"

# G2: Industry-Specific Terms (Must be present)
# NOTE: The mandatory 'MARKET_FINANCE_KEYWORDS' group has been removed from the
# query to broaden the collection, as per the methodological review.
INDUSTRY_KEYWORDS = {
    "Tech": "(semiconductor OR chip OR AI OR \"artificial intelligence\" OR GPU OR \"data center\" OR Apple OR AAPL OR NVIDIA OR NVDA OR hardware OR software OR tech OR \"chip ban\" OR \"tech exports\")",
    "Agri": "(farming OR \"farm equipment\" OR tractor OR Deere OR DE OR \"Archer Daniels Midland\" OR ADM OR agri OR farm OR food OR \"farm subsidy\")",
    "Energy": "(oil OR gas OR Chevron OR CVX OR Tesla OR TSLA OR EV OR \"electric vehicle\" OR battery OR renewable OR solar OR wind)"
}

# ==============================================================================
# 4. Data Collection Function (Now with page limit)
# ==============================================================================

def fetch_tweets_daily_chunk(query_string, api_key, max_pages):
    """
    Fetches tweets for a given query, stopping after a max number of pages.
    """
    all_tweets_data = []
    next_page_cursor = None
    pages_fetched = 0

    HEADERS = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }

    # print(f"    -> Query: {query_string}")

    while True:
        # *** CHANGE: Stop fetching if we have reached our page limit for the day ***
        if pages_fetched >= max_pages:
            print(f"    -> Reached page limit of {max_pages}. Moving to next day.")
            break

        params = {
            'query': query_string,
            'queryType': 'Top'
        }
        
        if next_page_cursor:
            params['cursor'] = next_page_cursor
        
        try:
            response = requests.get(BASE_URL, headers=HEADERS, params=params)
            response.raise_for_status() 
            data = response.json()
            pages_fetched += 1 # Increment page counter after a successful call
            
        except requests.exceptions.RequestException as e:
            print(f"    ERROR: API call failed: {e}")
            if 'response' in locals():
                print(f"    Status: {response.status_code}. Details: {response.text}")
            break
        
        if 'tweets' in data and data['tweets']:
            tweets_in_batch = data['tweets']
            print(f"    -> Fetched {len(tweets_in_batch)} tweets (Page {pages_fetched}/{max_pages}).")
            
            for tweet in tweets_in_batch:
                all_tweets_data.append({
                    'timestamp': tweet.get('createdAt'),
                    'text': tweet.get('text')
                })
        else:
            print("    -> No more tweets found for this day.")
            break

        if data.get('has_next_page'):
            next_page_cursor = data.get('next_cursor')
            time.sleep(6) # Pause between pages
        else:
            break
            
    return all_tweets_data

# ==============================================================================
# 5. Main Collection Loop (Now Iterates Day by Day)
# ==============================================================================

def run_full_collection_for_industry(industry_name, industry_query, api_key):
    """
    Collects data for a single industry across the full research period,
    using 1-day windows to enable daily sampling limits.
    """
    # *** CHANGE: The loop now moves one day at a time ***
    current_date = START_OF_RESEARCH
    all_industry_tweets = []
    
    base_query = f"{TARIFF_TRADE_KEYWORDS} {industry_query} lang:en -filter:retweets -filter:replies -@tariff_ai"

    print(f"\n=========================================================")
    print(f"--- STARTING {industry_name.upper()} DATA COLLECTION ---")
    print(f"=========================================================")
    
    while current_date <= END_OF_RESEARCH:
        # Define the end of the day
        end_date_chunk = current_date + timedelta(days=1)
        
        start_date_str = current_date.isoformat()
        end_date_str = end_date_chunk.isoformat()
        
        final_query = f"{base_query} since:{start_date_str} until:{end_date_str}"
        
        print(f"\n** Searching Date: {start_date_str} **")
        
        daily_data = fetch_tweets_daily_chunk(
            query_string=final_query,
            api_key=api_key,
            max_pages=MAX_PAGES_PER_DAY # Pass the new limit
        )
        
        if daily_data:
            all_industry_tweets.extend(daily_data)
            print(f"    -> Collected {len(daily_data)} tweets for this day. Total for {industry_name}: {len(all_industry_tweets)}")

        current_date = end_date_chunk
        time.sleep(6) # Small pause between days

    # --- Final Save ---
    if all_industry_tweets:
        df = pd.DataFrame(all_industry_tweets)
        df['industry'] = industry_name
        df = df.drop_duplicates(subset=['text', 'timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        
        output_filename = f"{industry_name.lower()}_tweets_full_dataset_{START_OF_RESEARCH}_to_{END_OF_RESEARCH}.csv"
        df.to_csv(output_filename, index=False, encoding='utf-8')
        
        print(f"\n\n✅ FULL DATASET SAVED for {industry_name}!")
        print(f"   Total Unique Tweets: {len(df)}")
        print(f"   File: {output_filename}")
    else:
        print(f"\n\n❌ WARNING: No tweets collected for {industry_name} during the entire period.")
        
# ==============================================================================
# 6. EXECUTION BLOCK
# ==============================================================================

if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY_HERE":
        print("FATAL ERROR: Please replace 'YOUR_API_KEY_HERE' in Section 1 with your actual API key.")
    else:
        # Run collection for each industry
        # run_full_collection_for_industry(
        #     "Tech", 
        #     INDUSTRY_KEYWORDS["Tech"], 
        #     API_KEY
        # )
        # run_full_collection_for_industry(
        #     "Agri", 
        #     INDUSTRY_KEYWORDS["Agri"], 
        #     API_KEY
        # )
        run_full_collection_for_industry(
            "Energy", 
            INDUSTRY_KEYWORDS["Energy"], 
            API_KEY
        )
        print("\n\n🎉 All data collection complete.")