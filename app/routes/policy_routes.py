from flask import Blueprint, request, jsonify, session
from app.extensions import db
from app.models import Visit

policy_bp = Blueprint("policy", __name__, url_prefix="/policy")


@policy_bp.route("/pending", methods=["GET"])
def list_pending_visits():
    """Host dashboard: show all visits waiting for manual approval."""
    visits = Visit.query.filter_by(status="pending_review").all()
    return jsonify([{
        "visit_id": v.id,
        "visitor_id": v.visitor_id,
        "resource_id": v.resource_id,
        "purpose": v.purpose,
        "scheduled_start": v.scheduled_start.isoformat(),
        "scheduled_end": v.scheduled_end.isoformat(),
    } for v in visits]), 200


@policy_bp.route("/approve/<int:visit_id>", methods=["POST"])
def approve_visit(visit_id):
    """
    Host manually approves a visit that the policy engine flagged
    (e.g. medium/high risk resource).
    """
    host_id = session.get("host_id")
    if host_id is None:
        return jsonify({"error": "Must be logged in as host"}), 401

    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({"error": "Visit not found"}), 404

    if visit.status != "pending_review":
        return jsonify({"error": f"Visit is not pending review (status: {visit.status})"}), 400

    visit.status = "approved"
    visit.approved_by = host_id
    db.session.commit()

    return jsonify({"message": "Visit approved", "visit_id": visit.id}), 200


@policy_bp.route("/deny/<int:visit_id>", methods=["POST"])
def deny_visit(visit_id):
    host_id = session.get("host_id")
    if host_id is None:
        return jsonify({"error": "Must be logged in as host"}), 401

    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({"error": "Visit not found"}), 404

    visit.status = "denied"
    visit.approved_by = host_id
    db.session.commit()

    return jsonify({"message": "Visit denied", "visit_id": visit.id}), 200