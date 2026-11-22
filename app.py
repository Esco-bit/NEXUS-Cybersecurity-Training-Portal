
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from datetime import datetime
from functools import wraps
import sqlite3
import os

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from assessments import PHISHING_ASSESSMENT


# ==================================================
# APPLICATION CONFIGURATION
# ==================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "local-training-only-change-before-deployment"
)

DATABASE = os.path.join(
    os.path.dirname(__file__),
    "nexus_users.db"
)

MAX_ATTEMPTS = 3

visits = []
attempts = []


# ==================================================
# DATABASE CONFIGURATION
# ==================================================

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            event TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


def record_event(user_id, username, event):
    connection = get_db()

    connection.execute("""
        INSERT INTO login_history
        (user_id, username, event, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        username,
        event,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


init_db()


# ==================================================
# AUTHENTICATION DECORATOR
# ==================================================

def login_required(route_function):

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please sign in to access the training portal.")
            return redirect(url_for("home"))

        return route_function(*args, **kwargs)

    return wrapper


# ==================================================
# SIGN IN
# ==================================================

@app.route("/", methods=["GET", "POST"])
def home():

    if "user_id" in session:
        return redirect(url_for("challenge"))

    message = ""

    failed_attempts = session.get("failed_attempts", 0)

    if request.method == "POST":

        if failed_attempts >= MAX_ATTEMPTS:

            message = (
                "Access temporarily locked. "
                "Use the training recovery options."
            )

        else:

            username = request.form.get(
                "username", ""
            ).strip()

            password = request.form.get(
                "password", ""
            )

            connection = get_db()

            user = connection.execute("""
                SELECT * FROM users
                WHERE username = ?
            """, (username,)).fetchone()

            connection.close()

            if user and check_password_hash(
                user["password_hash"], password
            ):

                session.clear()

                session["user_id"] = user["id"]
                session["username"] = user["username"]

                record_event(
                    user["id"],
                    user["username"],
                    "Successful sign-in"
                )

                return redirect(url_for("challenge"))

            failed_attempts += 1

            session["failed_attempts"] = failed_attempts

            attempts.append({
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "event": "Failed sign-in"
            })

            if failed_attempts >= MAX_ATTEMPTS:

                message = (
                    "Maximum attempts reached. "
                    "Access is temporarily locked."
                )

            else:

                message = (
                    "Incorrect username or password. "
                    "Please try again."
                )

    else:
        visits.append(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    failed_attempts = session.get("failed_attempts", 0)

    return render_template(
        "login.html",
        message=message,
        attempts_remaining=max(
            0, MAX_ATTEMPTS - failed_attempts
        ),
        show_recovery=failed_attempts >= MAX_ATTEMPTS
    )


# ==================================================
# USER REGISTRATION
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if "user_id" in session:
        return redirect(url_for("challenge"))

    message = ""

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        confirm_password = request.form.get(
            "confirm_password", ""
        )

        if len(username) < 3:

            message = "Username must contain at least 3 characters."

        elif len(username) > 30:

            message = "Username cannot exceed 30 characters."

        elif not username.replace("_", "").isalnum():

            message = (
                "Username can contain only letters, "
                "numbers and underscores."
            )

        elif len(password) < 10:

            message = "Password must contain at least 10 characters."

        elif password != confirm_password:

            message = "Passwords do not match."

        else:

            connection = get_db()

            try:

                password_hash = generate_password_hash(password)

                cursor = connection.execute("""
                    INSERT INTO users
                    (username, password_hash, created_at)
                    VALUES (?, ?, ?)
                """, (
                    username,
                    password_hash,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ))

                connection.commit()

                user_id = cursor.lastrowid

                record_event(
                    user_id,
                    username,
                    "Account registered"
                )

                # RESET FAILED LOGIN ATTEMPTS
                session.pop("failed_attempts", None)

                flash(
                    "Account created successfully. "
                    "You can now sign in."
                )

                return redirect(url_for("home"))

            except sqlite3.IntegrityError:

                message = "That username is already registered."

            finally:

                connection.close()

    return render_template(
        "register.html",
        message=message
    )


# ==================================================
# SIGN OUT
# ==================================================

@app.route("/logout")
@login_required
def logout():

    user_id = session.get("user_id")
    username = session.get("username")

    record_event(
        user_id,
        username,
        "Signed out"
    )

    session.clear()

    flash("You have successfully signed out.")

    return redirect(url_for("home"))


# ==================================================
# PASSWORD RECOVERY AND SIMULATED SSO
# ==================================================

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    message = ""

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        new_password = request.form.get(
            "new_password", ""
        )

        confirm_password = request.form.get(
            "confirm_password", ""
        )

        if not username:

            message = "Please enter your username."

        elif len(new_password) < 10:

            message = "New password must contain at least 10 characters."

        elif new_password != confirm_password:

            message = "The passwords do not match."

        else:

            connection = get_db()

            user = connection.execute("""
                SELECT id, username
                FROM users
                WHERE username = ?
            """, (username,)).fetchone()

            if user:

                new_hash = generate_password_hash(new_password)

                connection.execute("""
                    UPDATE users
                    SET password_hash = ?
                    WHERE id = ?
                """, (new_hash, user["id"]))

                connection.commit()

            connection.close()

            if user:

                session.pop("failed_attempts", None)

                flash(
                    "Password updated successfully. "
                    "You can now sign in with your new password."
                )

                return redirect(url_for("home"))

            else:

                message = "No account was found with that username."

    return render_template(
        "recovery.html",
        message=message
    )


@app.route("/sso-demo")
def sso_demo():
    return render_template("sso.html")


# ==================================================
# TRAINING DASHBOARD
# ==================================================

@app.route("/challenge")
@login_required
def challenge():

    return render_template(
        "challenge.html",
        username=session.get("username")
    )


# ==================================================
# PHISHING ASSESSMENT
# ==================================================

@app.route("/assessment")
@login_required
def assessment():

    return render_template(
        "assessment.html",
        assessment=PHISHING_ASSESSMENT
    )


@app.route("/grade", methods=["POST"])
@login_required
def grade_assessment():

    questions = PHISHING_ASSESSMENT["questions"]

    results = []
    score = 0

    for question in questions:

        submitted = request.form.get(
            f"q{question['id']}"
        )

        correct = (
            submitted is not None
            and submitted.isdigit()
            and int(submitted) == question["answer"]
        )

        if correct:
            score += question["points"]

        results.append({

            "question": question["question"],

            "selected": (
                question["options"][int(submitted)]
                if submitted is not None
                and submitted.isdigit()
                and 0 <= int(submitted) < len(question["options"])
                else "No answer submitted"
            ),

            "correct_answer": question["options"][
                question["answer"]
            ],

            "passed": correct,

            "explanation": question["explanation"],

            "points": question["points"],

        })

    total = sum(
        question["points"] for question in questions
    )

    return render_template(
        "results.html",
        results=results,
        score=score,
        total=total,
        percentage=round(
            (score / total) * 100
        ) if total else 0
    )


# ==================================================
# PRACTICAL TRAINING MODULES
# ==================================================

MODULES = {

    "url-analysis": {

        "title": "Suspicious URL Analysis",

        "category": "NETWORK SECURITY",

        "description": (
            "Investigate suspicious URLs and identify "
            "potential malicious indicators."
        ),

        "objectives": [
            "Identify suspicious domain names and typosquatting.",
            "Understand URL structure and encoded characters.",
            "Recognize suspicious redirects and subdomains.",
            "Explain why HTTPS does not guarantee trust."
        ],

        "scenario": (
            "An employee receives a message containing "
            "https://secure-company.example.login-check.test. "
            "They are asked to verify their account urgently."
        ),

        "tasks": [
            "Identify the registered domain in the example URL.",
            "Explain why the subdomain structure is suspicious.",
            "Identify two indicators of social engineering.",
            "Describe how you would investigate the URL safely without visiting it."
        ]
    },

    "linux-logs": {

        "title": "Linux Log Investigation",

        "category": "LINUX SECURITY",

        "description": (
            "Investigate authentication events and identify "
            "suspicious login activity."
        ),

        "objectives": [
            "Understand Linux authentication logs.",
            "Identify failed SSH login attempts.",
            "Recognize suspicious login patterns.",
            "Build an initial incident timeline."
        ],

        "scenario": (
            "A server records multiple failed SSH authentication "
            "attempts followed by a successful login from an "
            "unfamiliar IP address."
        ),

        "tasks": [
            "Identify the authentication events that require investigation.",
            "Explain what repeated failed SSH attempts may indicate.",
            "Determine which information you need to establish the source.",
            "Describe your next three defensive investigation steps."
        ]
    },

    "network-analysis": {

        "title": "Network Traffic Analysis",

        "category": "NETWORK SECURITY",

        "description": (
            "Understand network traffic and identify unusual "
            "communication patterns."
        ),

        "objectives": [
            "Understand TCP and UDP.",
            "Recognize DNS and HTTP traffic.",
            "Interpret source and destination addresses.",
            "Identify unusual connection patterns."
        ],

        "scenario": (
            "A workstation makes repeated DNS requests to an "
            "unfamiliar domain and establishes connections "
            "to an unusual external destination."
        ),

        "tasks": [
            "Explain the purpose of DNS.",
            "Identify the source and destination in a network connection.",
            "Explain why repeated unusual DNS requests deserve investigation.",
            "Describe how Wireshark can help investigate this activity."
        ]
    },

    "incident-response": {

        "title": "Incident Response",

        "category": "SECURITY OPERATIONS",

        "description": (
            "Investigate security incidents and select "
            "appropriate defensive actions."
        ),

        "objectives": [
            "Perform initial incident triage.",
            "Preserve digital evidence.",
            "Understand containment and eradication.",
            "Document incident response actions."
        ],

        "scenario": (
            "An employee reports that their workstation displayed "
            "an unexpected security alert and began communicating "
            "with an unfamiliar external server."
        ),

        "tasks": [
            "Identify the first information you should collect.",
            "Explain when endpoint isolation may be appropriate.",
            "Describe how you would preserve evidence.",
            "Outline containment, eradication and recovery."
        ]
    },

    "siem-soc": {

        "title": "SIEM & SOC Operations",

        "category": "SECURITY MONITORING",

        "description": (
            "Investigate security alerts and correlate events "
            "across systems."
        ),

        "objectives": [
            "Understand SIEM architecture.",
            "Interpret security alerts.",
            "Correlate related events.",
            "Document investigation findings."
        ],

        "scenario": (
            "Your SIEM generates alerts for repeated failed logins, "
            "a suspicious login and an unusual privilege escalation event."
        ),

        "tasks": [
            "Explain why these alerts may be related.",
            "Identify which event should receive immediate investigation.",
            "Describe the evidence you would collect.",
            "Write a short SOC incident summary."
        ]
    },

    "vulnerability-assessment": {

        "title": "Vulnerability Assessment",

        "category": "SYSTEM SECURITY",

        "description": (
            "Identify security weaknesses and recommend "
            "appropriate remediation."
        ),

        "objectives": [
            "Understand vulnerability scanning.",
            "Interpret vulnerability severity.",
            "Recognize outdated software risks.",
            "Recommend defensive remediation."
        ],

        "scenario": (
            "An authorized vulnerability scan identifies an "
            "outdated service, a weak configuration and an "
            "exposed administrative interface."
        ),

        "tasks": [
            "Explain the difference between a vulnerability and a threat.",
            "Prioritize the findings based on risk.",
            "Explain why exposed administrative interfaces are concerning.",
            "Recommend remediation and verification steps."
        ]
    }
}


@app.route("/module/<module_id>")
@login_required
def module(module_id):

    selected_module = MODULES.get(module_id)

    if selected_module is None:
        return "Module not found", 404

    return render_template(
        "module.html",
        module=selected_module,
        module_id=module_id
    )


# ==================================================
# USER AND SYSTEM RECORDS
# ==================================================

@app.route("/dashboard")
@login_required
def dashboard():

    connection = get_db()

    user_count = connection.execute("""
        SELECT COUNT(*) AS total FROM users
    """).fetchone()["total"]

    history = connection.execute("""
        SELECT username, event, timestamp
        FROM login_history
        ORDER BY id DESC
        LIMIT 50
    """).fetchall()

    connection.close()

    return {
        "registered_users": user_count,
        "total_visits": len(visits),
        "submission_events": len(attempts),
        "recent_visits": visits[-10:],
        "recent_attempts": attempts[-10:],
        "login_history": [
            dict(record) for record in history
        ]
    }


# ==================================================
# APPLICATION START
# ==================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5002,
        debug=True
    )
