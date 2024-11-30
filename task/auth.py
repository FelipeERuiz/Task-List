from flask import (
    Blueprint, redirect, url_for, flash, render_template
)
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/")
def register():
    return "Hola"
