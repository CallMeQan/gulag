from flask import Blueprint, session, render_template, redirect, url_for
from flask_login import login_required
from ..models import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')