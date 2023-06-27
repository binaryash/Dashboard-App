from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from app1.feed_reader import get_feeds
from datetime import datetime
from app1.datetime_1 import get_current_datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['MARKDOWN_EXTENSIONS'] = ['fenced_code']
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
from app1 import routes
from app1 import routes1
from app1 import routes2
from app1 import routes3

