### IMPORT
from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

from .env import DATABASE_URI, SECRET_KEY

# ====================================================================== #

### MAIN
# Config

Session(app)

# Create a database
with app.app_context():
    db.create_all()

# # Log out
# @app.route("/logout")
# @login_required # Should not used in place of "username" in session
# def logout():
#     logout_user()
#     session.pop('username', None)
#     session.clear()
#     return redirect(url_for("login"))



# Run cmd: "flask --app app run"
if __name__ == "__main__":
    port_number = 5000
    print(app.url_map)
    app.run(debug = True, port = port_number)