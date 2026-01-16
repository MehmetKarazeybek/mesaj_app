from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "render-secret-key"

DB_NAME = "messages.db"

# ------------------ DATABASE ------------------

def get_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

# Render + gunicorn için ŞART
init_db()

# ------------------ ROUTES ------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        if name and message:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO messages (name, message) VALUES (?, ?)",
                (name, message)
            )
            db.commit()
            db.close()

        return redirect("/")

    return render_template("index.html")


@app.route("/messages")
def messages():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, message FROM messages ORDER BY id ASC")
    data = cursor.fetchall()
    db.close()
    return jsonify(data)


@app.route("/health")
def health():
    return "OK"


# ------------------ MAIN ------------------

if __name__ == "__main__":
    app.run()
