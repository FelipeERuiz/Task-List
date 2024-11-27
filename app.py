from flask import Flask, render_template, request, g, flash, redirect, url_for
import mysql.connector

app = Flask(__name__)

app.secret_key = "mikey"


def get_connection():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host='localhost',
            user='chanchitofeliz',
            password='holamundo',
            database='tasks'
        )
    return g.db


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        content = request.form["content"]
        sql = "INSERT INTO task(content) VALUES(%s)"
        cursor.execute(sql, (content,))
        conn.commit()
        flash("Registro exitoso")

    cursor.execute("SELECT * FROM task")
    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<id>", methods=["GET", "DELETE"])
def delete(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "DELETE FROM task WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    flash("Tarea eliminada exitosamente")
    return redirect(url_for("index"))


@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql_select = "SELECT * FROM task WHERE id = %s"
    cursor.execute(sql_select, (id,))
    tasks = cursor.fetchall()

    if request.method == "POST":
        content = request.form["content"]
        sql_update = "UPDATE task SET content = %s WHERE id = %s"
        cursor.execute(sql_update, (content, id,))
        conn.commit()
        if cursor.execute:
            return redirect(url_for("index"))
    return render_template("update.html", tasks=tasks)
