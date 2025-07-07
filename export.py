import pandas as pd
from flask import send_file
from app.models import Mouvement, db
from io import BytesIO
from xhtml2pdf import pisa
from flask import render_template, make_response

# Export Excel
def exporter_mouvements_excel():
    mouvements = db.session.query(Mouvement).all()
    data = [{
        "Date": m.date.strftime('%Y-%m-%d %H:%M'),
        "Article": m.piece.nom,
        "Type": m.type,
        "Quantité": m.quantite,
        "Centre": m.centre.nom,
        "Utilisateur": f"{m.utilisateur.prenom} {m.utilisateur.nom}",
        "Commentaire": m.commentaire or ""
    } for m in mouvements]

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Mouvements")
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="mouvements.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Export PDF
def exporter_mouvements_pdf():
    mouvements = db.session.query(Mouvement).all()
    rendered = render_template("mouvements/export_pdf.html", mouvements=mouvements)
    pdf = BytesIO()
    pisa.CreatePDF(rendered, dest=pdf)
    pdf.seek(0)
    return send_file(pdf, as_attachment=True, download_name="mouvements.pdf", mimetype='application/pdf')
