from flask_admin.base import BaseView, expose
from flask_admin import AdminIndexView
from flask import render_template
from sqlalchemy.sql import func
from models import Piece, StockCentre, db

class StockGlobalAdmin(BaseView):
    @expose('/')
    def index(self):
        stock_data = (
            db.session.query(
                Piece.nom,
                func.sum(StockCentre.quantite).label('quantite_totale')
            )
            .join(StockCentre)
            .group_by(Piece.id)
            .all()
        )
        return self.render('admin/stock_global.html', stock_data=stock_data)
