import sqlite3
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from werkzeug.security import check_password_hash
from database.db import init_db, seed_db, create_user, get_user_by_email
from database import queries

app = Flask(__name__)
app.secret_key = "dev-secret-key"


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def login_required():
    if not session.get("user_id"):
        abort(401)


def _parse_iso_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _preset_range(preset, today=None):
    today = today or date.today()
    if preset == "month":
        n = 1
    elif preset == "3months":
        n = 3
    elif preset == "6months":
        n = 6
    else:
        return (None, None)
    months_back = n - 1
    y, m = today.year, today.month - months_back
    while m <= 0:
        m += 12
        y -= 1
    return (date(y, m, 1).isoformat(), today.isoformat())


def _detect_active_preset(date_from_str, date_to_str, today=None):
    if not date_from_str and not date_to_str:
        return "all"
    for name in ("month", "3months", "6months"):
        if (date_from_str, date_to_str) == _preset_range(name, today):
            return name
    return "custom"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        flash("All fields are required.")
        return render_template("register.html")

    if password != confirm_password:
        flash("Passwords do not match.")
        return render_template("register.html")

    if len(password) < 8:
        flash("Password must be at least 8 characters.")
        return render_template("register.html")

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        flash("Email already registered.")
        return render_template("register.html")

    flash("Account created! Please sign in.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"] = user["id"]
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user = queries.get_user_by_id(user_id)
    if user is None:
        session.clear()
        return redirect(url_for("login"))

    df = _parse_iso_date(request.args.get("date_from", "").strip())
    dt = _parse_iso_date(request.args.get("date_to", "").strip())
    if df and dt and df > dt:
        flash("Start date must be before end date.")
        df = dt = None

    df_iso = df.isoformat() if df else None
    dt_iso = dt.isoformat() if dt else None

    stats = queries.get_summary_stats(user_id, date_from=df_iso, date_to=dt_iso)
    transactions = queries.get_recent_transactions(user_id, date_from=df_iso, date_to=dt_iso)
    categories = queries.get_category_breakdown(user_id, date_from=df_iso, date_to=dt_iso)

    today = date.today()
    presets = {
        "month": _preset_range("month", today),
        "3months": _preset_range("3months", today),
        "6months": _preset_range("6months", today),
    }
    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
        date_from=df_iso or "",
        date_to=dt_iso or "",
        presets=presets,
        active_preset=_detect_active_preset(df_iso, dt_iso, today),
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
