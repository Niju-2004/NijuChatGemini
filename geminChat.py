import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
GEMINI_API = os.getenv("GEM_KEY", "").strip()
if not GEMINI_API:
    raise ValueError("API Key is missing! Set GEMINI_API in your .env file.")

genai.configure(api_key=GEMINI_API)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 40,
    "max_output_tokens": 1089,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config
)

def chat_with_gemini(user_query):
    try:
        response = model.generate_content(user_query)
        return response.text if response and hasattr(response, "text") else "No valid response from Gemini."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! 👋")
            break
        bot_response = chat_with_gemini(user_query)
        print("\nChatbot:", bot_response)
