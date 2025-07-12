from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import PasswordField

from forms import UtilisateurForm
from models import Utilisateur

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.nom == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        flash("Accès refusé.", "danger")
        return redirect(url_for('auth.login'))

class UtilisateurAdmin(SecureModelView):
    column_list = ('id', 'prenom', 'nom', 'nom_utilisateur', 'role')
    form = UtilisateurForm
    form_columns = ('prenom', 'nom', 'nom_utilisateur', 'mot_de_passe', 'role')

    def on_model_change(self, form, model, is_created):
        if form.mot_de_passe.data:
            model.set_password(form.mot_de_passe.data)


# Optionnel : RoleAdmin simple
class RoleAdmin(SecureModelView):
    column_list = ('id', 'nom')
    form_columns = ('nom',)

class JournalActiviteAdmin(SecureModelView):
    can_create = False
    can_edit = False
    can_delete = False

    column_list = ('utilisateur_nom', 'action', 'date', 'ip')
    column_filters = ('date',)

    def _utilisateur_nom(view, context, model, name):
        utilisateur = Utilisateur.query.get(model.utilisateur_id)
        return model.utilisateur.nom_utilisateur if model.utilisateur else "—"

    column_formatters = {
        'utilisateur_nom': _utilisateur_nom
    }


class CentreAdmin(SecureModelView):
    column_list = ('id', 'nom', 'type')
    form_columns = ('nom', 'type')
    column_searchable_list = ('nom',)

class PieceAdmin(SecureModelView):
    column_list = ('nom', 'reference', 'prix_achat', 'prix_vente', 'seuil', 'stock_total')

    def _stock_total(view, context, model, name):
        return sum([s.quantite for s in model.stocks])

    column_formatters = {
        'stock_total': _stock_total
    }


class StockCentreAdmin(SecureModelView):
    column_list = ('piece_nom', 'centre_nom', 'quantite')  # pas 'id'
    column_filters = ('centre.nom', 'piece.nom')
    form_columns = ('piece_id', 'centre_id', 'quantite')

    def _piece_nom(view, context, model, name):
        return model.piece.nom

    def _centre_nom(view, context, model, name):
        return model.centre.nom

    column_formatters = {
        'piece_nom': _piece_nom,
        'centre_nom': _centre_nom,
    }


class MouvementAdmin(SecureModelView):
    column_list = ('type', 'piece_nom', 'centre_nom', 'quantite', 'date', 'utilisateur_nom')
    form_columns = ('type', 'piece_id', 'centre_id', 'quantite', 'commentaire', 'utilisateur_id')

    def _piece_nom(view, context, model, name):
        return model.piece.nom

    def _centre_nom(view, context, model, name):
        return model.centre.nom

    def _utilisateur_nom(view, context, model, name):
        return model.utilisateur.nom_utilisateur if model.utilisateur else "—"

    column_formatters = {
        'piece_nom': _piece_nom,
        'centre_nom': _centre_nom,
        'utilisateur_nom': _utilisateur_nom
    }



class VenteAdmin(SecureModelView):
    column_list = ('id', 'piece.nom', 'quantite', 'prix', 'centre.nom', 'date', 'utilisateur_id')
    column_filters = ('centre_id', 'date')
    form_columns = ('piece_id', 'quantite', 'prix', 'centre_id', 'utilisateur_id')


class FactureAdmin(SecureModelView):
    column_list = ('id', 'vente_id', 'total', 'date')
    form_columns = ('vente_id', 'total')
    column_filters = ('date',)
