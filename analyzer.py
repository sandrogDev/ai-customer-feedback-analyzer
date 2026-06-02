import os
import time
from dotenv import load_dotenv
from google import genai

# 1. Load environment variables (the "safe")
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Error: API Key not found in the .env file!")

# 2. Initialize the Gemini client
client = genai.Client(api_key=API_KEY)

print("System ready. Starting file reading...\n")

# 3. Read raw data from file
with open("reviews.txt", "r", encoding="utf-8") as file:
    raw_lines = file.readlines()

# Clean the data
reviews = [line.strip() for line in raw_lines if line.strip() != ""]

# 4. The strict System Prompt in English
system_instruction = (
    "You are an expert e-commerce data analyst. Analyze the provided customer review. "
    "You MUST return ONLY 3 pieces of information, separated by the '|' (pipe) symbol, in a single line.\n"
    "Required information:\n"
    "1. SENTIMENT: Strictly choose between [Positive, Negative, Neutral]\n"
    "2. CRITICAL AREA: Strictly choose the involved department between [Product, Shipping, Support, Website]\n"
    "3. SUMMARY: Summarize the issue or praise in a maximum of 4 words."
)

print(f"Analyzing {len(reviews)} reviews using Artificial Intelligence...")

# 5. Process data and save to CSV
with open("results.csv", "w", encoding="utf-8") as file_out:
    
    # Write the CSV header (column names)
    file_out.write("Original Review|Sentiment|Critical Area|Summary\n")
    
    for i, review in enumerate(reviews, 1):
        # Build the full prompt
        full_prompt = f"{system_instruction}\n\nReview to analyze: '{review}'"
        
        # Call the AI model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        response_text = response.text.strip()
        print(f"Review #{i}: Completed!")
        
        # Save the structured row to the file
        file_out.write(f"{review}|{response_text}\n")
        
        # Pause to prevent rate-limiting errors (HTTP 503)
        time.sleep(3)

print("\nAWESOME! Analysis completed. Open the 'results.csv' file to see the finished work.")