from app import create_app, db
from models import Role, Utilisateur, Centre, Piece, StockCentre, Mouvement, Vente, Facture
from datetime import datetime

# Crée l'app Flask
app = create_app()

def seed_roles():
    print("📥 Insertion des rôles...")
    roles = ['Admin', 'Vendeur', 'Gestionnaire']
    for nom in roles:
        if not Role.query.filter_by(nom=nom).first():
            role = Role(nom=nom)
            db.session.add(role)
    db.session.commit()
    print("✅ Rôles insérés.")

def seed_utilisateurs():
    print("📥 Insertion des utilisateurs...")
    admin_role = Role.query.filter_by(nom='Admin').first()
    vendeur_role = Role.query.filter_by(nom='Vendeur').first()

    if not Utilisateur.query.filter_by(nom_utilisateur='admin').first():
        admin = Utilisateur(
            nom='Dupont',
            prenom='Alice',
            nom_utilisateur='admin',
            role=admin_role
        )
        admin.set_password('admin123')
        db.session.add(admin)

    if not Utilisateur.query.filter_by(nom_utilisateur='vendeur1').first():
        vendeur = Utilisateur(
            nom='Martin',
            prenom='Bob',
            nom_utilisateur='vendeur1',
            role=vendeur_role
        )
        vendeur.set_password('vendeur123')
        db.session.add(vendeur)

    db.session.commit()
    print("✅ Utilisateurs insérés.")

def seed_centres():
    print("📥 Insertion des centres...")
    centres_data = [
        {'nom': 'Centre Principal', 'type': 'Magasin'},
        {'nom': 'Entrepôt Central', 'type': 'Entrepôt'},
    ]
    for c in centres_data:
        if not Centre.query.filter_by(nom=c['nom']).first():
            centre = Centre(nom=c['nom'], type=c['type'])
            db.session.add(centre)
    db.session.commit()
    print("✅ Centres insérés.")

def seed_pieces():
    print("📥 Insertion des pièces...")
    pieces_data = [
        {'nom': 'Pneu 205/55 R16', 'reference': 'PN20555R16', 'prix_achat': 50.0, 'prix_vente': 75.0, 'seuil': 10},
        {'nom': 'Huile Moteur 5L', 'reference': 'HUILE5L', 'prix_achat': 20.0, 'prix_vente': 30.0, 'seuil': 5},
    ]
    for p in pieces_data:
        if not Piece.query.filter_by(reference=p['reference']).first():
            piece = Piece(
                nom=p['nom'],
                reference=p['reference'],
                prix_achat=p['prix_achat'],
                prix_vente=p['prix_vente'],
                seuil=p['seuil']
            )
            db.session.add(piece)
    db.session.commit()
    print("✅ Pièces insérées.")

def seed_stock_centres():
    print("📥 Insertion du stock par centre...")
    centre = Centre.query.filter_by(nom='Centre Principal').first()
    entrepot = Centre.query.filter_by(nom='Entrepôt Central').first()
    pneu = Piece.query.filter_by(reference='PN20555R16').first()
    huile = Piece.query.filter_by(reference='HUILE5L').first()

    stocks = [
        {'piece': pneu, 'centre': centre, 'quantite': 15},
        {'piece': pneu, 'centre': entrepot, 'quantite': 40},
        {'piece': huile, 'centre': centre, 'quantite': 8},
        {'piece': huile, 'centre': entrepot, 'quantite': 20},
    ]

    for s in stocks:
        exists = StockCentre.query.filter_by(piece_id=s['piece'].id, centre_id=s['centre'].id).first()
        if not exists:
            stock = StockCentre(piece_id=s['piece'].id, centre_id=s['centre'].id, quantite=s['quantite'])
            db.session.add(stock)
    db.session.commit()
    print("✅ Stocks insérés.")

def seed_mouvements():
    print("📥 Insertion des mouvements...")
    utilisateur = Utilisateur.query.filter_by(nom_utilisateur='admin').first()
    centre = Centre.query.filter_by(nom='Centre Principal').first()
    piece = Piece.query.filter_by(reference='PN20555R16').first()

    mouvement = Mouvement(
        piece_id=piece.id,
        centre_id=centre.id,
        type='Entrée',
        quantite=10,
        date=datetime.utcnow(),
        commentaire='Réception fournisseur',
        utilisateur_id=utilisateur.id
    )
    db.session.add(mouvement)
    db.session.commit()
    print("✅ Mouvements insérés.")

def seed_ventes():
    print("📥 Insertion des ventes...")
    utilisateur = Utilisateur.query.filter_by(nom_utilisateur='vendeur1').first()
    centre = Centre.query.filter_by(nom='Centre Principal').first()
    piece = Piece.query.filter_by(reference='PN20555R16').first()

    vente = Vente(
        piece_id=piece.id,
        quantite=2,
        prix=piece.prix_vente * 2,
        date=datetime.utcnow(),
        centre_id=centre.id,
        utilisateur_id=utilisateur.id
    )
    db.session.add(vente)
    db.session.commit()
    print("✅ Ventes insérées.")
    return vente

def seed_factures():
    print("📥 Insertion des factures...")
    vente = Vente.query.order_by(Vente.id.desc()).first()
    if vente:
        facture = Facture(
            vente_id=vente.id,
            total=vente.prix,
            date=datetime.utcnow()
        )
        db.session.add(facture)
        db.session.commit()
        print("✅ Factures insérées.")
    else:
        print("⚠️ Aucune vente trouvée pour créer une facture.")

def run_all_seeders():
    with app.app_context():
        seed_roles()
        seed_utilisateurs()
        seed_centres()
        seed_pieces()
        seed_stock_centres()
        seed_mouvements()
        seed_ventes()
        seed_factures()
