import jwt
from datetime import datetime
from flask import current_app
from app.extensions import db
from app.models import AccessToken, Visit, Resource


def issue_token(visit: Visit, device_posture: str = "trusted") -> AccessToken:
    """
    Issue a short-lived, scoped JWT for a single approved visit.
    Scope = visitor_id + resource_id + exact time window (not a generic pass).
    device_posture is captured at check-in time (simulated signal) and stored
    alongside the token so the enforcement point can apply risk-adaptive rules.
    """
    now = datetime.now()
    expires_at = visit.scheduled_end

    payload = {
        "visit_id": visit.id,
        "visitor_id": visit.visitor_id,
        "resource_id": visit.resource_id,
        "exp": expires_at,
    }

    token_str = jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm=current_app.config["JWT_ALGORITHM"],
    )

    access_token = AccessToken(
        visit_id=visit.id,
        token=token_str,
        issued_at=now,
        expires_at=expires_at,
        revoked=False,
        device_posture=device_posture,
    )
    db.session.add(access_token)
    db.session.commit()
    return access_token


def validate_token(token_str: str, requested_resource_id: int):
    """
    Zero Trust check: every access attempt is verified fresh — no implicit trust.
    Layers checked, in order: signature/expiry -> revocation -> scope -> device posture
    (risk-adaptive: an untrusted device is only blocked when the target resource is high-risk).
    Returns (is_valid: bool, reason: str, visit_id or None)
    """
    try:
        payload = jwt.decode(
            token_str,
            current_app.config["JWT_SECRET"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
            options={"verify_iat": False},
        )
    except jwt.ExpiredSignatureError:
        return False, "denied_expired", None
    except jwt.InvalidTokenError:
        return False, "denied_invalid", None

    record = AccessToken.query.filter_by(token=token_str).first()
    if record is None or record.revoked:
        return False, "denied_invalid", payload.get("visit_id")

    if payload.get("resource_id") != requested_resource_id:
        return False, "denied_scope", payload.get("visit_id")

    # Risk-adaptive device posture check: high-risk resource + untrusted device = deny
    resource = Resource.query.get(requested_resource_id)
    if resource is not None and resource.risk_level == "high" and record.device_posture == "untrusted":
        return False, "denied_device", payload.get("visit_id")

    return True, "granted", payload.get("visit_id")


def revoke_token(visit_id: int):
    """Manually revoke all tokens for a visit (e.g. host cancels visit early)."""
    tokens = AccessToken.query.filter_by(visit_id=visit_id).all()
    for t in tokens:
        t.revoked = True
    db.session.commit()