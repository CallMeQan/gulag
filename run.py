import dotenv, os
dotenv.load_dotenv()

if __name__ == '__main__':
    import app
    a = app.create_app_with_blueprint()
    a.run(debug = os.getenv('DEBUG'))