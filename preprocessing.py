import pandas as pd
import re # Regular expression library
import string # For punctuation handling
import html # For HTML entities
import emoji

# --- Preprocessing Function ---

def preprocess_tweet(text):
    """
    Cleans raw tweet text for sentiment analysis with FinBERT.
    Applies steps: lowercase, remove URLs, remove mentions, remove emojis,
    REDUCE consecutive punctuation, handle hashtags, remove HTML entities,
    remove extra whitespace/newlines, remove ambiguous unicode.
    """
    if not isinstance(text, str):
        return "" # Return empty string if input is not text (e.g., NaN)

    # 1. Lowercase
    text = text.lower()

    # 2. Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # 3. Remove Mentions (@ tags)
    text = re.sub(r'@\w+', '', text)

    # 4. Remove Emojis
    # 4. Remove Emojis (expanded pattern)
    # emoji_pattern = re.compile("["
    #                         u"\U0001F600-\U0001F64F"  # emoticons
    #                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    #                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
    #                         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    #                         u"\U00002702-\U000027B0"  # Dingbats
    #                         u"\U000024C2-\U0001F251"
    #                         u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    #                         u"\u2600-\u26FF"          # Miscellaneous Symbols
    #                         # Add more ranges if needed after inspection
    #                         "]+", flags=re.UNICODE)
    # # The line below that uses the pattern remains the same:
    # # text = emoji_pattern.sub(r'', text)
    # text = emoji_pattern.sub(r'', text)
    # 4. Remove Emojis (using emoji library)
    text = emoji.replace_emoji(text, replace='')

    # 5. Handle Hashtags: Remove '#' but keep the word
    text = re.sub(r'#(\w+)', r'\1', text)

    # 6. *** MODIFIED: Reduce Consecutive Punctuation to Single ***
    # Creates a pattern to find any punctuation character (escaped for regex)
    punct_chars = re.escape(string.punctuation)
    # Finds any character in punct_chars (group 1) followed by 1 or more
    # repetitions of that same character (\1+), replaces with just the character (\1)
    text = re.sub(r'([' + punct_chars + r'])\1+', r'\1', text)

    # 7. Remove HTML Entities (like &amp;, &lt;)
    text = html.unescape(text)

    # 8. Remove Ambiguous Unicode Characters
    # 8. Remove Ambiguous Unicode Characters (expanded list)
    text = re.sub(r'[\u200B\u200D\uFEFF\u00A0\u2066\u2069]', '', text)

    # 9. Remove Multiple Newlines and replace with a space
    text = re.sub(r'\n+', ' ', text)

    # 10. Remove Extra Whitespace
    text = text.strip()
    text = re.sub(r'\s{2,}', ' ', text)

    return text

# --- CHOOSE THE INDUSTRY YOU ARE PROCESSING ---
industry_to_process = 'tech' # Options: 'agri', 'energy', 'tech'
# --- LOAD THE CORRECT FILE ---
merged_file = f'{industry_to_process}_tweets_merged_full_dataset.csv'

try:
    df = pd.read_csv(merged_file)
    print(f"Successfully loaded {merged_file}")

    # Make sure the 'text' and 'industry' columns exist
    if 'text' in df.columns and 'industry' in df.columns:
        print("Applying preprocessing to the 'text' column...")
        # Create the 'cleaned_text' column
        df['cleaned_text'] = df['text'].apply(preprocess_tweet)
        print("Preprocessing complete. New column 'cleaned_text' added.")

        # --- SELECT AND SAVE DESIRED COLUMNS ---
        # Define the columns we want to keep
        columns_to_keep = ['timestamp', 'industry', 'cleaned_text']

        # Ensure 'timestamp' exists before trying to select it
        if 'timestamp' not in df.columns:
            print("ERROR: 'timestamp' column not found. Cannot proceed with saving.")
        else:
            # Create a new DataFrame with only the desired columns
            preprocessed_df = df[columns_to_keep].copy() # Use .copy() to avoid SettingWithCopyWarning

            # Optional: Display the first few rows of the new DataFrame
            print("\n--- Sample of the DataFrame to be saved ---")
            print(preprocessed_df.head())
            print("------------------------------------------")

            # Define the output filename
            output_preprocessed_file = f'{industry_to_process}_tweets_preprocessed.csv'

            # Save the new DataFrame to a CSV file
            try:
                preprocessed_df.to_csv(output_preprocessed_file, index=False, encoding='utf-8')
                print(f"✅ Saved preprocessed data (timestamp, industry, cleaned_text) to: {output_preprocessed_file}")
            except Exception as e:
                print(f"  ERROR saving file {output_preprocessed_file}: {e}")
        # ------------------------------------------

    else:
        missing_cols = []
        if 'text' not in df.columns:
            missing_cols.append('text')
        if 'industry' not in df.columns:
            missing_cols.append('industry')
        print(f"ERROR: Required column(s) {missing_cols} not found in the DataFrame.")

except FileNotFoundError:
    print(f"ERROR: File not found - {merged_file}. Make sure the file exists in the correct directory.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")