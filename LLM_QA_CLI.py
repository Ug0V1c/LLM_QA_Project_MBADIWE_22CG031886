import string
import os
import google.generativeai as genai

# --- CONFIGURATION ---

API_KEY = "AIzaSyAOqxBWmA_l33J2C863vABPfyWDRqKZ3iI"

# Configure the API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def preprocess_input(text):
    """
    1. Lowercase
    2. Remove punctuation
    3. Basic Tokenization (split by whitespace)
    """
    # Lowercase
    text = text.lower()

    # Remove punctuation using translation table
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenization (Creating a list of words)
    tokens = text.split()

    # Return rejoined text for the LLM prompt, or return tokens if logic requires
    return " ".join(tokens)


def get_llm_response(cleaned_text):
    """Sends the processed text to the LLM API."""
    try:
        response = model.generate_content(cleaned_text)
        return response.text
    except Exception as e:
        return f"Error communicating with API: {e}"


def main():
    print("--- CLI Q&A System (Type 'exit' to quit) ---")

    while True:
        user_input = input("\nAsk a question: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # 1. Preprocess
        processed_text = preprocess_input(user_input)
        print(f"[System Log] Processed Query: {processed_text}")

        # 2. Get Answer
        print("Thinking...")
        answer = get_llm_response(processed_text)

        # 3. Display
        print("-" * 40)
        print(f"Answer: {answer}")
        print("-" * 40)


if __name__ == "__main__":
    main()