import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

try:
    genai.configure(api_key="AIzaSyB8nlDylteUgHw_yFciUCTi2lPegShgAW0")
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    
app = Flask(__name__)

def chat_with_gemini(prompt):
    """
    Generates content using the Gemini model.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Provide a user-friendly error message if the API call fails
        return f"An error occurred while chatting with Gemini: {e}"

@app.route("/")
def index():
    """
    Renders the main chat interface HTML page.
    """
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    """
    API endpoint to handle chat requests (POST method).
    """
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"response": "Please provide a message."}), 400

    chatbot_response = chat_with_gemini(user_input)

    # Return the response as JSON
    return jsonify({"response": chatbot_response})

if __name__ == "__main__":
    app.run(debug=True)