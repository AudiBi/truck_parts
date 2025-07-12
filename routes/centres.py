from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Piece, StockCentre, db, Centre

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


@centre_bp.route('/centre/<int:id>/stock')
@login_required
def stock_par_centre(id):
    centre = Centre.query.get_or_404(id)

    stock_data = (
        db.session.query(
            Piece.nom.label("piece"),
            StockCentre.quantite,
            Piece.seuil
        )
        .join(Piece)
        .filter(StockCentre.centre_id == id)
        .all()
    )

    return render_template("stock_centre_detail.html",
                           centre=centre,
                           stock_data=stock_data)
