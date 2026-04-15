# ===============================
# Project: Contact Management System
# Name: (Your Name)
# Date: (Add Date)
# ===============================

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

contacts = []

@app.route('/')
def index():
    query = request.args.get('search')
    if query:
        filtered = [c for c in contacts if query.lower() in c['name'].lower() or query in c['phone']]
    else:
        filtered = contacts
    return render_template('index.html', contacts=filtered, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        if not name or not phone or not email:
            return "All fields are required!"

        contacts.append({'name': name, 'phone': phone, 'email': email})
        return redirect(url_for('index'))
    return render_template('add_contact.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    if request.method == 'POST':
        contacts[id]['name'] = request.form['name']
        contacts[id]['phone'] = request.form['phone']
        contacts[id]['email'] = request.form['email']
        return redirect(url_for('index'))
    return render_template('edit_contact.html', contact=contacts[id], id=id)

@app.route('/delete/<int:id>')
def delete_contact(id):
    contacts.pop(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)