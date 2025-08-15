from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

# Create the Flask application
app = Flask(__name__)

# Database setup
# create a database if it doesn't exist
def init_db():
    connection = sqlite3.connect('tasks.db')
    c = connection.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            due_date TEXT,
            status TEXT
        )
    ''')
    connection.commit()
    connection.close()
# Route to display the task list
@app.route('/')
def index():
    connection = sqlite3.connect('tasks.db')
    c = connection.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall() # Fetch all tasks from the database
    connection.close()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[3] == 'Completed')

    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    return render_template(
        'index.html',
        tasks=tasks,
        completion_rate=completion_rate
    )
# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    due_date = request.form['due_date']

    connection = sqlite3.connect('tasks.db')
    c = connection.cursor()
    c.execute('INSERT INTO tasks (title, due_date, status) VALUES (?, ?, ?)',
              (title, due_date, 'pending'))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))
# Route to change the status of a task to 'Completed'
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    connection = sqlite3.connect('tasks.db')
    c = connection.cursor()
    c.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))
# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    connection = sqlite3.connect('tasks.db')
    c = connection.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))
# To run the application
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
