from flask import Flask
from bot import start_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "IA Investidora está rodando!"

if __name__ == '__main__':
    start_bot()
    app.run(host='0.0.0.0', port=8080)
