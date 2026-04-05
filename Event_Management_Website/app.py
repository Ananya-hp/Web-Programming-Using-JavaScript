# Event Management Website
# Name: Ananya Sharma
# Roll No: ______
# Date: ______

from flask import Flask, render_template, request, redirect, flash, session

app = Flask(__name__)
app.secret_key = "secret"

events = [
    {"id":1,"name":"Music Fest","date":"2026-04-10","venue":"Delhi","description":"Live concert","image":"https://via.placeholder.com/300"},
    {"id":2,"name":"Tech Conference","date":"2026-05-01","venue":"Noida","description":"Tech talks","image":"https://via.placeholder.com/300"},
    {"id":3,"name":"Food Carnival","date":"2026-06-15","venue":"Gurgaon","description":"Food festival","image":"https://via.placeholder.com/300"},
    {"id":4,"name":"Art Exhibition","date":"2026-07-10","venue":"Delhi","description":"Art showcase","image":"https://via.placeholder.com/300"}
]

rsvp_count = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/events")
def events_page():
    return render_template("events.html", events=events, rsvp=rsvp_count)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        flash("Registration Successful!")
        return redirect("/events")
    return render_template("register.html", events=events)

@app.route("/rsvp/<int:id>")
def rsvp(id):
    rsvp_count[id] = rsvp_count.get(id, 0) + 1
    return redirect("/events")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form["username"]=="admin" and request.form["password"]=="123":
            session["admin"]=True
            return redirect("/admin")
        flash("Invalid Login")
    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("admin.html", events=events)

@app.route("/admin/add", methods=["POST"])
def add_event():
    events.append({
        "id": len(events)+1,
        "name": request.form["name"],
        "date": request.form["date"],
        "venue": request.form["venue"],
        "description": request.form["description"],
        "image": request.form["image"]
    })
    flash("Event Added")
    return redirect("/admin")

@app.route("/admin/delete/<int:id>")
def delete_event(id):
    global events
    events = [e for e in events if e["id"] != id]
    flash("Deleted Successfully")
    return redirect("/admin")

@app.route("/admin/edit/<int:id>", methods=["GET","POST"])
def edit_event(id):
    for e in events:
        if e["id"] == id:
            if request.method == "POST":
                e["name"] = request.form["name"]
                e["date"] = request.form["date"]
                e["venue"] = request.form["venue"]
                e["description"] = request.form["description"]
                e["image"] = request.form["image"]
                flash("Updated Successfully")
                return redirect("/admin")
            return render_template("edit.html", event=e)

if __name__ == "__main__":
    app.run(debug=True)