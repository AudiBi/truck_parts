from flask import Blueprint, send_file
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
from models import Vente, Facture

ticket_bp = Blueprint('tickets', __name__, url_prefix='/tickets')

@ticket_bp.route('/ticket/<int:vente_id>', methods=['GET'])
def ticket_vente_pdf(vente_id):
    vente = Vente.query.get_or_404(vente_id)
    facture = Facture.query.filter_by(vente_id=vente_id).first()

    buffer = BytesIO()

    # Largeur ticket ~58mm (58 * mm), hauteur libre (on met 300 pts par ex)
    width = 58 * mm
    height = 300

    c = canvas.Canvas(buffer, pagesize=(width, height))
    c.setFont("Helvetica", 9)

    y = height - 20  # marge top

    def draw_line(text, y_pos):
        c.drawString(5, y_pos, text)
        return y_pos - 12

    y = draw_line("** TICKET DE CAISSE **", y)
    y = draw_line(f"Date: {vente.date.strftime('%d/%m/%Y %H:%M')}", y)
    y = draw_line(f"Vente ID: {vente.id}", y)
    y = draw_line(f"Pièce: {vente.piece.nom}", y)
    y = draw_line(f"Quantité: {vente.quantite}", y)
    y = draw_line(f"Prix unitaire: {vente.prix:.2f} USD", y)
    total = facture.total if facture else vente.prix * vente.quantite
    y = draw_line(f"Total: {total:.2f} USD", y)
    y = draw_line(f"Centre: {vente.centre.nom}", y)

    if vente.utilisateur_id:
        utilisateur = vente.utilisateur
        y = draw_line(f"Vendeur: {utilisateur.prenom} {utilisateur.nom}", y)

    y = draw_line("--------------------------", y)
    y = draw_line("Merci pour votre achat !", y)

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True,
                     download_name=f"ticket_vente_{vente.id}.pdf")
