from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

db = SQLAlchemy()
bcrypt = Bcrypt()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    utilisateurs = db.relationship('Utilisateur', back_populates='role', lazy=True)


    def __repr__(self):
        return self.nom


class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    nom_utilisateur = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', back_populates='utilisateurs', lazy=True)
    centre_id = db.Column(db.Integer, db.ForeignKey('centres.id'), nullable=True)
    

    def set_password(self, mot_de_passe):
        self.password_hash = generate_password_hash(mot_de_passe).decode('utf-8')

    def check_password(self, mot_de_passe):
        return bcrypt.check_password_hash(self.password_hash, mot_de_passe)

    def __repr__(self):
        return f"{self.prenom} {self.nom} ({self.nom_utilisateur})"
class JournalActivite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    utilisateur = db.relationship('Utilisateur', backref='journal_activite')
    action = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(100), nullable=True)

class Centre(db.Model):
    __tablename__ = 'centres'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    stocks = db.relationship('StockCentre', backref='centre', lazy=True)

class Piece(db.Model):
    __tablename__ = 'pieces'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    reference = db.Column(db.String(100), unique=True, nullable=False)
    prix_achat = db.Column(db.Float, nullable=False)
    prix_vente = db.Column(db.Float, nullable=False)
    seuil = db.Column(db.Integer, default=0)
    stocks = db.relationship('StockCentre', backref='piece', lazy=True)

class StockCentre(db.Model):
    __tablename__ = 'stock_centre'
    id = db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('pieces.id'), nullable=False)
    centre_id = db.Column(db.Integer, db.ForeignKey('centres.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

class Mouvement(db.Model):
    __tablename__ = 'mouvements'
    id = db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('pieces.id'), nullable=False)
    centre_id = db.Column(db.Integer, db.ForeignKey('centres.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    commentaire = db.Column(db.Text, nullable=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=True)
    piece = db.relationship('Piece')
    centre = db.relationship('Centre')

class Vente(db.Model):
    __tablename__ = 'ventes'
    id = db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('pieces.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    centre_id = db.Column(db.Integer, db.ForeignKey('centres.id'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=True)
    piece = db.relationship('Piece')
    centre = db.relationship('Centre')

class Facture(db.Model):
    __tablename__ = 'factures'
    id = db.Column(db.Integer, primary_key=True)
    vente_id = db.Column(db.Integer, db.ForeignKey('ventes.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    vente = db.relationship('Vente')

