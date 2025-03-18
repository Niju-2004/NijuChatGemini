from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API = os.getenv("GEM_key")
if not GEMINI_API:
    raise ValueError("Please set the GEMINI_API environment variable in your .env file.")

genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.form['user_input']
    
    if user_query.lower() == 'quit':
        return jsonify({'response': 'Goodbye! 👋'})
    
    response = model.generate_content(user_query)
    return jsonify({'response': response.text if response else "No response from Gemini."})

if __name__ == '__main__':
    app.run(debug=True)