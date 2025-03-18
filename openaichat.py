import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEM_KEY = os.getenv("GEMINI_API_KEY")

if not GEM_KEY:
    print("Error: API key not found. Set GEMINI_API_KEY in the .env file.")
    exit(1)

# Configure Gemini API
genai.configure(api_key=GEM_KEY)

# Create chat model
model = genai.GenerativeModel("gemini-pro")

print("Gemini Chatbot (Type 'exit' to quit)")

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Gemini: Goodbye!")
        break

    response = model.generate_content(user_input)
    print(f"Gemini: {response.text}\n")
