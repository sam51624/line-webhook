from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return "LINE Webhook is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📨 ได้รับข้อมูลจาก LINE:", data)
    return 'OK'
