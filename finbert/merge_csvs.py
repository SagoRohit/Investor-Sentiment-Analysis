import pandas as pd
import glob
import os

# --- Configuration ---
# 1. Set the directory where your CSV files are located
#    (Use '.' if the script is in the SAME directory as the CSVs)
data_directory = '.' # Or specify the full path like 'D:\\CODE\\Tariff, Finance\\code'

# 2. Define the prefixes for each industry (must match the start of your filenames)
industry_prefixes = ['agri', 'energy', 'tech']

# 3. Define the output directory (optional, '.' saves in the current directory)
output_directory = '.'
# --- End Configuration ---

print(f"Starting CSV merge process in directory: {os.path.abspath(data_directory)}")

# Loop through each industry
for prefix in industry_prefixes:
    print(f"\nProcessing industry: {prefix.capitalize()}")

    # Construct the search pattern to find all CSV files for this industry
    # This pattern looks for files starting with the prefix, followed by '_tweets_full_dataset_'
    search_pattern = os.path.join(data_directory, f"{prefix}_tweets_full_dataset_*.csv")
    
    # Use glob to find all files matching the pattern
    industry_files = glob.glob(search_pattern)

    if not industry_files:
        print(f"  WARNING: No files found matching pattern: {search_pattern}")
        continue # Skip to the next industry if no files are found

    print(f"  Found {len(industry_files)} files to merge:")
    # for f in industry_files: # Optional: print the files being merged
    #     print(f"    - {os.path.basename(f)}")

    # List to hold individual DataFrames
    df_list = []

    # Read each CSV file and append its DataFrame to the list
    for filename in industry_files:
        try:
            df = pd.read_csv(filename)
            # Add a 'source_file' column (optional, but helpful for tracking)
            # df['source_file'] = os.path.basename(filename) 
            df_list.append(df)
            # print(f"    Read {len(df)} rows from {os.path.basename(filename)}") # Optional: Check rows read
        except Exception as e:
            print(f"  ERROR reading file {filename}: {e}")

    # Concatenate all DataFrames in the list into a single DataFrame
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        print(f"  Successfully concatenated {len(df_list)} files.")

        # --- Data Cleaning (Optional but Recommended) ---
        # 1. Drop exact duplicate rows (based on all columns)
        initial_rows = len(combined_df)
        combined_df = combined_df.drop_duplicates()
        duplicates_removed = initial_rows - len(combined_df)
        if duplicates_removed > 0:
            print(f"  Removed {duplicates_removed} exact duplicate rows.")

        # 2. Convert timestamp and sort (important for time series)
        try:
            combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
            combined_df = combined_df.sort_values(by='timestamp', ascending=True)
            print("  Converted 'timestamp' column to datetime and sorted.")
        except KeyError:
            print("  Warning: 'timestamp' column not found for sorting.")
        except Exception as e:
            print(f"  Error processing 'timestamp' column: {e}")
        # -----------------------------------------------

        # Define the output filename
        output_filename = os.path.join(output_directory, f"{prefix}_tweets_merged_full_dataset.csv")

        # Save the combined DataFrame to a new CSV file
        try:
            combined_df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"✅ Saved merged data for {prefix.capitalize()} to: {output_filename}")
            print(f"   Total unique rows: {len(combined_df)}")
        except Exception as e:
            print(f"  ERROR saving file {output_filename}: {e}")
    else:
        print(f"  No valid dataframes were created for {prefix.capitalize()}. Cannot merge.")

print("\n🎉 CSV merge process complete.")