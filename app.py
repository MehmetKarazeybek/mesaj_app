from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "messages.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT
        )
    """)
    db.commit()
    db.close()

# 🔥 KRİTİK SATIR – RENDER İÇİN ŞART
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        cursor.execute(
            "INSERT INTO messages (name, message) VALUES (?, ?)",
            (name, message)
        )
        db.commit()
        return redirect("/")

    cursor.execute("SELECT name, message FROM messages")
    messages = cursor.fetchall()
    db.close()

    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run()
