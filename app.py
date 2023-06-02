import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

from helpers import login_required, checkDue

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect SQLite database
db = SQL("sqlite:///organized.db")

current_date = date.today()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # User reached route via POST
    if request.method == "POST":
        # Check if reqest is from AJAX
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Make updates on their classes based on due date/time
            items = db.execute("SELECT * FROM todo WHERE user_id = ? AND class != 'Completed'",
                               session["user_id"])

            for item in items:
                # Check class
                todo_class = checkDue(item["due_date"], item["due_time"])

                if item["class"] != todo_class:
                    db.execute("UPDATE todo SET class = ? WHERE user_id = ? AND id = ?",
                               todo_class, session["user_id"], item['id'])

            return jsonify(success=True)  # Return a JSON response indicating success

        # Check if request is from add button
        if request.form.get("btn-identifier") == "addBtn":
            title = request.form.get("title")
            description = request.form.get("description")
            date = request.form.get("date")
            time = request.form.get("time")

            # Check if to-do item is either date or time
            if date or time:
                # To-do item with due date and due time
                if date and time:
                    # Check for class via due date
                    todo_class = checkDue(date, time)

                    db.execute("INSERT INTO todo (user_id, title, description, due_date, due_time, class) VALUES (?, ?, ?, ?, ?, ?)",
                               session["user_id"], title, description, date, time, todo_class)

                # To-do item with due date and no due time
                if date and not time:
                    # Check for class via due date
                    time = "23:59:59"
                    todo_class = checkDue(date, time)

                    db.execute("INSERT INTO todo (user_id, title, description, due_date, due_time, class) VALUES (?, ?, ?, ?, ?, ?)",
                               session["user_id"], title, description, date, time, todo_class)

                # To-do item with due time and no due date
                if time and not date:
                    # If no date given, give today's date

                    db.execute("INSERT INTO todo (user_id, title, description, due_date, due_time, class) VALUES (?, ?, ?, ?, ?, 'Today')",
                               session["user_id"], title, description, current_date, time)

            # If no date/time, place the to-do item in the 'Today' class
            else:
                db.execute("INSERT INTO todo (user_id, title, description, due_date, due_time, class) VALUES (?, ?, ?, ?, ?, 'Today')",
                           session["user_id"], title, description, date, time)

        # Check if request is from delete button
        if request.form.get("btn-identifier") == "deleteBtn":
            id = request.form.get("todo-id")

            item = db.execute("SELECT id FROM todo WHERE user_id = ? AND id = ?",
                              session["user_id"], id)

            # Delete selected item
            db.execute("DELETE FROM todo WHERE id = ?", item[0]["id"])

        # Check if request is from checkbox
        if request.form.get("btn-identifier") == "checkbox":
            id = request.form.get("todo-id")

            item = db.execute("SELECT * FROM todo WHERE user_id = ? AND id = ?",
                              session["user_id"], id)

            # Check if to-do item has a due date/time
            if item[0]["due_date"] or item[0]["due_time"]:
                # Check if item is marked complete
                if item[0]["class"] == "Completed":
                    # Check for class via due date
                    todo_class = checkDue(item[0]["due_date"], item[0]["due_time"])

                    db.execute("UPDATE todo SET class = ? WHERE user_id = ? AND id = ?",
                               todo_class, session["user_id"], id)
                else:
                    db.execute("UPDATE todo SET class = 'Completed' WHERE user_id = ? AND id = ?",
                               session["user_id"], id)
            else:
                # Check if item is marked complete
                if item[0]['class'] == "Completed":
                    db.execute("UPDATE todo SET class = 'Today' WHERE user_id = ? AND id = ?",
                               session["user_id"], id)
                else:
                    db.execute("UPDATE todo SET class = 'Completed' WHERE user_id = ? AND id = ?",
                               session["user_id"], id)

        return redirect("/")

    # User reached route via GET
    else:
        # Make updates on their classes based on due date/time
        items = db.execute("SELECT * FROM todo WHERE user_id = ? AND class != 'Completed'",
                           session["user_id"])

        for item in items:
            # Check class
            todo_class = checkDue(item["due_date"], item["due_time"])

            if item["class"] != todo_class:
                db.execute("UPDATE todo SET class = ? WHERE user_id = ? AND id = ?",
                           todo_class, session["user_id"], item["id"])

        # Retrieve all the to-do items of users and the total items within each class
        todo = db.execute("""SELECT *,
                                (SELECT COUNT(*) FROM todo WHERE user_id = ? AND class = 'Overdue') AS overdue_count,
                                (SELECT COUNT(*) FROM todo WHERE user_id = ? AND class = 'Today') AS today_count,
                                (SELECT COUNT(*) FROM todo WHERE user_id = ? AND class = 'Upcoming') AS upcoming_count,
                                (SELECT COUNT(*) FROM todo WHERE user_id = ? AND class = 'Completed') AS completed_count
                             FROM todo WHERE user_id = ? ORDER BY due_date, due_time""",
                          session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"])

        if todo:
            upcoming_count = todo[0]["upcoming_count"]
            today_count = todo[0]["today_count"]
            overdue_count = todo[0]["overdue_count"]
            completed_count = todo[0]["completed_count"]
        else:
            upcoming_count = 0
            today_count = 0
            overdue_count = 0
            completed_count = 0

        return render_template("index.html", todo=todo, today_count=today_count, upcoming_count=upcoming_count, overdue_count=overdue_count, completed_count=completed_count)


@app.route("/calendar")
@login_required
def calendar():
    events = db.execute("SELECT title, due_date, due_time, class FROM todo WHERE (user_id = ? AND class = 'Today') OR (user_id = ? AND class = 'Upcoming') OR (user_id = ? AND class = 'Overdue')",
                        session["user_id"], session["user_id"], session["user_id"])

    current_time = datetime.now().time()

    return render_template("calendar.html", events=events, current_date=current_date, current_time=current_time)


@app.route("/overview")
@login_required
def overview():
    tasks = db.execute("""SELECT COUNT(*) AS pending_count,
                            (SELECT COUNT(*) FROM todo WHERE class = 'Completed' AND user_id = ?) AS completed_count,
                            (SELECT COUNT(*) FROM todo WHERE class = 'Overdue' AND user_id = ?) AS overdue_count,
                            (SELECT COUNT(*) FROM todo WHERE class = 'Today' AND user_id = ?) AS today_count,
                            (SELECT COUNT(*) FROM todo WHERE class = 'Upcoming' AND user_id = ?) AS upcoming_count
                          FROM todo WHERE (class = 'Upcoming' AND user_id = ?) OR (class = 'Today' AND user_id = ?) OR (class = 'Overdue' AND user_id = ?)""",
                       session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"])

    return render_template("overview.html", completed_count=tasks[0]['completed_count'], pending_count=tasks[0]['pending_count'], overdue_count=tasks[0]['overdue_count'], today_count=tasks[0]['today_count'], upcoming_count=tasks[0]['upcoming_count'])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username and password was submitted
        if not username and not password:
            return render_template("login.html", msg1="Username cannot be empty", msg2="Password cannot be empty")

        # Check if username was submitted
        elif not username:
            return render_template("login.html", msg1="Username cannot be empty")

        # Check password was submitted
        elif not password:
            return render_template("login.html", msg2="Password cannot be empty", username=username)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists
        if len(rows) != 1:
            return render_template("login.html", msg1="Invalid username")

        # Ensure password is correct
        elif not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", msg2="Invalid password", username=username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign up user"""

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Hashed password
        hashed_password = generate_password_hash(password)

        # Select user database
        rows = db.execute("SELECT username FROM users")

        # Place the usernames in a list
        usernames = []
        for row in rows:
            usernames.append(row["username"].lower())

        print(usernames)

        # Check if all fields was submitted
        if not username and not password and not confirmation:
            return render_template("signup.html", msg1="Must enter username", msg2="Must enter password", msg3="Must confirm password")

        # Check if username was submitted
        elif not username:
            return render_template("signup.html", msg1="Must enter username")

        # Check if password and confirm password was submitted
        elif not password and not confirmation:
            return render_template("signup.html", msg2="Must enter password", msg3="Must confirm password", username=username)

        # Check if password was submitted
        elif not password:
            return render_template("signup.html", msg2="Must enter password", username=username)

        # Check if confirm password was submitted
        elif not confirmation:
            return render_template("signup.html", msg3="Must confirm password", username=username)

        # Check if username already exists in the database
        elif username.lower() in usernames:
            return render_template("signup.html", msg1="That username already exists")

        # Check if password matches with confirm password
        elif password != confirmation:
            return render_template("signup.html", msg2="Passwords do not match", msg3="Passwords do not match", username=username)

        # Insert username and hashed password into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   username, hashed_password)

        # Get id of new created id
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)

        # Assign session user_id to go directly to /index.html
        session["user_id"] = rows[0]["id"]

        flash("Registered")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
