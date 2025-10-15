from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables from the models."""
    db.create_all()
    print("Initialized the database and created all tables.")

if __name__ == '__main__':
    app.run(debug=True)
