from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Visitor, Visit, Resource
from app.services.policy_engine import evaluate_visit_request, check_conflicting_visits
from app.services.logger_service import log_access_attempt

visitor_bp = Blueprint("visitor", __name__, url_prefix="/visitor")


@visitor_bp.route("/register", methods=["POST"])
def register_visitor():
    """
    Step 1 of visitor flow: create visitor identity + request a visit.
    This does NOT grant access — it only creates a pending request that
    goes through the policy engine.
    """
    data = request.get_json()

    required = ["full_name", "email", "host_id", "resource_id", "scheduled_start", "scheduled_end"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    visitor = Visitor.query.filter_by(email=data["email"]).first()
    if visitor is None:
        visitor = Visitor(
            full_name=data["full_name"],
            email=data["email"],
            phone=data.get("phone"),
            id_proof_ref=data.get("id_proof_ref"),
        )
        db.session.add(visitor)
        db.session.commit()

    try:
        scheduled_start = datetime.fromisoformat(data["scheduled_start"])
        scheduled_end = datetime.fromisoformat(data["scheduled_end"])
    except ValueError:
        return jsonify({"error": "Dates must be ISO format, e.g. 2026-08-15T14:00:00"}), 400

    resource = Resource.query.get(data["resource_id"])
    if resource is None:
        return jsonify({"error": "Invalid resource_id"}), 400

    visit = Visit(
        visitor_id=visitor.id,
        host_id=data["host_id"],
        resource_id=data["resource_id"],
        purpose=data.get("purpose", ""),
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end,
        status="pending",
    )
    db.session.add(visit)
    db.session.commit()

    decision, reason = evaluate_visit_request(visit)

    if check_conflicting_visits(visit):
        decision, reason = "denied", "Conflicting visit already exists for this visitor"

    visit.status = decision
    db.session.commit()

    return jsonify({
        "message": "Visit request submitted",
        "visit_id": visit.id,
        "visitor_id": visitor.id,
        "decision": decision,
        "reason": reason,
    }), 201


@visitor_bp.route("/checkin/<int:visit_id>", methods=["POST"])
def check_in(visit_id):
    """
    Step 2: visitor checks in on arrival (e.g. scans QR / enters OTP).
    Only works if the visit was already approved and the time window is active.
    Also captures a simulated device-posture signal ("trusted"/"untrusted") sent
    from the check-in kiosk/device, used later for risk-adaptive enforcement.
    """
    data = request.get_json(silent=True) or {}
    device_posture = data.get("device_posture", "trusted")
    if device_posture not in ("trusted", "untrusted"):
        device_posture = "trusted"

    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({"error": "Visit not found"}), 404

    if visit.status != "approved":
        log_access_attempt(visit.id, visit.resource_id, "denied_invalid",
                            f"Check-in attempted but visit status is '{visit.status}'")
        return jsonify({"error": f"Visit is not approved (status: {visit.status})"}), 403

    now = datetime.now()
    if now < visit.scheduled_start or now > visit.scheduled_end:
        log_access_attempt(visit.id, visit.resource_id, "denied_expired",
                            "Check-in attempted outside scheduled time window")
        return jsonify({"error": "Outside scheduled visit window"}), 403

    # Risk-adaptive rule: an untrusted device cannot check in for a high-risk resource
    resource = Resource.query.get(visit.resource_id)
    if resource is not None and resource.risk_level == "high" and device_posture == "untrusted":
        log_access_attempt(visit.id, visit.resource_id, "denied_device",
                            "Untrusted device posture blocked check-in for a high-risk resource")
        return jsonify({"error": "Untrusted device is not permitted to check in for this resource"}), 403

    visit.status = "checked_in"
    db.session.commit()

    from app.services.token_service import issue_token
    access_token = issue_token(visit, device_posture=device_posture)

    return jsonify({
        "message": "Checked in successfully",
        "visit_id": visit.id,
        "token": access_token.token,
        "expires_at": access_token.expires_at.isoformat(),
        "device_posture": device_posture,
    }), 200


@visitor_bp.route("/checkout/<int:visit_id>", methods=["POST"])
def check_out(visit_id):
    """Visitor leaves — token revoked immediately, no need to wait for expiry."""
    from app.services.token_service import revoke_token

    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({"error": "Visit not found"}), 404

    visit.status = "checked_out"
    db.session.commit()
    revoke_token(visit.id)

    return jsonify({"message": "Checked out, access revoked", "visit_id": visit.id}), 200