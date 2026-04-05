# ===============================
# Project: Simple Blog (Experiment-5)
# Name: Ananya Sharma
# Date: 2026-04-05
# ===============================

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
posts = []

# -------------------------------
# Home (Read)
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html', posts=posts)

# -------------------------------
# Create
# -------------------------------
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        posts.append({
            'title': title,
            'content': content
        })

        return redirect(url_for('index'))

    return render_template('create.html')

# -------------------------------
# Update
# -------------------------------
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    post = posts[index]

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        return redirect(url_for('index'))

    return render_template('edit.html', post=post, index=index)

# -------------------------------
# Delete
# -------------------------------
@app.route('/delete/<int:index>')
def delete(index):
    posts.pop(index)
    return redirect(url_for('index'))

# -------------------------------
# Run App
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)