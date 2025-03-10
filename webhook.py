from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Lấy dữ liệu JSON gửi đến
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # Xử lý dữ liệu (ví dụ: in ra console)
    print("Received data:", data)

    # Bạn có thể thêm logic xử lý dữ liệu ở đây

    # Trả về phản hồi JSON cho Arduino Cloud
    return jsonify({"status": "success", "message": "Data received"}), 200

if __name__ == '__main__':
    # Chạy server Flask tại host 0.0.0.0 (để có thể truy cập từ bên ngoài)
    app.run(host='0.0.0.0', port=5000, debug=True)