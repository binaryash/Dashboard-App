"""Models File for Todo."""

from datetime import datetime
from enum import Enum
from core import db

# Association table for many-to-many relationship
todo_category = db.Table(
    "todo_category",
    db.Column("todo_id", db.Integer, db.ForeignKey("todo.id"), primary_key=True),
    db.Column(
        "category_id", db.Integer, db.ForeignKey("category.id"), primary_key=True
    ),
)


class Priority(str, Enum):
    A = "A"
    B = "B"
    C = "C"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completion_date = db.Column(db.Date)
    completion_time = db.Column(db.DateTime)
    priority = db.Column(db.Enum(Priority), default=Priority.C, nullable=False)

    categories = db.relationship("Category", secondary=todo_category, backref="todos")

    def __repr__(self):
        return f"<Task {self.id}>"
