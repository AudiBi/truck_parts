from flask import  request
from datetime import datetime
from models import db, JournalActivite

def enregistrer_action(utilisateur_id, action):
    from datetime import datetime
    journal = JournalActivite(
        utilisateur_id=utilisateur_id,
        action=action,
        ip=request.remote_addr,
        date=datetime.utcnow()
    )
    db.session.add(journal)
    db.session.commit()


