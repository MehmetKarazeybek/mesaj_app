from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

if not os.path.exists("database.db"):
    conn = get_db()
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, username TEXT, message TEXT)")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        msg = request.form["message"]
        conn = get_db()
        conn.execute("INSERT INTO messages (username, message) VALUES (?,?)", (session["user"], msg))
        conn.commit()
        conn.close()

    conn = get_db()
    messages = conn.execute("SELECT * FROM messages").fetchall()
    conn.close()
    return render_template("index.html", messages=messages, user=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
        if not user:
            conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (u, p))
            conn.commit()
        session["user"] = u
        return redirect("/")
    return '''
    <h2>Giriş / Kayıt</h2>
    <form method="post">
      <input name="username" placeholder="kullanıcı adı"><br>
      <input name="password" placeholder="şifre"><br>
      <button>Devam</button>
    </form>
    '''

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run()
