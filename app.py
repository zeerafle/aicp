from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import json

import datetime

load_dotenv()

app = Flask(__name__)
KOBOLD_URL = "http://localhost:8005"
PRE_PROMPT = "Here are current additional information. You're free to whether to talk about this or not\n"
USER = 'zeerafle'


# mask koboldai api
@app.route('/<path:path>', methods=['GET', 'POST'])
def api(path):
    print(path)
    # Handle specific route with custom processing
    if path == 'v1/completions':
        # Custom processing before forwarding
        data = proxy(request.json)
        
        # Forward the modified request to KoboldCPP
        response = requests.post(f"{KOBOLD_URL}/v1/completions", json=data)
        return jsonify(response.json())
    
    print(f"{KOBOLD_URL}/{path}")
    # For all other API calls, forward them directly without modification
    try:
        response = requests.request(
            method=request.method,
            url=f"{KOBOLD_URL}/{path}",
            headers={key: value for key, value in request.headers if key != 'Host'},
            json=request.json if request.method == 'POST' else None,
            params=request.args,
        )
        return jsonify(response.json())
    except Exception as e:
        print(e)
        return 'Fail'


def proxy(data):
    # Inject real-time data here
    add_prompt = PRE_PROMPT + f"Current time: {get_time()}\nCurrently listening: {get_recent_tracks()}"
    data['prompt'] = f'{add_prompt}\n{data['prompt']}'
    print(data)
    return data


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
        return f'{artist} - {title}'


if __name__ == '__main__':
    app.run(port=5000)