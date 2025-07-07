from flask import Blueprint, request, jsonify
from models import db, Facture, Vente
from datetime import datetime

facture_bp = Blueprint('factures', __name__, url_prefix='/factures')

@facture_bp.route('/ajouter', methods=['POST'])
def create_facture():
    data = request.json
    facture = Facture(
        vente_id=data['vente_id'],
        total=data['total'],
        date=datetime.strptime(data['date'], "%Y-%m-%d") if 'date' in data else datetime.utcnow()
    )
    db.session.add(facture)
    db.session.commit()
    return jsonify({"message": "Facture créée."}), 201

@facture_bp.route('/liste', methods=['GET'])
def get_all_factures():
    factures = Facture.query.all()
    return jsonify([
        {
            "id": f.id,
            "vente_id": f.vente_id,
            "total": f.total,
            "date": f.date.strftime("%Y-%m-%d %H:%M:%S")
        } for f in factures
    ])

@facture_bp.route('/rechercher/<int:id>', methods=['GET'])
def get_facture(id):
    facture = Facture.query.get_or_404(id)
    return jsonify({
        "id": facture.id,
        "vente_id": facture.vente_id,
        "total": facture.total,
        "date": facture.date.strftime("%Y-%m-%d %H:%M:%S")
    })

@facture_bp.route('/modifier/<int:id>', methods=['PUT'])
def update_facture(id):
    facture = Facture.query.get_or_404(id)
    data = request.json
    facture.vente_id = data.get('vente_id', facture.vente_id)
    facture.total = data.get('total', facture.total)
    if 'date' in data:
        facture.date = datetime.strptime(data['date'], "%Y-%m-%d")
    db.session.commit()
    return jsonify({"message": "Facture mise à jour."})

@facture_bp.route('/supprimer/<int:id>', methods=['DELETE'])
def delete_facture(id):
    facture = Facture.query.get_or_404(id)
    db.session.delete(facture)
    db.session.commit()
    return jsonify({"message": "Facture supprimée."})
