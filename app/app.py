import sys
import os
from pathlib import Path

# Add app directory to Python path for imports
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from flask import Flask, render_template, session
from flask_session import Session
from app.database.db import get_db_connection
from routes.auth import auth_bp

from app.routes.tasks import tasks_bp  # <-- ajouté
from app.routes.teams import teams_bp

app = Flask(__name__)

# Task and Team routes
app.register_blueprint(tasks_bp)
app.register_blueprint(teams_bp)

app.secret_key = os.environ.get('SECRET_KEY', 'replace_with_a_long_random_value')


# Auto-configuration for Flask-Session
app.register_blueprint(auth_bp)


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