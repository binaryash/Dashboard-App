from flask import Flask, render_template, url_for, redirect, request
from app1.feed_reader import get_feeds
from app1 import app, db
from app1.models import Todo
from app1.datetime_1 import get_current_datetime
from openpyxl import Workbook, load_workbook
from datetime import datetime as dt

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/feeds')
def feeds():
    entries = get_feeds()
    return render_template('feed_show.html', entries=entries)

@app.route('/datetime')
def datetime():
    current_datetime = get_current_datetime()
    return render_template('datetime_1.html', current_datetime=current_datetime)


