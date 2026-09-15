from flask import Blueprint, request, jsonify
from app.services.token_service import validate_token
from app.services.logger_service import log_access_attempt, get_recent_logs

access_bp = Blueprint("access", __name__, url_prefix="/access")
audit_bp = Blueprint("audit", __name__, url_prefix="/audit")


@access_bp.route("/check", methods=["POST"])
def check_access():
    """
    Simulates a door/system reader checking a visitor's token.
    Called every single time someone tries to access a resource —
    zero trust means nothing is remembered as "already trusted".

    Body: { "token": "<jwt>", "resource_id": 3 }
    """
    data = request.get_json()
    token_str = data.get("token")
    resource_id = data.get("resource_id")

    if not token_str or resource_id is None:
        return jsonify({"error": "token and resource_id are required"}), 400

    is_valid, reason, visit_id = validate_token(token_str, resource_id)

    log_access_attempt(visit_id, resource_id, reason, reason)

    if is_valid:
        return jsonify({"access": "granted", "visit_id": visit_id}), 200

    status_map = {
        "denied_expired": 403,
        "denied_scope": 403,
        "denied_invalid": 401,
        "denied_device": 403,
    }
    return jsonify({"access": "denied", "reason": reason}), status_map.get(reason, 403)


@audit_bp.route("/logs", methods=["GET"])
def audit_logs():
    """Returns recent access attempts as JSON for the audit log page."""
    logs = get_recent_logs(limit=50)
    return jsonify([{
        "id": l.id,
        "visit_id": l.visit_id,
        "resource_id": l.resource_id,
        "attempted_at": l.attempted_at.strftime("%Y-%m-%d %H:%M:%S"),
        "result": l.result,
        "reason": l.reason,
    } for l in logs]), 200