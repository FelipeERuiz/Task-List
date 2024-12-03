from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="mikey",
        DATABASE_HOST="localhost",
        DATABASE_USER="chanchitofeliz",
        DATABASE_PASSWORD="holamundo",
        DATABASE="tasks"
    )

    from . import auth
    app.register_blueprint(auth.auth)
    return app
