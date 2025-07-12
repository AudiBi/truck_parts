from flask_wtf import FlaskForm
from wtforms import DecimalField, FloatField, IntegerField, StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from models import Role


class LoginForm(FlaskForm):
    nom_utilisateur = StringField("Nom d'utilisateur", validators=[DataRequired()])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class UtilisateurForm(FlaskForm):
    prenom = StringField('Prénom', validators=[InputRequired()])
    nom = StringField('Nom', validators=[InputRequired()])
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[InputRequired()])
    role = QuerySelectField(
        'Rôle',
        query_factory=lambda: Role.query.all(),
        get_label='nom',
        allow_blank=False
    )
    mot_de_passe = PasswordField('Mot de passe')


class PieceForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    reference = StringField('Référence', validators=[DataRequired(), Length(max=50)])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=0)])
    prix_achat = DecimalField('Prix d\'achat', validators=[DataRequired(), NumberRange(min=0)])
    prix_vente = DecimalField('Prix de vente', validators=[DataRequired(), NumberRange(min=0)])
    seuil = IntegerField('Seuil d\'alerte', default=0, validators=[NumberRange(min=0)])
    submit = SubmitField('Enregistrer')


class VenteForm(FlaskForm):
    piece_id = SelectField('Pièce', coerce=int, validators=[DataRequired()])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=1)])
    prix = FloatField('Prix unitaire', validators=[DataRequired(), NumberRange(min=0)])
    centre_id = SelectField('Centre', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class MouvementForm(FlaskForm):
    type = SelectField('Type', choices=[('entrée', 'Entrée'), ('sortie', 'Sortie')], validators=[DataRequired()])
    piece_id = SelectField('Pièce', coerce=int, validators=[DataRequired()])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=1)])
    centre_id = SelectField('Centre', coerce=int, validators=[DataRequired()])
    commentaire = TextAreaField('Commentaire')
    submit = SubmitField('Enregistrer')
