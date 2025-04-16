from app import create_app_with_blueprint, socketio

app = create_app_with_blueprint()

if __name__ == '__main__':
    # Run
    socketio.run(app, host = "127.0.0.1", port = 5000, debug = True)