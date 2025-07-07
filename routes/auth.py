from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models import db, Utilisateur

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur.query.filter_by(nom_utilisateur=nom_utilisateur).first()

        if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
            session['utilisateur'] = {
                'id': utilisateur.id,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                'role': utilisateur.role.nom
            }
            flash('Connexion réussie.', 'success')
            if utilisateur.role.nom == 'admin':
                return redirect(url_for('admin_bp.admin_dashboard'))
            elif utilisateur.role.nom == 'vendeur':
                return redirect(url_for('vente_bp.dashboard_vendeur'))
            return redirect(url_for('dashboard'))

        flash('Identifiants invalides.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('auth.login'))
