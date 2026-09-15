from flask import Blueprint, jsonify, session
from datetime import datetime
from app.extensions import db
from app.models import Visit, AccessToken, Visitor, Resource

console_bp = Blueprint("console", __name__, url_prefix="/console")


@console_bp.route("/active-visits", methods=["GET"])
def active_visits():
    """
    Security console feed: every visit that is currently checked-in
    (has a live, non-revoked token) — the real-time picture of who
    is inside right now, which resource, and their device posture.
    """
    if not session.get("host_id"):
        return jsonify({"error": "Must be logged in as host"}), 401

    rows = (
        db.session.query(Visit, Visitor, Resource, AccessToken)
        .join(Visitor, Visit.visitor_id == Visitor.id)
        .join(Resource, Visit.resource_id == Resource.id)
        .join(AccessToken, AccessToken.visit_id == Visit.id)
        .filter(Visit.status == "checked_in", AccessToken.revoked == False)  # noqa: E712
        .all()
    )

    result = []
    for visit, visitor, resource, token in rows:
        result.append({
            "visit_id": visit.id,
            "visitor_name": visitor.full_name,
            "resource_name": resource.name,
            "resource_risk": resource.risk_level,
            "device_posture": token.device_posture,
            "expires_at": token.expires_at.isoformat(),
        })

    return jsonify(result), 200


@console_bp.route("/revoke/<int:visit_id>", methods=["POST"])
def revoke_from_console(visit_id):
    """One-click revoke straight from the security console."""
    if not session.get("host_id"):
        return jsonify({"error": "Must be logged in as host"}), 401

    from app.services.token_service import revoke_token

    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({"error": "Visit not found"}), 404

    visit.status = "checked_out"
    db.session.commit()
    revoke_token(visit.id)

    return jsonify({"message": "Access revoked from console", "visit_id": visit.id}), 200


@console_bp.route("/stats", methods=["GET"])
def console_stats():
    """
    Summary metrics for the console header — a lightweight version of the
    evaluation metrics the platform is expected to expose (authorization
    accuracy proxy, revocation count, active session count).
    """
    if not session.get("host_id"):
        return jsonify({"error": "Must be logged in as host"}), 401

    from app.models import AccessLog

    total_attempts = db.session.query(AccessLog).count()
    granted = db.session.query(AccessLog).filter_by(result="granted").count()
    denied = total_attempts - granted
    active_sessions = (
        db.session.query(Visit)
        .filter(Visit.status == "checked_in")
        .count()
    )
    revoked_tokens = db.session.query(AccessToken).filter_by(revoked=True).count()

    accuracy = round((granted / total_attempts) * 100, 1) if total_attempts else 0.0

    return jsonify({
        "total_attempts": total_attempts,
        "granted": granted,
        "denied": denied,
        "authorization_accuracy_pct": accuracy,
        "active_sessions": active_sessions,
        "revoked_tokens": revoked_tokens,
    }), 200