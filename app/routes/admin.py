from flask import Blueprint, session, render_template, redirect, url_for
from ..models import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('admin/dashboard.html')
    return redirect(url_for("home.index"))