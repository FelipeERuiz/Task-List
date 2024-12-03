from flask import (
    Blueprint, redirect, url_for, flash, render_template, request, session, g
)
import functools
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/signup", methods=["GET", "POST"])
def register():
    db, c = get_db()
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        c.execute(
            "SELECT id FROM user WHERE username = %s", (username,)
        )
        if not username:
            error = "Username es requerido"
        if not password:
            error = "Password es requerido"
        elif c.fetchone() is not None:
            error = f"El usuario {username} ya esta registrado"

        if error is None:
            c.execute(
                "INSERT INTO user (username, password) VALUES (%s, %s)", (
                    username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for("auth.login"))
    flash(error)
    return render_template("auth/register.html")


@auth.route("/signin", methods=["GET", "POST"])
def login():
    db, c = get_db()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        c.execute(
            "SELECT * FROM user WHERE username = %s", (
                username, )
        )

        user = c.fetchone()

        if not username:
            error = "Username es requerido"
        if not password:
            error = "Password es requerido"
        elif not check_password_hash(user["password"], password):
            error = "Contraseña invalida"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("task.add_task"))

        flash(error)
    return render_template("auth/login.html")

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'SELECT * FROM user WHERE id = %s', (user_id,)
        )
        g.user = c.fetchone()


def logged_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
