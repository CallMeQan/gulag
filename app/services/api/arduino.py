import os, json, requests, dotenv

dotenv.load_dotenv()

ARDUINO_URL_HISTORY_DATA = 'https://api2.arduino.cc/iot/v2/series/historic_data'
ARDUINO_AUTH_TOKEN = os.environ.get('ARDUINO_AUTH_TOKEN')

def get_token_file():
    URL = 'https://login.arduino.cc/oauth/token'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Auth0-Client': 'eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjIuMS4zIn0='
    }
    payload = {
        'client_id': 'e9qipA2N0k9P8vvre9fdGc6u9Kl9eHSP',
        'redirect_uri': 'https://app.arduino.cc',
        'code_verifier': 'vvnrpZM3Ie.JYOablXixaq8Lse0FaKrgZNHVsQRmjv.',
        'code': 'hP-AFQw0cRIjm1LkcCZEdw-M6JupQG-lcqrVE2V3N3oXx',
        'grant_type': 'authorization_code'
    }
    #response = requests.post(URL, headers=headers, data=json.dumps(payload))
    return requests.options(URL, headers={"access-control-request-headers":
'auth0-client'}).status_code
    #return response.ok

def get_history_data():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ARDUINO_AUTH_TOKEN,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }
    payload = {"properties":["f9258eb1-8317-4baf-ad8b-b63aeb6f582e","e0d2b5a1-cd30-48fc-b3fd-82c195319353","60616fbd-9373-4236-81c8-15eee3a141e4","fbaeb6b2-420e-4a89-a719-4efe46984b73","6b419129-5465-498d-b5ee-fa3b63ee3cfd"],"from":"2025-02-26T00:00:00.000Z","to":"2025-02-27T23:59:59.999Z"}
    response = requests.post(ARDUINO_URL_HISTORY_DATA, headers=headers, data=json.dumps(payload))
    return response.ok

print(get_token_file())