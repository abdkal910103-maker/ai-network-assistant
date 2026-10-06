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


def ask_ai(prompt, instructions):
    response = client.responses.create(
        model="openai/gpt-oss-20b",
        instructions=instructions,
        input=prompt
    )

    return response.output_text


@app.route("/")
def home():
    return render_template("index.html")


# Feature 1: General networking questions
@app.route("/api/ask", methods=["POST"])
def ask_ai_question():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "error": "Please enter a networking question."
            }), 400

        answer = ask_ai(
            question,
            (
                "You are an AI assistant specialized in computer networking. "
                "Explain networking concepts clearly and accurately. "
                "Use simple examples when useful."
            )
        )

        return jsonify({"answer": answer})

    except Exception as error:
        print("AI API error:", error)

        return jsonify({
            "error": "The AI service is temporarily unavailable. Please try again."
        }), 500


# Feature 2: Network troubleshooting
@app.route("/api/troubleshoot", methods=["POST"])
def troubleshoot():
    try:
        data = request.get_json()
        problem = data.get("problem", "").strip()

        if not problem:
            return jsonify({
                "error": "Please describe your network problem."
            }), 400

        answer = ask_ai(
            problem,
            (
                "You are a professional network troubleshooting assistant. "
                "Analyze the user's networking problem and provide a practical "
                "step-by-step troubleshooting procedure. "
                "Mention possible causes and useful commands such as ping, "
                "ipconfig, tracert, nslookup, or Linux equivalents when relevant. "
                "Keep the instructions clear and beginner-friendly."
            )
        )

        return jsonify({"answer": answer})

    except Exception as error:
        print("Troubleshooting API error:", error)

        return jsonify({
            "error": "The troubleshooting service is temporarily unavailable."
        }), 500


# Feature 3: Network command generator
@app.route("/api/commands", methods=["POST"])
def generate_commands():
    try:
        data = request.get_json()
        request_text = data.get("request", "").strip()

        if not request_text:
            return jsonify({
                "error": "Please describe what you want to check."
            }), 400

        answer = ask_ai(
            request_text,
            (
                "You are a computer networking command assistant. "
                "Generate useful networking commands based on the user's request. "
                "When appropriate, provide commands for Windows, Linux, and Cisco IOS. "
                "Clearly label each operating system or platform. "
                "Briefly explain what each command does."
            )
        )

        return jsonify({"answer": answer})

    except Exception as error:
        print("Command generator API error:", error)

        return jsonify({
            "error": "The command generator is temporarily unavailable."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)