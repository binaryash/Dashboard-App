import datetime
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from core import app

DATABASE = 'notes.db'


def create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, note TEXT)''')
    conn.commit()
    conn.close()


def insert_note_into_database(date, note):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO notes (date, note) VALUES (?, ?)", (date, note))
    conn.commit()
    conn.close()


def get_notes_from_database(date):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, note FROM notes WHERE date=?", (date,))
    notes = [{'id': row[0], 'note': row[1]} for row in c.fetchall()]
    conn.close()
    return notes


def get_note_from_database(note_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT note FROM notes WHERE id=?", (note_id,))
    note = c.fetchone()
    conn.close()
    return note[0] if note else None


def update_note_in_database(note_id, note):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE notes SET note=? WHERE id=?", (note, note_id))
    conn.commit()
    conn.close()


def delete_note_from_database(note_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()


@app.route('/event')
def event_home():
    current_date = datetime.date.today()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    return render_template('index.html', year=year, month=month, day=day)


@app.route('/create_note', methods=['POST'])
def create_note():
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    date = f"{year:04d}-{month:02d}-{day:02d}"
    note = request.form['note']

    create_database()  # Ensure the database and table exist

    insert_note_into_database(date, note)

    return redirect(url_for('event_home', message='Note created successfully!'))


@app.route('/view_notes', methods=['POST'])
def view_notes():
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    date = f"{year:04d}-{month:02d}-{day:02d}"

    create_database()  # Ensure the database and table exist

    notes = get_notes_from_database(date)

    return render_template('index.html', year=year, month=month, day=day, notes=notes)


@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if request.method == 'GET':
        note = get_note_from_database(note_id)
        if note:
            return render_template('edit_note.html', note_id=note_id, note=note)
        else:
            return redirect(url_for('event_home'))
    elif request.method == 'POST':
        note = request.form['note']
        update_note_in_database(note_id, note)
        return redirect(url_for('event_home', message='Note updated successfully!'))


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    delete_note_from_database(note_id)
    return redirect(url_for('event_home', message='Note deleted successfully!'))


