from turtle import pd
from flask import Blueprint, render_template, request, make_response, send_file
from flask_login import login_required
from sqlalchemy import func
from models import StockCentre, Piece, Centre, Mouvement, db
from xhtml2pdf import pisa
from io import BytesIO

rapport_bp = Blueprint('rapport', __name__, url_prefix='/rapport')

@rapport_bp.route('/rapport-stock')
@login_required
def rapport_stock():
    centre_id = request.args.get('centre_id', type=int)
    seuil = request.args.get('seuil', type=int)

    query = db.session.query(
        Piece.nom.label("piece"),
        Centre.nom.label("centre"),
        StockCentre.quantite,
        Piece.seuil,
        func.max(Mouvement.date).label("dernier_mouvement")
    ).join(Piece).join(Centre).outerjoin(
        Mouvement, (Mouvement.piece_id == StockCentre.piece_id) & (Mouvement.centre_id == StockCentre.centre_id)
    ).group_by(Piece.nom, Centre.nom, StockCentre.quantite, Piece.seuil)

    if centre_id:
        query = query.filter(Centre.id == centre_id)
    if seuil is not None:
        query = query.filter(Piece.seuil <= seuil)

    data = query.all()
    centres = Centre.query.all()

    return render_template('rapport_stock.html', data=data, centres=centres)


@rapport_bp.route('/rapport-stock/pdf')
@login_required
def rapport_stock_pdf():
    html = render_template('rapport_pdf.html', data=fetch_stock_data())  # même logique que ci-dessus
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf)
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=rapport_stock.pdf'
    return response

@rapport_bp.route('/rapport-stock/pdf')
@login_required
def rapport_stock_pdf():
    html = render_template('rapport_pdf.html', data=fetch_stock_data())  # même logique que ci-dessus
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf)
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=rapport_stock.pdf'
    return response

@rapport_bp.route('/rapport-stock/excel')
@login_required
def rapport_stock_excel():
    data = fetch_stock_data()  # même logique que ci-dessus
    df = pd.DataFrame(data, columns=['Pièce', 'Centre', 'Quantité', 'Seuil', 'Dernier Mouvement'])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Stock')
    output.seek(0)
    return send_file(output, download_name='rapport_stock.xlsx', as_attachment=True)

def fetch_stock_data():
    return db.session.query(
        Piece.nom.label("piece"),
        Centre.nom.label("centre"),
        StockCentre.quantite,
        Piece.seuil,
        func.max(Mouvement.date).label("dernier_mouvement")
    ).join(Piece).join(Centre).outerjoin(
        Mouvement, (Mouvement.piece_id == StockCentre.piece_id) & (Mouvement.centre_id == StockCentre.centre_id)
    ).group_by(Piece.nom, Centre.nom, StockCentre.quantite, Piece.seuil).all()
