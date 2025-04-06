def run_flask():
    import app
    from os import getenv
    a = app.create_app_with_blueprint()
    a.run(debug = getenv('DEBUG', False))

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    run_flask()