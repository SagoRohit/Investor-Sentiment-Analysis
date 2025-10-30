# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import matplotlib.dates as mdates
# from datetime import datetime

# # --- Configuration ---
# # This is the file you create by running the aggregation script
# input_file = 'daily_sentiment_index_all_industries.csv'
# output_image_file = 'daily_sentiment_index_plot.png'

# # Define the tariff announcement dates
# # (from Keywords_(Project_Shillong)[1].pdf, sources 328, 336, 339)
# tariff_events = {
#     '2025-01-20': '25% Tariffs on Canada/Mexico',
#     '2025-04-02': '"Liberation Day" Tariffs',
#     '2025-08-01': 'New Tariff Regime'
# }
# # --- End Configuration ---

# print(f"Attempting to load data from {input_file}...")
# try:
#     df = pd.read_csv(input_file)
# except FileNotFoundError:
#     print(f"---")
#     print(f"ERROR: Input file not found: {input_file}")
#     print(f"Please make sure you have run the aggregation script first to create this file.")
#     print(f"---")
#     exit()
# except Exception as e:
#     print(f"Error loading file: {e}")
#     exit()

# # --- Data Preparation ---
# # 1. Convert 'date' column to datetime objects for plotting
# try:
#     df['date'] = pd.to_datetime(df['date'])
# except KeyError:
#     print("ERROR: 'date' column not found in the file.")
#     exit()
# except Exception as e:
#     print(f"Error converting 'date' column: {e}")
#     exit()

# # 2. Check for required columns
# if 'daily_sentiment_score' not in df.columns or 'industry' not in df.columns:
#     print("ERROR: 'daily_sentiment_score' or 'industry' column not found.")
#     exit()

# print("Data loaded and prepared. Generating plot...")

# # --- Plotting ---
# # 1. Set a professional style (seaborn-whitegrid is clean for papers)
# sns.set(style="whitegrid", context="paper", font_scale=1.1)

# # 2. Create the figure and axes
# fig, ax = plt.subplots(figsize=(12, 7)) # Good size for a paper (width, height)

# # 3. Create the line plot
# lineplot = sns.lineplot(
#     data=df,
#     x='date',
#     y='daily_sentiment_score',
#     hue='industry',
#     palette='colorblind', # Good for accessibility
#     ax=ax,
#     linewidth=1.2 # Clean, thin lines
# )

# # 4. Add a horizontal line at y=0 (to separate positive/negative)
# ax.axhline(0, ls='--', color='black', linewidth=1, alpha=0.7, label='Neutral Sentiment')

# # 5. Add vertical lines for tariff events
# event_dates = [datetime.strptime(date, '%Y-%m-%d') for date in tariff_events.keys()]
# event_labels = list(tariff_events.values())

# for i, date in enumerate(event_dates):
#     ax.axvline(x=date, color='red', linestyle=':', linewidth=1.5, alpha=0.8)
#     # Add text labels for the events
#     # This tries to stagger the labels to avoid overlap
#     ax.text(date + pd.Timedelta(days=2), # Offset text slightly from line
#             ax.get_ylim()[1] - (i * 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0])), 
#             f'{event_labels[i]} ({date.strftime("%b %d")})', 
#             color='red', 
#             ha='left', 
#             fontsize=9,
#             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

# # 6. Customize Title and Labels (essential for a paper)
# ax.set_title(
#     'Daily Investor Sentiment Index by Industry (2025)',
#     fontsize=16,
#     fontweight='bold',
#     pad=20 
# )
# ax.set_ylabel('Daily Sentiment Score (Mean)', fontsize=12)
# ax.set_xlabel('Date', fontsize=12)

# # 7. Format the X-axis (Date)
# ax.xaxis.set_major_locator(mdates.MonthLocator()) # One tick per month
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
# ax.set_xlim(df['date'].min(), df['date'].max()) # Ensure plot spans the whole period
# plt.xticks(rotation=45, ha='right')

# # 8. Customize the Legend
# handles, labels = ax.get_legend_handles_labels()
# # Manually add the 'Neutral Sentiment' line to the legend
# handles.append(plt.Line2D([0], [0], ls='--', color='black', linewidth=1, alpha=0.7))
# labels.append('Neutral Sentiment')

