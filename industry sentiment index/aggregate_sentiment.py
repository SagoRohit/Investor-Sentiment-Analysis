import pandas as pd

# --- Configuration ---
# 1. List the sentiment files you created in the previous step
sentiment_files = [
    'agri_tweets_sentiment.csv',
    'energy_tweets_sentiment.csv',
    'tech_tweets_sentiment.csv'
]

# 2. Define the name for the final output file
output_file = 'daily_sentiment_index_all_industries.csv'
# --- End Configuration ---

# --- Load and Combine Data ---
all_dfs = []
print("Loading and combining sentiment files...")
for file in sentiment_files:
    try:
        df = pd.read_csv(file)
        # Ensure required columns exist
        if all(col in df.columns for col in ['timestamp', 'industry', 'sentiment_score']):
            all_dfs.append(df)
            print(f"  Loaded {file} ({len(df)} rows).")
        else:
            print(f"  WARNING: Skipping {file} due to missing required columns.")
    except FileNotFoundError:
        print(f"  WARNING: File not found - {file}. Skipping.")
    except Exception as e:
        print(f"  ERROR loading {file}: {e}")

if not all_dfs:
    print("No valid data loaded. Exiting.")
    exit()

# Combine all individual dataframes into one
combined_df = pd.concat(all_dfs, ignore_index=True)
print(f"Combined data into a single DataFrame with {len(combined_df)} total rows.")


# --- Perform Aggregation ---
print("\nAggregating tweet scores into a daily sentiment index...")

# 1. Convert 'timestamp' to datetime objects, handling potential errors
combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], errors='coerce')

# 2. Drop any rows where the timestamp could not be parsed
initial_rows = len(combined_df)
combined_df.dropna(subset=['timestamp'], inplace=True)
if initial_rows > len(combined_df):
    print(f"  Removed {initial_rows - len(combined_df)} rows with invalid timestamps.")

# 3. Extract the date part from the timestamp
combined_df['date'] = combined_df['timestamp'].dt.date

# 4. Group by 'date' and 'industry', then calculate the mean of 'sentiment_score'
#    Also, add a count of tweets per day for additional insight
daily_sentiment_index = combined_df.groupby(['date', 'industry']).agg(
    daily_sentiment_score=('sentiment_score', 'mean'),
    tweet_count=('sentiment_score', 'count')
).reset_index()

print("Aggregation complete.")

# --- Save the Final Index ---
try:
    # Sort the final index by date and then by industry for clarity
    daily_sentiment_index.sort_values(by=['date', 'industry'], inplace=True)

    daily_sentiment_index.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✅ Successfully saved the final daily sentiment index to: {output_file}")

    print("\n--- Sample of the Final Daily Sentiment Index ---")
    print(daily_sentiment_index.head(10))
    print("---------------------------------------------")
    print(f"Total daily records created: {len(daily_sentiment_index)}")

except Exception as e:
    print(f"ERROR saving the final index file: {e}")