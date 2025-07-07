from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class UtilisateurForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(max=100)])
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(max=100)])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    role_id = SelectField('Rôle', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class PieceForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    reference = StringField('Référence', validators=[DataRequired(), Length(max=50)])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=0)])
    prix_achat = DecimalField('Prix d\'achat', validators=[DataRequired(), NumberRange(min=0)])
    prix_vente = DecimalField('Prix de vente', validators=[DataRequired(), NumberRange(min=0)])
    seuil = IntegerField('Seuil d\'alerte', default=0, validators=[NumberRange(min=0)])
    submit = SubmitField('Enregistrer')


class MouvementForm(FlaskForm):
    piece_id = SelectField("Article", coerce=int, validators=[DataRequired()])
    type = SelectField("Type", choices=[('entrée', 'Entrée'), ('sortie', 'Sortie'), ('ajustement', 'Ajustement')], validators=[DataRequired()])
    quantite = IntegerField("Quantité", validators=[DataRequired(), NumberRange(min=1)])
    commentaire = StringField("Commentaire")
    utilisateur_id = SelectField("Utilisateur", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
