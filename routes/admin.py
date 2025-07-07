from flask import Blueprint, render_template, session
from decorators import login_required, role_required

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('dashboard/admin_dashboard.html', utilisateur=session.get('utilisateur'))
