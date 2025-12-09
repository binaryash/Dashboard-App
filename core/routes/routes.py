"""
Flask routes for displaying and filtering news feeds.

This file contains routes to:
- Display the home page (`/`)
- Show a list of news feeds with optional filters (`/feeds`)
- Provide filtered feed results dynamically via HTMX (`/feeds/results`)

Key Functions:
- `home`: Renders the home page.
- `feeds`: Displays news feed data with filtering options for source, type, and category.
- `feed_results`: An HTMX endpoint that updates feed results dynamically based on filter parameters.
"""

from flask import Flask, render_template, url_for, redirect, request
from core.news.feed_reader import get_feeds, get_filter_options
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
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 9, type=int)

    # Get filter parameters
    source = request.args.get("source", None)
    feed_type = request.args.get("type", None)
    category = request.args.get("category", None)

    # Get filtered feed data
    feed_data = get_feeds(
        page=page,
        per_page=per_page,
        source=source if source else None,
        feed_type=feed_type if feed_type else None,
        category=category if category else None,
    )

    # Get filter options for dropdowns
    filter_options = get_filter_options()

    # Add filter options and current filters to template data
    feed_data.update(filter_options)
    feed_data["current_source"] = source or ""
    feed_data["current_type"] = feed_type or ""
    feed_data["current_category"] = category or ""

    return render_template("feed_show.html", **feed_data)


@app.route("/feeds/results")
def feed_results():
    """HTMX endpoint for updating feed results"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 9, type=int)

    # Get filter parameters
    source = request.args.get("source", None)
    feed_type = request.args.get("type", None)
    category = request.args.get("category", None)

    # Get filtered feed data
    feed_data = get_feeds(
        page=page,
        per_page=per_page,
        source=source if source else None,
        feed_type=feed_type if feed_type else None,
        category=category if category else None,
    )

    return render_template("feed_results.html", **feed_data)
