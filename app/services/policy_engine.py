from datetime import datetime
from app.models import Resource, Visit


# Simple risk-based rule table: which resource risk levels need host approval
# vs can be auto-approved.
AUTO_APPROVE_RISK_LEVELS = {"low"}


def evaluate_visit_request(visit: Visit) -> tuple[str, str]:
    """
    Policy Decision Point (PDP).
    Evaluates context BEFORE granting/approving a visit request.
    Returns (decision, reason) where decision is one of:
        "approved", "pending_review", "denied"
    """
    now = datetime.now()

    # Rule 1: reject visits scheduled in the past
    if visit.scheduled_end <= now:
        return "denied", "Requested time window has already passed"

    # Rule 2: end time must be after start time
    if visit.scheduled_end <= visit.scheduled_start:
        return "denied", "Invalid time window: end before start"

    # Rule 3: cap visit duration (prevents someone requesting a 30-day "visit")
    max_duration_hours = 8
    duration = visit.scheduled_end - visit.scheduled_start
    if duration.total_seconds() > max_duration_hours * 3600:
        return "denied", f"Visit duration exceeds max allowed ({max_duration_hours}h)"

    # Rule 4: risk-based routing
    resource = Resource.query.get(visit.resource_id)
    if resource is None:
        return "denied", "Requested resource does not exist"

    if resource.risk_level in AUTO_APPROVE_RISK_LEVELS:
        return "approved", "Low-risk resource — auto-approved by policy"

    # Medium/high risk resources always require explicit host approval
    return "pending_review", f"Resource risk level '{resource.risk_level}' requires host approval"


def check_conflicting_visits(visit: Visit) -> bool:
    """
    Zero trust also means checking for overlapping/suspicious bookings —
    e.g. same visitor booked into two resources at the same time.
    Returns True if a conflict exists.
    """
    overlapping = Visit.query.filter(
        Visit.visitor_id == visit.visitor_id,
        Visit.id != (visit.id or -1),
        Visit.status.in_(["approved", "checked_in"]),
        Visit.scheduled_start < visit.scheduled_end,
        Visit.scheduled_end > visit.scheduled_start,
    ).first()
    return overlapping is not None