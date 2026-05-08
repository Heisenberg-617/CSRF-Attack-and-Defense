from flask import Flask, jsonify
from app.database.db import get_db_connection
from app.routes.tasks import tasks_bp  # <-- ajouté

app = Flask(__name__)
app.register_blueprint(tasks_bp)

app.secret_key = "replace_with_a_long_random_value"


# -------------------------
# HEALTH CHECK ROUTE
# -------------------------
@app.route("/")
def home():
    return "Flask is running 🚀"


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

        return jsonify({
            "status": "success",
            "connected_database": db_name
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------
# MAIN ENTRY
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)