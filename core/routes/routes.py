from flask import Flask, render_template, url_for, redirect, request
from core.news.feed_reader import get_feeds
from core import app, db
from core.models import Todo
from core.datetime_1 import get_current_datetime
from openpyxl import Workbook, load_workbook
from datetime import datetime as dt


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/feeds")
def feeds():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    feed_data = get_feeds(page=page, per_page=per_page)
    return render_template("feed_show.html", **feed_data)
