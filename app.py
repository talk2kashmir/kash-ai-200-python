import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import AzureOpenAI

load_dotenv()

open_ai_endpoint = os.getenv("OPEN_AI_ENDPOINT")
open_ai_key = os.getenv("OPEN_AI_KEY")
chat_model = os.getenv("CHAT_MODEL")
vector_model = os.getenv("VECTOR_MODEL")

print(f"OPEN_AI_ENDPOINT: {open_ai_endpoint}")
print(f"OPEN_AI_KEY: {open_ai_key}")
print(f"CHAT_MODEL: {chat_model}")
print(f"VECTOR_MODEL: {vector_model}")


client = AzureOpenAI(
	api_key=open_ai_key,
	azure_endpoint=open_ai_endpoint,
	api_version="2025-01-01-preview",
)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
	return jsonify({"status": "ok"}), 200

@app.route("/chat", methods=["POST"])
def chat():
	data = request.get_json()
	print(f"data:", data)
	user_message = data.get("message", "")
	print(f"user_message:", user_message)
	response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                },
            ],
            max_completion_tokens=2000,
            temperature=1,
            model=chat_model,
        )
	assistant_reply = response.choices[0].message.content
	print(f"assistant_reply:", assistant_reply)
	return assistant_reply


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)