# legend = ax.legend(handles=handles, labels=labels, title='Legend')
# plt.setp(legend.get_title(), fontsize='12', fontweight='bold')
# # Place legend outside the plot
# sns.move_legend(ax, "upper left", bbox_to_anchor=(1.02, 1))

# # 9. Final Touches
# sns.despine() # Remove top and right spines
# plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend

# # 10. Save the figure
# try:
#     fig.savefig(output_image_file, dpi=300, bbox_inches='tight') 
#     print(f"\n✅ Successfully saved plot to: {output_image_file}")
# except Exception as e:
#     print(f"Error saving plot: {e}")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime
import os

# --- Configuration ---
input_file = 'daily_sentiment_index_all_industries.csv'

# Define the tariff announcement dates
# (from Keywords_(Project_Shillong)[1].pdf)
tariff_events = {
    '2025-01-20': '25% Tariffs on Canada/Mexico',
    '2025-04-02': '"Liberation Day" Tariffs',
    '2025-08-01': 'New Tariff Regime'
}
event_dates = [datetime.strptime(date, '%Y-%m-%d') for date in tariff_events.keys()]
event_labels = list(tariff_events.values())
# --- End Configuration ---

print(f"Attempting to load data from {input_file}...")
try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"---")
    print(f"ERROR: Input file not found: {input_file}")
    print(f"Please make sure you have run the aggregation script first to create this file.")
    print(f"---")
    exit()
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# --- Data Preparation ---
try:
    df['date'] = pd.to_datetime(df['date'])
except KeyError:
    print("ERROR: 'date' column not found in the file.")
    exit()

if 'daily_sentiment_score' not in df.columns or 'industry' not in df.columns:
    print("ERROR: 'daily_sentiment_score' or 'industry' column not found.")
    exit()

# Get unique industry names
industries = df['industry'].unique()
print(f"Data loaded. Found industries: {industries}")

# --- Plotting Loop (One plot per industry) ---
for industry in industries:
    print(f"\nGenerating plot for: {industry.capitalize()}...")
    
    # 1. Filter data for the current industry
    industry_df = df[df['industry'] == industry].copy()
    
    if industry_df.empty:
        print(f"  No data found for {industry}. Skipping plot.")
        continue

    # 2. Set professional style
    sns.set(style="whitegrid", context="paper", font_scale=1.1)
    
    # 3. Create a NEW figure and axes for each plot
    fig, ax = plt.subplots(figsize=(12, 7))

    # 4. Create the line plot
    sns.lineplot(
        data=industry_df,
        x='date',
        y='daily_sentiment_score',
        color='navy', # Use a single, professional color
        ax=ax,
        linewidth=1.5
    )

    # 5. Add a horizontal line at y=0
    ax.axhline(0, ls='--', color='black', linewidth=1, alpha=0.7, label='Neutral Sentiment')

    # 6. Add vertical lines for tariff events
    for i, date in enumerate(event_dates):
        ax.axvline(x=date, color='red', linestyle=':', linewidth=1.5, alpha=0.8)
        # Add text labels
        ax.text(date + pd.Timedelta(days=2), 
                ax.get_ylim()[1] - (i * 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0])), 
                f'{event_labels[i]} ({date.strftime("%b %d")})', 
                color='red', 
                ha='left', 
                fontsize=9,
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    # 7. Customize Title and Labels
    ax.set_title(
        f'Daily Investor Sentiment Index - {industry.capitalize()} (2025)',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    ax.set_ylabel('Daily Sentiment Score (Mean)', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)

    # 8. Format the X-axis (Date)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    ax.set_xlim(industry_df['date'].min(), industry_df['date'].max())
    plt.xticks(rotation=45, ha='right')
    
    # 9. Add a simple legend for the neutral line
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    # 10. Final Touches
    sns.despine()
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # 11. Save the figure with a unique name
    output_image_file = f'daily_sentiment_plot_{industry.lower()}.png'
    try:
        fig.savefig(output_image_file, dpi=300, bbox_inches='tight')
        print(f"  ✅ Successfully saved plot to: {output_image_file}")
    except Exception as e:
        print(f"  Error saving plot: {e}")

print("\nAll individual plots generated.")