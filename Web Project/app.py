from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "tasksecret"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        due_date TEXT,
        priority TEXT,
        expected_time INTEGER,
        actual_time INTEGER,
        status TEXT DEFAULT 'Pending',
        reflection TEXT,
        distraction TEXT,
        difficulty TEXT,
        rating INTEGER,
        attachment TEXT,
        created_at TEXT
    )
""")

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid login")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
            return redirect("/")
        except:
            return render_template("register.html", error="Email already exists")
        finally:
            conn.close()
    return render_template("register.html")

from datetime import date

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id=? ORDER BY created_at DESC",
        (session['user_id'],)
    ).fetchall()
    conn.close()

    completed = len([t for t in tasks if t['status'] == 'Completed'])
    pending = len([t for t in tasks if t['status'] == 'Pending'])
    overdue = len([
        t for t in tasks
        if t['status'] == 'Pending' and t['due_date'] < date.today().strftime("%Y-%m-%d")
    ])

    return render_template(
        "dashboard.html",
        tasks=tasks,
        completed=completed,
        pending=pending,
        overdue=overdue
    )


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if 'user_id' not in session:
        return redirect("/")
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        expected_time = request.form['expected_time']
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = get_db()
        conn.execute("""
            INSERT INTO tasks
            (user_id, title, description, due_date, priority, expected_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session['user_id'],
            title,
            description,
            due_date,
            priority,
            expected_time,
            created_at
        ))
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    return render_template("add_task.html")

@app.route("/tasks")
def tasks():
    if 'user_id' not in session:
        return redirect("/")
    search = request.args.get("search", "")
    status = request.args.get("status", "")
    conn = get_db()
    query = "SELECT * FROM tasks WHERE user_id=?"
    params = [session['user_id']]

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
    if status:
        query += " AND status=?"
        params.append(status)

    query += " ORDER BY due_date ASC"
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    return render_template("tasks.html", tasks=tasks)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect("/")
    conn = get_db()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?",
        (task_id,)
    ).fetchone()
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        expected_time = request.form['expected_time']
        conn.execute("""
            UPDATE tasks
            SET title=?, description=?, due_date=?, priority=?, expected_time=?
            WHERE id=?
        """, (
            title,
            description,
            due_date,
            priority,
            expected_time,
            task_id
        ))
        conn.commit()
        conn.close()
        return redirect("/tasks")
    conn.close()
    return render_template("edit_task.html", task=task)

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/complete_task/<int:task_id>", methods=["GET", "POST"])
def complete_task(task_id):
    if 'user_id' not in session:
        return redirect("/")
    conn = get_db()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?",
        (task_id,)
    ).fetchone()

    if request.method == "POST":
        actual_time = request.form['actual_time']
        reflection = request.form['reflection']
        distraction = request.form['distraction']
        difficulty = request.form['difficulty']
        rating = request.form['rating']

        file = request.files['attachment']
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn.execute("""
            UPDATE tasks
            SET status='Completed',
                actual_time=?,
                reflection=?,
                distraction=?,
                difficulty=?,
                rating=?,
                attachment=?
            WHERE id=?
        """, (
            actual_time,
            reflection,
            distraction,
            difficulty,
            rating,
            filename,
            task_id
        ))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    conn.close()
    return render_template("complete_task.html", task=task)

@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect("/")
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/tasks")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
