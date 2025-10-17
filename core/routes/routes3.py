import datetime
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from core import app

DATABASE = "notes.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, note TEXT)"""
    )
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
    c.execute("SELECT id, note FROM notes WHERE date=? ORDER BY id DESC", (date,))
    notes = [{"id": row[0], "note": row[1]} for row in c.fetchall()]
    conn.close()
    return notes


def get_note_from_database(note_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT note, date FROM notes WHERE id=?", (note_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return {"note": result[0], "date": result[1]}
    return None


def update_note_in_database(note_id, note):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE notes SET note=? WHERE id=?", (note, note_id))
    conn.commit()
    conn.close()


def delete_note_from_database(note_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Get the date before deleting to return updated notes for that date
    c.execute("SELECT date FROM notes WHERE id=?", (note_id,))
    result = c.fetchone()
    date = result[0] if result else None

    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return date


@app.route("/event")
def event_home():
    create_database()
    current_date = datetime.date.today().isoformat()
    return render_template("index.html", selected_date=current_date)


@app.route("/create_note", methods=["POST"])
def create_note():
    date = request.form["date"]
    note = request.form["note"]

    create_database()
    insert_note_into_database(date, note)

    # Return the updated notes list for the created date
    notes = get_notes_from_database(date)
    return render_template("notes_list.html", notes=notes)


@app.route("/view_notes", methods=["POST"])
def view_notes():
    date = request.form["date"]
    create_database()
    notes = get_notes_from_database(date)
    return render_template("notes_list.html", notes=notes)


@app.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    if request.method == "GET":
        note_data = get_note_from_database(note_id)
        if note_data:
            return render_template("edit_note.html", note_id=note_id, note=note_data["note"], date=note_data["date"])
        else:
            return redirect(url_for("event_home"))
    elif request.method == "POST":
        note = request.form["note"]
        update_note_in_database(note_id, note)
        return redirect(url_for("event_home", message="Note updated successfully!"))


@app.route("/delete_note/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    date = delete_note_from_database(note_id)
    # Return updated notes list after deletion
    notes = get_notes_from_database(date) if date else []
    return render_template("notes_list.html", notes=notes)
