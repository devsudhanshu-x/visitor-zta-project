from app.extensions import db
from app.models import AccessLog


def log_access_attempt(visit_id, resource_id, result, reason):
    """
    Zero Trust principle: log EVERY access attempt, granted or denied.
    This is the audit trail evaluators/security reviewers rely on.

    result: "granted" | "denied_expired" | "denied_scope" | "denied_invalid"
    """
    entry = AccessLog(
        visit_id=visit_id,
        resource_id=resource_id,
        result=result,
        reason=reason,
    )
    db.session.add(entry)
    db.session.commit()
    return entry


def get_logs_for_visit(visit_id):
    """Fetch full access history for one visit — useful for the audit dashboard."""
    return AccessLog.query.filter_by(visit_id=visit_id).order_by(AccessLog.attempted_at.desc()).all()


def get_recent_logs(limit=50):
    """Fetch most recent access attempts across all visitors — for the live dashboard."""
    return AccessLog.query.order_by(AccessLog.attempted_at.desc()).limit(limit).all()