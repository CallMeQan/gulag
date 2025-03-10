import os, json, requests, dotenv

dotenv.load_dotenv()

PASSWORD = os.getenv('PASSWORD')
EMAIL = os.getenv('EMAIL')

ARDUINO_URL_HISTORY_DATA = 'https://api2.arduino.cc/iot/v2/series/historic_data'
ARDUINO_AUTH_TOKEN = os.environ.get('ARDUINO_AUTH_TOKEN')

def get_token_file():
    URL = 'https://login.arduino.cc/oauth/token'
    headers = {
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": "\"Chromium\";v=\"133\", \"Not(A:Brand\";v=\"99\"",
        "Content-Type": "application/x-www-form-urlencoded",
        "Auth0-Client": "eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjIuMS4zIn0=",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://app.arduino.cc",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.arduino.cc/",
        "Accept-Encoding": "gzip, deflate, br",
    }

    data = {
        "client_id": "e9qipA2N0k9P8vvre9fdGc6u9Kl9eHSP",
        "redirect_uri": "https://app.arduino.cc",
        "code_verifier": "yJH8vDqF2X.JsJuINCfp9hU.4q~iKkCpud8DHwbHUGt",
        "code": "9aleTStEISPxuuDgXhK2seL4P7uSGJtH5ZQBaDcsM9wh-",
        "grant_type": "authorization_code"
    }

    #response = requests.post(URL, headers=headers, data=json.dumps(payload))
    return requests.post(URL,headers=headers, data=data).status_code
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