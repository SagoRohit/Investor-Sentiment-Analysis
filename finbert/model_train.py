import pandas as pd
import torch # PyTorch is needed for Hugging Face transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax # To convert logits to probabilities
import numpy as np # For batch processing

# --- Configuration ---
# 1. Define the FinBERT model name
model_name = "ProsusAI/finbert"

# 2. Choose the industry file to process
industry_to_process = 'energy' # Options: 'agri', 'energy', 'tech'
preprocessed_file = f'{industry_to_process}_tweets_preprocessed.csv'
output_file = f'{industry_to_process}_tweets_sentiment.csv'

# 3. Set the batch size (adjust based on your RAM/GPU memory, 16 or 32 is usually good)
BATCH_SIZE = 16
# --- End Configuration ---

# --- Load Model and Tokenizer ---
try:
    print(f"Loading FinBERT model ({model_name})... This might take a moment.")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    # Optional: If you have a CUDA-enabled GPU, uncomment the next line
    # model.to('cuda') # Move model to GPU for faster processing
    print("Model and Tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    exit() # Stop if model can't be loaded

# --- Load Preprocessed Data ---
try:
    df = pd.read_csv(preprocessed_file)
    print(f"Loaded preprocessed data from {preprocessed_file} ({len(df)} rows).")
    # Ensure the cleaned_text column is string type and handle potential NaNs
    if 'cleaned_text' in df.columns:
        df['cleaned_text'] = df['cleaned_text'].astype(str).fillna('')
    else:
        print("ERROR: 'cleaned_text' column not found.")
        exit()
except FileNotFoundError:
    print(f"ERROR: File not found - {preprocessed_file}")
    exit()
except Exception as e:
    print(f"An error occurred loading the CSV: {e}")
    exit()

# --- Sentiment Prediction Function ---
def get_sentiment_batch(texts):
    """
    Analyzes a batch of texts using the loaded FinBERT model.
    Returns lists of probabilities for positive, negative, and neutral sentiments.
    """
    try:
        # Tokenize the batch
        inputs = tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
        
        # Optional: Move inputs to GPU if model is on GPU
        # if model.device.type == 'cuda':
        #     inputs = {k: v.to('cuda') for k, v in inputs.items()}

        # Get model predictions (no gradient calculation needed)
        with torch.no_grad():
            outputs = model(**inputs)

        # Apply softmax to convert logits to probabilities
        probabilities = softmax(outputs.logits.cpu().numpy(), axis=1) # Move logits to CPU before numpy

        # Probabilities are usually ordered [positive, negative, neutral] for this model
        # Verify this order based on model.config.id2label if needed
        # print(model.config.id2label) # -> {0: 'positive', 1: 'negative', 2: 'neutral'}

        pos_probs = probabilities[:, 0].tolist() # Probability of positive
        neg_probs = probabilities[:, 1].tolist() # Probability of negative
        neu_probs = probabilities[:, 2].tolist() # Probability of neutral

        return pos_probs, neg_probs, neu_probs

    except Exception as e:
        print(f"Error processing batch: {e}")
        # Return empty lists or lists of NaNs of the correct size
        batch_size = len(texts)
        return [np.nan] * batch_size, [np.nan] * batch_size, [np.nan] * batch_size


# --- Apply Function to DataFrame in Batches ---
# Prepare lists to store results
all_pos_probs = []
all_neg_probs = []
all_neu_probs = []

print(f"Starting sentiment analysis in batches of {BATCH_SIZE}...")
num_batches = int(np.ceil(len(df) / BATCH_SIZE))

for i in range(num_batches):
    start_index = i * BATCH_SIZE
    end_index = min((i + 1) * BATCH_SIZE, len(df))
    batch_texts = df['cleaned_text'][start_index:end_index].tolist()

    if not batch_texts:
        continue

    pos_probs, neg_probs, neu_probs = get_sentiment_batch(batch_texts)

    all_pos_probs.extend(pos_probs)
    all_neg_probs.extend(neg_probs)
    all_neu_probs.extend(neu_probs)

    print(f"  Processed batch {i+1}/{num_batches}")

print("Sentiment analysis complete.")

# --- Add Results to DataFrame ---
if len(all_pos_probs) == len(df):
    df['sentiment_positive'] = all_pos_probs
    df['sentiment_negative'] = all_neg_probs
    df['sentiment_neutral'] = all_neu_probs

    # Calculate the combined sentiment score
    df['sentiment_score'] = df['sentiment_positive'] - df['sentiment_negative']

    print("Added sentiment probabilities and score columns to DataFrame.")

    # Optional: Display sample results
    print("\n--- Sample of Data with Sentiment Scores ---")
    print(df[['timestamp', 'industry', 'cleaned_text', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'sentiment_score']].head())
    print("------------------------------------------")

    # --- Save Results ---
    try:
        # Keep only essential columns + sentiment results for the next step
        output_df = df[['timestamp', 'industry', 'cleaned_text', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'sentiment_score']]
        output_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ Successfully saved sentiment results to: {output_file}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")

else:
    print("ERROR: Length mismatch between original DataFrame and sentiment results. Cannot add columns.")