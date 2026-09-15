from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import Host

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register_host():
    """Register a new host/employee account."""
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    department = data.get("department")

    if not all([name, email, password]):
        return jsonify({"error": "name, email, and password are required"}), 400

    if Host.query.filter_by(email=email).first():
        return jsonify({"error": "Host with this email already exists"}), 409

    host = Host(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        department=department,
    )
    db.session.add(host)
    db.session.commit()

    return jsonify({"message": "Host registered", "host_id": host.id}), 201


@auth_bp.route("/login", methods=["POST"])
def login_host():
    """Host login — creates a server-side session (host dashboard uses this)."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    host = Host.query.filter_by(email=email).first()
    if host is None or not check_password_hash(host.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    session["host_id"] = host.id
    session["host_name"] = host.name

    return jsonify({"message": "Login successful", "host_id": host.id, "name": host.name}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout_host():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


def current_host_id():
    """Helper other route files can import to check who's logged in."""
    return session.get("host_id")