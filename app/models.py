from datetime import datetime
from app.extensions import db


class Host(db.Model):
    __tablename__ = "hosts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    visits = db.relationship("Visit", backref="host", lazy=True, foreign_keys="Visit.host_id")


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150))
    risk_level = db.Column(db.String(20), default="low")

    visits = db.relationship("Visit", backref="resource", lazy=True)


class Visitor(db.Model):
    __tablename__ = "visitors"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    id_proof_ref = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    visits = db.relationship("Visit", backref="visitor", lazy=True)


class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitors.id"), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"), nullable=False)
    purpose = db.Column(db.String(255))
    scheduled_start = db.Column(db.DateTime, nullable=False)
    scheduled_end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")
    approved_by = db.Column(db.Integer, db.ForeignKey("hosts.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tokens = db.relationship("AccessToken", backref="visit", lazy=True)
    logs = db.relationship("AccessLog", backref="visit", lazy=True)


class AccessToken(db.Model):
    __tablename__ = "access_tokens"

    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.id"), nullable=False)
    token = db.Column(db.String(2000), nullable=False)
    issued_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=False)
    device_posture = db.Column(db.String(20), default="trusted")
    # "trusted" or "untrusted" — simulated device-posture signal captured at check-in


class AccessLog(db.Model):
    __tablename__ = "access_logs"

    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.id"), nullable=True)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"), nullable=True)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(255))