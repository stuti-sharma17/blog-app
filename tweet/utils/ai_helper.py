from transformers import pipeline, set_seed

# Load the model only once when the file is imported
generator = pipeline(
    "text-generation",
    model="distilgpt2",
    tokenizer="distilgpt2",
    truncation=True,               # explicit truncation
    pad_token_id=50256             # GPT-2's EOS token
)

set_seed(42)  # Optional: for reproducible results

def generate_tweet_idea(prompt, max_length=50):
    """
    Generate a short tweet idea from a given prompt using GPT-2.
    Returns a single generated string or error message.
    """
    try:
        result = generator(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]["generated_text"].strip()
    except Exception as e:
        return f"Error generating tweet: {str(e)}"
