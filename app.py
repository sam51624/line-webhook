from flask import Flask, request
from openai import OpenAI
import requests
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

@app.route('/')
def index():
    return "LINE Webhook is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "events" not in data:
        return "No events", 200

    for event in data["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_msg = event["message"]["text"]
            reply_token = event["replyToken"]
            ai_response = ask_gpt(user_msg)
            reply_to_line(reply_token, ai_response)
    return "OK", 200

def ask_gpt(message):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "คุณคือผู้ช่วยอัจฉริยะ"},
                {"role": "user", "content": message}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return "ขออภัย ระบบมีปัญหาชั่วคราว กรุณาลองใหม่อีกครั้ง"

def reply_to_line(reply_token, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)

if __name__ == '__main__':
    app.run()
