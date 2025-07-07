from flask import Blueprint, request, jsonify
from models import db, Centre

centre_bp = Blueprint('centre', __name__, url_prefix='/centre')

@centre_bp.route('/ajouter', methods=['POST'])
def create_centre():
    data = request.json
    centre = Centre(nom=data['nom'], type=data['type'])
    db.session.add(centre)
    db.session.commit()
    return jsonify({"message": "Centre créé avec succès."}), 201

@centre_bp.route('/liste', methods=['GET'])
def get_all_centres():
    centres = Centre.query.all()
    return jsonify([{"id": c.id, "nom": c.nom, "type": c.type} for c in centres])

@centre_bp.route('/rechercher/<int:id>', methods=['GET'])
def get_centre(id):
    centre = Centre.query.get_or_404(id)
    return jsonify({"id": centre.id, "nom": centre.nom, "type": centre.type})

@centre_bp.route('/modifier/<int:id>', methods=['PUT'])
def update_centre(id):
    centre = Centre.query.get_or_404(id)
    data = request.json
    centre.nom = data.get('nom', centre.nom)
    centre.type = data.get('type', centre.type)
    db.session.commit()
    return jsonify({"message": "Centre mis à jour."})

@centre_bp.route('/supprimer/<int:id>', methods=['DELETE'])
def delete_centre(id):
    centre = Centre.query.get_or_404(id)
    db.session.delete(centre)
    db.session.commit()
    return jsonify({"message": "Centre supprimé."})
