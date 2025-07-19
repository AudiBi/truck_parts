from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
from flask_login import current_user, login_required
from decorators import role_requis
from forms import MouvementForm
from models import db, Mouvement, Piece, Centre
from datetime import datetime

from utils import enregistrer_action

mouvement_bp = Blueprint('mouvements', __name__, url_prefix='/mouvements')

@mouvement_bp.route('/dashboard')
@login_required
@role_requis('gestionnaire')
def dashboard_gestionnaire():
    enregistrer_action(current_user.id, "Consultation dashboard")
    return render_template('gestion/index.html')

@mouvement_bp.route('/mouvements')
@login_required
@role_requis('gestionnaire')
def lister_mouvements():
    piece_nom = request.args.get('piece')
    centre_id = request.args.get('centre')
    date_str = request.args.get('date')

    mouvements_query = Mouvement.query

    if piece_nom:
        mouvements_query = mouvements_query.join(Piece).filter(Piece.nom.ilike(f'%{piece_nom}%'))
    if centre_id:
        mouvements_query = mouvements_query.filter_by(centre_id=centre_id)
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            mouvements_query = mouvements_query.filter(db.func.date(Mouvement.date) == date.date())
        except ValueError:
            flash("Date invalide", "warning")

    mouvements = mouvements_query.order_by(Mouvement.date.desc()).all()
    centres = Centre.query.all()
    return render_template('gestion/lister_mouvements.html', mouvements=mouvements, centres=centres)


@mouvement_bp.route('/mouvements/nouveau', methods=['GET', 'POST'])
@login_required
@role_requis('gestionnaire')
def nouveau_mouvement():
    form = MouvementForm()
    form.piece_id.choices = [(p.id, p.nom) for p in Piece.query.all()]
    form.centre_id.choices = [(c.id, c.nom) for c in Centre.query.all()]

    if form.validate_on_submit():
        mouvement = Mouvement(
            type=form.type.data,
            piece_id=form.piece_id.data,
            quantite=form.quantite.data,
            centre_id=form.centre_id.data,
            commentaire=form.commentaire.data,
            utilisateur_id=current_user.id
        )
        db.session.add(mouvement)
        db.session.commit()
        flash("Mouvement enregistré.", "success")
        return redirect(url_for('mouvements.lister_mouvements'))

    return render_template('gestion/nouveau_mouvement.html', form=form)

@mouvement_bp.route('/mouvements/modifier/<int:mouvement_id>', methods=['GET', 'POST'])
@login_required
@role_requis('gestionnaire')
def modifier_mouvement(mouvement_id):
    mouvement = Mouvement.query.get_or_404(mouvement_id)
    pieces = Piece.query.all()
    centres = Centre.query.all()

    if request.method == 'POST':
        mouvement.piece_id = request.form['piece_id']
        mouvement.quantite = int(request.form['quantite'])
        mouvement.type = request.form['type']
        mouvement.commentaire = request.form['commentaire']
        mouvement.centre_id = request.form['centre_id']
        db.session.commit()
        flash("Mouvement mis à jour.", "success")
        return redirect(url_for('mouvements.lister_mouvements'))

    return render_template('gestion/modifier_mouvement.html', mouvement=mouvement, pieces=pieces, centres=centres)


@mouvement_bp.route('/mouvements/supprimer/<int:mouvement_id>', methods=['POST'])
@login_required
@role_requis('gestionnaire')
def supprimer_mouvement(mouvement_id):
    mouvement = Mouvement.query.get_or_404(mouvement_id)
    db.session.delete(mouvement)
    db.session.commit()
    flash("Mouvement supprimé.", "success")
    return redirect(url_for('mouvements.lister_mouvements'))


