from flask import Blueprint, request, jsonify
from models import db, Utilisateur

utilisateur_bp = Blueprint('utilisateurs', __name__, url_prefix='/utilisateurs')

@utilisateur_bp.route('/ajouter', methods=['GET', 'POST'])
def create_utilisateur():
    data = request.json
    utilisateur = Utilisateur(
        nom=data['nom'],
        prenom=data['prenom'],
        nom_utilisateur=data['nom_utilisateur'],
        role_id=data['role_id']
    )
    utilisateur.set_password(data['mot_de_passe'])
    db.session.add(utilisateur)
    db.session.commit()
    return jsonify({"message": "Utilisateur créé avec succès."}), 201

@utilisateur_bp.route('/liste', methods=['GET'])
def get_all_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return jsonify([
        {
            "id": u.id,
            "nom": u.nom,
            "prenom": u.prenom,
            "nom_utilisateur": u.nom_utilisateur,
            "role": u.role.nom
        } for u in utilisateurs
    ])

@utilisateur_bp.route('/rechercher/<int:id>', methods=['GET'])
def get_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    return jsonify({
        "id": utilisateur.id,
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
        "nom_utilisateur": utilisateur.nom_utilisateur,
        "role": utilisateur.role.nom
    })

@utilisateur_bp.route('/modifier<int:id>', methods=['PUT'])
def update_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    data = request.json
    utilisateur.nom = data.get('nom', utilisateur.nom)
    utilisateur.prenom = data.get('prenom', utilisateur.prenom)
    utilisateur.nom_utilisateur = data.get('nom_utilisateur', utilisateur.nom_utilisateur)
    if 'mot_de_passe' in data:
        utilisateur.set_password(data['mot_de_passe'])
    utilisateur.role_id = data.get('role_id', utilisateur.role_id)
    db.session.commit()
    return jsonify({"message": "Utilisateur mis à jour."})

@utilisateur_bp.route('/supprimer/<int:id>', methods=['DELETE'])
def delete_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé."})

# @utilisateur_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     utilisateur = Utilisateur.query.filter_by(nom_utilisateur=data['nom_utilisateur']).first()
#     if utilisateur and utilisateur.check_password(data['mot_de_passe']):
#         return jsonify({"message": "Connexion réussie", "user_id": utilisateur.id})
#     return jsonify({"message": "Identifiants invalides"}), 401
