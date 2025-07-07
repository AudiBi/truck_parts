from flask import Blueprint, request, jsonify
from models import db, Mouvement, Piece, Centre
from datetime import datetime

mouvement_bp = Blueprint('mouvements', __name__, url_prefix='/mouvements')

@mouvement_bp.route('/ajouter', methods=['POST'])
def create_mouvement():
    data = request.json
    mouvement = Mouvement(
        piece_id=data['piece_id'],
        centre_id=data['centre_id'],
        type=data['type'],
        quantite=data['quantite'],
        commentaire=data.get('commentaire'),
        utilisateur_id=data.get('utilisateur_id'),
        date=datetime.strptime(data['date'], "%Y-%m-%d") if 'date' in data else datetime.utcnow()
    )
    db.session.add(mouvement)
    db.session.commit()
    return jsonify({"message": "Mouvement enregistré."}), 201

@mouvement_bp.route('/liste', methods=['GET'])
def get_all_mouvements():
    mouvements = Mouvement.query.all()
    return jsonify([
        {
            "id": m.id,
            "piece": m.piece.nom,
            "centre": m.centre.nom,
            "type": m.type,
            "quantite": m.quantite,
            "commentaire": m.commentaire,
            "date": m.date.strftime("%Y-%m-%d %H:%M:%S")
        } for m in mouvements
    ])

@mouvement_bp.route('/rechercher/<int:id>', methods=['GET'])
def get_mouvement(id):
    mouvement = Mouvement.query.get_or_404(id)
    return jsonify({
        "id": mouvement.id,
        "piece": mouvement.piece.nom,
        "centre": mouvement.centre.nom,
        "type": mouvement.type,
        "quantite": mouvement.quantite,
        "commentaire": mouvement.commentaire,
        "date": mouvement.date.strftime("%Y-%m-%d %H:%M:%S")
    })

@mouvement_bp.route('/supprimer/<int:id>', methods=['DELETE'])
def delete_mouvement(id):
    mouvement = Mouvement.query.get_or_404(id)
    db.session.delete(mouvement)
    db.session.commit()
    return jsonify({"message": "Mouvement supprimé."})
