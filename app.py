from flask import Flask, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Crée les instances globales (sans app)
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'votre_clé_secrète'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise les extensions avec l'app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Import des Blueprints ici pour éviter les imports circulaires
    from routes import (
        auth,
        roles,
        utilisateurs,
        centres,
        mouvements,
        pieces,
        ventes,
        tickets,
        factures,
        admin
    )

    app.register_blueprint(utilisateurs.utilisateur_bp)
    app.register_blueprint(roles.role_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(centres.centre_bp)
    app.register_blueprint(pieces.piece_bp)
    app.register_blueprint(mouvements.mouvement_bp)
    app.register_blueprint(ventes.vente_bp)
    app.register_blueprint(factures.facture_bp)
    app.register_blueprint(tickets.ticket_bp)
    app.register_blueprint(admin.admin_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @app.route('/dashboard')
    def dashboard():
        if 'utilisateur' in session:
            role = session['utilisateur']['role']
            if role == 'admin':
                return redirect(url_for('admin_bp.admin_dashboard'))
            elif role == 'vendeur':
                return redirect(url_for('vente_bp.dashboard_vendeur'))
        return redirect(url_for('auth.login'))

    return app
