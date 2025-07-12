from io import BytesIO
from turtle import pd
from flask import Blueprint, flash, make_response, redirect, render_template, request, jsonify, send_file, url_for
from flask_login import current_user, login_required
from models import Piece, StockCentre, db

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')


@stock_bp.route('/centre/stock')
@login_required
def consulter_stock():
    centre_id = current_user.centre_id
    search = request.args.get('search', '')

    query = StockCentre.query.join(Piece).filter(StockCentre.centre_id == centre_id)

    if search:
        query = query.filter(Piece.nom.ilike(f'%{search}%'))

    stocks = query.all()

    # Préparer les infos avec détection de seuil
    stock_infos = []
    for stock in stocks:
        stock_infos.append({
            'stock': stock,
            'sous_seuil': stock.quantite < stock.piece.seuil
        })

    return render_template(
        'gestion/stock.html',
        stock_infos=stock_infos,
        search=search
    )

@stock_bp.route('/centre/stock/modifier/<int:stock_id>', methods=['GET', 'POST'])
@login_required
def modifier_quantite(stock_id):
    stock = StockCentre.query.get_or_404(stock_id)

    if request.method == 'POST':
        try:
            nouvelle_quantite = int(request.form['quantite'])
            stock.quantite = nouvelle_quantite
            db.session.commit()
            flash('Quantité mise à jour avec succès.', 'success')
        except ValueError:
            flash('Veuillez entrer une quantité valide.', 'danger')
        return redirect(url_for('stock.consulter_stock'))

    return render_template('gestion/modifier_quantite.html', stock=stock)


@stock_bp.route('/centre/export/excel')
@login_required
def export_excel():
    centre_id = current_user.centre_id
    stocks = StockCentre.query.filter_by(centre_id=centre_id).all()

    data = [{
        'Nom de la pièce': s.piece.nom,
        'Référence': s.piece.reference,
        'Quantité': s.quantite,
        'Seuil': s.piece.seuil
    } for s in stocks]

    df = pd.DataFrame(data)
    output = pd.ExcelWriter('stock_export.xlsx', engine='xlsxwriter')
    df.to_excel(output, index=False, sheet_name='Stock')
    output.close()

    with open("stock_export.xlsx", "rb") as f:
        content = f.read()

    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=stock_export.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response