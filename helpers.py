from cs50 import SQL
from flask import redirect, session
from functools import wraps
from datetime import datetime, date

# Connect SQLite database
db = SQL('sqlite:///organized.db')


# Used the distribution code given in PSET9 of CS50
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def checkDue(todo_date, todo_time):
    # Get current date/time
    current_dt = datetime.now()

    # Seperate components date and time components
    current_date = current_dt.date()
    current_time = current_dt.time()

    # Check if to-do item has a date
    if todo_date:
        due_dt_str = todo_date + ' ' + todo_time

        # Convert date string to datetime format
        due_dt = datetime.strptime(due_dt_str, '%Y-%m-%d %H:%M:%S')
        due_date = datetime.strptime(todo_date, '%Y-%m-%d').date()

        # Check if due time has passed
        if current_dt > due_dt:
            return "Overdue"
        else:
            # Check if due date is today, else upcoming
            if current_date == due_date:
                return "Today"
            else:
                return "Upcoming"

    elif todo_time:
        # Convert time string to time format
        due_time = datetime.strptime(todo_time, '%H:%M:%S').time()

        # Check if due time has passed
        if current_time > due_time:
            return "Overdue"
        else:
            return "Today"

    else:
        return "Today"