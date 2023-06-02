# ORGANIZED 1.0
#### Video Demo: https://www.youtube.com/watch?v=1ITltBLVgCw

#### Description:

**Organized** is a task management website that allows users to effectively manage their to-do lists, view their schedule and tasks for the month, and track their progress.

At first, I was very eager to start trying out different frameworks, libraries and languages, such as ReactJS, NodeJS, MongoDB, etc. However, I ultimately decided to firstly master the tools that we were taught in the CS50x course before moving on to new things.

## Tech Stack:
- JavaScript
- HTML
- CSS
- SQLite
- Python
- Flask

I used Bootstrap 5.3 to help create the front-end of the website and made sure it is as responsive as possible on all screen types. While the website's current design may not be the most visually appealing, the effort was mainly focused on the website's functionality.

- User Registration: The website supports user registration to allow individuals to have their own set of tasks and schedules. Each user is assigned a unique ID and username in the SQLite database.
- Create and Manage Tasks: Users can easily create or delete tasks, assign due dates, and add descriptions.
- Monthly Schedule View: The website provides a calendar view that has color-coded entries to help users visualize their tasks and schedule for the month.
- Progress Tracking: Users can view their total completed tasks and keep tabs on their pending ones.
- Real-time Updates: The website automatically refreshes every 30 minutes to display any updates with the tasks statuses based on their due dates/times.

## Pages:
- Login - Provides a brief description about ORGANIZED and a form for users to log in.
- Signup - Provides a form for new users to sign up.
- To-do/index - Contains four sections (Today, Upcoming, Overdue, and Completed) in which the tasks are seperated respective to their due date or completion status. There is also a blue button that is fixed on the bottom right of the screen that triggers a pop-up modal for users to add their tasks.
- Calendar - Shows all the tasks and schedules the user has for the months. At the moment, only supports a monthly view.
- Overview - Provides users with the total number of completed tasks and pending tasks. It also includes a pie chart to further help users visualize their tasks.

## Insights:
Real-time updates is accomplished by sending AJAX requests at regular intervals using SetInterval function with a delay of 1,800,000 ms (30 minutes).

Once the AJAX request is sent, the 'checkDue()' function is called. This function takes two arguments: the due date and due time of an item. It compares these values with the current date and time to determine the appropriate 'class' for the item.

```
def checkDue(todo_date, todo_time):
    # Check whether todo_date or todo_time has a value
    # Compare with current date and/or time accordingly
    # Return the appropriate class
    return <class>
```

In addition to the real-time updates every 30 minutes, the 'checkDue()' function is also used in the 'GET' request route. This ensures that every time the user manually reloads the page, it also displays the latest updates with the tasks.

## Roadmap:
There are still a lot of things to add or improve with Organized 1.0:
- Task prioritization and categorization
- Task filtering and searching
- Reminders and notifications
- Yearly, weekly, and daily calendar views
- Draggable and editable items
- Collaborative task management
- Improved UI design

But, for now, I feel very proud of what I have created, and so, this was Organized 1.0.

## Contact:
If you have any questions, suggestions, or feedback, feel free to reach out at  castroirvan@gmail.com