"""A Flask web application for managing personal adventures.

This application allows users to register, log in, add, view, and manage 
their personal adventure entries. It uses Flask for the web framework, 
and SQLAlchemy for database interactions."""
#pylint: disable=import-error

import secrets
from functools import wraps
from flask import Flask, render_template, request, redirect, session, g, send_file
from util import add_entry, retrieve_entries, retrieve_entry
from blueprints import authentication, user_profile
from country import COUNTRIES

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

app.register_blueprint(authentication)
app.register_blueprint(user_profile)

def login_required(f):
    """Decorator to restrict access to a route for logged-in users only."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def set_uid():
    if "user_id" in session:
        if "user_id" not in g:
            g.user_id = session["user_id"]

@app.route("/")
@login_required
def main():
    """The main page view function, showing recent adventures."""

    adventures = retrieve_entries(g.user_id)
    return render_template("index.html", adventures=adventures)

@app.route("/add-entry", methods=["GET"])
@login_required
def add_adventure():
    """Displays the form to add a new adventure entry."""

    return render_template("add_entry.html")

@app.route("/view-diary")
@login_required
def personal_adventures():
    """Shows the user's personal adventure diary."""

    adventures = retrieve_entries(g.user_id)
    return render_template("diary.html", adventures = adventures)

@app.route("/save-entry", methods=["POST"])
@login_required
def save_entry():
    """Processes and saves a new adventure entry."""

    title = request.form.get("title")
    country = request.form.get("country")
    city = request.form.get("city")
    date = request.form.get("date")
    experience = request.form.get("editor_data")
    user_id = session["user_id"]
    add_entry(user_id, title, country, city, date, experience)
    return redirect("/view-diary")

@app.route("/view-entry")
def view_entry():
    """Displays a specific adventure entry."""

    adventure_id = None
    if "id" in request.args:
        adventure_id = int(request.args["id"])
        adventure = retrieve_entry(adventure_id)
        return render_template("view_entry.html", adventure = adventure)

    return redirect("/view-diary")

@app.route("/flag")
@login_required
def get_flag():
    """Fetches SVG data for a country flag"""

    if "country" not in request.args:
        return ("", 404)
    
    country_name = request.args["country"].lower()

    for country in COUNTRIES:
        if country["name"].lower() == country_name:
            abbr = country["code"]
            return send_file(f"{app.static_folder}/images/flags/{abbr}.svg", mimetype="text/plain")
        
    return ("", 404)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
