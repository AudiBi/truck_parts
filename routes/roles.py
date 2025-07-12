from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Role
from utils import role_requis

role_bp = Blueprint('roles', __name__, url_prefix='/roles')

@role_bp.route('/ajouter', methods=['POST'])
@jwt_required()
@role_requis("admin")
def ajouter_role():
    data = request.get_json()
    if Role.query.filter_by(nom=data['nom']).first():
        return jsonify({"message": "Rôle déjà existant"}), 400
    role = Role(nom=data['nom'])
    db.session.add(role)
    db.session.commit()
    return jsonify({"message": "Rôle créé"}), 201

@role_bp.route('/liste', methods=['GET'])
@jwt_required()
def liste_roles():
    roles = Role.query.all()
    return jsonify([{"id": r.id, "nom": r.nom} for r in roles])
