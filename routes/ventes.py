from flask import Blueprint, render_template, request, jsonify, session
from models import db, Vente, Piece, Centre
from decorators import login_required, role_required
from datetime import datetime

vente_bp = Blueprint('ventes', __name__, url_prefix='/ventes')

@vente_bp.route('/dashboard')
@login_required
@role_required('vendeur')
def dashboard_vendeur():
    return render_template('dashboard/dashboard_vendeur.html', utilisateur=session.get('utilisateur'))

@vente_bp.route('', methods=['POST'])
def create_vente():
    data = request.json
    vente = Vente(
        piece_id=data['piece_id'],
        quantite=data['quantite'],
        prix=data['prix'],
        centre_id=data['centre_id'],
        utilisateur_id=data.get('utilisateur_id'),
        date=datetime.strptime(data['date'], "%Y-%m-%d") if 'date' in data else datetime.utcnow()
    )
    db.session.add(vente)
    db.session.commit()
    return jsonify({"message": "Vente enregistrée."}), 201

@vente_bp.route('', methods=['GET'])
def get_all_ventes():
    ventes = Vente.query.all()
    return jsonify([
        {
            "id": v.id,
            "piece": v.piece.nom,
            "quantite": v.quantite,
            "prix": v.prix,
            "centre": v.centre.nom,
            "date": v.date.strftime("%Y-%m-%d %H:%M:%S")
        } for v in ventes
    ])

@vente_bp.route('/<int:id>', methods=['GET'])
def get_vente(id):
    vente = Vente.query.get_or_404(id)
    return jsonify({
        "id": vente.id,
        "piece": vente.piece.nom,
        "quantite": vente.quantite,
        "prix": vente.prix,
        "centre": vente.centre.nom,
        "date": vente.date.strftime("%Y-%m-%d %H:%M:%S")
    })

@vente_bp.route('/<int:id>', methods=['PUT'])
def update_vente(id):
    vente = Vente.query.get_or_404(id)
    data = request.json
    vente.piece_id = data.get('piece_id', vente.piece_id)
    vente.quantite = data.get('quantite', vente.quantite)
    vente.prix = data.get('prix', vente.prix)
    vente.centre_id = data.get('centre_id', vente.centre_id)
    vente.utilisateur_id = data.get('utilisateur_id', vente.utilisateur_id)
    if 'date' in data:
        vente.date = datetime.strptime(data['date'], "%Y-%m-%d")
    db.session.commit()
    return jsonify({"message": "Vente mise à jour."})

@vente_bp.route('/<int:id>', methods=['DELETE'])
def delete_vente(id):
    vente = Vente.query.get_or_404(id)
    db.session.delete(vente)
    db.session.commit()
    return jsonify({"message": "Vente supprimée."})
