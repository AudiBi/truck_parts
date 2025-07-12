from flask import Blueprint, flash, redirect, render_template, request, jsonify, session, url_for
from flask_login import current_user, login_required
from decorators import role_requis
from forms import VenteForm
from models import db, Vente, Piece, Centre
from datetime import datetime

from utils import enregistrer_action

vente_bp = Blueprint('ventes', __name__, url_prefix='/ventes')

@vente_bp.route('/dashboard')
@login_required
@role_requis('vendeur')
def dashboard_vendeur():
    enregistrer_action(current_user.id, "Consultation dashboard ventes")
    return render_template('vente/index.html')

@vente_bp.route('/ventes/nouvelle', methods=['GET', 'POST'])
@login_required
@role_requis('vendeur')
def nouvelle_vente():
    form = VenteForm()
    form.piece_id.choices = [(p.id, p.nom) for p in Piece.query.all()]
    form.centre_id.choices = [(c.id, c.nom) for c in Centre.query.all()]

    if form.validate_on_submit():
        vente = Vente(
            piece_id=form.piece_id.data,
            quantite=form.quantite.data,
            prix=form.prix.data,
            centre_id=form.centre_id.data,
            utilisateur_id=current_user.id
        )
        db.session.add(vente)
        db.session.commit()
        flash("Vente enregistrée.", "success")
        return redirect(url_for('ventes.lister_ventes'))

    return render_template('vente/nouvelle_vente.html', form=form)



@vente_bp.route('/ventes')
@login_required
@role_requis('vendeur')
def lister_ventes():
    piece_nom = request.args.get('piece')
    centre_id = request.args.get('centre')
    date_str = request.args.get('date')

    ventes_query = Vente.query

    if piece_nom:
        ventes_query = ventes_query.join(Piece).filter(Piece.nom.ilike(f'%{piece_nom}%'))
    if centre_id:
        ventes_query = ventes_query.filter_by(centre_id=centre_id)
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            ventes_query = ventes_query.filter(db.func.date(Vente.date) == date.date())
        except ValueError:
            flash("Date invalide", "warning")

    ventes = ventes_query.order_by(Vente.date.desc()).all()
    centres = Centre.query.all()
    return render_template('vente/lister_ventes.html', ventes=ventes, centres=centres)

@vente_bp.route('/ventes/modifier/<int:vente_id>', methods=['GET', 'POST'])
@login_required
@role_requis('vendeur')
def modifier_vente(vente_id):
    vente = Vente.query.get_or_404(vente_id)
    pieces = Piece.query.all()
    centres = Centre.query.all()

    if request.method == 'POST':
        vente.piece_id = request.form['piece_id']
        vente.quantite = int(request.form['quantite'])
        vente.prix = float(request.form['prix'])
        vente.centre_id = request.form['centre_id']
        db.session.commit()
        flash("Vente mise à jour.", "success")
        return redirect(url_for('vente.lister_ventes'))

    return render_template('vente/modifier_vente.html', vente=vente, pieces=pieces, centres=centres)


@vente_bp.route('/ventes/supprimer/<int:vente_id>', methods=['POST'])
@login_required
@role_requis('vendeur')
def supprimer_vente(vente_id):
    vente = Vente.query.get_or_404(vente_id)
    db.session.delete(vente)
    db.session.commit()
    flash("Vente supprimée.", "success")
    return redirect(url_for('vente.lister_ventes'))



