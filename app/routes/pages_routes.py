from flask import Blueprint, render_template, redirect, session

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    """Landing page — redirects to visitor registration, the main entry point."""
    return redirect("/visitor/register-page")


@pages_bp.route("/host/login")
def host_login_page():
    return render_template("login.html")


@pages_bp.route("/host/dashboard")
def host_dashboard_page():
    if not session.get("host_id"):
        return redirect("/host/login")
    return render_template("host_dashboard.html")


@pages_bp.route("/visitor/register-page")
def visitor_register_page():
    return render_template("visitor_register.html")


@pages_bp.route("/access/simulate")
def access_simulate_page():
    return render_template("access_status.html")


@pages_bp.route("/audit/log")
def audit_log_page():
    return render_template("audit_log.html")


@pages_bp.route("/security-console")
def security_console_page():
    if not session.get("host_id"):
        return redirect("/host/login")
    return render_template("security_console.html")