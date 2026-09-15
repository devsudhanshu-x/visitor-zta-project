from flask import Flask
from app.config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.visitor_routes import visitor_bp
    from app.routes.policy_routes import policy_bp
    from app.routes.access_routes import access_bp, audit_bp
    from app.routes.pages_routes import pages_bp
    from app.routes.console_routes import console_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(visitor_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(access_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(console_bp)

    return app