import sys
import os
from pathlib import Path

# Ensure the app directory is in Python path so imports work correctly
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from flask import Flask, render_template, session
from database.db import get_db_connection

# Authentication /  Task and team features routes
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.teams import teams_bp
from routes.admin import admin_bp

# Create Flask app instance
app = Flask(__name__)

# Register feature routes (blueprints)
app.register_blueprint(tasks_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Secret key used to sign session cookies
app.secret_key = os.environ.get('SECRET_KEY', 'replace_with_a_long_random_value')

# -------------------------
# HEALTH CHECK ROUTE
# -------------------------
@app.route("/")
def home():
    return render_template('index.html')


# -------------------------
# DB TEST ROUTE (VERY IMPORTANT)
# -------------------------
@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()

        cursor.close()
        conn.close()

        return {
            "status": "success",
            "connected_database": db_name[0] if db_name else "Unknown"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500


@app.route("/seed-check")
def seed_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM teams")
        team_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            "status": "success",
            "counts": {
                "users": user_count,
                "teams": team_count,
                "tasks": task_count
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500


@app.context_processor
def inject_user_role():
    return dict(current_role=session.get('role', 'guest'))

# -------------------------
# ERROR HANDLERS
# -------------------------
@app.errorhandler(403)
def handle_csrf_error(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def handle_404_error(e):
    return render_template('errors/404.html'), 404


# -------------------------
# MAIN ENTRY
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)