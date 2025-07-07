from flask.cli import FlaskGroup
from app import create_app
from seed import run_all_seeders

app = create_app()
cli = FlaskGroup(app)

@cli.command("seed-db")
def seed_db():
    confirmation = input("Cette opération va insérer des données initiales dans la base. Continuer ? [y/N]: ")
    if confirmation.lower() == 'y':
        run_all_seeders()
        print("Seed terminé.")
    else:
        print("Opération annulée.")

if __name__ == "__main__":
    cli()
