"""Routes for TODOs."""

from flask import Flask, render_template, url_for, redirect, request
from core.feed_reader import get_feeds
from core import app, db
from core.models import Todo
from core.datetime_1 import get_current_datetime
from core.todo.todo import Todos

@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        try:
            Todos.create_task(task_content)
            return redirect('/incomplete')
        except:
            return 'There was an issue with adding your task'
    else:
        tasks = Todos.get_all_tasks()
        return render_template('todo_index.html', tasks=tasks)

@app.route('/complete/<int:id>')
def complete(id):
    Todos.mark_task_complete(id)
    return redirect('/incomplete')

@app.route('/delete/<int:id>')
def delete(id):
    try:
        Todos.delete_task(id)
        return redirect('/index')
    except:
        return 'cant delete'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todos.get_task_by_id(id)

    if request.method == 'POST':
        try:
            Todos.update_task(id, request.form['content'], request.form['completion_date'])
            return redirect('/index')
        except:
            return 'issue in updating'
    else:
        return render_template('todo_update.html', task=task)

@app.route('/incomplete')
def incomplete():
    tasks = Todos.get_incomplete_tasks()
    return render_template('incomplete_tasks.html', tasks=tasks)
