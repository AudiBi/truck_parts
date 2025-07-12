from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import db, Utilisateur, Role, JournalActivite
from utils import role_requis, enregistrer_action
from sqlalchemy import and_
from datetime import datetime

utilisateur_bp = Blueprint('utilisateurs', __name__, url_prefix='/utilisateurs')


# LOGIN
# @utilisateur_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     utilisateur = Utilisateur.query.filter_by(nom_utilisateur=data['nom_utilisateur']).first()
#     if utilisateur and utilisateur.check_password(data['mot_de_passe']):
#         access_token = create_access_token(identity={
#             'id': utilisateur.id,
#             'role': utilisateur.role.nom
#         })
#         enregistrer_action(utilisateur.id, "Connexion")
#         return jsonify(access_token=access_token), 200
#     return jsonify({"message": "Identifiants invalides"}), 401

# CHANGER LE MOT DE PASSE
@utilisateur_bp.route('/changer-mot-de-passe', methods=['PUT'])
@jwt_required()
def changer_mot_de_passe():
    data = request.get_json()
    identite = get_jwt_identity()
    utilisateur = Utilisateur.query.get_or_404(identite['id'])

    mot_de_passe_actuel = data.get('mot_de_passe_actuel')
    nouveau_mot_de_passe = data.get('nouveau_mot_de_passe')

    if not utilisateur.check_password(mot_de_passe_actuel):
        return jsonify({"message": "Mot de passe actuel incorrect."}), 401

    utilisateur.set_password(nouveau_mot_de_passe)
    db.session.commit()

    enregistrer_action(utilisateur.id, "Changement de mot de passe")
    return jsonify({"message": "Mot de passe mis à jour avec succès."})

# PROFIL
@utilisateur_bp.route('/me', methods=['GET'])
@jwt_required()
def get_mon_profil():
    identite = get_jwt_identity()
    utilisateur = Utilisateur.query.get_or_404(identite['id'])

    return jsonify({
        "id": utilisateur.id,
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
        "nom_utilisateur": utilisateur.nom_utilisateur,
        "role": utilisateur.role.nom
    })

# TOUS LES JOURNAUX
@utilisateur_bp.route('/journal/tous', methods=['GET'])
@jwt_required()
@role_requis("admin")
def journal_tous_utilisateurs():
    limit = request.args.get('limite', type=int)
    query = JournalActivite.query.order_by(JournalActivite.date.desc())

    if limit:
        query = query.limit(limit)

    logs = query.all()

    return jsonify([
        {
            "utilisateur_id": log.utilisateur_id,
            "action": log.action,
            "ip": log.ip,
            "date": log.date.strftime("%Y-%m-%d %H:%M:%S")
        } for log in logs
    ])

# JOURNAL PERSONEL
@utilisateur_bp.route('/journal', methods=['GET'])
@jwt_required()
def voir_journal_personnel():
    identite = get_jwt_identity()
    limit = request.args.get('limite', type=int)

    query = JournalActivite.query.filter_by(utilisateur_id=identite['id']).order_by(JournalActivite.date.desc())
    if limit:
        query = query.limit(limit)

    logs = query.all()

    return jsonify([
        {
            "action": log.action,
            "ip": log.ip,
            "date": log.date.strftime("%Y-%m-%d %H:%M:%S")
        } for log in logs
    ])

