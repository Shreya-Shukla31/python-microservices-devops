# backend/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, requests, time
from sqlalchemy.exc import OperationalError

# Create the SQLAlchemy instance without app
db = SQLAlchemy()
migrate = Migrate()

# Define models first
class User(db.Model):
    _tablename_ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Create the Flask app
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:mysecretpassword@db:5432/mydb"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB and Migrate once
    db.init_app(app)
    migrate.init_app(app, db)

    # Routes
    @app.route("/api/data", methods=["GET", "POST"])
    def data():
        if request.method == "POST":
            payload = request.json or {}
            name = payload.get("name", "anonymous")
            u = User(name=name)
            db.session.add(u)
            db.session.commit()

            # Send log to logger service
            logger_url = os.getenv("LOGGER_URL", "http://logger:9000/log")
            try:
                requests.post(logger_url, json={"event": "new_user", "name": name}, timeout=2)
            except Exception:
                pass

            return jsonify({"id": u.id, "name": u.name}), 201

        users = User.query.all()
        return jsonify([{"id": u.id, "name": u.name} for u in users])

    return app

def wait_for_db(app):
    max_retries = 10
    for i in range(max_retries):
        try:
            with app.app_context():
                # Attempt to connect to the database
                with db.engine.connect() as connection:
                    print("Database connected! ")
                    break
        except OperationalError:
            print(f"Database not ready, retrying {i+1}/{max_retries}...")
            time.sleep(5)
    else:
        print("Could not connect to database. Exiting.")
        exit(1)

# Create the app and then wait for the database
app = create_app()
wait_for_db(app)
if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5000)