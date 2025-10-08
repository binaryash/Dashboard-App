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
            # ADD THIS: Check for HTMX request
            if request.headers.get('HX-Request'):
                tasks = Todos.get_all_tasks()
                return render_template('todo_body.html', tasks=tasks)
            return redirect('/index')
        except Exception as e:
            return f'There was an issue with adding your task: {str(e)}', 500
    else:
        tasks = Todos.get_all_tasks()
        return render_template('todo_index.html', tasks=tasks)

@app.route('/complete/<int:id>')
def complete(id):
    try:
        Todos.mark_task_complete(id)
        # ADD THIS: Check for HTMX request
        if request.headers.get('HX-Request'):
            tasks = Todos.get_all_tasks()
            return render_template('todo_body.html', tasks=tasks)
        return redirect('/index')
    except Exception as e:
        return f'Error completing task: {str(e)}', 500

@app.route('/delete/<int:id>')
def delete(id):
    try:
        Todos.delete_task(id)
        # ADD THIS: Check for HTMX request
        if request.headers.get('HX-Request'):
            tasks = Todos.get_all_tasks()
            return render_template('todo_body.html', tasks=tasks)
        return redirect('/index')
    except Exception as e:
        return f'Error deleting task: {str(e)}', 500

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        Todos.update_task(id, request.form['content'], request.form.get('completion_date', ''))
        # ADD THIS: Check for HTMX request
        if request.headers.get('HX-Request'):
            tasks = Todos.get_all_tasks()
            return render_template('todo_body.html', tasks=tasks)
        return redirect('/index')
    except Exception as e:
        return f'Error updating task: {str(e)}', 500

@app.route('/filter-tasks', methods=['GET'])
def filter_tasks():
    """Filter tasks based on dropdown selection"""
    status = request.args.get('status', 'all')

    if status == 'incomplete':
        tasks = Todos.get_incomplete_tasks()
    elif status == 'completed':
        tasks = Todos.get_completed_tasks()
    else:  # 'all'
        tasks = Todos.get_all_tasks()

    # Check if HTMX request
    if request.headers.get('HX-Request'):
        return render_template('todo_body.html', tasks=tasks)
    return render_template('todo_index.html', tasks=tasks)

# Keep the original routes for backward compatibility
@app.route('/incomplete')
def incomplete():
    tasks = Todos.get_incomplete_tasks()
    if request.headers.get('HX-Request'):
        return render_template('todo_body.html', tasks=tasks)
    return render_template('todo_index.html', tasks=tasks)

@app.route('/completed')
def completed():
    tasks = Todos.get_completed_tasks()
    if request.headers.get('HX-Request'):
        return render_template('todo_body.html', tasks=tasks)
    return render_template('todo_index.html', tasks=tasks)

@app.route('/all-tasks')
def all_tasks():
    tasks = Todos.get_all_tasks()
    if request.headers.get('HX-Request'):
        return render_template('todo_body.html', tasks=tasks)
    return render_template('todo_index.html', tasks=tasks)

@app.route('/search-tasks', methods=['GET'])
def search_tasks():
    """Search tasks based on query"""
    query = request.args.get('q', '').strip()

    tasks = Todos.search_tasks(query)

    # Check if HTMX request
    if request.headers.get('HX-Request'):
        return render_template('todo_body.html', tasks=tasks)
    return render_template('todo_index.html', tasks=tasks)


@app.route('/update-task', methods=['POST'])
def update_task():
    try:
        task_id = request.form.get('task_id')
        content = request.form.get('content')
        completion_date = request.form.get('completion_date', '')

        Todos.update_task(int(task_id), content, completion_date)

        if request.headers.get('HX-Request'):
            tasks = Todos.get_all_tasks()
            return render_template('todo_body.html', tasks=tasks)
        return redirect('/index')
    except Exception as e:
        return f'Error updating task: {str(e)}', 500
