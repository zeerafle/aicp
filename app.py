from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import json

import datetime

load_dotenv()

app = Flask(__name__)
KOBOLD_URL = "http://localhost:8005/api/v1/generate"
PRE_PROMPT = "Here are current additional information. You're free to whether to talk about this or not\n"
USER = 'zeerafle'

# catch the requested prompt
@app.route('/api/v1/generate', methods=['POST'])
def proxy():
    data = request.json
    # Inject real-time data here
    prompt = PRE_PROMPT + f"Current time: {get_time()}\n\nCurrently listening:\n{get_recent_tracks()}"
    return jsonify(prompt)


def get_time():
    now = datetime.datetime.now()
    return str(now)

def get_recent_tracks():
    params = {"method": "user.getrecenttracks",
              "user": USER,
              "api_key": os.getenv('LASTFM_API_KEY'),
              "limit": 1,
              "format": "json"}
    response = requests.get(os.environ['LASTFM_API_ROOT'], params=params)
    if response.status_code == 200:
        track = response.json()['recenttracks']['track'][0]
        artist = track['artist']['#text']
        title = track['name']
        # print(artist, '-', title)
        return f'{artist} - {title}'


if __name__ == '__main__':
    app.run(port=5000)