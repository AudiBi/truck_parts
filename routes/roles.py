from flask import Blueprint, request, jsonify
from models import db, Role

role_bp = Blueprint('roles', __name__, url_prefix='/roles')

@role_bp.route('/ajouter', methods=['POST'])
def create_role():
    data = request.json
    role = Role(nom=data['nom'])
    db.session.add(role)
    db.session.commit()
    return jsonify({"message": "Rôle créé avec succès."}), 201

@role_bp.route('/liste', methods=['GET'])
def get_all_roles():
    roles = Role.query.all()
    return jsonify([{"id": r.id, "nom": r.nom} for r in roles])

@role_bp.route('/rechercher/<int:id>', methods=['GET'])
def get_role(id):
    role = Role.query.get_or_404(id)
    return jsonify({"id": role.id, "nom": role.nom})

@role_bp.route('/modifier/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.json
    role.nom = data.get('nom', role.nom)
    db.session.commit()
    return jsonify({"message": "Rôle mis à jour."})

@role_bp.route('/supprimer/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({"message": "Rôle supprimé."})
