from flask import Blueprint, request, redirect, session, render_template, g
from util import check_login_credentials, add_user, entry_count, retrieve_user, change_password, check_passwd_comp
from functools import wraps
from logs import logger
from common_passwords import COMMON_PASSWORDS

def login_required(f):
    """Decorator to restrict access to a route for logged-in users only."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

authentication = Blueprint("authentication", __name__)

@authentication.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login."""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_id = check_login_credentials(username, password)
        if user_id:
            session["user_logged_in"] = True
            session["user_id"] = user_id
            return redirect("/")

        #Log failed login attempt
        logger.warning("failed login attempt", extra={"ip": request.remote_addr})
        return render_template("login.html")

    return render_template("login.html")

@authentication.route("/register", methods=["GET", "POST"])
def register():
    """Handles new user registration."""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if password in COMMON_PASSWORDS:
            return render_template("register.html", common_password_used=True)
        
        if check_passwd_comp(password):
            add_user(username, password)
            return redirect("/login")

        return render_template("register.html", passwd_complexity_check_failed=True)

    return render_template("register.html")

@authentication.route("/logout")
@login_required
def logout():
    """
    Logs out the user.

    Clears the session and redirects to the login page.
    """

    session.clear()
    return redirect("/login")

user_profile = Blueprint("user_settings", __name__)

@user_profile.route("/user-profile")
@login_required
def profile(**kwargs):
    user_id = g.user_id
    num_entries = entry_count(user_id)
    user = retrieve_user(user_id)

    return render_template("user_profile.html", num_entries = num_entries, username = user.username, **kwargs)

@user_profile.route("/change-password", methods=["POST"])
@login_required
def change_pwd():
    old_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_new_password = request.form.get("confirm_new_password")

    if new_password in COMMON_PASSWORDS:
        return profile(common_password_used=True)

    if (new_password != confirm_new_password):
        return profile(passwords_do_not_match=True)
    
    if not check_passwd_comp(new_password):
        return profile(passwd_complexity_check_failed=True)
    
    success = change_password(g.user_id, old_password, new_password)

    if not success:
        return profile(password_update_failed=True)
    
    return profile(password_updated=True)

