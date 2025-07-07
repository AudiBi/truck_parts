from flask import Blueprint, request, jsonify
from models import db, Piece

piece_bp = Blueprint('pieces', __name__, url_prefix='/pieces')

@piece_bp.route('/ajouter', methods=['POST'])
def create_piece():
    data = request.json
    piece = Piece(
        nom=data['nom'],
        reference=data['reference'],
        prix_achat=data['prix_achat'],
        prix_vente=data['prix_vente'],
        seuil=data.get('seuil', 0)
    )
    db.session.add(piece)
    db.session.commit()
    return jsonify({"message": "Pièce créée avec succès."}), 201

@piece_bp.route('/liste', methods=['GET'])
def get_all_pieces():
    pieces = Piece.query.all()
    return jsonify([
        {
            "id": p.id,
            "nom": p.nom,
            "reference": p.reference,
            "prix_achat": p.prix_achat,
            "prix_vente": p.prix_vente,
            "seuil": p.seuil
        } for p in pieces
    ])

@piece_bp.route('/rechercher/<int:id>', methods=['GET'])
def get_piece(id):
    piece = Piece.query.get_or_404(id)
    return jsonify({
        "id": piece.id,
        "nom": piece.nom,
        "reference": piece.reference,
        "prix_achat": piece.prix_achat,
        "prix_vente": piece.prix_vente,
        "seuil": piece.seuil
    })

@piece_bp.route('/modifier/<int:id>', methods=['PUT'])
def update_piece(id):
    piece = Piece.query.get_or_404(id)
    data = request.json
    piece.nom = data.get('nom', piece.nom)
    piece.reference = data.get('reference', piece.reference)
    piece.prix_achat = data.get('prix_achat', piece.prix_achat)
    piece.prix_vente = data.get('prix_vente', piece.prix_vente)
    piece.seuil = data.get('seuil', piece.seuil)
    db.session.commit()
    return jsonify({"message": "Pièce mise à jour."})

@piece_bp.route('/supprimer/<int:id>', methods=['DELETE'])
def delete_piece(id):
    piece = Piece.query.get_or_404(id)
    db.session.delete(piece)
    db.session.commit()
    return jsonify({"message": "Pièce supprimée."})
