# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from forms import LoginForm
from models import Utilisateur
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(nom_utilisateur=form.nom_utilisateur.data).first()
        if user and user.check_password(form.mot_de_passe.data):
            login_user(user)
            flash('Connexion réussie.', 'success')

            # Redirection selon le rôle
            role = user.role.nom.lower()
            if role == 'admin':
                return redirect(url_for('admin.index'))
            elif role == 'vendeur':
                return redirect(url_for('ventes.dashboard_vendeur'))
            elif role == 'gestionnaire':
                return redirect(url_for('mouvements.dashboard_gestionnaire'))
            else:
                flash("Rôle utilisateur inconnu.", "warning")
                return redirect(url_for('auth.login'))

        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('auth.login'))
