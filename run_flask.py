
if __name__ == '__main__':
    import app
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()
    a = app.create_app_with_blueprint()
    a.run(debug = getenv('DEBUG'))