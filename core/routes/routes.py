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
    entries = get_feeds()
    return render_template("feed_show.html", entries=entries)