# RECHERCHER JOURNAL
@utilisateur_bp.route('/journal/rechercher', methods=['GET'])
@jwt_required()
@role_requis("admin")
def rechercher_journal():
    utilisateur_id = request.args.get('utilisateur_id', type=int)
    date_debut = request.args.get('date_debut')  # format: YYYY-MM-DD
    date_fin = request.args.get('date_fin')      # format: YYYY-MM-DD
    motcle = request.args.get('motcle', type=str)
    limite = request.args.get('limite', type=int)

    query = JournalActivite.query

    if utilisateur_id:
        query = query.filter_by(utilisateur_id=utilisateur_id)

    if date_debut:
        try:
            date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
            query = query.filter(JournalActivite.date >= date_debut_obj)
        except ValueError:
            return jsonify({"message": "Format de date_debut invalide (YYYY-MM-DD)"}), 400

    if date_fin:
        try:
            date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d")
            query = query.filter(JournalActivite.date <= date_fin_obj)
        except ValueError:
            return jsonify({"message": "Format de date_fin invalide (YYYY-MM-DD)"}), 400

    if motcle:
        query = query.filter(JournalActivite.action.ilike(f"%{motcle}%"))

    query = query.order_by(JournalActivite.date.desc())
    if limite:
        query = query.limit(limite)

    logs = query.all()

    return jsonify([
        {
            "utilisateur_id": log.utilisateur_id,
            "action": log.action,
            "ip": log.ip,
            "date": log.date.strftime("%Y-%m-%d %H:%M:%S")
        } for log in logs
    ])

# AJOUTER UN UTILISATEUR
@utilisateur_bp.route('/ajouter', methods=['POST'])
@jwt_required()
@role_requis("admin")
def create_utilisateur():
    data = request.json
    if Utilisateur.query.filter_by(nom_utilisateur=data['nom_utilisateur']).first():
        return jsonify({"message": "Nom d'utilisateur déjà utilisé"}), 400
    if not Role.query.get(data['role_id']):
        return jsonify({"message": "Rôle invalide"}), 400

    utilisateur = Utilisateur(
        nom=data['nom'],
        prenom=data['prenom'],
        nom_utilisateur=data['nom_utilisateur'],
        role_id=data['role_id']
    )
    utilisateur.set_password(data['mot_de_passe'])
    db.session.add(utilisateur)
    db.session.commit()

    enregistrer_action(get_jwt_identity()['id'], "Création d'un utilisateur")
    return jsonify({"message": "Utilisateur créé avec succès."}), 201


# LISTER TOUS LES UTILISATEURS
@utilisateur_bp.route('/liste', methods=['GET'])
@jwt_required()
@role_requis("admin")
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


# AFFICHER UN UTILISATEUR PAR ID
@utilisateur_bp.route('/rechercher/<int:id>', methods=['GET'])
@jwt_required()
@role_requis("admin")
def get_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    return jsonify({
        "id": utilisateur.id,
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
        "nom_utilisateur": utilisateur.nom_utilisateur,
        "role": utilisateur.role.nom
    })


# MODIFIER UN UTILISATEUR
@utilisateur_bp.route('/modifier/<int:id>', methods=['PUT'])
@jwt_required()
@role_requis("admin")
def update_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    data = request.json

    if 'nom_utilisateur' in data and data['nom_utilisateur'] != utilisateur.nom_utilisateur:
        if Utilisateur.query.filter_by(nom_utilisateur=data['nom_utilisateur']).first():
            return jsonify({"message": "Nom d'utilisateur déjà utilisé"}), 400

    utilisateur.nom = data.get('nom', utilisateur.nom)
    utilisateur.prenom = data.get('prenom', utilisateur.prenom)
    utilisateur.nom_utilisateur = data.get('nom_utilisateur', utilisateur.nom_utilisateur)

    if 'mot_de_passe' in data:
        utilisateur.set_password(data['mot_de_passe'])

    if 'role_id' in data:
        if not Role.query.get(data['role_id']):
            return jsonify({"message": "Rôle invalide"}), 400
        utilisateur.role_id = data['role_id']

    db.session.commit()
    enregistrer_action(get_jwt_identity()['id'], f"Mise à jour de l'utilisateur ID {id}")
    return jsonify({"message": "Utilisateur mis à jour."})


# SUPPRIMER UN UTILISATEUR
@utilisateur_bp.route('/supprimer/<int:id>', methods=['DELETE'])
@jwt_required()
@role_requis("admin")
def delete_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    db.session.delete(utilisateur)
    db.session.commit()
    enregistrer_action(get_jwt_identity()['id'], f"Suppression de l'utilisateur ID {id}")
    return jsonify({"message": "Utilisateur supprimé."})
