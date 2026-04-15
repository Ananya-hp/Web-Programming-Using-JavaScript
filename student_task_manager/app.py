from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "tasksecret"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        subject TEXT,
        due_date TEXT,
        priority TEXT,
        expected_time INTEGER,
        status TEXT DEFAULT 'Pending',
        attachment TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (request.form['email'], request.form['password'])
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Login")

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (request.form['name'], request.form['email'], request.form['password'])
            )
            conn.commit()
            return redirect("/login")
        except:
            return render_template("register.html", error="Email already exists")
        finally:
            conn.close()

    return render_template("register.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/login")

    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session['user_id'],)
    ).fetchall()
    conn.close()

    completed = len([t for t in tasks if t['status'] == "Completed"])
    pending = len([t for t in tasks if t['status'] == "Pending"])

    today = date.today().strftime("%Y-%m-%d")

    overdue = len([
        t for t in tasks
        if t['status'] == "Pending" and t['due_date'] and t['due_date'] < today
    ])

    # ✅ GRAPH DATA
    chart_labels = ["Completed", "Pending"]
    chart_values = [completed, pending]

    return render_template(
        "dashboard.html",
        tasks=tasks,
        completed=completed,
        pending=pending,
        overdue=overdue,
        current_date=today,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

# ---------------- ADD TASK ----------------
@app.route("/add_task", methods=["GET","POST"])
def add_task():
    if 'user_id' not in session:
        return redirect("/login")

    if request.method == "POST":
        conn = get_db()
        conn.execute("""
        INSERT INTO tasks(user_id,title,description,subject,due_date,priority,expected_time,created_at)
        VALUES(?,?,?,?,?,?,?,?)
        """, (
            session['user_id'],
            request.form['title'],
            request.form['description'],
            request.form['subject'],
            request.form['due_date'],
            request.form['priority'],
            request.form['expected_time'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_task.html")

# ---------------- TASK LIST (SEARCH + FILTER) ----------------
@app.route("/tasks")
def tasks():
    if 'user_id' not in session:
        return redirect("/login")

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")

    query = "SELECT * FROM tasks WHERE user_id=?"
    params = [session['user_id']]

    if search:
        query += " AND (title LIKE ? OR subject LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    if status:
        query += " AND status=?"
        params.append(status)

    if priority:
        query += " AND priority=?"
        params.append(priority)

    conn = get_db()
    tasks = conn.execute(query, params).fetchall()
    conn.close()

    return render_template("tasks.html", tasks=tasks)

# ---------------- EDIT TASK ----------------
@app.route("/edit_task/<int:id>", methods=["GET","POST"])
def edit_task(id):
    if 'user_id' not in session:
        return redirect("/login")

    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        conn.execute("""
        UPDATE tasks 
        SET title=?,description=?,subject=?,due_date=?,priority=? 
        WHERE id=?
        """, (
            request.form['title'],
            request.form['description'],
            request.form['subject'],
            request.form['due_date'],
            request.form['priority'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/tasks")

    return render_template("edit_task.html", task=task)

# ---------------- COMPLETE TASK ----------------
@app.route("/complete_task/<int:id>", methods=["GET","POST"])
def complete_task(id):
    if 'user_id' not in session:
        return redirect("/login")

    if request.method == "POST":
        file = request.files['attachment']
        filename = None

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db()
        conn.execute(
            "UPDATE tasks SET status='Completed', attachment=? WHERE id=?",
            (filename, id)
        )
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("complete_task.html")

# ---------------- SUBJECT DASHBOARD ----------------
@app.route("/subject_dashboard")
def subject_dashboard():
    if 'user_id' not in session:
        return redirect("/login")

    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session['user_id'],)
    ).fetchall()
    conn.close()

    subject_data = {}

    for task in tasks:
        subject = task['subject'] if task['subject'] else "General"
        if subject not in subject_data:
            subject_data[subject] = []
        subject_data[subject].append(task)

    return render_template("subject_dashboard.html", subject_data=subject_data)

# ---------------- DELETE ----------------
@app.route("/delete_task/<int:id>")
def delete_task(id):
    if 'user_id' not in session:
        return redirect("/login")

    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)