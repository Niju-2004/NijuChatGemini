from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import socket

# Load environment variables
load_dotenv()
GEMINI_API = os.getenv("GEMINI_API")  # Ensure this matches the key in Render's environment variables
if not GEMINI_API:
    raise ValueError("Please set the GEMINI_API environment variable in your .env file or Render dashboard.")

genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_query = request.form['user_input']
        
        if user_query.lower() == 'quit':
            return jsonify({'response': 'Goodbye! 👋'})
        
        response = model.generate_content(user_query)
        return jsonify({'response': response.text if response else "No response from Gemini."})
    
    except Exception as e:
        logging.error(f"Error processing chat request: {e}")
        return jsonify({'response': f"An error occurred: {str(e)}"}), 500

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to an external server (doesn't actually send data)
        s.connect(("8.8.8.8", 80))
        # Get the socket's own address
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logging.error(f"Failed to get local IP address: {e}")
        return "127.0.0.1"  # Fallback to localhost

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Use Render's PORT environment variable
    ip = get_local_ip()
    logging.info(f"The app is running on http://{ip}:{port}")
    print(f"The app is running on http://{ip}:{port}")
    app.run(debug=False, host="0.0.0.0", port=port)  # Disable debug mode for production