
if __name__ == '__main__':
    import app
    a = app.create_app_with_blueprint()
    a.run(debug=True)