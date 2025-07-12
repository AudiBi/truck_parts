"""Ajout du champ centre_id dans Utilisateur

Revision ID: 4832d910f6c4
Revises: 
Create Date: 2025-07-10 15:34:53.974194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4832d910f6c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('utilisateurs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('centre_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_utilisateurs_centre_id',  # nom explicite de la contrainte
            'centres',                    # table référencée
            ['centre_id'],                # champ local
            ['id']                        # champ cible
        )

def downgrade():
    with op.batch_alter_table('utilisateurs', schema=None) as batch_op:
        batch_op.drop_constraint('fk_utilisateurs_centre_id', type_='foreignkey')
        batch_op.drop_column('centre_id')
