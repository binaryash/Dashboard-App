from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from core.news.feed_reader import get_feeds
from datetime import datetime
from core.datetime_1 import get_current_datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["MARKDOWN_EXTENSIONS"] = ["fenced_code"]
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config["UPLOAD_FOLDER"] = "uploads"
from core.routes import routes
from core.routes import todo_routes
from core.routes import routes3
