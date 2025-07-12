from flask_admin import BaseView, expose
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for
from flask_login import current_user
from models import Role, Utilisateur, db

class DashboardView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        stats = {
            'total_utilisateurs': db.session.query(Utilisateur).count(),
            'total_roles': db.session.query(Role).count(),
        }
        
        return self.render('admin/dashboard.html', stats=stats)
