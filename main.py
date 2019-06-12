from flask import Flask
from src.flib import sender
from config.config import sleeping_time_in_secs
import time

app = Flask(__name__)

@app.route('/')
def index():
    while True:
        sender()
        time.sleep(sleeping_time_in_secs)