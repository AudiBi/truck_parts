from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_login import LoginManager

# Import des modèles et des vues admin
from dashboard import DashboardView
from decorators import role_requis
from models import Centre, Facture, JournalActivite, Mouvement, Piece, StockCentre, Vente, db, bcrypt, Utilisateur, Role
from admin import CentreAdmin, FactureAdmin, JournalActiviteAdmin, MouvementAdmin, PieceAdmin, RoleAdmin, StockCentreAdmin, UtilisateurAdmin, SecureModelView, VenteAdmin

from flask_admin.menu import MenuLink

from stockGlobal import StockGlobalAdmin

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'change-moi-en-vrai-secret'
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['SECRET_KEY'] = 'une-autre-cle-secrete-pour-session'  # utile pour Flask-Login et flash
    
    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Utilisateur.query.get(int(user_id))
    
    # Flask-Admin setup
    admin = Admin(app, name='Truck Parts Admin', index_view=DashboardView(name="Tableau de bord"), template_mode='bootstrap4')
   
    admin.add_view(UtilisateurAdmin(Utilisateur, db.session, name='Utilisateurs'))
    admin.add_view(SecureModelView(Role, db.session, name='Rôles'))

    admin.add_view(JournalActiviteAdmin(JournalActivite, db.session, category="Suivi"))
    admin.add_view(CentreAdmin(Centre, db.session, category="Stock"))
    admin.add_view(PieceAdmin(Piece, db.session, category="Stock"))
    admin.add_view(StockCentreAdmin(StockCentre, db.session, category="Stock"))
    admin.add_view(MouvementAdmin(Mouvement, db.session, category="Stock"))
    admin.add_view(VenteAdmin(Vente, db.session, category="Ventes"))
    admin.add_view(FactureAdmin(Facture, db.session, category="Ventes"))

    admin.add_view(StockGlobalAdmin(name="Stock Global", endpoint='stock_global', category="Rapports"))
    
    # Lien personnalisé pour déconnexion
    admin.add_link(MenuLink(name='Déconnexion', url='/auth/logout'))
    
    # Importer et enregistrer les blueprints
    from routes import auth, mouvements, ventes, stock
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(mouvements.mouvement_bp)
    app.register_blueprint(ventes.vente_bp)
    app.register_blueprint(stock.stock_bp)

    # Redirection de la racine vers la page login
    @app.route('/')
    def index():
        return redirect('/auth/login')

    # Exemple d’une route protégée avec JWT + rôle
    from flask import jsonify
    from flask_jwt_extended import jwt_required
    @app.route('/admin-only', methods=['GET'])
    @jwt_required()
    @role_requis('admin')
    def admin_only():
        return jsonify({"message": "Bienvenue admin !"})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
