
from flask import current_app, g
import mysql.connector


def get_db():
    if g not in "db":
        g.db = mysql.connector.connect(
            host=current_app.config["DATABASE_HOST"],
            user=current_app.config["DATABASE_USER"],
            password=current_app.config["DATABASE_PASSWORD"],
            database=current_app.config["DATABASE"]
        )
        g.c = g.db.cursor(dictionary=True)
        return g.db, g.c
    
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
