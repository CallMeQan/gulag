# flask --app upload_json run -h localhost -p 1234
from flask import Flask, jsonify

data = {
    "user_id": "12345",
    "data": [
        {
        "timestamp": "2025-03-23T16:40:00Z",
        "latitude": 10.0285,
        "longitude": 105.8542
        },
     
        {
        "timestamp": "2025-03-23T16:45:00Z",
        "latitude": 10.0288,
        "longitude": 105.8551
        }
    ]
}

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    return jsonify(data)

# flask --app upload_json run -h localhost -p 1234
if __name__ == "__main__":
    port = 1234
    app.run(host = '127.0.0.1', port = port,  )