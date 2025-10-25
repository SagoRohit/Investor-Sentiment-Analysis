import requests
import json
from datetime import datetime, timezone, timedelta
import time
# ==============================================================================
# Twitter API Test with Your Exact Query - FIXED VERSION
# ==============================================================================

def test_twitter_api_with_query():
    """
    Fixed test using your exact Twitter search query
    """
    # 🔑 Replace with your actual API key
    API_KEY = "**"
    
    # 🌐 API Endpoint
    BASE_URL = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    
    # 🔍 Your exact query from Twitter
    TWITTER_QUERY = "nasa OR usa lang:en until:2025-02-15 since:2025-01-22"
    
    # Headers
    HEADERS = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    print("=" * 70)
    print("🐦 TWITTER API TEST WITH YOUR EXACT QUERY - FIXED")
    print("=" * 70)
    print(f"🔍 Query: {TWITTER_QUERY}")
    print(f"🌐 Endpoint: {BASE_URL}")
    print("-" * 70)
    
    # Convert Twitter-style dates to ISO format for API
    start_time = "2025-01-22T00:00:00Z"
    end_time = "2025-02-15T23:59:59Z"
    
    # API Parameters
    params = {
        'query': TWITTER_QUERY,
        'start_time': start_time,
        'end_time': end_time,
        'max_results': 10,
    }
    
    print(f"📅 Date Range: {start_time} to {end_time}")
    print(f"📊 Max Results: {params['max_results']}")
    print("-" * 70)
    
    try:
        # Make the API request
        print("🔄 Making API request...")
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Call Successful!")
            print(f"📦 Response Keys: {list(data.keys())}")
            print("-" * 70)
            
            # FIX: Check for tweets in the correct key 'tweets' instead of 'data'
            if 'tweets' in data and data['tweets']:
                tweets_found = len(data['tweets'])
                print(f"🎉 SUCCESS! Found {tweets_found} tweets!")
                print(f"📄 Has next page: {data.get('has_next_page', 'N/A')}")
                print("\n" + "=" * 50)
                print("📝 SAMPLE TWEETS:")
                print("=" * 50)
                
                for i, tweet in enumerate(data['tweets'][:5], 1):  # Show first 5 tweets
                    print(f"\n{i}. Tweet ID: {tweet.get('id')}")
                    print(f"   Created: {tweet.get('createdAt')}")
                    print(f"   URL: {tweet.get('url')}")
                    print(f"   Language: {tweet.get('lang')}")
                    print(f"   Text: {tweet.get('text')}")
                    print(f"   Likes: {tweet.get('likeCount')}")
                    print(f"   Retweets: {tweet.get('retweetCount')}")
                    print(f"   Views: {tweet.get('viewCount')}")
                    print("-" * 40)
                
                # Show total count
                print(f"\n📊 TOTAL TWEETS FOUND: {tweets_found}")
                
            else:
                print("❌ No tweets found in 'tweets' key")
                print(f"   Available keys: {list(data.keys())}")
                if 'tweets' in data:
                    print(f"   'tweets' key exists but is empty: {data['tweets']}")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ NETWORK ERROR: Cannot connect to Twitter API")
        print("   Please check your internet connection")
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT ERROR: API request took too long")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {e}")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

# ==============================================================================
# Test with simpler query to verify API works
# ==============================================================================

def test_simple_query():
    """
    Test with a very simple query to confirm basic functionality
    """
    API_KEY = "new1_736fd36e2c8641a9bbe183518fc81aca"
    BASE_URL = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    
    HEADERS = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    print("\n" + "=" * 70)
    print("🔍 SIMPLE QUERY TEST")
    print("=" * 70)
    
    # Very simple query that should definitely return results
    simple_queries = [
        "nasa",
        "usa", 
        "hello",
        "the"
    ]
    
    for i, query in enumerate(simple_queries):
        print(f"\nTesting query: '{query}'")
        if i>0:
            print("Waiting 6 seconds....")
            time.sleep(6)
        params = {
            'query': f"{query} lang:en",
            'start_time': "2025-10-20T00:00:00Z",
            'end_time': "2025-10-21T23:59:59Z",
            'max_results': 5,
        }
        
        try:
            response = requests.get(BASE_URL, headers=HEADERS, params=params)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'tweets' in data and data['tweets']:
                    print(f"  ✅ Found {len(data['tweets'])} tweets")
                else:
                    print(f"  ❌ No tweets found")
            else:
                print(f"  ❌ API error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

# ==============================================================================
# Check API response structure in detail
# ==============================================================================

def check_api_structure():
    """
    Make a small request and show the exact API response structure
    """
    API_KEY = "****"
    BASE_URL = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    
    HEADERS = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    print("\n" + "=" * 70)
    print("🔬 API RESPONSE STRUCTURE ANALYSIS")
    print("=" * 70)
    
    params = {
        'query': "nasa lang:en",
        'start_time': "2025-10-21T00:00:00Z", 
        'end_time': "2025-10-21T23:59:59Z",
        'max_results': 2,
    }
    
    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        data = response.json()
        
        print("Full response structure:")
        print(json.dumps(data, indent=2))
        
        if 'tweets' in data and data['tweets']:
            print(f"\nFirst tweet full structure:")
            print(json.dumps(data['tweets'][0], indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

# ==============================================================================
# RUN THE TESTS
# ==============================================================================

if __name__ == "__main__":
    # Run the fixed main test
    # test_twitter_api_with_query()
    
    # Run simple query tests
    # test_simple_query()
    
    # Uncomment the line below to see the full API response structure
    # check_api_structure()
    
    print("\n" + "=" * 70)
    print("✅ TESTING COMPLETE")
    print("=" * 70)