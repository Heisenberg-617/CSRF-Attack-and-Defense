from flask import Flask
# from database.db import init_db

app = Flask(__name__)
app.secret_key = "replace_with_a_long_random_value"  # needed for session

# Configure DB (example)
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'csrf_project'
# app.config['MYSQL_HOST'] = 'db'  # Docker service name
# init_db(app)  # sets up mysql connection

@app.route("/")
def home():
    return "Flask is working 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)