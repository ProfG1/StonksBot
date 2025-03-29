from flask import Flask
from threading import Thread
from dotenv import load_dotenv
import os

# Initialize the Flask app
app = Flask(__name__)

load_dotenv()

@app.route('/')
def index():
    return "Alive"

def run():
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def const_online():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    const_online()
