if __name__ == '__main__':
    from app import create_app_with_blueprint, socketio
    from dotenv import load_dotenv
    from os import getenv
    load_dotenv()
    app = create_app_with_blueprint()
    socketio.run(app, host="0.0.0.0", port="8000", debug=getenv("DEBUG", default = True))