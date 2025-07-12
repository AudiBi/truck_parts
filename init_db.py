from app import create_app
from models import db, Role, Utilisateur

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Création des rôles
    admin_role = Role(nom='admin')
    vendeur_role = Role(nom='vendeur')
    gestionnaire_role = Role(nom='gestionnaire')
    db.session.add_all([admin_role, vendeur_role, gestionnaire_role])
    db.session.commit()

    # Utilisateur admin
    admin = Utilisateur(
        nom='Admin',
        prenom='Super',
        nom_utilisateur='admin'
    )
    admin.set_password('admin123')
    admin.role = admin_role

    # Utilisateur vendeur
    vendeur = Utilisateur(
        nom='Dupont',
        prenom='Jean',
        nom_utilisateur='vendeur'
    )
    vendeur.set_password('vendeur123')
    vendeur.role = vendeur_role

    # Utilisateur gestionnaire
    gestionnaire = Utilisateur(
        nom='Martin',
        prenom='Julie',
        nom_utilisateur='gestionnaire'
    )
    gestionnaire.set_password('gestion123')
    gestionnaire.role = gestionnaire_role

    db.session.add_all([admin, vendeur, gestionnaire])
    db.session.commit()
    print("Base initialisée avec succès.")
