"""
tipsy.py -- A flask-based todo list
"""
from flask import Flask, render_template, redirect, request, url_for, g, session
import model

app = Flask(__name__)

@app.before_request
def set_up_db():
    g.db = model.connect_db()

@app.route("/")
def index():
    return render_template("index.html", user_name="chriszf")

@app.route("/save_task", methods=["POST"])
def save_task():
    title = request.form['title']
    model.new_task(g.db, title)
    return redirect("/tasks")

@app.route("/tasks")
def list_tasks():
    user_id = session.get("user_id", None)
    tasks_from_db = model.get_tasks(g.db, user_id)
    return render_template("list_tasks.html", tasks=tasks_from_db)

@app.route("/task/<int:id>", methods=["GET"])
def view_task(id):
    task_from_db = model.get_task(g.db, id)
    return render_template("view_task.html", task=task_from_db)

@app.route("/task/<int:id>", methods=["POST"])
def complete_task(id):
    model.complete_task(g.db, id)
    return redirect("/tasks")

@app.route("/set_date")
def set_date():
    session['date'] = datetime.datetime.now()
    return "Date Set"

@app.route("/get_date")
def get_date():
    return str(session['date'])

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    user_info = model.authenticate(g.db, email, password)
    if user_info != None:
        session['user_id'] = user_info['id']
        return redirect("/tasks")
    else:
        return redirect("/login")
        

app.secret_key = 'secret_key'

@app.teardown_request
def close_db(e):
    g.db.close()

if __name__ == "__main__":
    app.run(debug=True)
