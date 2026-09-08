from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "error": "Please enter a networking question."
            }), 400

        response = client.responses.create(
            model="openai/gpt-oss-20b",
            instructions=(
                "You are an AI assistant specialized in computer networking. "
                "Explain networking concepts clearly and accurately."
            ),
            input=question
        )

        return jsonify({
            "answer": response.output_text
        })

    except Exception as error:
        print("AI API error:", error)

        return jsonify({
            "error": "The AI service is temporarily unavailable. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)